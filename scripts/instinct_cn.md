# Instinct CLI 文档

## 概述

`instinct.py` 是一个命令行工具，用于管理 Homunculus 系统中的"直觉"（Instincts）。直觉是系统学习和记忆的基本单位，通过持续学习 v2 框架来积累和进化。

## 核心概念

### 什么是直觉（Instinct）？

直觉是一个包含以下信息的结构化数据：
- **id**: 唯一标识符
- **trigger**: 触发条件（何时应用该直觉）
- **confidence**: 置信度（0-1，表示该直觉的可靠性）
- **domain**: 领域分类（如 workflow、coding、design 等）
- **content**: 具体的行动指南或知识内容

### 直觉的来源

- **Personal（个人）**: 用户自己创建的直觉
- **Inherited（继承）**: 从其他来源导入的直觉

### 直觉的进化

直觉可以进化为：
- **Skills（技能）**: 相关直觉的集合
- **Commands（命令）**: 工作流直觉演变成的可执行命令
- **Agents（代理）**: 复杂的多步骤自动化代理

## 目录结构

```
~/.claude/homunculus/
├── instincts/
│   ├── personal/          # 个人直觉存储
│   └── inherited/         # 继承的直觉存储
├── evolved/
│   ├── skills/            # 进化后的技能
│   ├── commands/          # 进化后的命令
│   └── agents/            # 进化后的代理
└── observations.jsonl     # 观察日志
```

## 文件格式

直觉文件采用 YAML 前置元数据 + 内容的格式：

```yaml
---
id: unique-instinct-id
trigger: "when creating a new feature"
confidence: 0.85
domain: workflow
source: personal
---

## Action
具体的行动步骤或知识内容...

## Context
背景信息...
```

## 命令详解

### 1. status - 查看状态

显示所有直觉的概览，包括数量、置信度、触发条件等。

**用法**:
```bash
python instinct.py status
```

**输出内容**:
- 个人直觉和继承直觉的数量统计
- 按领域分组的直觉列表
- 每个直觉的置信度（用进度条表示）
- 触发条件和行动摘要
- 观察日志统计

**示例输出**:
```
============================================================
  INSTINCT STATUS - 15 total
============================================================

  Personal:  10
  Inherited: 5

## WORKFLOW (8)

  ██████████ 100%  feature-creation-workflow
            trigger: when creating a new feature
            action: Follow the standard feature creation process...

  ████████░░  80%  code-review-checklist
            trigger: when reviewing code
            action: Check for common issues...
```

### 2. import - 导入直觉

从文件或 URL 导入直觉。支持重复检测和置信度过滤。

**用法**:
```bash
python instinct.py import <source> [options]
```

**参数**:
- `source`: 文件路径或 HTTP/HTTPS URL
- `--dry-run`: 预览导入内容，不实际保存
- `--force`: 跳过确认提示
- `--min-confidence <value>`: 最小置信度阈值（0-1）

**导入逻辑**:
1. 解析源文件中的直觉
2. 与现有直觉比对：
   - **新增**: 不存在的直觉
   - **更新**: 存在但新版本置信度更高
   - **跳过**: 重复且置信度相同或更低
3. 应用最小置信度过滤
4. 显示导入摘要并请求确认
5. 保存到 `inherited/` 目录

**示例**:
```bash
# 从 URL 导入
python instinct.py import https://example.com/instincts.yaml

# 从本地文件导入，最小置信度 0.7
python instinct.py import ./my_instincts.yaml --min-confidence 0.7

# 预览导入内容
python instinct.py import ./instincts.yaml --dry-run
```

### 3. export - 导出直觉

导出直觉到文件，支持按领域和置信度过滤。

**用法**:
```bash
python instinct.py export [options]
```

**参数**:
- `--output <file>` 或 `-o <file>`: 输出文件路径（不指定则输出到标准输出）
- `--domain <domain>`: 只导出指定领域的直觉
- `--min-confidence <value>`: 最小置信度阈值

**示例**:
```bash
# 导出所有直觉到文件
python instinct.py export --output my_instincts.yaml

# 导出 workflow 领域的高置信度直觉
python instinct.py export --domain workflow --min-confidence 0.8 -o workflow_instincts.yaml

# 输出到标准输出
python instinct.py export --domain coding
```

### 4. evolve - 分析和进化

分析直觉集群，建议可以进化成技能、命令或代理的候选。

