# Everything Claude Code vs Homunculus: 完整对比分析

## 项目概述

| 维度 | Everything Claude Code | Homunculus |
|------|----------------------|-----------|
| **项目名称** | Instinct | Homunculus v2.0-alpha |
| **定位** | 学习系统核心库 | 完整的 Claude Code 插件 |
| **版本** | 基础版本 | v2.0.0（完全重写） |
| **主要目标** | 观察、学习、进化的基础框架 | 一个有生命的、自适应的助手 |

---

## 核心架构差异

### 1. 项目结构组织

#### Everything Claude Code
```
everything-claude-code/
├── agents/              # 观察者代理
│   ├── observer.md
│   └── start-observer.sh
├── commands/            # 5个命令
│   ├── init.md
│   ├── status.md
│   ├── evolve.md
│   ├── export.md
│   ├── import.md
│   └── install-opencode.md  # 额外命令
├── skills/              # 2个技能
│   ├── session-memory/
│   └── instinct-apply/
├── hooks/               # 观察钩子
│   ├── hooks.json
│   ├── observe.sh
│   └── on_stop.sh
├── scripts/             # Python 脚本
│   └── instinct.py
└── docs/                # 规划文档
```

#### Homunculus
```
homunculus/
├── plugins/homunculus/  # 插件核心
│   ├── agents/
│   │   └── observer.md
│   ├── commands/        # 5个命令（无 install-opencode）
│   ├── skills/
│   ├── hooks/
│   └── scripts/         # Shell 脚本（无 Python）
├── landing/             # React 登陆页面
│   ├── src/
│   ├── public/
│   └── package.json
├── scripts/             # 模拟脚本
│   ├── sim-init.sh
│   └── sim-evolve.sh
└── demo files           # 演示录制文件
```

**关键差异：**
- **Homunculus** 包含 **React 登陆页面**（完整的营销和展示层）
- **Homunculus** 包含 **演示录制文件**（demo.tape, evolve.tape 等）
- **Everything Claude Code** 有额外的 `install-opencode` 命令
- **Everything Claude Code** 包含 Python 脚本，**Homunculus** 仅用 Shell

---

## 功能对比

### 命令集合

| 命令 | Everything Claude Code | Homunculus | 差异 |
|------|----------------------|-----------|------|
| `/init` | ✅ 初始化系统 | ✅ 初始化系统 | 相同逻辑 |
| `/status` | ✅ 详细状态报告 | ✅ 简化状态报告 | Homunculus 更简洁 |
| `/evolve` | ✅ 高级聚类分析 | ✅ 基础聚类分析 | Everything 更详细 |
| `/export` | ✅ YAML/JSON 格式 | ✅ tar.gz 格式 | 格式和方式不同 |
| `/import` | ✅ 导入 YAML/JSON | ✅ 导入 tar.gz | 格式和方式不同 |
| `/install-opencode` | ✅ 特殊命令 | ❌ 不存在 | **Everything 独有** |

### 观察机制

#### Everything Claude Code
```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "*",
        "command": "${CLAUDE_PLUGIN_ROOT}/hooks/observe.sh pre",
        "timeout": 3
      }
    ],
    "PostToolUse": [
      {
        "matcher": "*",
        "command": "${CLAUDE_PLUGIN_ROOT}/hooks/observe.sh post",
        "timeout": 3
      }
    ],
    "Stop": [...]
  }
}
```

#### Homunculus
```json
{
  "hooks": {
    "UserPromptSubmit": [
      {
        "command": "${CLAUDE_PLUGIN_ROOT}/scripts/observe.sh prompt"
      }
    ],
    "PostToolUse": [
      {
        "matcher": ".*",
        "command": "${CLAUDE_PLUGIN_ROOT}/scripts/observe.sh tool"
      }
    ],
    "Stop": [...]
  }
}
```

**关键差异：**
- **Everything Claude Code** 使用 `PreToolUse` + `PostToolUse`（工具执行前后）
- **Homunculus** 使用 `UserPromptSubmit` + `PostToolUse`（用户提示 + 工具执行后）
- **Homunculus** 捕获**用户意图**（prompt），**Everything** 捕获**工具执行**细节

---

## 设计哲学差异

### Everything Claude Code 的优势

