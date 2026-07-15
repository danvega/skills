---
name: resilience
description: >-
  Add retries and concurrency limits with Spring Framework 7's BUILT-IN resilience — @Retryable
  (exponential backoff + jitter), @ConcurrencyLimit, and @EnableResilientMethods — no Spring Retry or
  Resilience4j dependency. Use when a Boot 4 / FW 7 task needs fault tolerance: retry a flaky call,
  back off and re-try, limit concurrent executions of an expensive method, or the user reaches for
  spring-retry / @Recover / Resilience4j annotations. Do NOT use for circuit breakers, rate limiting,
  or bulkheads beyond simple concurrency caps (still Resilience4j territory), nor for HTTP-client
  timeouts/connection pools.
---

# Core resilience — @Retryable & @ConcurrencyLimit (Framework 7)

**Baseline:** Spring Boot 4.0+, Spring Framework 7.0+, Java 25+.

Framework 7 brings retry and concurrency control into core — **no external library**. Claude gets
this wrong by adding the `org.springframework.retry:spring-retry` dependency and importing
`@Retryable` from `org.springframework.retry.annotation`. In Boot 4 the annotations live in core
Spring (`org.springframework.*` resilience support) and are enabled with `@EnableResilientMethods`.

## When to use / not use

Use for method-level retry with backoff and for capping concurrent executions. **Do NOT** reach here
for circuit breakers, token-bucket rate limiting, or full bulkheads — those still warrant Resilience4j.
And this is not a substitute for proper client read/connect timeouts.

## The idiom

**1. Enable it once:**

```java
@Configuration
@EnableResilientMethods   // turns on @Retryable and @ConcurrencyLimit
public class ResilienceConfig { }
```

**2. Retry with exponential backoff + jitter:**

```java
@Retryable(
    maxAttempts = 4,
    delay = 500,          // ms before first retry
    multiplier = 2.0,     // 500ms, 1s, 2s, 4s ...
    maxDelay = 5000,      // cap per-attempt delay
    jitter = 100          // random spread to avoid thundering herd
)
public String fetchData(String id) {
    // throws on failure -> retried with increasing delay
}
```

**3. Limit concurrency:**

```java
@ConcurrencyLimit(2)   // at most 2 concurrent executions; the rest queue and wait
public String performHeavyOperation(String taskId) { ... }
```

**4. Combine** (single-flight with retry):

```java
@ConcurrencyLimit(1)
@Retryable(maxAttempts = 2, delay = 1000)
public String criticalOperation(String id) { ... }
```

## Gotchas

- These are **proxy-based** (like `@Transactional`): only **external** calls through the bean are
  intercepted. A self-invocation (`this.fetchData(...)`) is **not** retried. Call across a bean
  boundary.
- Scope `@Retryable` to the operations that are actually transient/idempotent — retrying a
  non-idempotent write can double-apply side effects.
- Restrict which exceptions retry (e.g. transient I/O) rather than retrying everything, so genuine
  bugs surface fast instead of looping.
- This replaces basic Spring Retry usage; if migrating, drop the `spring-retry` dependency and the
  old `@EnableRetry` and switch imports to core.

<details>
<summary>Legacy (Spring Boot 3.x) — external Spring Retry</summary>

```xml
<dependency><groupId>org.springframework.retry</groupId><artifactId>spring-retry</artifactId></dependency>
```
```java
@EnableRetry                                   // 3.x
import org.springframework.retry.annotation.Retryable;
```

Boot 4: remove the dependency, replace `@EnableRetry` with `@EnableResilientMethods`, and import the
core annotations.
</details>

## References

- Demo: https://github.com/danvega/quick-bytes
- Video: https://youtu.be/CT1wGTwOfg0 · Blog: https://www.danvega.dev/blog/spring-boot-4-native-retry-support
- Docs: https://docs.spring.io/spring-framework/reference/core/resilience.html
