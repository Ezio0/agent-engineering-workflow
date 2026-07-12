# 10 — Coding Practices (Cross-Cutting)

> **Status**: Active
> **Last reviewed**: 2026-07-12
> **Related**: [中文版](_index_zh.md)
>
> Cross-cutting topic. Applies to **all code written in any project** — Stage 6
> (Implementation) consumes this. Stage 6 (Implementation) does NOT duplicate
> these rules; it references this section.

---

## 1. Overview

Coding Practices is the **craft layer**. Where Stage 6 is the procedure
("how do I execute a task"), Stage 10 is the style ("how do I write the code
itself").

**Strict boundary with Stage 6:**

| Concern | Stage |
|---------|-------|
| How to load context, pick a task, run the 5-step loop | Stage 6 |
| **How to write a function, name a variable, handle an error, log an event** | **Stage 10** |
| How to commit | Stage 8 |
| How to verify the report | Stage 7 |

This section is **language-agnostic by default**; language-specific guidance
appears in §10 (Language Notes) with concrete idioms for Python / TypeScript /
etc. The principles apply universally; only the syntax differs.

### Three load-bearing principles

These three ideas appear throughout the section. Memorize them.

1. **Readability > cleverness.** Code is read 100× more than it's written.
   Optimize for the reader, not the writer.
2. **Explicit > implicit.** Type hints, named arguments, error codes. Implicit
   behavior is a debugging time bomb.
3. **No magic in user data path.** Engine code must never carry hardcoded
   user values, environment values, or "tuning" constants that should be
   config. This is also enforced by the architecture principle in SOUL.md;
   see §10 for cross-reference.

---

## 2. Naming

### 2.1 Case conventions by language

| Language | Variables / functions | Classes | Constants | Modules / files |
|----------|------------------------|---------|-----------|------------------|
| Python | `snake_case` | `PascalCase` | `UPPER_SNAKE_CASE` | `snake_case.py` |
| TypeScript / JS | `camelCase` | `PascalCase` | `UPPER_SNAKE_CASE` | `kebab-case.ts` |
| Go | `camelCase` (unexported) / `PascalCase` (exported) | `PascalCase` | `PascalCase` (no const convention) | `snake_case.go` |
| Rust | `snake_case` | `PascalCase` | `UPPER_SNAKE_CASE` | `snake_case.rs` |

**No mixed conventions** within a single language. Pick one. Don't write
`My_Variable` in Python, `myFunction` in JS, etc.

### 2.2 Naming goals

| Goal | Means | Example |
|------|-------|---------|
| **Clarity** | Full words, not abbreviations | `user_count`, not `usr_cnt` |
| **Searchability** | Distinctive names, not generic | `parse_config_file`, not `process` |
| **Pronounceability** | Easy to say in conversation | `parser`, not `psr` |
| **No encoding** | No type info in name | `users`, not `user_list` / `userArr` |

### 2.3 The `_` prefix convention

`_` prefix means **private to module / class** — "do not import from outside".

```python
# Good
def public_api():
    return _helper()

def _helper():           # underscore prefix = private
    ...
```

```python
# Bad — exported by accident
def helper():           # looks public, but shouldn't be
    ...

# Caller now depends on helper() even though it was intended private
from module import helper
```

**However:** `_` is a **convention**, not enforcement. Other languages use
`private` / `internal` keywords. Python relies on convention. Trust the
convention; rename if you accidentally call a private function from outside.

### 2.4 Names to avoid

| Anti-pattern | Why |
|--------------|-----|
| `data`, `info`, `stuff`, `temp`, `val`, `obj` | Tells reader nothing |
| `foo`, `bar`, `baz` | Toy examples, not production |
| Single letters except loop counters | `i`/`j`/`k` OK; `a`/`x` not OK |
| Type-encoded names (`str_name`, `int_count`) | Type belongs in hint, not name |
| Redundant prefixes (`class_foo`, `func_bar`) | Class is `Foo`, function is `bar` |
| Trailing `_` for "I don't know" | Rename instead |
| Names matching keywords (`class`, `type`) | Syntax error or shadowing |

---

## 3. Types and Signatures

### 3.1 Type hints: when required, when optional

| Language | Required when | Optional when |
|----------|---------------|---------------|
| Python | Public API, library boundaries, anything in Spec | One-line scripts, throwaway tests |
| TypeScript | **Always** (no `any` in committed code) | Never optional |
| Rust | **Always** (compiler-enforced) | Never optional |

### 3.2 Type hints — what to annotate

```python
# Annotate public function signatures
def calculate_score(user_id: str, weights: dict[str, float]) -> float:
    ...

# Internal helpers — annotate when shared, skip when obvious
def _normalize(x: float) -> float:        # obvious from name + body
    return x / 100.0

# Variables — annotate only when type isn't obvious from RHS
config_path: Path = Path("/etc/app.toml")  # Path from string — annotate
items = []                                  # obvious — skip
```

### 3.3 What NOT to over-type

```python
# Overkill — type is obvious
count: int = 0
name: str = "alice"

# Useful — type isn't obvious from value
scores: dict[str, list[float]] = {}
results: list[UserResult] = parse_results(scores)

# Wrong — type lies
def get_user(id: int) -> User:           # returns User, not None
    return self._cache.get(id) or User.default()
    # ^ should be -> User | None, OR handle the default explicitly
```

### 3.4 `Optional[T]` vs `T | None`

In Python 3.10+, prefer `T | None`. In 3.9 and earlier, use `Optional[T]`.
Pick one per codebase; don't mix in the same file.

### 3.5 Avoid `Any`

`Any` defeats type checking. Use it only when:
- Interfacing with untyped libraries
- Dynamic data (e.g., JSON parsing) before validation

Never use `Any` to silence a type error without understanding it.

---

## 4. Error Handling

### 4.1 The four levels

| Level | When to use | Example |
|-------|-------------|---------|
| **Validation error** | Caller passed invalid input | `ValueError`, `TypeError` |
| **Domain error** | Business rule violated | `UserNotFoundError`, `InsufficientFundsError` |
| **Infrastructure error** | External system failed | `DatabaseConnectionError`, `TimeoutError` |
| **Internal error** | Programmer mistake, never expected | `AssertionError`, `RuntimeError` |

Pick the right level. A "user not found" is **not** an infrastructure error;
a "database timeout" is **not** a validation error. Mixing them defeats
error-handling strategy.

### 4.2 Custom exceptions vs builtins

```python
# Custom domain exception
class UserNotFoundError(LookupError):
    """Raised when a user_id lookup fails."""
    
    def __init__(self, user_id: str):
        self.user_id = user_id
        super().__init__(f"User not found: {user_id}")

# Caller
try:
    user = get_user(uid)
except UserNotFoundError as e:
    logger.warning(f"User lookup failed: {e.user_id}")
    return None
```

**Why custom?** Builtins (`KeyError`, `ValueError`) are too generic. Custom
exceptions let callers handle specifically. **But**: only create custom
exceptions for domain rules, not for every function.

### 4.3 Never swallow exceptions

```python
# NEVER
try:
    do_something()
except Exception:
    pass

# OK if intentional + logged
try:
    do_optional_thing()
except SomeSpecificError as e:
    logger.debug(f"Optional thing skipped: {e}")

# Better: fail loud if unexpected
try:
    do_something()
except ExpectedError as e:
    handle(e)
except Exception as e:
    logger.exception("Unexpected error in do_something")
    raise
```

If you catch, do one of: (a) handle meaningfully, (b) log + re-raise,
(c) log + return a defined fallback. Bare `except: pass` is a bug.

### 4.4 Error messages

**Good error messages:**
- State what failed (`"User not found: {user_id}"`)
- Include the value that caused it (`"Invalid input: got {value}, expected ..."`)
- Suggest the fix if obvious (`"Check the user_id; it must be a UUID"`)

**Bad error messages:**
- `"Error"` (no information)
- `"Something went wrong"` (cliché)
- `"Invalid"` (no detail on what was invalid)

### 4.5 When to raise vs return error

| Pattern | Use when |
|---------|----------|
| **Raise exception** | Exceptional conditions; happy path doesn't include errors |
| **Return Result type** (`(T, Error)` tuple or `Result[T, E]`) | Expected alternative outcomes; caller should handle every case |

Prefer raise for "this should never happen in correct usage"; prefer return
for "this is one of several outcomes the caller must handle".

---

## 5. Logging

### 5.1 Levels

| Level | When | Example |
|-------|------|---------|
| `DEBUG` | Diagnostic detail; off in production | `"Cache hit for key=X"` |
| `INFO` | Notable events in normal flow | `"User logged in: {user_id}"` |
| `WARNING` | Recoverable problems | `"Rate limit hit, backing off 30s"` |
| `ERROR` | Operation failed, but service continues | `"Failed to send email to {user_id}"` |
| `CRITICAL` | Service cannot continue | `"Database unreachable, shutting down"` |

### 5.2 What to log

| Log | Why |
|-----|-----|
| External API calls (request + response code, NOT body) | Audit + debugging |
| State transitions (logged in, started, completed) | Audit |
| Failures (with full context) | Debugging |
| Slow operations (with duration) | Performance debugging |

| Do NOT log | Why |
|-------------|-----|
| PII (passwords, tokens, full emails) | Security / compliance |
| Request/response **bodies** for sensitive endpoints | Security |
| Hot-path debug logs (every loop iteration) | Performance |
| `"Starting function X"` at the top of every function | Noise |

### 5.3 Logging API

```python
# Good — structured, contextual
logger.info("user.login", extra={"user_id": uid, "ip": ip})
logger.warning("rate_limit.hit", extra={"user_id": uid, "retry_after": 30})

# Avoid — unformatted strings, no context
logger.info("user logged in")
logger.warning(f"rate limit hit")        # extra={} preferred over f-string
```

### 5.4 `print` is not logging

`print` goes to stdout, has no level, no timestamp, no context. Use it only
for CLI output to the user. Never for diagnostic logging in library code.

```python
# CLI tool — print is correct
def main():
    print(f"Processing {len(files)} files...")
    ...

# Library code — print is wrong
def process_files(files):
    print(f"Processing {len(files)} files...")  # BAD
    logger.info("process_files.start", extra={"count": len(files)})
    ...
```

---

## 6. Comments and Docstrings

### 6.1 The cardinal rule: WHY, not WHAT

```python
# Bad — describes what code does (already obvious)
# Increment counter by 1
counter += 1

# Good — describes why
# Skip the first item because it contains legacy data
counter += 1
```

Code shows WHAT. Comments show WHY. If a comment describes WHAT, it's a sign
the code could be clearer instead.

### 6.2 When to write a comment

| Situation | Comment? |
|-----------|----------|
| Code does something non-obvious | YES — explain why |
| Choosing between two approaches | YES — note the trade-off |
| Referencing a spec / bug / issue | YES — `// See Spec §3.2` |
| Code does exactly what it says | NO — let code speak |
| "TODO" with no follow-up | NO — file a task, then comment |
| Repeating the function name | NO — redundant |

### 6.3 Docstrings

Use docstrings for **public API** only. Internal helpers don't need them if
the name + signature + 2-line body is self-explanatory.

```python
def calculate_user_score(user_id: str, weights: dict[str, float]) -> float:
    """Calculate a personalized score for the given user.

    Combines base score from the global model with the user's behavior
    weights (clicks, dwell time, conversions). Output is in [0.0, 1.0].

    Args:
        user_id: Stable UUID; same user_id always produces same score
            (deterministic).
        weights: Per-feature weights in [0.0, 1.0]. Negative weights
            are clamped to 0.0.

    Returns:
        Score in [0.0, 1.0]. Returns 0.5 (neutral) if user has no
        behavior history.

    Raises:
        UserNotFoundError: If user_id doesn't exist.
        InvalidWeightsError: If weights dict has unknown keys.
    """
```

### 6.4 Outdated comments are worse than no comments

A wrong comment actively misleads. Update or delete on every change. If
you change code and the comment becomes stale, the comment must change too.
Reviewers should reject commits where comments contradict code.

---

## 7. Function and Module Design

### 7.1 Function size

| Lines | Verdict |
|-------|---------|
| 1-10 | Ideal |
| 10-30 | OK if doing one thing |
| 30-50 | Refactor candidate |
| 50+ | Almost certainly doing too many things |

A function doing one thing rarely exceeds 30 lines. If yours does, ask
"what is this actually doing?" — usually it's 2-3 functions in a trench
coat.

### 7.2 Arguments

| Count | Verdict |
|-------|---------|
| 0-3 | Ideal |
| 4 | OK if necessary |
| 5+ | Use a config object / dataclass |

```python
# Bad — too many positional args
def create_user(name, email, age, country, language, role):
    ...

# Good — config object
@dataclass
class UserSpec:
    name: str
    email: str
    age: int
    country: str
    language: str
    role: Role

def create_user(spec: UserSpec):
    ...
```

### 7.3 Avoid flag arguments

```python
# Bad — boolean arg = two functions in one
def render(text: str, as_html: bool): ...

# Good — separate functions
def render_text(text: str): ...
def render_html(html: str): ...
```

Boolean arguments usually signal that the function is doing two different
things based on the flag. Split them.

### 7.4 Module size

A module should fit on one screen (≈ 300-500 lines). Beyond that:
- Multiple concerns → split into modules
- Sub-domains → package with sub-modules

### 7.5 Imports

```python
# Standard library
import os
from pathlib import Path

# Third-party
import requests
from pydantic import BaseModel

# Local
from myproject.models import User
from myproject.utils import normalize
```

Three groups, blank line between. Sorted alphabetically within each group
(use `isort` or `ruff` to enforce).

### 7.6 Public API surface

Mark the public API explicitly. Two patterns:

**Python (convention):**
```python
# module.py

# Public
def parse_input(...): ...
def validate(...): ...

# Private (underscore prefix)
def _normalize(...): ...
def _internal_helper(...): ...
```

**TypeScript (explicit):**
```typescript
// index.ts — barrel file lists public API
export { parseInput } from './parser';
export { validate } from './validator';
// Internal modules are NOT re-exported
```

Document public API in module docstring. Don't document private functions
unless their logic is genuinely subtle.

---

## 8. Tests (Style, Not Coverage)

Stage 4 (Test Plan) defines **what** to test and coverage thresholds. Stage
10 defines **how** to write the tests.

### 8.1 Test structure: AAA

```python
def test_user_score_normalizes_correctly():
    # Arrange
    user = User(id="u1", behavior={"clicks": 100})
    weights = {"clicks": 0.5, "dwell": 0.5}
    
    # Act
    score = calculate_user_score(user.id, weights)
    
    # Assert
    assert score == 0.5
```

Three blocks, separated by blank lines. Don't skip Arrange — even if it's
one line.

### 8.2 One assertion per test (when possible)

```python
# OK — one assertion, clear intent
def test_user_score_returns_zero_for_empty_behavior():
    user = User(id="u1", behavior={})
    assert calculate_user_score(user.id, ...) == 0.5

# Avoid — multiple assertions, unclear which failed
def test_user_score():
    user = User(...)
    score = calculate_user_score(user.id, ...)
    assert score > 0
    assert score <= 1.0
    assert score != 0.5
```

Multiple assertions are OK when they verify **properties of the same value**
(e.g., `0 <= score <= 1`). But avoid "test 5 different things in one
function."

### 8.3 Test naming

`test_<unit>_<scenario>_<expected_outcome>`

```python
# Good
def test_parse_config_with_missing_field_raises_validation_error():
    ...

def test_calculate_score_with_negative_weights_clamps_to_zero():
    ...

# Bad
def test_parser():                          # what does it test?
    ...
def test_1():                              # meaningless
    ...
```

### 8.4 No test logic

```python
# Bad — if/else inside test
def test_score():
    if config.environment == "prod":
        assert score > 0.9
    else:
        assert score > 0.5

# Good — separate tests for separate conditions
def test_score_in_production_meets_threshold():
    ...

def test_score_in_development_meets_lower_threshold():
    ...
```

If a test contains branching logic, the test is verifying multiple things
and needs to be split.

### 8.5 Test fixtures

Use fixtures for shared setup. Don't reach for global state.

```python
@pytest.fixture
def fresh_user():
    return User(id="u1", name="Alice", created_at=now())

def test_user_age_increments_with_time(fresh_user):
    fresh_user.birthday()
    assert fresh_user.age == 1
```

### 8.6 Mocking

Mock at the boundary (HTTP / DB / time). Don't mock the unit under test.

```python
# Good — mock external dependency
def test_send_email_calls_provider(mocker):
    mock_provider = mocker.patch("myapp.email.provider.send")
    send_welcome_email(user_id="u1")
    mock_provider.assert_called_once()

# Bad — mock internal logic
def test_calculate_score(mocker):
    mocker.patch("myapp.scoring._normalize")  # tests nothing real
    calculate_user_score(...)
```

---

## 9. Dependencies and Tooling

### 9.1 Tooling (defaults)

| Tool | Purpose | When required |
|------|---------|---------------|
| **ruff** (or flake8 + isort + black) | Linting + formatting | Every Python project |
| **mypy** (or pyright) | Type checking | Libraries, large codebases |
| **eslint + prettier** | Linting + formatting | Every TS/JS project |
| **pre-commit** | Run tools before commit | Recommended for all |
| **pytest** | Test runner (Python) | Default |
| **vitest** / **jest** | Test runner (TS/JS) | Default |

Configure via `pyproject.toml` / `package.json` / `.pre-commit-config.yaml`.
Commit the config; don't rely on defaults that drift between machines.

### 9.2 Dependency management

**Three rules:**

1. **Pin versions in production** (`requirements.txt`, `package-lock.json`,
   `Cargo.lock`, `go.sum`). No `^` / `~` in deployable artifacts.
2. **Update dependencies deliberately**, not "by running `pip install --upgrade`".
   Test before committing the bump.
3. **Audit dependencies before adding**. New dep = new attack surface + new
   supply chain risk + new license obligations.

```toml
# pyproject.toml — pin for production
[project]
dependencies = [
    "requests==2.31.0",       # pinned, exact
    "pydantic==2.5.0",         # pinned, exact
]

[project.optional-dependencies]
dev = [
    "pytest==7.4.0",
    "ruff==0.1.0",
]
```

```toml
# pyproject.toml — looser for libraries (callers pin)
[project]
dependencies = [
    "requests>=2.28,<3",       # range, callers pin exact
]
```

### 9.3 Pre-commit hooks

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.1.0
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format
```

Pre-commit enforces formatting/linting before each commit. Skips are allowed
but rare. Don't disable pre-commit because "this one file is special" —
fix the file.

---

## 10. Language Notes (Idioms)

### 10.1 Python idioms

```python
# Use dataclasses / Pydantic, not naked dicts
@dataclass
class UserScore:
    user_id: str
    score: float
    computed_at: datetime

# Context managers for resources
with open(path) as f:
    data = f.read()

# Generators for large sequences
def read_large_file(path: Path) -> Iterator[str]:
    with open(path) as f:
        for line in f:
            yield line.strip()

# Use | for type union (3.10+) or Optional for older
def find_user(uid: str) -> User | None: ...

# f-strings, not .format() or %
name = f"User {user.name} ({user.id})"

# Comprehensions, but readable ones
active_users = [u for u in users if u.is_active]  # OK
matrix = [[x*y for y in range(3)] for x in range(3)]  # OK

# Generator expression for big data
total = sum(item.price for item in items)  # NOT sum([item.price for item in items])
```

**Don't:**
- Use `type()` for runtime checks — use `isinstance()`
- Catch `Exception` broadly — catch specific types
- Mutate function arguments (pure functions are easier to reason about)
- Use `__slots__` "for performance" without measuring first

### 10.2 TypeScript idioms

```typescript
// Prefer `unknown` over `any` — force type checking
function parseConfig(input: unknown): Config {
    if (!isConfig(input)) throw new Error("Invalid config");
    return input;
}

// Type guards
function isConfig(x: unknown): x is Config {
    return typeof x === "object" && x !== null && "version" in x;
}

// Use discriminated unions for state
type RequestState =
    | { status: "idle" }
    | { status: "loading" }
    | { status: "success"; data: T }
    | { status: "error"; error: Error };

// const by default; let only when reassignment is needed
const MAX_RETRIES = 3;
let attempts = 0;
```

**Don't:**
- Use `any` to silence the compiler
- Use `==` — always `===`
- Mix named and positional args confusingly
- Promise-chain when async/await is clearer

### 10.3 SQL idioms

```sql
-- Explicit columns, not SELECT *
SELECT user_id, name, created_at FROM users WHERE active = true;

-- Parameterized queries (NEVER string interpolation)
SELECT * FROM users WHERE id = $1;        -- PostgreSQL
SELECT * FROM users WHERE id = ?;          -- SQLite

-- Index for the WHERE / ORDER BY
CREATE INDEX idx_users_active ON users(active);

-- Use transactions for multi-statement writes
BEGIN;
    INSERT INTO users (id, name) VALUES ('u1', 'Alice');
    INSERT INTO user_settings (user_id, key) VALUES ('u1', 'theme');
COMMIT;
```

---

## 11. Architecture Discipline (No Magic in User Data Path)

This rule is also enforced by the architecture principle recorded in the
system's persistent memory (cross-cutting). It is restated here because
coding practice is the level at which it manifests.

### 11.1 The rule

Engine code (the scoring engine, routing engine, recommendation engine, etc.)
must NEVER contain hardcoded:

- User-specific values (`user_id`, `user_profile`, `user_tier`)
- Environment-specific values (paths, URLs, secrets, thresholds)
- "Tuning" constants that should be config-driven

### 11.2 The test

> "If a different user / environment walked in tomorrow, would this code
> need to change?" If yes, the value is data, not code. Move it to
> `data/user_profiles/{user_id}.json` or `.env`.

### 11.3 Where values belong

| Type | Belongs in | Example |
|------|-----------|---------|
| Algorithm weights | Engine code (with config override) | `WEIGHTS = {"clicks": 0.5}` |
| User-specific data | `data/user_profiles/{user_id}.json` | `{"tier": "premium", "theme": "dark"}` |
| Environment paths / URLs | `.env` + config loader | `DATABASE_URL=postgres://...` |
| Secrets | `.env` + secrets manager | `API_KEY=...` |
| Thresholds per environment | `config/{env}.yaml` | `staging: rate_limit=10`, `prod: rate_limit=100` |

### 11.4 Common violations

```python
# Bad — hardcoded user_id
def calculate_score(user_id="u123"):  # never default to a real user
    ...

# Bad — environment-specific path
config_path = "/etc/myapp/prod.toml"   # hardcoded production path

# Bad — magic threshold
if clicks > 47:                         # where does 47 come from?
    promote_user()

# Good — all three are config-driven
def calculate_score(user_id: str): ...
config_path = Path(os.environ["MYAPP_CONFIG"])
PROMOTION_THRESHOLD = int(os.environ["PROMOTION_THRESHOLD"])
```

---

## 12. Open Questions (Decision Deadlines)

| # | Question | Deadline | Owner |
|---|----------|----------|-------|
| Q1 | Should the project enforce type hints on internal helpers via mypy `--strict`, or only on public API? Current default: public API only. | After 3rd mypy run | Ezio |
| Q2 | For Python, is `dict[str, Any]` ever acceptable, or always require a TypedDict? | After 2nd occurrence | Ezio |
| Q3 | When a Stage 6 implementation generates boilerplate (e.g., Pydantic models from schema), should that count as "code" or "config" for review purposes? Current rule: code, requires review. | After 2nd occurrence | Ezio |

---

## 13. References

- [`../06-implementation/_index_en.md`](../06-implementation/_index_en.md) — Stage 6 owns **how** to execute a task; this section owns **how** to write the code
- [`../04-test-plan/_index_en.md`](../04-test-plan/_index_en.md) — Test Plan defines what tests to write; §8 above defines how
- [`../05-multi-agent-coordination/_index_en.md`](../05-multi-agent-coordination/_index_en.md) — Multi-agent rules apply; agents should follow these styles consistently
- [`../11-governance/_index_en.md`](../11-governance/_index_en.md) — Cross-cutting rules (commit authority, profiles) live there
- [`../90-pitfalls/_index_en.md`](../90-pitfalls/_index_en.md) — Coding pitfalls indexed
- [`~/.hermes/profiles/ezio-zero/skills/software-development/coding-workflow/`](../90-pitfalls/_index_en.md) — Existing `coding-workflow` skill (will be updated to reference this section)
- System architecture principle (persistent memory, `SOUL.md` §Architecture Principles) — "No hardcoded user data in engine code"