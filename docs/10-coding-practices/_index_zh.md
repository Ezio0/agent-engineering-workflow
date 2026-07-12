# 10 — Coding Practices（编码实践，横向）

> **状态**：活跃
> **最后审阅**：2026-07-12
> **关联**：[English version](_index_en.md)
>
> 本文档的英文版：_index_en.md
>
> 横向主题。适用于**任何项目中写的所有代码**——Stage 6（实施）消费本节。
> Stage 6 **不**重复这些规则；它引用本节。

---

## 1. 概述

Coding Practices 是**手艺层**。Stage 6 是流程（"我怎么执行 task"），Stage 10
是风格（"代码本身怎么写"）。

**与 Stage 6 的严格边界：**

| 关注点 | Stage |
|--------|-------|
| 如何加载上下文、选 task、跑 5 步循环 | Stage 6 |
| **如何写函数、命名变量、处理错误、打日志** | **Stage 10** |
| 如何 commit | Stage 8 |
| 如何验证报告 | Stage 7 |

本节**默认与语言无关**；特定语言指导在 §10（语言笔记），含 Python / TypeScript
等具体惯用法。原则普适；只有语法不同。

### 三条支撑原则

这三条贯穿整个 section。记住它们。

1. **可读性 > 巧妙**。代码被读的概率比被写的多 100 倍。为读者优化，不是作者。
2. **显式 > 隐式**。类型提示、命名参数、错误码。隐式行为是调试时的定时炸弹。
3. **用户数据路径无魔法**。引擎代码绝不携带硬编码的用户值、环境值、或应该是
   config 的"调优"常量。这也由 SOUL.md 中的架构原则强制；交叉引用见 §11。

---

## 2. 命名

### 2.1 按语言的命名风格

| 语言 | 变量 / 函数 | 类 | 常量 | 模块 / 文件 |
|------|------------|-----|------|------------|
| Python | `snake_case` | `PascalCase` | `UPPER_SNAKE_CASE` | `snake_case.py` |
| TypeScript / JS | `camelCase` | `PascalCase` | `UPPER_SNAKE_CASE` | `kebab-case.ts` |
| Go | `camelCase`（未导出）/ `PascalCase`（导出） | `PascalCase` | `PascalCase`（无 const 约定） | `snake_case.go` |
| Rust | `snake_case` | `PascalCase` | `UPPER_SNAKE_CASE` | `snake_case.rs` |

**同一语言内不混用**。选一个。不要在 Python 写 `My_Variable`，在 JS 写
`myFunction`。

### 2.2 命名目标

| 目标 | 手段 | 例子 |
|------|------|------|
| **清晰** | 全词，不用缩写 | `user_count`，不是 `usr_cnt` |
| **可搜** | 独特名字，不通用 | `parse_config_file`，不是 `process` |
| **可发音** | 容易在对话中说 | `parser`，不是 `psr` |
| **无编码** | 名字里无类型信息 | `users`，不是 `user_list` / `userArr` |

### 2.3 `_` 前缀约定

`_` 前缀意为**模块 / 类私有**——"不要从外部 import"。

```python
# 好
def public_api():
    return _helper()

def _helper():           # 下划线前缀 = 私有
    ...
```

```python
# 坏 — 意外导出
def helper():           # 看起来 public，但不该是
    ...

# 调用者现在依赖 helper()，即使本意是私有
from module import helper
```

**但是：** `_` 是**约定**，不是强制。其他语言用 `private` / `internal` 关键字。
Python 依赖约定。信任约定；如果意外从外部调用了私有函数，重命名。

### 2.4 要避免的命名

| 反模式 | 为什么 |
|--------|--------|
| `data`、`info`、`stuff`、`temp`、`val`、`obj` | 告诉读者零信息 |
| `foo`、`bar`、`baz` | 玩具例子，不是生产 |
| 单字母除了循环计数器 | `i`/`j`/`k` OK；`a`/`x` 不 OK |
| 类型编码名（`str_name`、`int_count`） | 类型在 hint 里，不在名字里 |
| 冗余前缀（`class_foo`、`func_bar`） | 类就是 `Foo`，函数就是 `bar` |
| 末尾 `_` 表"我不知道" | 改名 |
| 匹配关键字的名字（`class`、`type`） | 语法错误或遮蔽 |