**用法**:
```bash
python instinct.py evolve [--generate]
```

**参数**:
- `--generate`: 生成进化后的结构（当前为占位符）

**分析内容**:

#### 技能候选（Skill Candidates）
- 识别触发器相似的直觉集群
- 需要至少 2 个直觉
- 显示集群大小、平均置信度和涉及的领域

#### 命令候选（Command Candidates）
- 来自 workflow 领域且置信度 ≥ 70% 的直觉
- 自动生成建议的命令名称

#### 代理候选（Agent Candidates）
- 包含 3+ 个直觉的集群
- 平均置信度 ≥ 75%
- 表示可以自动化的复杂工作流

**示例**:
```bash
python instinct.py evolve
```

**示例输出**:
```
============================================================
  EVOLVE ANALYSIS - 15 instincts
============================================================

High confidence instincts (>=80%): 8

Potential skill clusters found: 3

## SKILL CANDIDATES

1. Cluster: "feature development"
   Instincts: 4
   Avg confidence: 85%
   Domains: workflow, coding
   Instincts:
     - feature-creation-workflow
     - code-review-checklist
     - testing-strategy

## COMMAND CANDIDATES (2)

  /feature-workflow
    From: feature-creation-workflow
    Confidence: 100%

## AGENT CANDIDATES (1)

  feature-development-agent
    Covers 4 instincts
    Avg confidence: 85%
```

## 工作流示例

### 场景 1: 建立个人知识库

```bash
# 1. 导入来自团队的直觉
python instinct.py import https://team.example.com/instincts.yaml --min-confidence 0.7

# 2. 查看当前状态
python instinct.py status

# 3. 分析可以进化的模式
python instinct.py evolve

# 4. 导出高置信度的直觉用于分享
python instinct.py export --min-confidence 0.8 -o high_confidence.yaml
```

### 场景 2: 持续学习循环

```bash
# 1. 定期导入新学到的直觉
python instinct.py import ./learned_instincts.yaml --force

# 2. 监控直觉库的增长
python instinct.py status

# 3. 识别可以自动化的工作流
python instinct.py evolve

# 4. 与团队分享最有价值的直觉
python instinct.py export --domain workflow --min-confidence 0.85 -o team_workflows.yaml
```

## 关键特性

### 置信度管理
- 每个直觉都有置信度评分（0-1）
- 导入时可以通过置信度过滤
- 导出时可以只导出高置信度的直觉
- 更新时只有更高置信度的版本才会覆盖现有直觉

### 重复检测
- 导入时自动检测重复的直觉 ID
- 避免导入置信度更低的重复版本
- 支持更新置信度更高的版本

### 集群分析
- 通过触发器相似性识别相关直觉
- 自动规范化触发器（移除常见关键词）
- 计算集群的平均置信度

### 干运行模式
- `--dry-run` 选项可以预览导入内容
- 不实际修改任何文件
- 用于验证导入的正确性

## 技术细节

### 文件解析
- 支持 YAML 前置元数据格式
- 使用 `---` 作为分隔符
- 自动处理多个直觉在一个文件中的情况

### 数据存储
- 个人直觉存储在 `~/.claude/homunculus/instincts/personal/`
- 导入的直觉存储在 `~/.claude/homunculus/instincts/inherited/`
- 文件名格式: `{source_name}-{timestamp}.yaml`

### 观察日志
- 记录在 `~/.claude/homunculus/observations.jsonl`
- 每行一个 JSON 对象
- 用于跟踪系统的学习过程

## 扩展可能性

当前代码预留了以下扩展点：

1. **生成进化结构**: `cmd_evolve` 中的 `--generate` 选项可以实现自动生成技能、命令和代理文件

2. **观察集成**: 可以集成观察日志来计算直觉的使用频率和有效性

3. **版本控制**: 可以添加直觉的版本历史和变更跟踪

4. **协作分享**: 可以实现直觉的团队分享和评分机制

## 总结

`instinct.py` 是 Homunculus 持续学习系统的核心工具，提供了：
- 📊 **管理**: 组织和分类直觉
- 📥 **导入**: 从各种来源学习
- 📤 **导出**: 分享和备份知识
- 🧠 **进化**: 识别可以自动化的模式

通过这个工具，AI 助手可以不断积累、组织和进化自己的知识库，实现真正的持续学习。
