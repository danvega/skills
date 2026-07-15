---
name: modular-auto-config
description: >-
  Navigate Spring Boot 4's modular auto-configuration — the breaking change that split the monolithic
  spring-boot-autoconfigure JAR into focused modules, so features only auto-configure when their
  starter is present. Use when migrating Spring Boot 3.x → 4, choosing/adding starters, or debugging
  "it worked before and now it doesn't": missing auto-config, H2 console gone, RestClient/Flyway not
  wired, or the renamed spring-boot-starter-web → spring-boot-starter-webmvc. Also covers the
  spring-boot-autoconfigure-classic escape hatch. Do NOT use for writing your OWN @AutoConfiguration
  classes, or for runtime bean wiring (see bean-registration).
---

# Modular auto-configuration (Spring Boot 4)

**Baseline:** Spring Boot 4.0+, Spring Framework 7.0+, Java 25+.

Boot 4 split the one giant `spring-boot-autoconfigure` JAR (it had grown to 2MB+ covering Kafka,
Security, Mongo, Flyway, JPA, …) into **focused modules**. You now get auto-config **only for what's
explicitly on the classpath**. This is a breaking change, and it's exactly what trips Claude up: it
assumes a raw dependency still "just works" (H2 console, RestClient, Flyway), or uses the old
`spring-boot-starter-web` name.

## When to use / not use

Use when migrating 3.x→4, picking starters, or diagnosing a feature that silently stopped
auto-configuring. **Do NOT** use for authoring your own `@AutoConfiguration` classes, or for
programmatic bean registration — that's `bean-registration`.

## Why things break

In 3.x, one JAR held all auto-config: having JDBC + Web + the H2 **raw** dependency was enough for the
H2 console to switch on. In 4.x the H2-console auto-config lives in its own module
(`spring-boot-h2-console`); the raw `com.h2database:h2` jar no longer drags it in, so the console
silently disappears. Same shape for RestClient, Flyway, etc.

## Fixes

**Use the starter, not the raw dependency** — starters bundle the library *and* its auto-config:

```xml
<!-- Before (3.x): raw dependency -->
<dependency>
  <groupId>com.h2database</groupId><artifactId>h2</artifactId><scope>runtime</scope>
</dependency>

<!-- After (4.x): the starter brings the auto-config module too -->
<dependency>
  <groupId>org.springframework.boot</groupId><artifactId>spring-boot-starter-h2-console</artifactId>
</dependency>
```

**Add only the modules you need** (smaller footprint — good for microservices/native):

```xml
<dependency>
  <groupId>org.springframework.boot</groupId><artifactId>spring-boot-starter-restclient</artifactId>
</dependency>
<dependency>
  <groupId>org.springframework.boot</groupId><artifactId>spring-boot-autoconfigure-data-jpa</artifactId>
</dependency>
```

**Escape hatch for a fast migration** — restore 3.x "everything bundled" behavior, then peel back to
specific starters over time:

```xml
<dependency>
  <groupId>org.springframework.boot</groupId><artifactId>spring-boot-autoconfigure-classic</artifactId>
</dependency>
```

## Common migration issues

| Symptom | Fix |
|---|---|
| `spring-boot-starter-web` not resolving | renamed to **`spring-boot-starter-webmvc`** |
| H2 console not working | `spring-boot-starter-h2-console` |
| RestClient not auto-configured | add `spring-boot-starter-restclient` (also unblocks `http-interface-clients`) |
| Flyway not running | add the appropriate Flyway starter |
| Lots of missing auto-config during migration | add `spring-boot-autoconfigure-classic` as a stopgap |

## Gotchas

- **`spring-boot-starter-web` → `spring-boot-starter-webmvc`** is the rename people hit first.
- Prefer **starters** over `spring-boot-autoconfigure-*` modules unless you specifically want the
  library already present and just need its auto-config.
- Treat `autoconfigure-classic` as a **migration bridge**, not an end state — it brings back the
  bundle you were trying to slim down.
- When a Boot 4 feature "isn't configured," the answer is almost always *a missing module*, not a code
  bug — check the classpath first.

## References

- Spring blog: https://spring.io/blog/2025/10/28/modularizing-spring-boot
- Migration guide: https://github.com/spring-projects/spring-boot/wiki/Spring-Boot-4.0-Migration-Guide#module-dependencies
- Video: https://youtu.be/kTLuhE7_jGU · Blog: https://www.danvega.dev/blog/spring-boot-4-modularization