---

## 3. 类型和签名

### 3.1 类型提示：何时必须，何时可选

| 语言 | 何时必须 | 何时可选 |
|------|---------|---------|
| Python | Public API、库边界、Spec 里的任何东西 | 一次性脚本、临时测试 |
| TypeScript | **永远**（已提交代码无 `any`） | 永不可选 |
| Rust | **永远**（编译器强制） | 永不可选 |

### 3.2 类型提示——标注什么

```python
# 标注 public 函数签名
def calculate_score(user_id: str, weights: dict[str, float]) -> float:
    ...

# 内部 helper —— 共享时标注，明显时跳过
def _normalize(x: float) -> float:        # 名字 + body 已明显
    return x / 100.0

# 变量 —— RHS 类型不明显时标注
config_path: Path = Path("/etc/app.toml")  # Path 从 string 来 — 标注
items = []                                  # 明显 — 跳过
```

### 3.3 不要过度类型化

```python
# 过度 —— 类型明显
count: int = 0
name: str = "alice"

# 有用 —— 值看不出类型
scores: dict[str, list[float]] = {}
results: list[UserResult] = parse_results(scores)

# 错 —— 类型在撒谎
def get_user(id: int) -> User:           # 返回 User，不是 None
    return self._cache.get(id) or User.default()
    # ^ 应该是 -> User | None，或显式处理 default
```

### 3.4 `Optional[T]` vs `T | None`

Python 3.10+ 偏好 `T | None`。3.9 及更早用 `Optional[T]`。一个 codebase
选一个；同一文件不混用。

### 3.5 避免 `Any`

`Any` 让类型检查失效。仅在以下情况用：
- 跟无类型库对接
- 动态数据（如 JSON parsing）验证前

不要用 `Any` 来不弄清楚就消音类型错误。

---

## 4. 错误处理

### 4.1 四个层级

| 层级 | 何时用 | 例子 |
|------|--------|------|
| **验证错误** | 调用者传了无效输入 | `ValueError`、`TypeError` |
| **领域错误** | 违反业务规则 | `UserNotFoundError`、`InsufficientFundsError` |
| **基础设施错误** | 外部系统失败 | `DatabaseConnectionError`、`TimeoutError` |
| **内部错误** | 程序员错误，从不预期 | `AssertionError`、`RuntimeError` |

选对层级。"user not found" **不**是基础设施错误；"database timeout" **不**
是验证错误。混用让错误处理策略失效。

### 4.2 自定义异常 vs 内置

```python
# 自定义领域异常
class UserNotFoundError(LookupError):
    """Raised when a user_id lookup fails."""
    
    def __init__(self, user_id: str):
        self.user_id = user_id
        super().__init__(f"User not found: {user_id}")

# 调用者
try:
    user = get_user(uid)
except UserNotFoundError as e:
    logger.warning(f"User lookup failed: {e.user_id}")
    return None
```

**为什么自定义？** 内置（`KeyError`、`ValueError`）太通用。自定义异常让调用者
精确处理。**但是：**只为领域规则创建自定义异常，不要为每个函数。

### 4.3 永不吞异常

```python
# 永不
try:
    do_something()
except Exception:
    pass

# OK 如果有意 + 记日志
try:
    do_optional_thing()
except SomeSpecificError as e:
    logger.debug(f"Optional thing skipped: {e}")

# 更好：意外时失败响亮
try:
    do_something()
except ExpectedError as e:
    handle(e)
except Exception as e:
    logger.exception("Unexpected error in do_something")
    raise
```

如果 catch，做以下之一：(a) 有意义地处理，(b) 记日志 + re-raise，(c) 记日志 +
返回定义的 fallback。裸 `except: pass` 是 bug。

### 4.4 错误消息

**好错误消息：**
- 说明什么失败（`"User not found: {user_id}"`）
- 包含导致它的值（`"Invalid input: got {value}, expected ..."`）
- 如果明显，建议修复（`"Check the user_id; it must be a UUID"`）

**坏错误消息：**
- `"Error"`（无信息）
- `"Something went wrong"`（陈词）
- `"Invalid"`（没说清什么 invalid）

