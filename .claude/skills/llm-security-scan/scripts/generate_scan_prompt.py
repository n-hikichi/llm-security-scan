#!/usr/bin/env python3
"""
Generate security scan prompt based on project type detection.
"""

import os
import sys
import json
import subprocess
from pathlib import Path


def run_detection(project_dir, detect_script):
    """Run the project type detection script."""
    try:
        result = subprocess.run(
            ['python3', detect_script, project_dir],
            capture_output=True,
            text=True,
            check=True
        )
        return json.loads(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Error running detection script: {e.stderr}", file=sys.stderr)
        return None
    except json.JSONDecodeError as e:
        print(f"Error parsing detection result: {e}", file=sys.stderr)
        return None


def read_prompt_file(prompt_file):
    """Read the content of a prompt file."""
    try:
        with open(prompt_file, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        print(f"Error: Prompt file not found: {prompt_file}", file=sys.stderr)
        return None
    except Exception as e:
        print(f"Error reading prompt file: {e}", file=sys.stderr)
        return None


def generate_security_prompt(project_dir, skill_dir):
    """
    Generate a security scan prompt based on the project directory.
    
    Args:
        project_dir: Path to the project directory to scan
        skill_dir: Path to the skill directory (contains scripts and references)
    
    Returns:
        str: Generated prompt text, or None if generation failed
    """
    detect_script = os.path.join(skill_dir, 'scripts', 'detect_project_type.py')
    
    # Detect project type
    detection = run_detection(project_dir, detect_script)
    if detection is None:
        return None
    
    project_type = detection.get('project_type')
    confidence = detection.get('confidence', 0.0)
    indicators = detection.get('indicators', {})
    
    # Generate header
    prompt_parts = []
    prompt_parts.append("# JavaScript プロジェクトセキュリティスキャン")
    prompt_parts.append("")
    prompt_parts.append(f"## プロジェクト分析結果")
    prompt_parts.append(f"- **プロジェクトタイプ**: {project_type}")
    prompt_parts.append(f"- **信頼度**: {confidence:.2%}")
    prompt_parts.append("")
    
    if indicators.get('client_signals'):
        prompt_parts.append("### クライアントサイドの指標:")
        for signal in indicators['client_signals']:
            prompt_parts.append(f"  - {signal}")
        prompt_parts.append("")
    
    if indicators.get('server_signals'):
        prompt_parts.append("### サーバーサイドの指標:")
        for signal in indicators['server_signals']:
            prompt_parts.append(f"  - {signal}")
        prompt_parts.append("")
    
    prompt_parts.append("---")
    prompt_parts.append("")
    
    # Load appropriate prompt file(s)
    if project_type == 'client':
        prompt_file = os.path.join(skill_dir, 'references', 'cli-security-prompt.md')
        prompt_content = read_prompt_file(prompt_file)
        if prompt_content:
            prompt_parts.append(prompt_content)
    
    elif project_type == 'server':
        prompt_file = os.path.join(skill_dir, 'references', 'sv-security-prompt.md')
        prompt_content = read_prompt_file(prompt_file)
        if prompt_content:
            prompt_parts.append(prompt_content)
    
    elif project_type == 'both':
        prompt_parts.append("## 注意: クライアント/サーバー両方の特性が検出されました")
        prompt_parts.append("")
        prompt_parts.append("このプロジェクトはクライアントサイドとサーバーサイドの両方のコードを含んでいます。")
        prompt_parts.append("両方の観点からセキュリティレビューを実施してください。")
        prompt_parts.append("")
        prompt_parts.append("---")
        prompt_parts.append("")
        
        # Include both prompts
        cli_prompt_file = os.path.join(skill_dir, 'references', 'cli-security-prompt.md')
        sv_prompt_file = os.path.join(skill_dir, 'references', 'sv-security-prompt.md')
        
        cli_content = read_prompt_file(cli_prompt_file)
        sv_content = read_prompt_file(sv_prompt_file)
        
        if cli_content:
            prompt_parts.append("# クライアントサイド セキュリティレビュー")
            prompt_parts.append("")
            prompt_parts.append(cli_content)
            prompt_parts.append("")
            prompt_parts.append("---")
            prompt_parts.append("")
        
        if sv_content:
            prompt_parts.append("# サーバーサイド セキュリティレビュー")
            prompt_parts.append("")
            prompt_parts.append(sv_content)
    
    else:  # unknown
        prompt_parts.append("## 警告: プロジェクトタイプを特定できませんでした")
        prompt_parts.append("")
        prompt_parts.append("package.json を確認するか、手動でプロジェクトタイプを指定してください。")
        prompt_parts.append("")
        prompt_parts.append("使用可能なプロンプト:")
        prompt_parts.append("- クライアントサイド: references/cli-security-prompt.md")
        prompt_parts.append("- サーバーサイド: references/sv-security-prompt.md")
        return None
    
    return "\n".join(prompt_parts)


def main():
    if len(sys.argv) < 3:
        print("Usage: generate_scan_prompt.py <project_directory> <skill_directory>", file=sys.stderr)
        sys.exit(1)
    
    project_dir = sys.argv[1]
    skill_dir = sys.argv[2]
    
    if not os.path.isdir(project_dir):
        print(f"Error: {project_dir} is not a directory", file=sys.stderr)
        sys.exit(1)
    
    if not os.path.isdir(skill_dir):
        print(f"Error: {skill_dir} is not a directory", file=sys.stderr)
        sys.exit(1)
    
    prompt = generate_security_prompt(project_dir, skill_dir)
    
    if prompt:
        print(prompt)
    else:
        sys.exit(1)


if __name__ == '__main__':
    main()
