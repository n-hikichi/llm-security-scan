# ChangeLog

## [2.2.0] - 2026-11-11

推奨モデルを `claude-fable-5-1` から **`claude-fable-5-2`** に変更。SKILL.md・`rules/`・公式 prompt・出力の形・引数・allowed-tools は**変えていない**(モデルの差し替えのみ。`operation.md` §6 の再評価の引き金のうち「使用モデルの変更」に当たるので、評価ケースで再評価した)。5.1 の記述は、過去の評価の記録(下の Previous)に分け、現行の記述は 5.2 に統一した。

### Changed
- `README.md`、`docs/procedure.md`、`docs/multi-scan-integration.md`: 推奨・標準のモデルを `claude-fable-5-2` に。
- `examples/multi-scan/run-3-llm.sh`: 既定のモデルを `${LLM_SCAN_MODEL:-claude-fable-5-2}` に(環境変数で上書き可は従来どおり)。

### Verified(再評価。モデル `claude-fable-5-2`。評価ケースは非公開)
- 差分ケース(陽性 7、陰性 5。合成ケースを含む)を各 1 回、境界のケース 2 本を各 3 回: 拒否・空応答なしに完走。陽性の検出は 5.1 と同等、陰性の誤検知なし(合成の陰性ケースに `ssrf` の所見なし)。
- 全体モード(実在の製品コード 5 コンポーネント × モデル 2 × 前提情報の有無 2 の 25 本。モデルを伏せた採点): 完走 25/25。退行の確認の組(秘密実体、判定の fail-open)は維持。5.1 が「捨てた候補」にしていた指摘のうち 2 種が、5.2 では要確認に残った(所見への格上げではない)。5.2 だけに出た新しい所見は 0 件。
- 5.1 は、DB のパスワードなどの実値をレポートに書くことがあったが、5.2 は伏せる傾向だった(採点者の記録)。
- 所要は、5.1 の約半分。出力の形の失敗(途中経過の文だけで終わる)は、自動の再実行で回復する範囲(5.1 と同程度)。
- multi-scan の runner(`run-3-llm.sh` 相当)を、環境変数 `LLM_SCAN_MODEL=claude-fable-5-2` で通し、ヘッダのモデル ID と保存の検査を確認した。
- 限界: ケース数・実行回数は小さく、方向の確認にとどまる。1 つの製品コードでの評価。前提情報(`SECURITY_REVIEW_CONTEXT.md`)を渡した場合の効果は一様でなく、特定の指摘(接続文字列のログ出力など)が消える場合があった。前提情報は、`rules/sut-context.template.md` の記述を見直したうえで使うこと(従来の注意のとおり、書いた事実はコードで確認される前提)。

### Previous(過去の評価の記録。現行の推奨ではない)
- 2.1.0 までの推奨は `claude-fable-5-1`(下の各版の Verified を参照)。

## [2.1.0] - 2026-11-09

後方互換(出力の節の構成・引数・allowed-tools は変えない)。ルールに SSRF の観点を足したので、評価ケースで再評価した(下の Verified)。

### Added
- `rules/org-specific.md`(対訳と、prompt に差し込む本文)に「サーバー側リクエスト偽造(SSRF)」を追加。送信側の HTTP・ネットワークのリクエスト(fetch、axios、got、requests、webhook・プロキシ・URL プレビュー、内部サービスの呼び出しなど)のうち、**宛先のホスト・ポート・スキームを呼び出し元が制御できるもの**(直接、または保存済みのデータ経由)、回避できる宛先の検査(解決前の文字列だけの検査、ブロックリスト、リダイレクト、Host / X-Forwarded-Host の信用)、そこから内部サービスやクラウドのメタデータに届くもの。カテゴリ識別子は `ssrf`(SKILL.md と README に追記)。
- **公式の除外 13(「SSRF vulnerabilities that only control the path. SSRF is only a concern if it can control the host or protocol.」)は維持**。固定された(サーバー設定の)ホストの後ろの**パスやクエリだけ**を制御できるものは報告しない。ただし、ホストまたはスキームを制御できる場合、または「パス」が固定ホストの外へ出られる場合(`//` で始まる値、`@` を含む値、パスの代わりに絶対 URL を受け付けるもの)は報告する。
- 公式 prompt には SSRF のカテゴリが無く、除外 13 があるだけだった。この追加は、新しい検出機能というより、**拾うもの(ホスト・スキームの制御)と拾わないもの(パスのみ)の境界を明示して、拾い漏れと過剰な指摘を減らす補強**。

### Verified
- モデル `claude-fable-5-1`、各 1 回の実行。評価ケースは非公開(合成ケースの作り方は評価リポジトリ側)。
- 合成ケース 2 本: 利用者指定の URL にそのまま fetch するもの(陽性)は `ssrf` を報告(公式のみでも報告した)。固定ホストの後ろのファイル名だけを選べるもの(陰性)は、所見にならず、捨てた候補として除外 13 に当たると説明された。
- 既存の評価ケース 11 本(差分スキャン): `ssrf` の誤検知なし。正解の所見は 9 本で同じ。境界のケース 2 本(所見 ↔ 要確認)は、過去の実行でも揺れていたもので、`ssrf` の語は出ておらず、原因は新ルールと断定できない(再実行はしていない)。
- 実在の製品コードの全体スキャン(3 パッケージ、旧ルールの結果と比較): `ssrf` の新しい所見は 0 件。送信リクエストの宛先は固定ホストで、パスのみの制御と判断され、除外 13 のとおり報告されなかった。所見・要確認の件数に小さな差があったが、実行間のぶれと区別していない。
- 未確認: 公式が見逃しやすい形(保存済み URL の後の取得、Host 系ヘッダ由来の送信先、webhook の登録先)での追加効果。

### Notes
- 認可マトリクス(BOLA/IDOR)は別 skill `llm-a2b-security-scan` の担当で、本 skill には足さない。「攻撃者はアプリを介さず API を直接呼ぶ」前提は、prompt を変えず、`rules/sut-context.template.md` の "API reachability" 行で宣言する(2.0.x で template に追記済み)。
- SSRF の SAST(`semgrep-security-scan`)は、候補のまま(未着手)。

## [2.0.2] - 2026-11-06

後方互換。**SKILL.md とルールは変えない**(判定は変わらないので、評価ケースでの再評価は要らない)。

### Added
- `save_report.py`:環境変数 `LLM_SCAN_SKILL_VERSION` があれば、Markdown の「## 1. ヘッダ」の節の末尾に「- skill の版: <値>」を **script が**追記する(multi-scan の統合サマリー Agent が「レポートに skill の版の数値が無い」と指摘したため。LLM に書かせると誤りうるので、決定的に入れる)。値は `^[A-Za-z0-9._+-]{1,64}$` に合うものだけ(合わなければ追記せず note を出す)。ヘッダに既にあれば足さない。未設定なら従来どおり(互換)。
- `examples/multi-scan/run-3-llm.sh`:`LLM_SCAN_SKILL_VERSION="$(git describe --tags --always --dirty)"` を渡す。`-dirty` が付けば、タグの版と作業ツリーが違う。

### Changed
- 製品のリポジトリに、ローカルのセッションメモ(`.claude/projects/.../memory/MEMORY.md`)が追跡されていたので、追跡をやめた(`.gitignore` は `.claude/projects/` 全体に広げた。ファイルは手元に残る。内容は 2026-03 の作業メモで、固有の情報は含まない)。

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
