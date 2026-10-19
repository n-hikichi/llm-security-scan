# ChangeLog

## [2.0.0] - 2026-10-19

skill を公式 `/security-review` prompt([anthropics/claude-code-security-review](https://github.com/anthropics/claude-code-security-review) `0c6a49f`)ベースに作り直した。multi-scan の I/F を変えるメジャーバージョンアップ(`docs/multi-scan-integration.md`)。

### Added
- `references/upstream-security-review.md` / `upstream/security-review.md` — 公式 prompt の無改変コピー(`docs/upstream.md` でハッシュ管理)
- `rules/org-specific.md` — 自社の追加観点(テナント境界、トークンの扱い、ログイン CSRF、リポジトリ内の秘密実体、安全に関わる判定の fail-open)。対訳つき
- `rules/exclusions.md` — 自社の追加除外・判断基準、データの扱いルール。対訳つき
- `rules/sut-context.template.md` — 対象ごとの前提情報 `SECURITY_REVIEW_CONTEXT.md` のテンプレート
- `references/report-schema.json` — JSON 出力の固定スキーマ(schema_version 2.0)
- `scripts/save_report.py` — レポートの検査(題名・5 節)と保存。拒否・空応答を失敗として検知
- `examples/multi-scan/run-3-llm.sh` — multi-scan 用 runner の例(読み取り専用、モデル明示)
- `docs/operation.md` — 運用設計(権限の境界、入力の信頼区分、人間によるレビュー、失敗の検知、再評価トリガ)
- `docs/procedure.md` — 実施手順(v1 手順の改訂版。旧手順との差分を含む)
- `docs/multi-scan-integration.md` — multi-scan 側への連絡事項
- 全体モード(`full [<パス>]`)、JSON 出力(`json`)、レポートの「要確認」(確信度 5〜7)セクション

### Changed
- 差分モード(PR 差分)を既定にした。全体スキャンは節目用
- agent は読み取り専用(`Read Glob Grep Task`)。レポートは標準出力で返し、保存は呼び出し側
- 対象言語の制限をなくした(Python 等も対象)
- 推奨モデルを `claude-fable-5-1` に定め、レポートのヘッダと JSON に使用モデル ID を記録
- 依存関係の既知の脆弱性は報告しない(SCA 工程へ)。`npm audit` も実行しない
- SKILL.md を日本語化。出力は日本語の 5 節構成(ヘッダ / 所見 / 完全性の所見 / 要確認 / 確認した範囲)
- README.md を v2 向けに全面改訂

### Removed
- `scripts/detect_project_type.py`、`scripts/generate_scan_prompt.py`(client / server の自動判定)
- `references/cli-security-prompt.md`、`references/sv-security-prompt.md`(自作チェックリスト)
- `references/mcp-serena-integration.md`(Serena は不要)
- HTTP 待ち受けを Critical とする指示、ベストプラクティス・アクションプランの全列挙
- v1 の文書(`getting-started.*`、`how-to-start-LLM-base-scan.*`、`external-spec.*`)。内容が v2 と合わないため削除。v1 の最終コミット `fb3a80b`(タグ `v1.0.0` には external-spec と pptx が含まれない)で参照できる。v2 では README と `docs/procedure.md` を正とする

### Known issues
- `claude -p` の標準出力に、sub-task の待ち時間に出た途中経過の文がレポートの前に混入することがある。`save_report.py` は題名の行より前を捨てて対処する(題名の直後に混入した行は本文に残る)。skill 側の「最終応答はレポートのみ」の徹底は次の改訂で
- 差分モードでも `committed_secret` の走査がリポジトリ全体に及ぶことがある(差分外の秘密が「要確認(差分外の既存問題)」として載り、所要時間が延びる)。差分モードでは変更ファイルに限定する文言を次の改訂で明確にする
- 確信度が 7 と 8 の境目にある候補は、実行ごとに「所見」と「要確認」の間で入れ替わる。要確認は必ず読む運用にする(`docs/operation.md` §4)
- `json` 引数で実行したのに「## 6. 機械可読出力」が無い場合、`save_report.py` は終了コード 0 で JSON を書かない(runner からは検知できない)。JSON の必須化(終了コード 5)は次の改訂で

## [1.0.0] - 2026-03-10

### Added
- **README.md** - Project overview with quick start guide
- **getting-started.md** - Beginner guide with Markdown slide format (convertible to PPTX)
- **Project structure documentation** - Emphasis on `.claude` directory importance and MCP/Skill integration
- **LLM portability documentation** - Appendix D explaining technical feasibility of supporting other LLMs beyond Claude

## [Unreleased]

### Changed
- **how-to-start-LLM-base-scan.md**: Removed redundant "install serena in advance" instruction. Section 1-b (`claude mcp add serena`) already handles serena installation, making the introductory text unnecessary. Clarified that uv is required as a prerequisite for the installation command in section 1-b. (2026-03-10)
- **how-to-start-LLM-base-scan.md**: Added Appendix D explaining LLM portability and flexibility. Documents that the tool architecture supports migration to other LLMs (Codex, Gemini, Llama) beyond Claude, with technical rationale and migration strategies. (2026-03-10)
- **how-to-start-LLM-base-scan.md** and **getting-started.md**: Clarified automatic project detection mechanism. Project type (language/framework/architecture) is auto-detected within the launch directory. Added Footnote [3] in how-to-start explaining cwd-based exploration logic. (2026-03-10)
- **getting-started.md**: Changed "入力と出力の流れ" section to clarify that auto-detection happens within the launch directory, not that LLM selects which repo to scan. (2026-03-10)

### Removed
- **how-to-start-LLM-base-scan.md**: Removed Appendix D (WIP Web version example) as it was incomplete/under construction. (2026-03-10)
- **getting-started.md**: Removed "将来の拡張可能性" (future expansion possibilities) subsection from v1.0.0 scope to focus on current JavaScript/Node.js support. (2026-03-10)
- **getting-started.md**: Removed "付録 C：Python 拡張概要" (Appendix C: Python expansion overview). Detailed implementation approaches not relevant for beginner guide. (2026-03-10)