#### 1. **更详细的技术规范**
- `commands/evolve.md` 有 **241 行**，包含：
  - 详细的聚类算法说明
  - 多个标志选项（`--domain`, `--threshold`, `--type`）
  - 技能创建的 TDD 流程集成
  - 生成文件的完整格式示例
  
- `commands/status.md` 有 **111 行**，包含：
  - 多种过滤和排序选项
  - 详细的输出格式示例
  - 陈旧本能检测逻辑

#### 2. **Python 脚本支持**
- 包含 `scripts/instinct.py`，可以：
  - 处理复杂的聚类算法
  - 支持多种输出格式（YAML, JSON, Markdown）
  - 实现高级过滤和统计

#### 3. **更强大的导出功能**
- 支持多种格式：YAML, JSON, Markdown
- 支持选择性导出（按域、按置信度）
- 包含隐私考虑（剥离敏感信息）
- 导出 **127 行** 的详细说明

#### 4. **更完整的观察者代理**
- `agents/observer.md` 有 **142 行**
- 包含详细的模式检测规则：
  - 用户更正检测
  - 错误解决方案检测
  - 重复工作流检测
  - 工具偏好检测
- 置信度计算公式明确
- 包含完整的分析示例

#### 5. **额外的命令**
- `install-opencode.md` 用于安装特殊工具
- 提供更多的扩展性

---

### Homunculus 的优势

#### 1. **完整的产品化方案**
- **React 登陆页面**（`landing/`）：
  - 提供视觉化的营销展示
  - 用户友好的界面
  - 完整的项目演示能力

#### 2. **更简洁的实现**
- 所有脚本都是 Shell（无 Python 依赖）
- 更轻量级，更容易部署
- 命令更简洁（5 个核心命令）

#### 3. **演示和文档**
- 包含多个 `.tape` 文件（asciinema 录制）：
  - `demo.tape` - 基础演示
  - `evolve.tape` - 进化演示
  - `evolve-v2.tape`, `evolve-v3.tape` - 版本演进
  - `demo-evolve.tape` - 进化演示
- 提供实际的使用演示

#### 4. **更人性化的设计**
- 命令输出更简洁，更有"个性"
- `status.md` 强调"check in"的概念（检查状态）
- `evolve.md` 更简短（59 行），但核心逻辑完整
- 整体设计更像一个"生命体"而不是"工具"

#### 5. **观察者代理的简化**
- `agents/observer.md` 有 **110 行**（更简洁）
- 核心逻辑相同，但实现更直接
- 强调"静默运行"（silent run）

#### 6. **后台处理**
- `session-memory` 技能会在会话开始时**生成观察者代理**
- 观察者在后台运行（Haiku 模型）
- 更好的性能和用户体验

---

## 数据流和处理差异

### Everything Claude Code 的数据流

```
Session Start
    ↓
Hook 捕获 PreToolUse/PostToolUse
    ↓
observations.jsonl 记录
    ↓
观察者代理分析（需要手动触发或定时）
    ↓
创建 instincts/personal/
    ↓
用户运行 /evolve
    ↓
Python 脚本聚类分析
    ↓
生成 evolved/{commands,skills,agents}/
```

### Homunculus 的数据流

```
Session Start
    ↓
session-memory 技能激活
    ↓
生成观察者代理（后台，Haiku）
    ↓
Hook 捕获 UserPromptSubmit + PostToolUse
    ↓
observations.jsonl 记录
    ↓
观察者代理自动分析（后台运行）
    ↓
创建 instincts/personal/（自动批准）
    ↓
检测聚类 → identity.json 标记
    ↓
用户运行 /homunculus:evolve
    ↓
Shell 脚本处理
    ↓
生成 evolved/{commands,skills,agents}/
```

**关键差异：**
- **Everything Claude Code**：观察者需要手动或定时触发
- **Homunculus**：观察者在会话开始时自动生成并后台运行（更自动化）

---

## 技术实现细节

### 导出格式

#### Everything Claude Code
```yaml
version: "2.0"
exported_by: "learning-instinct"
export_date: "2025-01-22T10:30:00Z"

instincts:
  - id: prefer-functional-style
    trigger: "when writing new functions"
    action: "Use functional patterns over classes"
    confidence: 0.8
    domain: code-style
    observations: 8
```

#### Homunculus
```bash
tar -czf instincts-TIMESTAMP.tar.gz \
  -C .claude/homunculus/instincts personal

# 包含 manifest.json
{
  "exported": "2025-01-22T10:30:00Z",
  "version": "2.0.0",
  "instincts": {"personal": 12},
  "domains": "code-style,testing,git"
}
```

