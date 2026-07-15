---
name: spring-security-mfa
description: >-
  Require multi-factor authentication in Spring Security 7 (Boot 4) with
  @EnableMultiFactorAuthentication — declare required factors (password + one-time token), let Spring
  route users through each, and plug in a custom OneTimeTokenService. Use when a Boot 4 task involves
  MFA / 2FA / step-up auth, one-time tokens (OTT), magic links, or factor-based authorization with
  Spring Security 7. Do NOT use for basic single-factor form/HTTP-Basic login, OAuth2/OIDC client or
  resource-server setup, or method-level @PreAuthorize rules unrelated to factors.
---

# Multi-factor authentication — Spring Security 7 (Boot 4)

**Baseline:** Spring Boot 4.0+, Spring Security 7.0+, Java 25+.

Security 7 adds `@EnableMultiFactorAuthentication`: you **declare** the required factors and Spring
automatically routes a user through any factor they haven't satisfied before granting access. Claude
gets this wrong by hand-building session flags, custom filters, and manual redirect logic to fake
"step 1 then step 2". In Security 7 that orchestration is declarative.

## When to use / not use

Use to require more than one auth factor (e.g. password **and** a one-time token). **Do NOT** use for
single-factor login, OAuth2/OIDC, or `@PreAuthorize` authorization unrelated to factor completion.

## The idiom

**1. Declare required factors:**

```java
@Configuration
@EnableWebSecurity
@EnableMultiFactorAuthentication(authorities = {
        FactorGrantedAuthority.PASSWORD_AUTHORITY,
        FactorGrantedAuthority.OTT_AUTHORITY          // password + one-time token
})
public class SecurityConfig {

    @Bean
    SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
        return http
            .authorizeHttpRequests(auth -> auth
                .requestMatchers("/admin/**").hasRole("ADMIN")
                .anyRequest().authenticated())
            .formLogin(Customizer.withDefaults())
            .oneTimeTokenLogin(Customizer.withDefaults())   // the second factor
            .build();
    }
}
```

Spring tracks which `FactorGrantedAuthority` values the session has and redirects to complete the
missing one — you don't write that routing.

**2. Customize the OTT** (e.g. a 5-digit PIN instead of a UUID) by implementing `OneTimeTokenService`:

```java
@Component
public class CustomOneTimeTokenService implements OneTimeTokenService {
    private final Map<String, OneTimeToken> tokens = new ConcurrentHashMap<>();

    @Override
    public OneTimeToken generate(GenerateOneTimeTokenRequest request) {
        String token = String.format("%05d", new Random().nextInt(100000));
        Instant expiresAt = Instant.now().plus(5, ChronoUnit.MINUTES);
        var ott = new DefaultOneTimeToken(token, request.getUsername(), expiresAt);
        tokens.put(token, ott);
        // real impl: email/SMS the link; demo logs it:
        System.out.println("OTT login: http://localhost:8080/login/ott?token=" + token);
        return ott;
    }

    @Override
    public Authentication consume(ConsumeOneTimeTokenRequest request) {
        OneTimeToken token = tokens.remove(request.getToken());
        if (token == null || token.getExpiresAt().isBefore(Instant.now()))
            throw new InvalidOneTimeTokenException("Invalid or expired token");
        return new OneTimeTokenAuthenticationToken(token.getUsername());
    }
}
```

## Gotchas

- The factor flow is **driven by the declared authorities** — a user with only `PASSWORD_AUTHORITY`
  is redirected to satisfy `OTT_AUTHORITY` before reaching protected resources. Don't re-implement
  that gate manually.
- `consume` must **remove/invalidate** the token (single-use) and check expiry — the example does
  both; a token left in the map is a replay risk.
- The in-memory `Map` token store is demo-only — back it with a real store (DB/Redis) in production,
  and deliver the link via email/SMS rather than logging it.
- This is distinct from method authorization: factors gate authentication completion, not
  `@PreAuthorize` rules.

## References

- Demo: https://github.com/danvega/mfa
- Video: https://youtu.be/KmNAqlaKwjw · Blog: https://www.danvega.dev/blog/spring-security-7-multi-factor-authentication
- Docs: https://docs.spring.io/spring-security/reference/servlet/authentication/mfa.html
- OTT: https://docs.spring.io/spring-security/reference/servlet/authentication/onetimetoken.html
