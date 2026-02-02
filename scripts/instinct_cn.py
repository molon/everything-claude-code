#!/usr/bin/env python3
"""
Instinct CLI - Manage instincts for Continuous Learning v2

Commands:
  status   - Show all instincts and their status
  import   - Import instincts from file or URL
  export   - Export instincts to file
  evolve   - Cluster instincts into skills/commands/agents
"""

import argparse
import sys
import re
import urllib.request
from pathlib import Path
from datetime import datetime
from collections import defaultdict

# ─────────────────────────────────────────────
# Configuration
# ─────────────────────────────────────────────

# 定义 Homunculus 系统的目录结构
HOMUNCULUS_DIR = Path.home() / '.claude' / 'homunculus'
INSTINCTS_DIR = HOMUNCULUS_DIR / 'instincts'
PERSONAL_DIR = INSTINCTS_DIR / 'personal'  # 个人创建的直觉
INHERITED_DIR = INSTINCTS_DIR / 'inherited'  # 继承/导入的直觉
EVOLVED_DIR = HOMUNCULUS_DIR / 'evolved'  # 进化后的技能/命令/代理
OBSERVATIONS_FILE = HOMUNCULUS_DIR / 'observations.jsonl'  # 观察日志文件

# 确保所有必要的目录都存在
for d in [PERSONAL_DIR, INHERITED_DIR,
          EVOLVED_DIR / 'skills', EVOLVED_DIR / 'commands',
          EVOLVED_DIR / 'agents']:
    d.mkdir(parents=True, exist_ok=True)

# ─────────────────────────────────────────────
# Instinct Parser - 直觉解析器
# ─────────────────────────────────────────────


def parse_instinct_file(content: str) -> list[dict]:
    """
    解析类似 YAML 格式的直觉文件。
    文件格式：使用 --- 作为分隔符，分隔元数据和内容
    """
    instincts = []
    current = {}
    in_frontmatter = False
    content_lines = []

    for line in content.split('\n'):
        if line.strip() == '---':
            if in_frontmatter:
                # 前置元数据结束
                in_frontmatter = False
                if current:
                    current['content'] = '\n'.join(content_lines).strip()
                    instincts.append(current)
                    current = {}
                    content_lines = []
            else:
                # 前置元数据开始
                in_frontmatter = True
                if current:
                    current['content'] = '\n'.join(content_lines).strip()
                    instincts.append(current)
                current = {}
                content_lines = []
        elif in_frontmatter:
            # 解析 YAML 格式的前置元数据（key: value）
            if ':' in line:
                key, value = line.split(':', 1)
                key = key.strip()
                value = value.strip().strip('"').strip("'")
                # 置信度转换为浮点数
                if key == 'confidence':
                    current[key] = float(value)
                else:
                    current[key] = value
        else:
            # 收集内容行
            content_lines.append(line)

    # 处理最后一个直觉（可能没有结尾的 ---）
    if current:
        current['content'] = '\n'.join(content_lines).strip()
        instincts.append(current)

    # 只返回有 id 的直觉
    return [i for i in instincts if i.get('id')]


def load_all_instincts() -> list[dict]:
    """
    从个人和继承目录加载所有直觉。
    为每个直觉添加源文件和源类型的元数据。
    """
    instincts = []

    for directory in [PERSONAL_DIR, INHERITED_DIR]:
        if not directory.exists():
            continue
        # 遍历所有 .yaml 文件
        for file in directory.glob("*.yaml"):
            try:
                content = file.read_text()
                parsed = parse_instinct_file(content)
                # 为每个直觉添加源信息
                for inst in parsed:
                    inst['_source_file'] = str(file)
                    inst['_source_type'] = directory.name
                instincts.extend(parsed)
            except (OSError, ValueError) as e:
                print(f"Warning: Failed to parse {file}: {e}",
                      file=sys.stderr)

    return instincts


# ─────────────────────────────────────────────
# Status Command - 状态命令
# ─────────────────────────────────────────────

