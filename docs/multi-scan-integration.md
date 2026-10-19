# multi-scan オーケストレータとの接続(v2)

multi-scan リポジトリから git clone されている。
それとの同期をとるための know how。付録 B(各 Agent の I/F 変更報告)に転記する想定。

## 1. 破壊的変更(SemVer メジャー:1.0.0 → 2.0.0)

| I/F | v1 | v2 | multi-scan 側の対応 |
|---|---|---|---|
| 許可ツール(`--allowedTools`) | `Read Write Edit Glob Grep Bash(python3:*) Bash(cat:*) … mcp__serena__*` | **`Read Glob Grep Task`** | `run-3-llm.sh` のホワイトリストを縮小。`top-prompt.md` Phase 3 の生成テンプレートも同様 |
| レポートの保存 | agent が `test-results/security/llm-security-report.md` に Write | agent は標準出力に返す。**runner が `scripts/save_report.py` で検査して保存** | `run-3-llm.sh` を `examples/multi-scan/run-3-llm.sh` の形に置き換える |
| MCP Serena | `--mcp-config` で起動 | 不要 | `serena-mcp-config.sh` の呼び出しを外す(残しても害はないが、起動時間と失敗要因が増える) |
| prompt の引数 | 「`.sut-config` から SCAN_PATH を取得し…」 | 「引数 `full <SCAN_PATH> json` で実行」 | heredoc の文面を差し替え |
| モデル | 指定なし(既定) | `--model claude-fable-5-1` を明示 | 環境変数 `LLM_SCAN_MODEL` で上書き可にした |
| JSON の形式 | パッケージごとに不定 | `references/report-schema.json`(schema_version 2.0)に固定 | `run-5-summary.sh` の集計で `summary` / `findings` / `integrity_findings` / `needs_triage` を読める |

## 2. 据え置いたもの

- skill の名前とパス:`.claude/skills/llm-security-scan/SKILL.md`(prompt の `@` 参照はそのまま)
- `.sut-config` から対象パスを読む方式、`--add-dir` で渡す方式
- 出力ファイル名:`test-results/security/llm-security-report.md` / `llm-security-report.json`
- watchdog(`claude-watchdog.sh`)との併用:出力 glob を `llm-security-report.raw.md` にすれば従来どおり使える

## 3. 新しく渡すもの

- 対象リポジトリのルート(または対象コンポーネント)に **`SECURITY_REVIEW_CONTEXT.md`** を置く。無くても動くが、TLS・テナント・ロールの判断精度が下がる。multi-scan の Phase 1(環境確認)で配布するのがよい。
- Python コンポーネントも対象にできる。`.sut-config` に Python のディレクトリを書けば同じ runner で動く。

## 4. 統合サマリー(`run-5-summary.sh`)への影響

- v2 の件数は v1 より大幅に少ない(堅牢化・依存関係・DoS を報告しない)。v1 の件数と横並びで比較しない。
- `needs_triage`(要確認)を必ずサマリーに載せる。本文の所見が 0 でも、ここに境界の候補が入る。
- `integrity_findings`(完全性の所見)は脆弱性の件数と分けて集計する。
- パッケージをまたぐ問題(例:ロール付与の API と、そのロールを信用する別パッケージ)は、各パッケージの `needs_triage` の `to_confirm` に「他コンポーネントの確認」として現れることが多い。横断サマリーで突き合わせる。

## 5. 確認済みの動作

- `examples/multi-scan/run-3-llm.sh` を multi-scan と同じ配置(ツール用ディレクトリ + `.sut-config` + `--add-dir`)で実行し、読み取り専用で完走、Markdown と JSON が所定のファイル名で保存され、JSON がスキーマに適合することを確認した(2026-09-30、`claude-fable-5-1`)。
