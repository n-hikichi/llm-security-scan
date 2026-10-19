#!/usr/bin/env python3
"""claude -p の標準出力(レポート)を検査し、Markdown と JSON に分けて保存する。

usage: save_report.py <raw-output-file> <out-dir>

- 1 行目が所定の見出しでなければ、拒否・空応答・途中終了とみなして exit 3
- 5 つの節がそろっていなければ exit 3
- 「## 6. 機械可読出力」の JSON ブロックがあれば取り出して llm-security-report.json に保存
  (JSON として読めなければ exit 4。Markdown は保存する)
"""
import json
import re
import sys
from pathlib import Path

TITLE = "# セキュリティレビュー レポート"
SECTIONS = ["## 1. ヘッダ", "## 2. 所見", "## 3. 完全性の所見", "## 4. 要確認", "## 5. 確認した範囲"]


def main():
    if len(sys.argv) != 3:
        print(__doc__, file=sys.stderr)
        return 2
    raw = Path(sys.argv[1]).read_text(encoding="utf-8").strip()
    out_dir = Path(sys.argv[2])
    out_dir.mkdir(parents=True, exist_ok=True)

    lines = raw.splitlines()
    if not lines or lines[0].strip() != TITLE:
        print(f"error: レポートの 1 行目が「{TITLE}」ではありません(拒否・空応答・途中終了の可能性)", file=sys.stderr)
        return 3
    missing = [s for s in SECTIONS if not any(line.startswith(s) for line in lines)]
    if missing:
        print(f"error: レポートの節が足りません: {missing}", file=sys.stderr)
        return 3

    rc = 0
    body = raw
    m = re.search(r"^## 6\. 機械可読出力.*?```json\s*\n(.*?)\n```", raw, flags=re.S | re.M)
    if m:
        body = raw[: m.start()].rstrip()
        try:
            data = json.loads(m.group(1))
            (out_dir / "llm-security-report.json").write_text(
                json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
            )
        except json.JSONDecodeError as e:
            print(f"error: 機械可読出力が JSON として読めません: {e}", file=sys.stderr)
            rc = 4
    (out_dir / "llm-security-report.md").write_text(body + "\n", encoding="utf-8")
    return rc


if __name__ == "__main__":
    sys.exit(main())
