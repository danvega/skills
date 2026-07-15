---
name: null-safety
description: >-
  Apply JSpecify null-safety annotations in Spring Boot 4 / Spring Framework 7 — package-level
  @NullMarked plus @Nullable for the exceptions, giving compile-time/IDE null checking and clean
  Kotlin interop. Use whenever working on a Boot 4 / FW 7 codebase and the task touches null
  handling, NPE prevention, "should this be Optional", method/field nullability, package-info.java,
  or org.jspecify imports — even if the user doesn't say "JSpecify". Do NOT use for general Optional
  API design unrelated to Boot 4, or for Spring's old org.springframework.lang.@Nullable (that is
  the legacy pattern this skill replaces).
---

# JSpecify null safety (Spring Boot 4 / Framework 7)

**Baseline:** Spring Boot 4.0+, Spring Framework 7.0+, Java 25+.

Framework 7 standardized on **JSpecify** (`org.jspecify.annotations.*`) for null safety and
re-annotated its own API with it. The idiom is *non-null by default, opt into nullable* — declared
at the **package** level, not per field. This is what Claude gets wrong: it reaches for
`org.springframework.lang.@Nullable`/`@NonNull` (now deprecated) or sprinkles `@Nullable` everywhere
instead of flipping the package default.

## When to use / not use

Use when adding or reviewing null contracts in a Boot 4 / FW 7 module. **Do NOT** hand-roll
`Optional` wrappers for fields, and **do NOT** use Spring's old `org.springframework.lang`
annotations — see Legacy below.

## The idiom

Mark the whole package non-null once, in `package-info.java`:

```java
// src/main/java/dev/danvega/demo/package-info.java
@NullMarked
package dev.danvega.demo;

import org.jspecify.annotations.NullMarked;
```

Now every type, parameter, and return in that package is **non-null by default**. Only annotate the
exceptions:

```java
import org.jspecify.annotations.Nullable;

public class UserService {

    // Non-null by default (from @NullMarked) — callers can rely on a real User
    public User findById(Long id) {
        return userRepository.findById(id)
            .orElseThrow(() -> new UserNotFoundException(id));
    }

    // Explicitly nullable parameter — the one allowed null
    public List<User> search(@Nullable String name) {
        return (name == null) ? userRepository.findAll()
                              : userRepository.findByNameContaining(name);
    }
}
```

## Setup & gotchas

- Dependency: `org.jspecify:jspecify` (Boot manages the version; usually already transitive via
  Framework 7 — add it explicitly if you import the annotations directly).
- These are **build/IDE-time** contracts, not runtime enforcement. Nothing throws on a null at
  runtime just because a field is `@NullMarked` — wire IntelliJ/NullAway/Checker Framework to get
  the actual warnings. Don't promise the user runtime guarantees.
- Put `@NullMarked` on **`package-info.java`**, not on each class. Per-class is noisy and easy to
  forget; the package default is the whole point.
- `@Nullable` is a **type-use** annotation in JSpecify — `List<@Nullable String>` means nullable
  elements, `@Nullable List<String>` means a nullable list. Placement matters.
- Kotlin reads these automatically: a non-null Java return becomes a Kotlin non-null type, a
  `@Nullable` one becomes `T?`. Great for mixed codebases.

<details>
<summary>Legacy (Spring Boot 3.x) — don't use in Boot 4</summary>

```java
// Spring's own annotations — deprecated in favor of JSpecify
import org.springframework.lang.Nullable;
import org.springframework.lang.NonNull;
```

3.x used `org.springframework.lang.@Nullable/@NonNull` (declaration annotations, applied per
element). FW 7 deprecates these; migrate to `org.jspecify` with a package-level `@NullMarked`.
</details>

## References

- Coffeeshop demo: https://github.com/danvega/coffeeshop
- Video: https://youtu.be/QlGnaRoujL8 · Blog: https://www.danvega.dev/blog/spring-boot-4-null-safety
- JSpecify: https://jspecify.dev/ · FW null safety: https://docs.spring.io/spring-framework/reference/core/null-safety.html
