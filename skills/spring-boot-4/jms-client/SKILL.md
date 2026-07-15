---
name: jms-client
description: >-
  Send and receive JMS messages with the fluent JmsClient API (Spring Framework 6.1+/Boot 4) instead
  of JmsTemplate — covers basic send, QoS (priority/TTL/delay), custom headers, synchronous receive,
  receive-and-convert, and request-reply. Use when a Boot 4 task involves JMS / message queues /
  ActiveMQ Artemis: producing or consuming messages, "send an order to a queue", RPC-over-JMS, or the
  user reaches for JmsTemplate. Do NOT use for Kafka or RabbitMQ/AMQP (different APIs), or for plain
  in-process events (use ApplicationEventPublisher).
---

# JmsClient — fluent JMS (Spring Framework 6.1+, current in Boot 4)

**Baseline:** Spring Boot 4.0+, Spring Framework 7.0+ (API since 6.1), Java 25+.

`JmsClient` is the modern, fluent, type-safe replacement for `JmsTemplate`: chainable sends, built-in
conversion, and per-message QoS without juggling `MessageCreator`/`MessagePostProcessor`. Claude gets
this wrong by defaulting to `JmsTemplate.convertAndSend(...)` and anonymous `MessageCreator` lambdas.
Prefer `JmsClient` in Boot 4.

## When to use / not use

Use for JMS messaging (Artemis/ActiveMQ). **Do NOT** use for Kafka or RabbitMQ — those have their own
clients — and don't use JMS for purely in-JVM events (`ApplicationEventPublisher` is lighter).

## The idiom

Inject `JmsClient` (auto-configured when a JMS `ConnectionFactory` is present) and chain:

```java
@Service
public class OrderMessagingService {
    private final JmsClient jms;
    public OrderMessagingService(JmsClient jms) { this.jms = jms; }

    public void sendOrder(Order order) {
        jms.send("orders.queue").withBody(order);             // basic fire-and-forget
    }

    public void sendPriorityOrder(Order order) {
        jms.send("orders.queue")                               // quality of service
           .withPriority(9)
           .withTimeToLive(Duration.ofMinutes(5))
           .withBody(order);
    }

    public OrderConfirmation processOrder(Order order) {       // request-reply (RPC style)
        return jms.requestAndReceive("orders.queue")
                  .withBody(order)
                  .convertTo(OrderConfirmation.class);
    }
}
```

Consume with `@JmsListener` (unchanged from 3.x):

```java
@Component
public class OrderConsumer {
    @JmsListener(destination = "orders.queue")
    public void onOrder(Order order) { /* process */ }
}
```

## The 7 patterns it covers

basic send · QoS (TTL/priority/delivery delay) · custom headers (`.withHeader(...)`) · synchronous
receive with timeout · receive-and-convert (type-safe) · request-reply · reusable operation handle
(preconfigure a `send(...)` builder once and reuse for throughput).

## Gotchas

- `JmsClient` is only auto-configured if a `ConnectionFactory` exists — bring a broker starter
  (Artemis/ActiveMQ) and config. Under modular auto-config, ensure the JMS starter is present (see
  `modular-auto-config`).
- `requestAndReceive` **blocks** waiting for the reply — set a receive timeout; don't call it on a
  hot request thread without one.
- `withBody(object)` uses the configured `MessageConverter` (JSON via Jackson is typical) — give the
  consumer a compatible converter or it won't deserialize.
- `@JmsListener` is still the consumer API; `JmsClient` is the producer/synchronous-receive side.

Local broker:

```bash
docker-compose up -d         # ActiveMQ Artemis; console http://localhost:8161 (admin/admin)
./mvnw spring-boot:run
```

## References

- Demo: https://github.com/danvega/jms-orders
- Video: https://youtu.be/91xVrWlzIe4 · Blog: https://www.danvega.dev/blog/jms-client
- Docs: https://docs.spring.io/spring-boot/reference/messaging/jms.html