### 4.5 何时 raise vs return error

| 模式 | 何时用 |
|------|--------|
| **Raise 异常** | 异常条件；happy path 不含错误 |
| **Return Result 类型**（`(T, Error)` 元组或 `Result[T, E]`） | 预期的替代结果；调用者应处理每个 case |

正确用法不该发生的事用 raise；调用者必须处理的多种结果之一用 return。

---

## 5. 日志

### 5.1 级别

| 级别 | 何时 | 例子 |
|------|------|------|
| `DEBUG` | 诊断细节；生产关 | `"Cache hit for key=X"` |
| `INFO` | 正常流的显著事件 | `"User logged in: {user_id}"` |
| `WARNING` | 可恢复问题 | `"Rate limit hit, backing off 30s"` |
| `ERROR` | 操作失败，但服务继续 | `"Failed to send email to {user_id}"` |
| `CRITICAL` | 服务无法继续 | `"Database unreachable, shutting down"` |

### 5.2 记什么

| 记 | 为什么 |
|----|--------|
| 外部 API 调用（请求 + 响应码，**不**含 body） | 审计 + 调试 |
| 状态转换（登录、开始、完成） | 审计 |
| 失败（带完整上下文） | 调试 |
| 慢操作（带耗时） | 性能调试 |

| **不**记 | 为什么 |
|---------|--------|
| PII（密码、token、完整邮箱） | 安全 / 合规 |
| 敏感端点的请求/响应 **body** | 安全 |
| 热路径 debug 日志（每次循环迭代） | 性能 |
| 每个函数顶部 `"Starting function X"` | 噪音 |

### 5.3 日志 API

```python
# 好 —— 结构化、有上下文
logger.info("user.login", extra={"user_id": uid, "ip": ip})
logger.warning("rate_limit.hit", extra={"user_id": uid, "retry_after": 30})

# 避免 —— 无格式化字符串、无上下文
logger.info("user logged in")
logger.warning(f"rate limit hit")        # extra={} 优于 f-string
```

### 5.4 `print` 不是日志

`print` 去 stdout，无级别、无时间戳、无上下文。**仅**用于给用户的 CLI 输出。
库代码的诊断日志永远不要用。

```python
# CLI 工具 —— print 正确
def main():
    print(f"Processing {len(files)} files...")
    ...

# 库代码 —— print 错
def process_files(files):
    print(f"Processing {len(files)} files...")  # BAD
    logger.info("process_files.start", extra={"count": len(files)})
    ...
```

---

## 6. 注释和 Docstring

### 6.1 核心规则：WHY，不是 WHAT

```python
# 坏 —— 描述代码做了什么（已明显）
# Increment counter by 1
counter += 1

# 好 —— 描述为什么
# Skip the first item because it contains legacy data
counter += 1
```

代码展示 WHAT。注释展示 WHY。如果注释描述 WHAT，说明代码本身可以更清晰。

### 6.2 何时写注释

| 情况 | 注释？ |
|------|--------|
| 代码做了不明显的事 | 是 —— 解释为什么 |
| 在两个方法间选择 | 是 —— 注明 trade-off |
| 引用 spec / bug / issue | 是 —— `// 见 Spec §3.2` |
| 代码做了什么就说什么 | 否 —— 让代码自己说 |
| "TODO" 无 follow-up | 否 —— 建 task，再写注释 |
| 重复函数名 | 否 —— 冗余 |

### 6.3 Docstring

**仅**对 **public API** 用 docstring。内部 helper 如果名字 + 签名 + 2 行 body
已自解释，不需 docstring。

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

### 6.4 过时注释比没注释更糟

错的注释主动误导。每次改动更新或删除。如果改了代码注释变 stale，注释必须改。
Reviewer 应拒绝注释与代码矛盾的 commit。

---

## 7. 函数和模块设计

### 7.1 函数大小

| 行数 | 评判 |
|------|------|
| 1-10 | 理想 |
| 10-30 | OK 如果只做一件事 |
| 30-50 | 重构候选 |
| 50+ | 几乎肯定做太多事 |

做一件事的函数很少超过 30 行。如果超了，问"这实际在做什么？"——通常这是
2-3 个函数穿了件外套。

