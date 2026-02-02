# Learning Instinct - 独特内容分析

本文档列出 `learning-instinct/SKILL.md` 中其他 SKILL 文件没有提及的特别内容。

## 1. 架构对比 (What's New in v2)

**仅在 learning-instinct 中出现**

| 特性 | v1 | v2 |
|------|----|----|
| Observation | Stop hook (session end) | PreToolUse/PostToolUse (100% reliable) |
| Analysis | Main context | Background agent (Haiku) |
| Granularity | Full skills | Atomic "instincts" |
| Confidence | None | 0.3-0.9 weighted |
| Evolution | Direct to skill | Instincts → cluster → skill/command/agent |
| Sharing | None | Export/import instincts |

**其他 SKILL 的覆盖范围：**
- `init`: 只涉及初始化
- `session-memory`: 只涉及会话加载
- `apply`: 只涉及应用
- `status`: 只涉及查看
- `evolve`: 只涉及演化
- `import/export`: 只涉及导入导出

**缺失：** 没有任何 SKILL 详细说明 v1 到 v2 的演进历史和架构变化。

---

## 2. 系统工作流程图 (How It Works)

**仅在 learning-instinct 中出现**

完整的数据流图：
```
Session Activity
      │
      │ Hooks capture prompts + tool use (100% reliable)
      ▼
observations.jsonl
      │
      │ Observer agent reads (background, Haiku)
      ▼
PATTERN DETECTION
      │
      │ Creates/updates
      ▼
instincts/personal/
      │
      │ /evolve clusters
      ▼
evolved/
```

**其他 SKILL 的覆盖范围：**
- `init`: 只说明初始化步骤
- `session-memory`: 只说明加载上下文
- `apply`: 只说明应用方式
- `status`: 只说明查看方式
- `evolve`: 只说明演化规则

**缺失：** 没有任何 SKILL 展示完整的端到端工作流程。

---

## 3. Hooks 配置详解 (Quick Start - Enable Observation Hooks)

**仅在 learning-instinct 中出现**

详细的 `~/.claude/settings.json` 配置示例：

### 作为插件安装
```json
{
  "hooks": {
    "PreToolUse": [...],
    "PostToolUse": [...]
  }
}
```

### 手动安装到 `~/.claude/skills`
```json
{
  "hooks": {
    "PreToolUse": [...],
    "PostToolUse": [...]
  }
}
```

**其他 SKILL 的覆盖范围：**
- 没有任何 SKILL 涉及 hooks 的配置
- `session-memory` 只说"hooks 自动捕获"
- `apply` 只说"观察自动进行"

**缺失：** 没有任何 SKILL 告诉用户如何实际配置 hooks。

---

## 4. Hooks vs Skills 的对比 (Why Hooks vs Skills for Observation?)

**仅在 learning-instinct 中出现**

```
v1 relied on skills to observe. Skills are probabilistic—they fire ~50-80% of the time based on Claude's judgment.

Hooks fire 100% of the time, deterministically. This means:
- Every tool call is observed
- No patterns are missed
- Learning is comprehensive
```

**其他 SKILL 的覆盖范围：**
- 没有任何 SKILL 解释为什么选择 hooks 而不是 skills
- `session-memory` 只说"hooks 捕获观察"

**缺失：** 没有任何 SKILL 说明这个关键的架构决策理由。

---

## 5. 向后兼容性 (Backward Compatibility)

**仅在 learning-instinct 中出现**

```
v2 is fully compatible with v1:
- Existing ~/.claude/skills/learned/ skills still work
- Stop hook still runs (but now also feeds into v2)
- Gradual migration path: run both in parallel
```

**其他 SKILL 的覆盖范围：**
- 没有任何 SKILL 提及向后兼容性
- 没有任何 SKILL 说明如何与 v1 共存

**缺失：** 没有迁移指南或兼容性说明。

---

## 6. 隐私政策 (Privacy)

**仅在 learning-instinct 中出现**

```
- Observations stay local on your machine
- Only instincts (patterns) can be exported
- No actual code or conversation content is shared
- You control what gets exported
```

**其他 SKILL 的覆盖范围：**
- `export`: 有隐私考虑（什么包含/不包含）
- 其他 SKILL 都没有提及隐私

**缺失：** 没有其他 SKILL 强调本地存储和隐私保护。

---

## 7. 完整的 Instinct 模型示例

**仅在 learning-instinct 中出现**

```yaml
---
id: prefer-functional-style
trigger: "when writing new functions"
confidence: 0.7
domain: "code-style"
source: "session-observation"
---

# Prefer Functional Style

## Action
Use functional patterns over classes when appropriate.

## Evidence
- Observed 5 instances of functional pattern preference
- User corrected class-based approach to functional on 2025-01-15
```

**其他 SKILL 的覆盖范围：**
- `apply`: 有简化的 instinct 结构示例
- `status`: 有输出格式示例
- `export`: 有导出格式示例

**缺失：** 没有其他 SKILL 展示完整的 instinct 元数据结构（包括 `id`, `source` 等）。

---

## 8. 目录初始化说明 (Initialize Directory Structure)

**仅在 learning-instinct 中出现**

```bash
mkdir -p ~/.claude/homunculus/{instincts/{personal,inherited},evolved/{agents,skills,commands}}
touch ~/.claude/homunculus/observations.jsonl
```

**其他 SKILL 的覆盖范围：**
- `init`: 有详细的目录创建脚本
- `learning-instinct`: 有简化的一行命令

**缺失：** 没有其他 SKILL 提供快速初始化命令。

---

## 9. 命令快速参考 (Use the Instinct Commands)

**仅在 learning-instinct 中出现**

```bash
/status              # Show learned instincts with confidence scores
/evolve              # Cluster related instincts into skills/commands
/export              # Export instincts for sharing
/import              # Import instincts from others
```

**其他 SKILL 的覆盖范围：**
- 每个 SKILL 只记录自己的命令
- 没有统一的命令快速参考

**缺失：** 没有其他 SKILL 提供完整的命令列表。

---

## 10. 版本号和元数据

**仅在 learning-instinct 中出现**

```yaml
---
name: learning-instinct
description: Instinct-based learning system...
version: 2.0.0
---
```

**其他 SKILL 的覆盖范围：**
- 没有其他 SKILL 声明版本号

**缺失：** 没有版本管理信息。

---

## 总结

### Learning Instinct 的核心独特内容：

1. **架构文档** - v1 vs v2 对比、系统工作流程
2. **配置指南** - Hooks 的详细配置方式
3. **设计决策** - 为什么选择 hooks、为什么是 instincts
4. **兼容性说明** - 与 v1 的共存方式
5. **隐私保证** - 数据本地化和隐私政策
6. **完整示例** - Instinct 的完整元数据结构
7. **快速参考** - 所有命令的统一列表
8. **版本信息** - 系统版本号

### 其他 SKILL 的角色：

- **init**: 初始化系统
- **session-memory**: 加载会话上下文
- **apply**: 应用已学习的行为
- **status**: 查看已学习的 instincts
- **evolve**: 将 instincts 演化为更高级结构
- **import/export**: 导入导出 instincts

### 建议：

`learning-instinct` 是整个系统的**架构和概念文档**，而其他 SKILL 是**操作指南**。它们各有其用途，不应该重复。