**差异：**
- **Everything Claude Code**：结构化的 YAML/JSON 格式，便于解析和分析
- **Homunculus**：二进制 tar.gz 格式，更简单但不易于检查

---

## 命令详细对比

### `/init` 命令

**相同点：**
- 都检查 identity.json 是否存在
- 都询问用户的技术水平（4 个等级）
- 都创建相同的目录结构
- 都生成相同的 identity.json 格式

**差异：**
- Everything Claude Code：123 行
- Homunculus：120 行
- 基本相同，只是格式略有不同

### `/status` 命令

**Everything Claude Code（111 行）：**
- 支持多个标志：`--domain`, `--source`, `--min-confidence`, `--stale`, `--sort`, `--json`
- 输出包含详细的分类统计
- 包含"陈旧本能"检测
- 包含"最近活动"部分
- 更适合数据分析和监控

**Homunculus（78 行）：**
- 简化的实现，核心信息相同
- 强调"check in"的概念
- 按用户技术水平定制响应
- 更人性化，更简洁

### `/evolve` 命令

**Everything Claude Code（241 行）：**
- 详细的聚类规则说明
- 支持多个标志：`--domain`, `--dry-run`, `--threshold`, `--type`, `--execute`
- 包含 TDD 流程集成（superpowers:writing-skills）
- 详细的输出格式示例
- 支持技能创建工具集成

**Homunculus（59 行）：**
- 简化的实现，核心逻辑相同
- 基本的聚类检测（5+ 本能 = 进化机会）
- 更直接的流程
- 强调"增长"而不是"技术细节"

### `/export` 命令

**Everything Claude Code（127 行）：**
- 支持多种格式：YAML, JSON, Markdown
- 支持过滤：`--domain`, `--min-confidence`, `--output`, `--format`, `--include-evidence`
- 详细的隐私考虑说明
- 包含证据文本选项

**Homunculus（77 行）：**
- 简单的 tar.gz 打包
- 包含 manifest.json 元数据
- 更简洁，但功能较少

---

## 观察者代理对比

### Everything Claude Code（142 行）

**特点：**
- 详细的模式检测规则：
  1. 用户更正（"No, use X instead of Y"）
  2. 错误解决（错误 → 修复序列）
  3. 重复工作流（相同工具序列）
  4. 工具偏好（某些工具优先使用）
- 明确的置信度计算公式
- 包含完整的分析示例
- 保守的方法（3+ 观察 = 创建本能）

### Homunculus（110 行）

**特点：**
- 简化的模式检测：
  1. 重复序列（3+ 次相同工具序列）
  2. 错误→修复模式
  3. 偏好（某些工具优先）
  4. 接受/拒绝信号
- 置信度范围明确（0.3-0.5, 0.5-0.7, 0.7-0.9, 0.9+）
- 强调"静默运行"
- 自动聚类检测和标记

---

## 会话内存技能对比

### Everything Claude Code（43 行）

```markdown
1. Load Context
   - 加载 identity.json
   - 计数本能
   - 检查进化准备
   - 查看最近活动

2. Greet With Context
   - "Back to [PROJECT]. [N] instincts. [Session count] sessions together."
   - 如果有进化准备："I've clustered enough in [DOMAIN]."

3. During Session
   - 观察自动捕获（无需手动）
   - 应用学到的本能

4. At Session End
   - Stop hook 处理一切
   - 会话计数自动增加
```

### Homunculus（60 行）

```markdown
1. Spawn Observer (Background)
   - 检查是否有观察
   - 生成观察者代理（后台，Haiku）
   - 使用 Task 工具

2. Load Context
   - 加载 identity.json
   - 计数本能
   - 检查进化准备
   - 查看最近活动

3. Greet With Context
   - 相同的问候格式
   - 进化准备通知

4. During Session
   - 观察自动捕获
   - 应用学到的本能

5. At Session End
   - Stop hook 处理一切
```

**关键差异：**
- **Homunculus** 在会话开始时**生成观察者代理**（后台运行）
- **Everything Claude Code** 没有明确的观察者生成步骤

---

## 文件大小和复杂度对比