### 7.2 参数

| 个数 | 评判 |
|------|------|
| 0-3 | 理想 |
| 4 | OK 如果必要 |
| 5+ | 用 config 对象 / dataclass |

```python
# 坏 —— 太多位置参数
def create_user(name, email, age, country, language, role):
    ...

# 好 —— config 对象
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

### 7.3 避免 flag 参数

```python
# 坏 —— 布尔参数 = 一个函数做两件事
def render(text: str, as_html: bool): ...

# 好 —— 拆成两个
def render_text(text: str): ...
def render_html(html: str): ...
```

布尔参数通常意味着函数根据 flag 做不同的事。拆开。

### 7.4 模块大小

模块应一屏装下（≈ 300-500 行）。超过：
- 多个关注点 → 拆成模块
- 子领域 → package 含子模块

### 7.5 Imports

```python
# 标准库
import os
from pathlib import Path

# 第三方
import requests
from pydantic import BaseModel

# 本地
from myproject.models import User
from myproject.utils import normalize
```

三组，组间空行。每组按字母序（用 `isort` 或 `ruff` 强制）。

### 7.6 Public API 表面

明确标记 public API。两种模式：

**Python（约定）：**
```python
# module.py

# Public
def parse_input(...): ...
def validate(...): ...

# Private（下划线前缀）
def _normalize(...): ...
def _internal_helper(...): ...
```

**TypeScript（显式）：**
```typescript
// index.ts — barrel 文件列出 public API
export { parseInput } from './parser';
export { validate } from './validator';
// 内部模块**不**重导出
```

public API 在模块 docstring 里记录。除非逻辑真的微妙，否则不记录私有函数。

---

## 8. 测试（风格，非覆盖）

Stage 4（Test Plan）定义**测什么**和覆盖率阈值。Stage 10 定义**怎么写**测试。

### 8.1 测试结构：AAA

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

三块，块间空行。不要跳过 Arrange —— 即使只有一行。

### 8.2 一个测试一个断言（能的话）

```python
# OK —— 一个断言，意图清晰
def test_user_score_returns_zero_for_empty_behavior():
    user = User(id="u1", behavior={})
    assert calculate_user_score(user.id, ...) == 0.5

# 避免 —— 多断言，不知哪个失败
def test_user_score():
    user = User(...)
    score = calculate_user_score(user.id, ...)
    assert score > 0
    assert score <= 1.0
    assert score != 0.5
```

多断言在验证**同一值的属性**时 OK（如 `0 <= score <= 1`）。但避免"一个
函数测 5 件事"。

### 8.3 测试命名

`test_<unit>_<scenario>_<expected_outcome>`

```python
# 好
def test_parse_config_with_missing_field_raises_validation_error():
    ...

def test_calculate_score_with_negative_weights_clamps_to_zero():
    ...

# 坏
def test_parser():                          # 测什么？
    ...
def test_1():                              # 无意义
    ...
```

### 8.4 测试无逻辑

```python
# 坏 —— 测试里有 if/else
def test_score():
    if config.environment == "prod":
        assert score > 0.9
    else:
        assert score > 0.5

# 好 —— 不同条件拆测试
def test_score_in_production_meets_threshold():
    ...

def test_score_in_development_meets_lower_threshold():
    ...
```

如果测试含分支逻辑，测试在验证多件事，需拆分。

### 8.5 测试 fixture

用 fixture 做共享 setup。不要伸手用全局状态。

```python
@pytest.fixture
def fresh_user():
    return User(id="u1", name="Alice", created_at=now())

def test_user_age_increments_with_time(fresh_user):
    fresh_user.birthday()
    assert fresh_user.age == 1
```

### 8.6 Mock

在边界 mock（HTTP / DB / time）。不要 mock 被测单元。

```python
# 好 —— mock 外部依赖
def test_send_email_calls_provider(mocker):
    mock_provider = mocker.patch("myapp.email.provider.send")
    send_welcome_email(user_id="u1")
    mock_provider.assert_called_once()

# 坏 —— mock 内部逻辑
def test_calculate_score(mocker):
    mocker.patch("myapp.scoring._normalize")  # 没测真实逻辑
    calculate_user_score(...)
