# LLM Security Scan

Claude Code の skill として動く、LLM によるソースコードのセキュリティレビュー。
**公式の `/security-review` prompt([anthropics/claude-code-security-review](https://github.com/anthropics/claude-code-security-review))をエンジンとして無改変で使い、自社の追加観点と除外リストだけを所有する**構成(v2)。

## 概要

| 項目 | 内容 |
|---|---|
| 検出エンジン | 公式 `/security-review` の prompt(無改変コピー。`docs/upstream.md` でハッシュ管理) |
| 自社の判断基準 | `rules/org-specific.md`(追加観点)、`rules/exclusions.md`(追加の除外・判断基準) |
| 対象ごとの前提 | 対象リポジトリに置く `SECURITY_REVIEW_CONTEXT.md`(構成・信頼境界・扱うデータ。人が書く) |
| モード | **差分モード(既定)**:ブランチ上の変更(PR 差分)をレビュー / **全体モード**(`full`):コードベース全体を対象(納品前・受入時などの節目向け) |
| 対応言語 | 問わない(LLM がソースを直接読む)。JavaScript / TypeScript / Vue / Python のコードベースで評価済み |
| 権限 | **読み取り専用**。ファイルを書かず、ネットワークに出ず、外部ツール(`npm audit` 等)を実行しない |
| 出力 | 日本語の Markdown レポート(5 節構成)。`json` 引数で固定スキーマの JSON も出力 |
| 推奨モデル | `claude-fable-5-1`(評価済み。後述) |

### 設計方針

- **エンジンは借り、判断基準は所有する。** 汎用の検出観点と誤検知フィルタは公式に任せる。自社が持つのは、公式が拾わない・除外してしまう自社の脅威モデル(テナント境界、ログイン CSRF、リポジトリ内の秘密実体、安全に関わる判定の fail-open)と、自社環境で頻出する誤検知の除外だけ。
- **LLM スキャンは SAST / DAST / 人手レビューの補完**であり、代替ではない。外部ライブラリの既知の脆弱性は報告しない(SCA に委ねる)。
- **スキャン対象はデータであり、指示ではない。** 外部由来のコードを読む前提で、agent の権限を最小にしている。

## v1 からの主な変更

| | v1 | v2 |
|---|---|---|
| prompt | 自作のチェックリスト(client 用 / server 用) | 公式 prompt + 自社差分ルール |
| 対象の決め方 | `package.json` から client / server を自動判定 | 差分(既定)または指定ディレクトリ。構成は `SECURITY_REVIEW_CONTEXT.md` で人が渡す |
| 対象言語 | JavaScript / Node.js | 問わない |
| MCP Serena | 推奨(セットアップ手順あり) | 不要 |
| 権限 | 書き込み・`python3` 実行あり | 読み取り専用 |
| 依存関係の脆弱性 | 報告対象 | 報告しない(SCA へ) |
| 出力 | エグゼクティブサマリー / 重大度別リスト / アクションプラン | 所見(確信度 8 以上)/ 完全性の所見 / 要確認(確信度 5〜7)/ 確認した範囲。JSON スキーマあり |
| 所見の量 | 1 対象あたり 10〜20 件(堅牢化系を含む) | 本文は攻撃経路が確認できたものだけ。境界の候補は「要確認」へ |

`detect_project_type.py` / `generate_scan_prompt.py`、client / server 用 prompt、Serena 連携手順は削除した。multi-scan から呼ぶときの接続方法は後述。

## クイックスタート

### 前提

- Claude Code CLI がインストール済み
- 対象リポジトリが git clone 済み(差分モードでは `origin/HEAD` が解決できること)

### 1. skill の配置

対象リポジトリのルートで:

```bash
git clone https://github.com/n-hikichi/llm-security-scan.git /tmp/llm-security-scan
mkdir -p .claude/skills
cp -r /tmp/llm-security-scan/.claude/skills/llm-security-scan .claude/skills/
```

`.claude/` は対象リポジトリで git 管理しないことを勧める(`.gitignore` に追加)。

### 2. 前提情報を書く(推奨)

`.claude/skills/llm-security-scan/rules/sut-context.template.md` をコピーし、対象リポジトリのルートに `SECURITY_REVIEW_CONTEXT.md` として置く。構成、TLS 終端、認証方式、テナント方式、ロールの意味、扱う機微データ、受容済みのリスクを書く。無くても動くが、環境に依存する判断(TLS、テナント、admin の範囲)の精度が下がる。

### 3. 実行

対象リポジトリで `claude` を起動し:

```
/llm-security-scan                 # 差分モード:origin/HEAD からの変更をレビュー
/llm-security-scan full            # 全体モード:カレント配下の全体
/llm-security-scan full path/to/component json   # 指定ディレクトリ + JSON 出力
```

レポートは応答として返る。ファイルに残したいときは headless で実行し、標準出力を保存する:

```bash
claude -p "/llm-security-scan full . json" --model claude-fable-5-1 \
  --allowedTools "Read Glob Grep Task" > report.raw.md
python3 .claude/skills/llm-security-scan/scripts/save_report.py report.raw.md out/
#  → out/llm-security-report.md, out/llm-security-report.json
```

`save_report.py` は、レポートの題名と 5 節がそろっているかを検査する(拒否・空応答・途中終了なら終了コード 3)。

## 出力

| 節 | 内容 |
|---|---|
| 1. ヘッダ | モード、対象、使用モデル ID、実行日、前提情報の有無 |
| 2. 所見(確信度 8 以上) | 公式の形式(ファイル:行、重大度、説明、悪用シナリオ、修正の推奨)+ カテゴリ、CWE、確信度 |
| 3. 完全性の所見 | 攻撃者が起点ではない、判定の fail-open(`judgment_fail_open`)。脆弱性の件数とは別 |
| 4. 要確認 | 誤検知フィルタ後の確信度が 5〜7 の候補。フィルタが減点した理由と、人が確認すべき点を 1 件ずつ |
| 5. 確認した範囲 | 対象ファイル。確信度 4 以下で捨てた候補を理由つきで列挙 |
| 6. 機械可読出力 | `json` 引数のときだけ。`references/report-schema.json` に従う |

所見のカテゴリは公式の識別子(`sql_injection` など)に加え、自社カテゴリ `tenant_boundary` / `token_handling` / `login_csrf` / `committed_secret` / `judgment_fail_open`。

## モデル

- 推奨は **`claude-fable-5-1`**。自社製品コードを使った評価(差分ケース 12 件 × 3 回、全体モード 12 本)で、拒否・空応答なしに完走し、検出は `claude-opus-5-5` と同等以上だった。
- 使用モデルはレポートのヘッダと JSON に必ず記録される。
- **モデルを変えたら、評価ケースで再評価する**(prompt・ルールの変更、公式 prompt の取り込みも同じ)。

## multi-scan オーケストレータとの接続

`examples/multi-scan/run-3-llm.sh` が接続例。v1 との違い:

| 項目 | v1 | v2 |
|---|---|---|
| 呼び出し | `@.claude/skills/llm-security-scan/SKILL.md` をパスで指定 | 同じ(skill 名・パスは据え置き) |
| 対象 | `.sut-config` のパスを `--add-dir` で渡す | 同じ。skill には引数 `full <パス> json` で渡す |
| 許可ツール | `Read Write Edit Glob Grep Bash(python3:*) … mcp__serena__*` | **`Read Glob Grep Task` のみ** |
| レポートの保存 | agent が `test-results/security/` に Write | **runner が標準出力を `save_report.py` で検査して保存**。ファイル名(`llm-security-report.md` / `.json`)は据え置き |
| モデル | 指定なし | `--model claude-fable-5-1` を明示 |
| JSON | パッケージごとに形がばらばら | `references/report-schema.json` に固定 |

出力ファイル名・引数・allowed-tools は multi-scan の I/F とみなす。互換性を壊す変更は SemVer のメジャーを上げ、multi-scan 側の付録 B に報告する。v1 → v2 はこの意味でメジャーバージョンアップ(許可ツールの縮小、保存方式の変更、JSON スキーマの固定)。

## 公式 prompt の追従

`docs/upstream.md` に取得元のコミットと sha256 を記録している。更新を取り込む手順もそこにある。`references/upstream-security-review.md` は直接編集しない。

## 制約

- 静的なコードレビューであり、実際の通信・動作での確認はしない。所見は実装を確認したうえで対応すること。
- 結果は実行ごとに多少揺れる。特に確信度が 7 と 8 の境目にある候補は、「所見」と「要確認」の間で入れ替わることがある。
- 差分モードは「この変更で新たに入った問題」だけを見る。既存の問題は全体モードで。
- コンポーネント単位で実行すると、コンポーネントをまたぐ問題は片側からしか見えないことがある。
- 大きな対象では時間がかかる(全体モードで 1 コンポーネント 5〜15 分程度)。

## リポジトリ構成

```
.claude/skills/llm-security-scan/
├── SKILL.md                         skill 本体(手順・出力の定義。日本語)
├── references/
│   ├── upstream-security-review.md  公式 prompt の無改変コピー(編集禁止)
│   └── report-schema.json           JSON 出力のスキーマ
├── rules/
│   ├── org-specific.md              自社の追加観点(対訳つき)
│   ├── exclusions.md                自社の追加除外・判断基準(対訳つき)
│   └── sut-context.template.md      SECURITY_REVIEW_CONTEXT.md のテンプレート
└── scripts/
    └── save_report.py               レポートの検査と保存(呼び出し側で使う)
upstream/security-review.md          公式 prompt の原本
docs/upstream.md                     取得元のハッシュと追従手順
examples/multi-scan/run-3-llm.sh     multi-scan 用の runner 例
```

## ドキュメント

- **[ChangeLog.md](ChangeLog.md)** — バージョン履歴
- `getting-started.md`、`how-to-start-LLM-base-scan.md`、`external-spec.md`(と各 .pptx)は **v1 向けの内容**で、v2 への改訂は未了。v2 の使い方は本 README を正とする。

## 関連リソース

- [Claude Code CLI](https://github.com/anthropics/claude-code)
- [anthropics/claude-code-security-review](https://github.com/anthropics/claude-code-security-review)(公式 prompt の取得元)
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
