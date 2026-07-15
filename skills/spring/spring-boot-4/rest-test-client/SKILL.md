---
name: rest-test-client
description: >-
  Test REST APIs with Spring Framework 7's RestTestClient — one fluent client for every level, via
  bindToController (unit), bindTo(MockMvc), bindToApplicationContext, bindToServer (E2E), and
  bindToRouterFunction. Use when writing or migrating tests for HTTP endpoints in a Boot 4 / FW 7
  project (check the build file — users rarely state the version) and you want a single consistent
  API instead of switching between MockMvc, WebTestClient, and
  TestRestTemplate. Do NOT use when the user specifically wants AssertJ-style server-side assertions
  or to compare the two testing tools (see mock-vs-rest), nor for non-HTTP unit tests.
---

# RestTestClient (Spring Framework 7)

**Baseline:** Spring Boot 4.0+, Spring Framework 7.0+, Java 17+ (25 recommended).

`RestTestClient` is FW 7's unified REST testing client: the **same fluent API** (`.get().uri(...)
.exchange().expectStatus()...`) from isolated unit tests up to full E2E — only the `bindTo*` factory
changes. Claude gets this wrong by reaching for the old trio: `MockMvc` for slices,
`WebTestClient` for reactive, `TestRestTemplate` for E2E. In Boot 4, one client spans all of them.

## When to use / not use

Use to test HTTP endpoints at any level with one API. **Do NOT** use it when the task is *which test
tool to pick* or wants AssertJ handler-level assertions — that's `mock-vs-rest`
(`MockMvcTester`). Not for plain non-HTTP unit tests.

## The five bind modes

```java
RestTestClient.bindToController(new TodoController(service)).build();   // unit, no Spring context
RestTestClient.bindTo(mockMvc).build();                                 // slice (@WebMvcTest)
RestTestClient.bindToApplicationContext(context).build();              // full context, mocked HTTP
RestTestClient.bindToServer().baseUrl("http://localhost:" + port).build(); // E2E over real HTTP
RestTestClient.bindToRouterFunction(routerFunction).build();            // functional endpoints
```

Pick the lowest level that exercises what you're testing — speed drops and realism rises as you move
down the list.

## Examples across the pyramid

```java
// Unit — controller in isolation with a mocked service
@ExtendWith(MockitoExtension.class)
class TodoControllerTest {
    @Mock TodoService service;
    RestTestClient client;
    @BeforeEach void setUp() { client = RestTestClient.bindToController(new TodoController(service)).build(); }

    @Test void getsAll() {
        when(service.findAll()).thenReturn(List.of(new Todo(1L, "Learn Spring", false)));
        client.get().uri("/api/todos").exchange()
              .expectStatus().isOk()
              .expectBody().jsonPath("$[0].title").isEqualTo("Learn Spring");
    }
}
```

```java
// Slice — bind to MockMvc to get validation/security filters
@WebMvcTest(TodoController.class)
class TodoControllerMvcTest {
    @Autowired MockMvc mockMvc;
    @MockitoBean TodoService service;   // @MockBean was removed in Boot 4
    @Test void rejectsInvalid() {
        RestTestClient.bindTo(mockMvc).build()
            .post().uri("/api/todos").contentType(MediaType.APPLICATION_JSON)
            .bodyValue(new Todo(null, "", false)).exchange()
            .expectStatus().isBadRequest();
    }
}
```

```java
// E2E — real server, real HTTP
@SpringBootTest(webEnvironment = WebEnvironment.RANDOM_PORT)
class TodoIntegrationTest {
    @LocalServerPort int port;
    @Test void createsAndReturns201() {
        RestTestClient.bindToServer().baseUrl("http://localhost:" + port).build()
            .post().uri("/api/todos").contentType(MediaType.APPLICATION_JSON)
            .bodyValue(new Todo(null, "Integration test", false)).exchange()
            .expectStatus().isCreated();
    }
}
```

## Gotchas

- Mock beans in slices with **`@MockitoBean`** (`org.springframework.test.context.bean.override.mockito`) —
  Boot 4 removed the deprecated `@MockBean`/`@SpyBean`.
- `expectBody()` chains `jsonPath(...)` assertions; `expectBody(MyDto.class)` deserializes a typed
  body. Use the typed form when you want to assert on fields as objects.
- It works with **any** `HttpMessageConverter` (XML, etc.), not just JSON — an edge where it beats
  `MockMvcTester`.
- Maximize `bindToController` tests for speed; keep `bindToServer` E2E tests few — they're slow and
  the most brittle.
- The assertion grammar mirrors the old `WebTestClient`, so migrations from it are nearly mechanical.

## References

- Demo: https://github.com/danvega/rest-test-client
- Video: https://youtu.be/dPM8n0uNhes · Blog: https://www.danvega.dev/blog/spring-framework-7-rest-test-client
- Docs: https://docs.spring.io/spring-framework/reference/testing/resttestclient.html