def cmd_status(_args):
    """显示所有直觉的状态概览。"""
    instincts = load_all_instincts()

    if not instincts:
        print("No instincts found.")
        print("\nInstinct directories:")
        print(f"  Personal:  {PERSONAL_DIR}")
        print(f"  Inherited: {INHERITED_DIR}")
        return

    # 按领域分组
    by_domain = defaultdict(list)
    for inst in instincts:
        domain = inst.get('domain', 'general')
        by_domain[domain].append(inst)

    # 打印标题
    print(f"\n{'='*60}")
    print(f"  INSTINCT STATUS - {len(instincts)} total")
    print(f"{'='*60}\n")

    # 按来源统计
    personal = [i for i in instincts if i.get('_source_type') == 'personal']
    inherited = [i for i in instincts if i.get('_source_type') == 'inherited']
    print(f"  Personal:  {len(personal)}")
    print(f"  Inherited: {len(inherited)}")
    print()

    # 按领域打印直觉列表
    for domain in sorted(by_domain.keys()):
        domain_instincts = by_domain[domain]
        print(f"## {domain.upper()} ({len(domain_instincts)})")
        print()

        # 按置信度排序（从高到低）
        for inst in sorted(
                domain_instincts,
                key=lambda x: -x.get('confidence', 0.5)
        ):
            conf = inst.get('confidence', 0.5)
            # 用进度条表示置信度
            conf_bar = ('█' * int(conf * 10) +
                        '░' * (10 - int(conf * 10)))
            trigger = inst.get('trigger', 'unknown trigger')

            print(f"  {conf_bar} {int(conf*100):3d}%  "
                  f"{inst.get('id', 'unnamed')}")
            print(f"            trigger: {trigger}")

            # 从内容中提取 Action 部分
            content = inst.get('content', '')
            action_match = re.search(
                r'## Action\s*\n\s*(.+?)(?:\n\n|\\n##|$)',
                content, re.DOTALL
            )
            if action_match:
                action = action_match.group(1).strip().split('\n')[0]
                truncated = (
                    action[:57] + '...' if len(action) > 60 else action
                )
                print(f"            action: {truncated}")

            print()

    # 显示观察统计
    if OBSERVATIONS_FILE.exists():
        with open(OBSERVATIONS_FILE, encoding='utf-8') as f:
            obs_count = sum(1 for _ in f)
        print("─────────────────────────────────────────────────────────")
        print(f"  Observations: {obs_count} events logged")
        print(f"  File: {OBSERVATIONS_FILE}")

    print(f"\n{'='*60}\n")


# ─────────────────────────────────────────────
# Import Command - 导入命令
# ─────────────────────────────────────────────

def cmd_import(args):
    """
    从文件或 URL 导入直觉。
    支持置信度过滤和重复检测。
    """
    source = args.source

    # 获取内容（支持 HTTP/HTTPS URL 或本地文件）
    if source.startswith('http://') or source.startswith('https://'):
        print(f"Fetching from URL: {source}")
        try:
            with urllib.request.urlopen(source) as response:
                content = response.read().decode('utf-8')
        except (urllib.error.URLError, UnicodeDecodeError) as e:
            print(f"Error fetching URL: {e}", file=sys.stderr)
            return 1
    else:
        # 本地文件路径
        path = Path(source).expanduser()
        if not path.exists():
            print(f"File not found: {path}", file=sys.stderr)
            return 1
        with open(path, encoding='utf-8') as f:
            content = f.read()

    # 解析新直觉
    new_instincts = parse_instinct_file(content)
    if not new_instincts:
        print("No valid instincts found in source.")
        return 1

    print(f"\nFound {len(new_instincts)} instincts to import.\n")

    # 加载已存在的直觉
    existing = load_all_instincts()
    existing_ids = {i.get('id') for i in existing}

    # 分类：新增、重复、更新
    to_add = []
    duplicates = []
    to_update = []

    for inst in new_instincts:
        inst_id = inst.get('id')
        if inst_id in existing_ids:
            # 检查是否应该更新（新置信度更高）
            existing_inst = next(
                (e for e in existing if e.get('id') == inst_id),
                None
            )
            if existing_inst:
                if inst.get('confidence', 0) > existing_inst.get(
                        'confidence', 0):
                    to_update.append(inst)
                else:
                    duplicates.append(inst)
        else:
            to_add.append(inst)

    # 按最小置信度过滤
    min_conf = args.min_confidence or 0.0
    to_add = [i for i in to_add if i.get('confidence', 0.5) >= min_conf]
    to_update = [i for i in to_update if i.get('confidence', 0.5) >= min_conf]

    # 显示导入摘要
    if to_add:
        print(f"NEW ({len(to_add)}):")
        for inst in to_add:
            print(f"  + {inst.get('id')} "
                  f"(confidence: {inst.get('confidence', 0.5):.2f})")

    if to_update:
        print(f"\nUPDATE ({len(to_update)}):")
        for inst in to_update:
            print(f"  ~ {inst.get('id')} "
                  f"(confidence: {inst.get('confidence', 0.5):.2f})")

    if duplicates:
        print(f"\nSKIP ({len(duplicates)} - "
              "already exists with equal/higher confidence):")
        for inst in duplicates[:5]:
            print(f"  - {inst.get('id')}")
        if len(duplicates) > 5:
            print(f"  ... and {len(duplicates) - 5} more")

    # 干运行模式（预览不保存）
    if args.dry_run:
        print("\n[dry-run] No changes made.")
        return 0

    # 确认导入
    if not args.force and (to_add or to_update):
        response = input("\nProceed with import? (y/n) ")
        if response.lower() != 'y':
            print("Cancelled.")
            return 0

    # 写入继承目录
    timestamp = datetime.now().isoformat()
    source_name = Path(source).stem
    output_file = INHERITED_DIR / f"{source_name}-{timestamp}.yaml"

    all_to_write = to_add + to_update

    output_content = (
        f"# Imported from {source}\n"
        f"# Date: {datetime.now().isoformat()}\n\n"
    )

    # 生成 YAML 格式的输出
    for inst in all_to_write:
        output_content += "---\n"
        output_content += f"id: {inst.get('id')}\n"
        output_content += f"trigger: \"{inst.get('trigger', 'unknown')}\"\n"
        output_content += f"confidence: {inst.get('confidence', 0.5)}\n"
        output_content += f"domain: {inst.get('domain', 'general')}\n"
        output_content += "source: inherited\n"
        output_content += f"imported_from: \"{source}\"\n"
        if inst.get('source_repo'):
            output_content += f"source_repo: {inst.get('source_repo')}\n"
        output_content += "---\n\n"
        output_content += inst.get('content', '') + '\n\n'

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(output_content)

    print("\n✅ Import complete!")
    print(f"   Added: {len(to_add)}")
    print(f"   Updated: {len(to_update)}")
    print(f"   Saved to: {output_file}")
    return 0


