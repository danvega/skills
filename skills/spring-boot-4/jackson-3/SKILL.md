---
name: jackson-3
description: >-
  Work with Jackson 3 JSON in Spring Boot 4 — the new tools.jackson packages, auto-configured
  JsonMapper, ISO-8601 date defaults, immutable builder config, and @JsonView hierarchies for
  response shaping. Use whenever a Boot 4 task touches JSON serialization/deserialization config:
  customizing the mapper, date/enum formatting, filtering fields per endpoint, fixing
  com.fasterxml.jackson imports, or "different fields for summary vs detail". Do NOT use for choosing
  REST client vs server code, or for Boot 3.x Jackson 2 setups (that is the legacy this replaces).
---

# Jackson 3 (Spring Boot 4)

**Baseline:** Spring Boot 4.0+, Spring Framework 7.0+, Java 17+.

Boot 4 ships **Jackson 3**. Two things Claude gets wrong: (1) it imports
`com.fasterxml.jackson.*` and configures a mutable `ObjectMapper` — Jackson 3 moved to the
**`tools.jackson.*`** packages with an immutable, builder-based `JsonMapper`; (2) it expects numeric
timestamp dates — Jackson 3 defaults to **ISO-8601 strings**.

## When to use / not use

Use for JSON config and response shaping in Boot 4. **Do NOT** use for client-vs-server design
questions, or to re-teach a Boot 3.x Jackson 2 mapper (see Legacy).

## What changed

| | Jackson 2 (Boot 3.x) | Jackson 3 (Boot 4) |
|---|---|---|
| Packages | `com.fasterxml.jackson` | `tools.jackson` (annotations stay `com.fasterxml.jackson.annotation`) |
| Core type | `ObjectMapper` (mutable) | `JsonMapper` (immutable, built via builder) |
| Dates | numeric timestamp | ISO-8601 string |
| Exceptions | checked | unchecked (better in lambdas/streams) |

Spring **auto-configures a `JsonMapper` bean** — inject it; don't `new` one. Customize via
`spring.jackson.*` properties or a `JsonMapper.Builder` customizer bean.

```properties
spring.jackson.use-jackson2-defaults=false      # opt into Jackson 3 defaults (ISO dates, etc.)
spring.jackson.serialization.indent-output=true
```

## Response shaping with @JsonView (avoid DTO sprawl)

Instead of a DTO per view, define a view hierarchy and annotate fields once:

```java
public class Views {
    public interface Summary {}
    public interface Public extends Summary {}      // Public includes Summary fields
    public interface Internal extends Public {}      // Internal includes everything
}

public record Donut(
    @JsonView(Views.Summary.class)  Long id,
    @JsonView(Views.Summary.class)  String name,
    @JsonView(Views.Public.class)   String description,
    @JsonView(Views.Public.class)   BigDecimal price,
    @JsonView(Views.Internal.class) Integer stockCount,
    @JsonView(Views.Internal.class) LocalDateTime createdAt
) {}
```

```java
@RestController
@RequestMapping("/api/donuts")
class DonutController {
    @GetMapping            @JsonView(Views.Summary.class)  List<Donut> summary()  { ... }
    @GetMapping("/public") @JsonView(Views.Public.class)   List<Donut> publik()   { ... }
    @GetMapping("/internal")@JsonView(Views.Internal.class) List<Donut> internal() { ... }
}
```

## Gotchas

- `@JsonView` annotations are still `com.fasterxml.jackson.annotation.JsonView` — only the
  **databind/core** packages moved to `tools.jackson`. Don't "fix" the annotation import.
- Jackson 3 databind ships with a compatibility bridge (3.0.x databind + jackson-annotations 2.20),
  so existing annotations keep working.
- For client-side request filtering, Jackson 3's `hint()` replaces wrapping returns in
  `MappingJacksonValue`.
- Inject the auto-configured `JsonMapper`; constructing your own bypasses Spring's settings and
  registered modules.

<details>
<summary>Legacy (Spring Boot 3.x) — Jackson 2</summary>

```java
import com.fasterxml.jackson.databind.ObjectMapper;        // moved to tools.jackson in v3
@Bean ObjectMapper objectMapper() { return new ObjectMapper().registerModule(new JavaTimeModule()); }
```

Boot 4: drop the manual `ObjectMapper`; rely on the auto-configured `tools.jackson.json.JsonMapper`
and `spring.jackson.*` properties. Set `spring.jackson.use-jackson2-defaults=true` only as a
temporary bridge if old timestamp behavior is required.
</details>

## References

- Demo: https://github.com/danvega/donut-shop
- Video: https://youtu.be/4cvP_qroLH4 
- Blog: https://www.danvega.dev/blog/jackson-3-spring-boot-4
- Spring blog: https://spring.io/blog/2025/10/07/introducing-jackson-3-support-in-spring
