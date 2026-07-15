---
name: api-versioning
description: >-
  Version REST endpoints with Spring Framework 7's first-class API versioning — the `version`
  attribute on @GetMapping/@RequestMapping plus ApiVersionConfigurer, instead of manual path routing
  or separate controllers. Use when a Boot 4 / FW 7 task is about evolving an API you EXPOSE while
  keeping old clients working: "v1 vs v2 endpoint", "version this response", header/media-type/path
  versioning, deprecation/Sunset headers. Do NOT use for choosing a client to CALL a versioned API
  (see http-interface-clients), or for general request mapping unrelated to versions.
---

# API versioning (Spring Framework 7)

**Baseline:** Spring Boot 4.0+, Spring Framework 7.0+, Java 25+.

Framework 7 adds a `version` attribute to request-mapping annotations plus an `ApiVersionConfigurer`
to pick the versioning strategy. Claude gets this wrong by hand-rolling version routing — separate
`/api/v1/...` and `/api/v2/...` paths, manual `Accept`-header parsing, or duplicate controllers. In
FW 7 the framework resolves the version and routes for you.

## When to use / not use

Use to serve multiple versions of an endpoint you own. **Do NOT** use this to *consume* a versioned
API — that's `http-interface-clients` (set the version header on the client). For plain, unversioned
routing, ordinary `@GetMapping` is fine.

## The idiom

**1. Enable a versioning strategy** via `WebMvcConfigurer`:

```java
@Configuration
public class ApiVersioningConfig implements WebMvcConfigurer {
    @Override
    public void configureApiVersioning(ApiVersionConfigurer configurer) {
        configurer.useMediaTypeParameterVersioning();   // Accept: application/json;version=1.0
        // alternatives: .useRequestHeaderVersioning("X-API-Version")
        //               .usePathSegmentVersioning(...) / .useQueryParameterVersioning("version")
    }
}
```

**2. Tag handlers with `version`** — same path, the framework dispatches by version:

```java
@RestController
@RequestMapping("/api/users")
public class UserController {

    @GetMapping(version = "1.0")
    public UserDTOv1 getUserV1(@PathVariable Long id) { ... }   // {"id":1,"name":"Dan Vega"}

    @GetMapping(version = "2.0")
    public UserDTOv2 getUserV2(@PathVariable Long id) { ... }   // {"id":1,"firstName":...,"lastName":...}
}
```

**3. Clients select the version** (media-type-parameter strategy shown):

```bash
curl -H "Accept: application/json;version=1.0" http://localhost:8080/api/users/1
curl -H "Accept: application/json;version=2.0" http://localhost:8080/api/users/1
```

## Gotchas

- Pick **one** strategy in `configureApiVersioning` and use it consistently; the `version` attribute
  is interpreted according to it.
- `version = "1.1+"` matches "1.1 or higher" — handy for "current and forward" handlers so you don't
  re-tag every minor bump.
- Configure a baseline/default version so requests with no version header still resolve, rather than
  404-ing.
- Pair with RFC-compliant `Deprecation`, `Sunset`, and `Link` response headers to signal v1 retirement
  — versioning is the routing half; the headers are how clients learn to migrate.

## References

- Demo: https://github.com/danvega/api-users
- Video: https://youtu.be/qjo2tYf01xo · Blog: https://www.danvega.dev/blog/spring-boot-4-api-versioning
- Docs: https://docs.spring.io/spring-framework/reference/web/webmvc-versioning.html
