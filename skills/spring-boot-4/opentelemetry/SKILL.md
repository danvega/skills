---
name: opentelemetry
description: >-
  Add production observability to Spring Boot 4 with the official spring-boot-starter-opentelemetry —
  automatic tracing of HTTP/JDBC, trace/span IDs in logs, and OTLP export to Grafana/Jaeger/Zipkin,
  plus @Observed for custom spans. Use when a Boot 4 task is about observability/telemetry: tracing,
  distributed traces, metrics export, log-trace correlation, OpenTelemetry/OTLP, or wiring to an LGTM
  stack. Do NOT use for plain Actuator health/info endpoints, or for app logging config unrelated to
  trace correlation.
---

# OpenTelemetry starter (Spring Boot 4)

**Baseline:** Spring Boot 4.0+, Spring Framework 7.0+, Java 25+.

Boot 4 adds an **official** `spring-boot-starter-opentelemetry`: one dependency gives automatic
instrumentation (HTTP server/client, JDBC), trace/span IDs injected into logs, and OTLP export.
Claude gets this wrong by hand-assembling Micrometer Tracing + an OTel bridge + exporter dependencies
(often alpha) and bespoke config. In Boot 4 the starter wires that for you — Micrometer is still used
internally, but you export via OTLP.

## When to use / not use

Use to add tracing/metrics/log-correlation and ship telemetry to an OTel backend. **Do NOT** use for
basic Actuator health/info, or for logging changes that have nothing to do with trace context.

## The idiom

**1. One dependency:**

```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-opentelemetry</artifactId>
</dependency>
```

**2. Point it at a collector and set sampling:**

```yaml
spring:
  application:
    name: my-service          # becomes the service.name on every span
management:
  tracing:
    sampling:
      probability: 1.0         # 100% in dev; lower in prod to control volume
  otlp:
    tracing:
      endpoint: http://localhost:4318/v1/traces
```

**3. Log correlation is automatic** — trace context appears in each line:

```
2025-11-18 10:30:45 INFO [traceId=abc123, spanId=def456] Processing request...
```

**4. Custom spans with `@Observed`** (HTTP and JDBC are already traced):

```java
@Service
public class OrderService {
    @Observed(name = "order.process", contextualName = "processOrder")
    public Order processOrder(OrderRequest request) {
        return orderRepository.save(createOrder(request));   // becomes its own span
    }
}
```

## Auto-instrumented out of the box

incoming HTTP requests · `RestTemplate` / `RestClient` outgoing calls · `WebClient` · JDBC queries ·
log trace/span injection.

## Gotchas

- `@Observed` needs an `ObservedAspect` — the starter provides it; if custom spans don't appear,
  confirm AOP is on the classpath and the bean is proxied (no self-invocation).
- Set `management.tracing.sampling.probability` **below 1.0 in production** — 100% sampling is for dev
  only or you'll flood the backend.
- The OTLP **traces** endpoint is `/v1/traces` (port 4318 for HTTP); metrics/logs have their own
  paths. Point each signal at the right endpoint.
- Always set `spring.application.name` — it's the `service.name` that lets the backend group your
  traces.

```bash
docker-compose up -d          # Grafana LGTM stack
./mvnw spring-boot:run
open http://localhost:3000    # view traces
```

## References

- Demo: https://github.com/danvega/ot
- Video: https://www.youtube.com/watch?v=6_Y41z7OIv8 · Blog: https://www.danvega.dev/blog/opentelemetry-spring-boot
- Spring blog: https://spring.io/blog/2025/11/18/opentelemetry-with-spring-boot
