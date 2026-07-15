---
name: mock-vs-rest
description: >-
  Decide between MockMvcTester and RestTestClient for controller tests in Spring Framework 7, and use
  MockMvcTester's AssertJ-native server-side assertions. Use when a testing task in a Boot 4 / FW 7
  project (check the build file — users rarely state the version) is a CHOICE between the two tools,
  or specifically wants MockMvcTester — AssertJ assertThat(...) on responses, handler/exception
  inspection, multipart/file-upload tests, or HttpServletRequest access.
  Do NOT use for a deep how-to on RestTestClient's bind modes (see rest-test-client) — this skill is
  the comparison + the MockMvcTester side.
---

# MockMvcTester vs RestTestClient — which to use (Framework 7)

**Baseline:** Spring Boot 4.0+, Spring Framework 7.0+, Java 17+ (25 recommended).

Boot 4 gives you two modern controller-test tools: `MockMvcTester` (since FW 6.2) is server-side
testing with **native AssertJ** integration and handler inspection; `RestTestClient` (new in FW 7)
is the unified client that runs the same API against mock or real HTTP. Claude gets this wrong by defaulting to raw
`MockMvc` + `andExpect(...)` matchers; both replacements read far better. This skill is the **decision
guide** plus the `MockMvcTester` how-to — for RestTestClient's bind modes see `rest-test-client`.

## When to use / not use

Use to pick a tool or to write `MockMvcTester` (AssertJ) tests. **Do NOT** use for a full
RestTestClient walkthrough — that's its own skill.

## Decision guide

| Scenario | Use |
|---|---|
| File uploads / multipart | **MockMvcTester** |
| Inspect the handler method / thrown exception | **MockMvcTester** |
| Fine-grained `HttpServletRequest` access | **MockMvcTester** |
| Fluent AssertJ `assertThat(...)` on the response | **MockMvcTester** |
| Same tests must run against mock *and* real HTTP | **RestTestClient** |
| Non-JSON content types (XML, etc.) | **RestTestClient** |
| Typed response-body handling across the test pyramid | **RestTestClient** |

Rule of thumb: **server-side, AssertJ, deep introspection → MockMvcTester; one client from unit to
E2E, any converter → RestTestClient.** They coexist; many suites use both.

## MockMvcTester (the AssertJ side)

```java
@WebMvcTest(BookController.class)
class BookControllerMockMvcTesterTest {

    @Autowired MockMvcTester mockMvcTester;   // auto-configured in @WebMvcTest

    @Test void returnsBook() {
        assertThat(mockMvcTester.get().uri("/api/books/1"))
            .hasStatusOk()
            .bodyJson().extractingPath("$.title").isEqualTo("Clean Code");
    }

    @Test void returnsAllBooks() {
        assertThat(mockMvcTester.get().uri("/api/books"))
            .hasStatusOk()
            .bodyJson().extractingPath("$.length()").isEqualTo(3);
    }
}
```

Same endpoint with `RestTestClient` for contrast (expect-style, not AssertJ):

```java
RestTestClient.bindTo(mockMvc).build()
    .get().uri("/api/books/1").exchange()
    .expectStatus().isOk()
    .expectBody().jsonPath("$.title").isEqualTo("Clean Code");
```

## Gotchas

- `MockMvcTester` returns assertable results you pass to AssertJ's `assertThat(...)` — `.hasStatusOk()`,
  `.bodyJson().extractingPath(...)`. Don't mix in the old `.andExpect(...)` style; that's the thing
  being replaced.
- `MockMvcTester` never hits a real socket (it's server-side mock dispatch), so it can't test the
  actual HTTP/connector layer — use `RestTestClient.bindToServer()` for that.
- Prefer `MockMvcTester` when you need to assert on the resolved handler or a thrown exception;
  `RestTestClient` only sees the HTTP response.

```bash
./mvnw test -Dtest=BookControllerMockMvcTesterTest
./mvnw test -Dtest=BookControllerRestTestClientTest
```

## References

- Demo: https://github.com/danvega/mock-vs-rest
- Video: https://youtu.be/xWcqvrpj2PM · Blog: https://www.danvega.dev/blog/mock-vs-rest
- MockMvcTester: https://docs.spring.io/spring-framework/reference/testing/spring-mvc-test-framework/server-performing-requests.html
