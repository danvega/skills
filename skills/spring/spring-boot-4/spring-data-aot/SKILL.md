---
name: spring-data-aot
description: >-
  Enable and validate Spring Data AOT repositories in Spring Boot 4 — move query generation to build
  time for 50-70% faster startup, lower memory, and GraalVM-ready images, via the process-aot Maven
  goal. Use when a task in a Boot 4 project involves Spring Data repositories and startup
  performance, cold starts, native images, or build-time query validation, or when repository methods
  unexpectedly fall back to runtime reflection — even if the user never mentions a version (check the
  build file). Do NOT use for writing the query methods themselves (ordinary Spring Data
  derived/@Query work unchanged) or for non-repository AOT/native config.
---

# Spring Data AOT repositories (Spring Boot 4)

**Baseline:** Spring Boot 4.0+, Spring Framework 7.0+, Java 17+ (25 recommended).

Spring Data AOT pre-generates repository implementations **at build time** instead of parsing method
names and queries at startup — 50-70% faster startup, less memory, and native-image-ready. Claude
gets this wrong by assuming AOT is automatic (it needs the `process-aot` goal) and by trusting that a
bad query method fails the build (it doesn't — it silently falls back to reflection at startup).

## When to use / not use

Use to turn on and *verify* AOT repos, especially for serverless/native. **Do NOT** use it to write
query methods — derived queries and `@Query` are written exactly as before; AOT just changes *when*
they're processed.

## Enable it (Maven)

Repositories are written normally:

```java
public interface CoffeeRepository extends CrudRepository<Coffee, Long> {
    List<Coffee> findByNameContainingIgnoreCase(String name);            // SQL generated at build
    List<Coffee> findByRoastLevelAndOrigin(String roastLevel, String origin);

    @Query("SELECT * FROM coffee WHERE price < :maxPrice ORDER BY price")
    List<Coffee> findAffordableCoffees(BigDecimal maxPrice);
}
```

AOT runs during `package` **only if** the goal is configured — without it, repos fall back to
runtime reflection:

```xml
<plugin>
  <groupId>org.springframework.boot</groupId>
  <artifactId>spring-boot-maven-plugin</artifactId>
  <executions>
    <execution>
      <id>process-aot</id>
      <goals><goal>process-aot</goal></goals>
    </execution>
  </executions>
</plugin>
```

```bash
./mvnw clean package
ls target/spring-aot/main/sources/    # inspect & debug the generated repository code
```

## The critical validation gap (real gotcha)

The AOT processor does **not fail the build** on an invalid method like `findByNamme` (typo) — it
logs an error, marks the method for runtime processing, and the app only fails **at startup**, not at
build. So a "successful" build can still ship a broken repo.

**Fix:** add a test that compares declared repository methods against the AOT-generated metadata
(a JSON file per repository under `target/classes/`) and fails if any were skipped. Run it after
`./mvnw package` — the metadata only exists once AOT has run:

```java
class AotRepositoryValidationTest {   // plain JUnit — no Spring context needed

    @Test
    void coffeeRepositoryMethodsAreAotProcessed() throws IOException {
        JsonNode metadata = JsonMapper.builder().build().readTree(
            Paths.get("target/classes/dev/danvega/coffee/coffee/CoffeeRepository.json").toFile());

        Set<String> processed = StreamSupport.stream(metadata.get("methods").spliterator(), false)
            .map(m -> m.get("name").asText()).collect(Collectors.toSet());

        Set<String> declared = Arrays.stream(CoffeeRepository.class.getDeclaredMethods())
            .map(Method::getName).collect(Collectors.toSet());

        declared.removeAll(processed);
        assertTrue(declared.isEmpty(), "AOT skipped (fell back to reflection): " + declared);
    }
}
```

A signature-aware version (handles overloads) is in the demo repo:
`src/test/java/dev/danvega/coffee/AotRepositoryValidationTest.java`.

## Known limitations (these fall back to reflection)

Value expressions needing runtime evaluation · certain collection return types · `ScrollPosition`
parameters. The validation test above is how you notice when a method silently dropped to reflection.

## References

- Demo: https://github.com/danvega/spring-data-aot
- Video: https://youtu.be/s_kmDbitE8s · Blog: https://www.danvega.dev/blog/spring-data-aot-repositories
- Docs: https://docs.spring.io/spring-data/commons/reference/aot.html