```

---

## 9. 依赖和工具

### 9.1 工具（默认）

| 工具 | 用途 | 何时必须 |
|------|------|---------|
| **ruff**（或 flake8 + isort + black） | Linting + formatting | 每个 Python 项目 |
| **mypy**（或 pyright） | 类型检查 | 库、大 codebase |
| **eslint + prettier** | Linting + formatting | 每个 TS/JS 项目 |
| **pre-commit** | commit 前跑工具 | 全部推荐 |
| **pytest** | Test runner（Python） | 默认 |
| **vitest** / **jest** | Test runner（TS/JS） | 默认 |

通过 `pyproject.toml` / `package.json` / `.pre-commit-config.yaml` 配置。
**提交**配置；不要依赖会漂移的默认值。

### 9.2 依赖管理

**三条规则：**

1. **生产固定版本**（`requirements.txt`、`package-lock.json`、`Cargo.lock`、
   `go.sum`）。可部署产物中无 `^` / `~`。
2. **刻意**更新依赖，不是"跑 `pip install --upgrade`"。提交 bump 前测。
3. **添加前审查依赖**。新依赖 = 新攻击面 + 新供应链风险 + 新许可证义务。

```toml
# pyproject.toml —— 生产固定
[project]
dependencies = [
    "requests==2.31.0",       # 固定，精确
    "pydantic==2.5.0",         # 固定，精确
]