# ─────────────────────────────────────────────
# Export Command - 导出命令
# ─────────────────────────────────────────────

def cmd_export(args):
    """
    导出直觉到文件。
    支持按领域和置信度过滤。
    """
    instincts = load_all_instincts()

    if not instincts:
        print("No instincts to export.")
        return 1

    # 按领域过滤（如果指定）
    if args.domain:
        instincts = [i for i in instincts if i.get('domain') == args.domain]
    # 按最小置信度过滤
    if args.min_confidence:
        instincts = [
            i for i in instincts
            if i.get('confidence', 0.5) >= args.min_confidence
        ]

    if not instincts:
        print("No instincts match the criteria.")
        return 1

    # 生成输出内容
    output = (
        f"# Instincts export\n"
        f"# Date: {datetime.now().isoformat()}\n"
        f"# Total: {len(instincts)}\n\n"
    )

    for inst in instincts:
        output += "---\n"
        # 按顺序输出元数据字段
        for key in ['id', 'trigger', 'confidence', 'domain',
                    'source', 'source_repo']:
            if inst.get(key):
                value = inst[key]
                if key == 'trigger':
                    output += f'{key}: "{value}"\n'
                else:
                    output += f"{key}: {value}\n"
        output += "---\n\n"
        output += inst.get('content', '') + '\n\n'

    # 写入文件或输出到标准输出
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(output)
        print(f"Exported {len(instincts)} instincts to {args.output}")
    else:
        print(output)

    return 0


# ─────────────────────────────────────────────
# Evolve Command - 进化命令
# ─────────────────────────────────────────────

