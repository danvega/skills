---
name: http-interface-clients
description: >-
  Build declarative HTTP clients in Spring Boot 4 with @ImportHttpServices + @HttpExchange
  interfaces — zero boilerplate, no manual RestClient/proxy-factory wiring. Use whenever a Boot 4
  app needs to CALL another HTTP/REST service (third-party API, another microservice): the user says
  "client for service X", "consume this API", "fetch from an endpoint", or reaches for RestTemplate /
  WebClient / RestClientAdapter / HttpServiceProxyFactory — even if the user never mentions a version
  (check the build file). Do NOT use for defining your OWN server
  endpoints (that is plain @RestController), for versioning endpoints you expose (see api-versioning),
  or for adding retries to the calls (see resilience).
---

# HTTP Interface Clients (Spring Boot 4)

**Baseline:** Spring Boot 4.0+, Spring Framework 7.0+, Java 17+ (25 recommended).

Boot 4 adds `@ImportHttpServices`, which registers `@HttpExchange` interfaces as beans for you. You
define the client as an **interface**; Spring generates the implementation. This is what Claude gets
wrong: it writes `RestTemplate` boilerplate, or hand-wires `RestClientAdapter` + `HttpServiceProxyFactory`
in a `@Bean` method. In Boot 4 that wiring is gone.

## When to use / not use

Use to consume an external/other-service HTTP API. **Do NOT** use for your own controllers
(`@RestController`), to version endpoints you serve (see `api-versioning`), or to add retry/backoff —
layer `resilience`'s `@Retryable` on the calling service method instead.

## The idiom

**1. Declare the interface** with `@HttpExchange` + per-method verb annotations:

```java
@HttpExchange(url = "https://jsonplaceholder.typicode.com", accept = "application/json")
public interface TodoService {

    @GetExchange("/todos")
    List<Todo> getAllTodos();

    @GetExchange("/todos/{id}")
    Todo getTodoById(@PathVariable Long id);

    @PostExchange("/todos")
    Todo createTodo(@RequestBody Todo todo);
}
```

**2. Import it** — that's the whole configuration:

```java
@Configuration(proxyBeanMethods = false)
@ImportHttpServices(TodoService.class)   // register multiple: { TodoService.class, UserService.class }
public class HttpClientConfig { }
```

**3. Inject and use** like any bean:

```java
@Service
class TodoFacade {
    private final TodoService todos;
    TodoFacade(TodoService todos) { this.todos = todos; }   // constructor-injected proxy
}
```

## Gotchas

- The HTTP client backing the proxy comes from auto-config. Under modular auto-config you must have a
  client starter on the classpath (e.g. `spring-boot-starter-restclient`) — without it the proxy
  can't be built. See the `modular-auto-config` skill if this fails to wire.
- Prefer configuring the base URL per group over baking it into the `url` attribute:
  `spring.http.serviceclient.<group>.base-url=...` properties (group defaults to `"default"`;
  same prefix covers timeouts/headers), or a `RestClientHttpServiceGroupConfigurer` bean for
  programmatic control (auth headers, etc.).
- Return records/DTOs, not raw `String` — the converter deserializes for you, and records keep it
  type-safe.
- `@GetExchange`/`@PostExchange` etc. are shorthand for `@HttpExchange(method = ...)`; use the
  shorthands.

<details>
<summary>Legacy (Spring Boot 3.x) — the boilerplate Boot 4 removes</summary>

```java
@Bean
TodoService todoService(RestClient.Builder builder) {
    RestClient client = builder.baseUrl("https://jsonplaceholder.typicode.com").build();
    var adapter = RestClientAdapter.create(client);
    var factory = HttpServiceProxyFactory.builderFor(adapter).build();
    return factory.createClient(TodoService.class);
}
```

Replace this entire `@Bean` with `@ImportHttpServices(TodoService.class)`. Don't reach for
`RestTemplate` at all in Boot 4.
</details>

## References

- Demo: https://github.com/danvega/sb4-http-interfaces
- Video: https://youtu.be/TEd5e4Thu7M · Blog: https://www.danvega.dev/blog/http-interfaces-spring-boot-4
- Docs: https://docs.spring.io/spring-framework/reference/integration/rest-clients.html#rest-http-service-client