[project.optional-dependencies]
dev = [
    "pytest==7.4.0",
    "ruff==0.1.0",
]
```

```toml
# pyproject.toml —— 库宽松（调用者固定）
[project]
dependencies = [
    "requests>=2.28,<3",       # 范围，调用者固定精确
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

Pre-commit 在每次 commit 前强制 format/lint。允许跳过但罕见。不要因为"这个
文件特殊"就禁 pre-commit——修文件。

---

## 10. 语言笔记（惯用法）

### 10.1 Python 惯用法

```python
# 用 dataclasses / Pydantic，不要裸 dict
@dataclass
class UserScore:
    user_id: str
    score: float
    computed_at: datetime

# 用 context manager 管资源
with open(path) as f:
    data = f.read()

# 用 generator 处理大序列
def read_large_file(path: Path) -> Iterator[str]:
    with open(path) as f:
        for line in f:
            yield line.strip()

# 用 | 表 type union（3.10+），或 Optional（更早）
def find_user(uid: str) -> User | None: ...

# f-string，不用 .format() 或 %
name = f"User {user.name} ({user.id})"

# 推导式，但可读的
active_users = [u for u in users if u.is_active]  # OK
matrix = [[x*y for y in range(3)] for x in range(3)]  # OK

# 大数据用 generator expression
total = sum(item.price for item in items)  # 不是 sum([item.price for item in items])
```

**不要：**
- 用 `type()` 做运行检查 —— 用 `isinstance()`
- 宽泛 catch `Exception` —— catch 具体类型
- 修改函数参数（纯函数更易推理）
- 不测量就用 `__slots__` "为性能"

### 10.2 TypeScript 惯用法

```typescript
// 偏好 `unknown` 而非 `any` —— 强制类型检查
function parseConfig(input: unknown): Config {
    if (!isConfig(input)) throw new Error("Invalid config");
    return input;
}

// Type guards
function isConfig(x: unknown): x is Config {
    return typeof x === "object" && x !== null && "version" in x;
}

// 用 discriminated unions 表状态
type RequestState =
    | { status: "idle" }
    | { status: "loading" }
    | { status: "success"; data: T }
    | { status: "error"; error: Error };

// 默认 const；只重赋值时用 let
const MAX_RETRIES = 3;
let attempts = 0;
```

**不要：**
- 用 `any` 消音编译器
- 用 `==` —— 永远 `===`
- 命名参数和位置参数混用混乱
- 异步/await 更清晰时用 Promise chain

### 10.3 SQL 惯用法

```sql
-- 显式列名，不是 SELECT *
SELECT user_id, name, created_at FROM users WHERE active = true;

-- 参数化查询（永远不要字符串插值）
SELECT * FROM users WHERE id = $1;        -- PostgreSQL
SELECT * FROM users WHERE id = ?;          -- SQLite

-- 为 WHERE / ORDER BY 加索引
CREATE INDEX idx_users_active ON users(active);

-- 多语句写入用事务
BEGIN;
    INSERT INTO users (id, name) VALUES ('u1', 'Alice');
    INSERT INTO user_settings (user_id, key) VALUES ('u1', 'theme');
COMMIT;
```

---

## 11. 架构纪律（用户数据路径无魔法）

此规则也由系统持久内存中的架构原则强制（横向）。在此重述因为它体现在编码实践
层面。

### 11.1 规则

引擎代码（评分引擎、路由引擎、推荐引擎等）**绝不**含硬编码的：

- 用户特定值（`user_id`、`user_profile`、`user_tier`）
- 环境特定值（路径、URL、密钥、阈值）
- 应该是 config 驱动的"调优"常量

### 11.2 测试

> "如果明天走进一个完全不同的用户 / 环境，这段代码需要改吗？"如果需要，
> 该值是数据，不是代码。移到 `data/user_profiles/{user_id}.json` 或 `.env`。

### 11.3 值属于哪里

| 类型 | 属于 | 例子 |
|------|------|------|
| 算法权重 | 引擎代码（带 config 覆盖） | `WEIGHTS = {"clicks": 0.5}` |
| 用户特定数据 | `data/user_profiles/{user_id}.json` | `{"tier": "premium", "theme": "dark"}` |
| 环境路径 / URL | `.env` + config 加载器 | `DATABASE_URL=postgres://...` |
| 密钥 | `.env` + secrets 管理器 | `API_KEY=***` |
| 每环境阈值 | `config/{env}.yaml` | `staging: rate_limit=10`, `prod: rate_limit=100` |

### 11.4 常见违规

```python
# 坏 —— 硬编码 user_id
def calculate_score(user_id="u123"):  # 绝不默认真实用户
    ...

# 坏 —— 环境特定路径
config_path = "/etc/myapp/prod.toml"   # 硬编码生产路径

# 坏 —— 魔法阈值
if clicks > 47:                         # 47 从哪来？
    promote_user()

# 好 —— 三者都是 config 驱动
def calculate_score(user_id: str): ...
config_path = Path(os.environ["MYAPP_CONFIG"])
PROMOTION_THRESHOLD = int(os.environ["PROMOTION_THRESHOLD"])
```

---

## 12. 开放问题（决策截止）

| # | 问题 | 截止 | 负责人 |
|---|------|------|--------|
| Q1 | 项目应通过 mypy `--strict` 强制内部 helper 的类型提示，还是仅 public API？当前默认：仅 public API。 | 第 3 次 mypy 跑后 | Ezio |
| Q2 | Python 允许 `dict[str, Any]`，还是永远要 TypedDict？ | 第 2 次发生后 | Ezio |
| Q3 | 当 Stage 6 实施生成样板（如 Pydantic 模型从 schema 生成），算"代码"还是"配置"用于评审？当前规则：代码，要 review。 | 第 2 次发生后 | Ezio |

---

## 13. 参考

- [`../06-implementation/_index_zh.md`](../06-implementation/_index_zh.md) — Stage 6 拥有**怎么**执行 task；本节拥有**怎么**写代码
- [`../04-test-plan/_index_zh.md`](../04-test-plan/_index_zh.md) — Test Plan 定义测什么；上面 §8 定义怎么测
- [`../05-multi-agent-coordination/_index_zh.md`](../05-multi-agent-coordination/_index_zh.md) — 多 agent 规则适用；agents 应一致遵循这些风格
- [`../11-governance/_index_zh.md`](../11-governance/_index_zh.md) — 横向规则（commit 权限、profiles）在那里
- [`../90-pitfalls/_index_zh.md`](../90-pitfalls/_index_zh.md) — 编码 pitfalls 索引
- [`~/.hermes/profiles/ezio-zero/skills/software-development/coding-workflow/`](../90-pitfalls/_index_zh.md) — 现有 `coding-workflow` skill（将更新为引用本节）
- 系统架构原则（持久内存，`SOUL.md` §Architecture Principles）—— "引擎代码无硬编码用户数据"