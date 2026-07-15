---
name: bean-registration
description: >-
  Register beans programmatically in Spring Framework 7 with the BeanRegistrar interface — pick or
  configure beans at startup from properties/environment/conditions, with a clean lambda API and AOT
  support. Use when a task in a Boot 4 / FW 7 project needs DYNAMIC bean definitions — "register a
  bean based on a property", conditional wiring the @Conditional annotations can't express,
  plugin/strategy selection, or the user reaches for BeanDefinitionRegistryPostProcessor /
  BeanFactoryPostProcessor / ImportBeanDefinitionRegistrar — even if the user never mentions a
  version (check the build file). Do NOT use for ordinary static beans (just use @Bean/@Component) or
  for simple on/off toggles that @ConditionalOnProperty already handles.
---

# Programmatic bean registration — BeanRegistrar (Framework 7)

**Baseline:** Spring Boot 4.0+, Spring Framework 7.0+, Java 17+ (25 recommended).

Framework 7 adds the `BeanRegistrar` interface: a clean, AOT-friendly way to register beans in code,
with access to the `Environment`. It replaces the verbose `BeanDefinitionRegistryPostProcessor` /
`ImportBeanDefinitionRegistrar` dance. Claude gets this wrong by reaching for those old
post-processor APIs (lots of `BeanDefinitionBuilder`/`RootBeanDefinition` ceremony) when a
`BeanRegistrar` is a few lines.

## When to use / not use

Use when *which* bean (or how it's configured) is decided at runtime from properties/environment.
**Do NOT** use for static beans — `@Bean`/`@Component` is correct there — and don't reach for it when
`@ConditionalOnProperty` already covers a simple toggle. Reserve it for selection logic richer than
annotations express.

## The idiom

**1. Implement `BeanRegistrar`** — `register` receives a `BeanRegistry` and the `Environment`:

```java
public class MessageServiceRegistrar implements BeanRegistrar {

    @Override
    public void register(BeanRegistry registry, Environment env) {
        String type = env.getProperty("app.message-type", "email");

        switch (type.toLowerCase()) {
            case "email" -> registry.registerBean("messageService", EmailMessageService.class,
                spec -> spec.description("Email service via BeanRegistrar"));
            case "sms"   -> registry.registerBean("messageService", SmsMessageService.class,
                spec -> spec.description("SMS service via BeanRegistrar"));
            default      -> throw new IllegalStateException("Unknown app.message-type: " + type);
        }
    }
}
```

**2. Import it** from any `@Configuration`:

```java
@Configuration
@Import(MessageServiceRegistrar.class)
public class ModernConfig { }
```

The `spec ->` lambda configures the `BeanRegistry.Spec` — `description(...)`, `prototype()`,
`primary()`, `lazyInit()`, `supplier(...)`, etc.

## Gotchas

- `register` runs **early**, during bean-definition registration — the `Environment` is available,
  but other application beans generally are **not yet instantiated**. Decide based on config, not on
  injected collaborators.
- Use `spec.supplier(...)` when you need to compute the instance yourself; otherwise pass the class
  and let Spring instantiate + autowire it.
- It's **AOT/native-image compatible** — a reason to prefer it over runtime reflection-heavy
  post-processors.
- Why `BeanRegistrar` over `@Bean`: equal simplicity, far more flexibility (it's a lambda over the
  registry), where `BeanDefinitionRegistryPostProcessor` was flexible but verbose.

<details>
<summary>Legacy (pre-FW7) — the verbose path BeanRegistrar replaces</summary>

```java
public class MyBdrpp implements BeanDefinitionRegistryPostProcessor {
    @Override public void postProcessBeanDefinitionRegistry(BeanDefinitionRegistry registry) {
        var bd = BeanDefinitionBuilder.genericBeanDefinition(EmailMessageService.class)
                    .getBeanDefinition();
        registry.registerBeanDefinition("messageService", bd);
    }
}
```

Prefer `BeanRegistrar` — it's less code, gives typed `Environment` access, and works under AOT.
</details>

## References

- Demo: https://github.com/danvega/sb4-bean-registrar
- Video: https://youtu.be/yh760wTFL_4 · Blog: https://www.danvega.dev/blog/programmatic-bean-registration
- Docs: https://docs.spring.io/spring-framework/reference/core/beans/java/programmatic-bean-registration.html