| 文件/目录 | Everything Claude Code | Homunculus | 差异 |
|----------|----------------------|-----------|------|
| commands/evolve.md | 241 行 | 59 行 | Everything 4.1 倍 |
| commands/status.md | 111 行 | 78 行 | Everything 1.4 倍 |
| commands/export.md | 127 行 | 77 行 | Everything 1.6 倍 |
| agents/observer.md | 142 行 | 110 行 | Everything 1.3 倍 |
| skills/session-memory | 43 行 | 60 行 | Homunculus 1.4 倍 |
| 总命令数 | 6 个 | 5 个 | Everything 多 1 个 |
| 包含登陆页面 | ❌ | ✅ | Homunculus 有 |
| 包含演示文件 | ❌ | ✅ | Homunculus 有 |
| Python 脚本 | ✅ | ❌ | Everything 有 |

---

## 优势总结

### Everything Claude Code 的优势

1. **更强大的技术能力**
   - Python 脚本支持复杂算法
   - 多种导出格式（YAML, JSON, Markdown）
   - 更详细的命令选项和标志
   - 更完整的聚类分析说明

2. **更好的数据分析**
   - 详细的统计输出
   - 陈旧本能检测
   - 多种排序和过滤选项
   - 更适合监控和调试

3. **更灵活的扩展**
   - 额外的 `install-opencode` 命令
   - TDD 流程集成
   - 技能创建工具集成

4. **更详细的文档**
   - 每个命令都有详细的说明
   - 包含完整的示例
   - 更适合开发者

### Homunculus 的优势

1. **完整的产品化方案**
   - React 登陆页面（营销和展示）
   - 演示录制文件（实际使用演示）
   - 更完整的项目结构

2. **更好的自动化**
   - 观察者在会话开始时自动生成
   - 后台运行，无需手动触发
   - 自动聚类检测和标记

3. **更简洁的实现**
   - 所有脚本都是 Shell（无 Python 依赖）
   - 更轻量级，更容易部署
   - 命令更简洁，更易使用

4. **更人性化的设计**
   - 命令输出更有"个性"
   - 强调"生命体"而不是"工具"
   - 按用户技术水平定制响应
   - 更好的用户体验

5. **更好的性能**
   - 观察者使用 Haiku 模型（成本低）
   - 后台运行，不阻塞主线程
   - 更快的响应时间

---

## 技术栈对比

| 方面 | Everything Claude Code | Homunculus |
|------|----------------------|-----------|
| **脚本语言** | Bash + Python | Bash only |
| **依赖** | Python 3 | 无额外依赖 |
| **UI** | 无 | React + Tailwind |
| **演示** | 无 | asciinema (.tape) |
| **数据格式** | YAML/JSON/Markdown | tar.gz + JSON |
| **模型** | 未指定 | Haiku（观察者） |

---

## 使用场景建议

### 选择 Everything Claude Code 如果你：
- 需要**强大的数据分析能力**
- 想要**多种导出格式**
- 需要**详细的技术文档**
- 想要**更多的命令选项**
- 有 Python 环境
- 需要**监控和调试功能**

### 选择 Homunculus 如果你：
- 需要**完整的产品方案**（包括 UI）
- 想要**更简洁的实现**
- 需要**自动化的观察**
- 想要**更好的用户体验**
- 需要**轻量级部署**
- 想要**演示和营销材料**
- 更看重**易用性而不是功能**

---

## 演进关系

**Everything Claude Code** 是 **Homunculus v2.0** 的**核心库和参考实现**。

- **Homunculus** 采用了 Everything Claude Code 的核心概念（instincts, hooks, observer）
- **Homunculus** 添加了**产品化层**（React UI, 演示, 简化实现）
- **Everything Claude Code** 提供了**更强大的技术基础**
- **Homunculus** 提供了**更好的用户体验**

---

## 结论

| 维度 | 赢家 |
|------|------|
| **技术深度** | Everything Claude Code |
| **产品完整性** | Homunculus |
| **易用性** | Homunculus |
| **可扩展性** | Everything Claude Code |
| **自动化程度** | Homunculus |
| **部署难度** | Homunculus（更简单） |
| **功能丰富度** | Everything Claude Code |
| **用户体验** | Homunculus |

**最终评价：**
- **Everything Claude Code** 是一个**强大的技术框架**，适合需要深度定制和分析的开发者
- **Homunculus** 是一个**完整的产品**，适合需要开箱即用的用户

两者都基于相同的核心理念（观察、学习、进化），但针对不同的使用场景进行了优化。