def cmd_evolve(args):
    """
    分析直觉并建议进化方向。
    识别可以演变成技能、命令或代理的直觉集群。
    """
    instincts = load_all_instincts()

    if len(instincts) < 3:
        print("Need at least 3 instincts to analyze patterns.")
        print(f"Currently have: {len(instincts)}")
        return 1

    print(f"\n{'='*60}")
    print(f"  EVOLVE ANALYSIS - {len(instincts)} instincts")
    print(f"{'='*60}\n")

    # 按领域分组
    by_domain = defaultdict(list)
    for inst in instincts:
        domain = inst.get('domain', 'general')
        by_domain[domain].append(inst)

    # 高置信度直觉（技能候选）
    high_conf = [i for i in instincts if i.get('confidence', 0) >= 0.8]
    print(f"High confidence instincts (>=80%): {len(high_conf)}")

    # 查找集群（触发器相似的直觉）
    trigger_clusters = defaultdict(list)
    for inst in instincts:
        trigger = inst.get('trigger', '')
        # 规范化触发器（移除常见关键词）
        trigger_key = trigger.lower()
        for keyword in ['when', 'creating', 'writing', 'adding',
                        'implementing', 'testing']:
            trigger_key = trigger_key.replace(keyword, '').strip()
        trigger_clusters[trigger_key].append(inst)

    # 找出有 2+ 个直觉的集群（技能候选）
    skill_candidates = []
    for trigger, cluster in trigger_clusters.items():
        if len(cluster) >= 2:
            # 计算平均置信度
            avg_conf = (sum(i.get('confidence', 0.5)
                        for i in cluster) / len(cluster))
            skill_candidates.append({
                'trigger': trigger,
                'instincts': cluster,
                'avg_confidence': avg_conf,
                'domains': list(
                    set(i.get('domain', 'general') for i in cluster)
                )
            })

    # 按集群大小和置信度排序
    skill_candidates.sort(
        key=lambda x: (-len(x['instincts']), -x['avg_confidence'])
    )

    print(f"\nPotential skill clusters found: {len(skill_candidates)}")

    if skill_candidates:
        print("\n## SKILL CANDIDATES\n")
        for i, cand in enumerate(skill_candidates[:5], 1):
            print(f"{i}. Cluster: \"{cand['trigger']}\"")
            print(f"   Instincts: {len(cand['instincts'])}")
            print(f"   Avg confidence: {cand['avg_confidence']:.0%}")
            print(f"   Domains: {', '.join(cand['domains'])}")
            print("   Instincts:")
            for inst in cand['instincts'][:3]:
                print(f"     - {inst.get('id')}")
            print()

    # 命令候选（工作流直觉）
    workflow_instincts = [
        i for i in instincts
        if i.get('domain') == 'workflow' and i.get('confidence', 0) >= 0.7
    ]
    if workflow_instincts:
        print(f"\n## COMMAND CANDIDATES ({len(workflow_instincts)})\n")
        for inst in workflow_instincts[:5]:
            trigger = inst.get('trigger', 'unknown')
            # 建议命令名称
            cmd_name = (
                trigger.replace('when ', '')
                .replace('implementing ', '')
                .replace('a ', '')
                .replace(' ', '-')[:20]
            )
            print(f"  /{cmd_name}")
            print(f"    From: {inst.get('id')}")
            print(f"    Confidence: {inst.get('confidence', 0.5):.0%}")
            print()

    # 代理候选（复杂多步骤模式）
    agent_candidates = [
        c for c in skill_candidates
        if len(c['instincts']) >= 3 and c['avg_confidence'] >= 0.75
    ]
    if agent_candidates:
        print(f"\n## AGENT CANDIDATES ({len(agent_candidates)})\n")
        for cand in agent_candidates[:3]:
            agent_name = (
                cand['trigger'].replace(' ', '-')[:20] + '-agent'
            )
            print(f"  {agent_name}")
            print(f"    Covers {len(cand['instincts'])} instincts")
            print(f"    Avg confidence: {cand['avg_confidence']:.0%}")
            print()

    if args.generate:
        print("\n[Would generate evolved structures here]")
        print("  Skills would be saved to:", EVOLVED_DIR / 'skills')
        print("  Commands would be saved to:", EVOLVED_DIR / 'commands')
        print("  Agents would be saved to:", EVOLVED_DIR / 'agents')

    print(f"\n{'='*60}\n")
    return 0


# ─────────────────────────────────────────────
# Main - 主程序入口
# ─────────────────────────────────────────────

def main():
    """Instinct CLI 的主入口点。"""
    parser = argparse.ArgumentParser(
        description='Instinct CLI for Continuous Learning v2'
    )
    subparsers = parser.add_subparsers(
        dest='command', help='Available commands'
    )

    # Status 子命令
    subparsers.add_parser(
        'status', help='Show instinct status'
    )

    # Import 子命令
    import_parser = subparsers.add_parser(
        'import', help='Import instincts'
    )
    import_parser.add_argument('source', help='File path or URL')
    import_parser.add_argument(
        '--dry-run', action='store_true',
        help='Preview without importing'
    )
    import_parser.add_argument(
        '--force', action='store_true',
        help='Skip confirmation'
    )
    import_parser.add_argument(
        '--min-confidence', type=float,
        help='Minimum confidence threshold'
    )

    # Export 子命令
    export_parser = subparsers.add_parser(
        'export', help='Export instincts'
    )
    export_parser.add_argument(
        '--output', '-o', help='Output file'
    )
    export_parser.add_argument(
        '--domain', help='Filter by domain'
    )
    export_parser.add_argument(
        '--min-confidence', type=float,
        help='Minimum confidence'
    )

    # Evolve 子命令
    evolve_parser = subparsers.add_parser(
        'evolve', help='Analyze and evolve instincts'
    )
    evolve_parser.add_argument(
        '--generate', action='store_true',
        help='Generate evolved structures'
    )

    args = parser.parse_args()

    # 根据命令调用相应的处理函数
    if args.command == 'status':
        return cmd_status(args)
    elif args.command == 'import':
        return cmd_import(args)
    elif args.command == 'export':
        return cmd_export(args)
    elif args.command == 'evolve':
        return cmd_evolve(args)
    else:
        parser.print_help()
        return 1


if __name__ == '__main__':
    sys.exit(main() or 0)
