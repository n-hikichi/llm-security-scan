# Upstream 追従記録

| 項目 | 値 |
|---|---|
| リポジトリ | https://github.com/anthropics/claude-code-security-review |
| コピー元パス | `.claude/commands/security-review.md` |
| コミット | `0c6a49f1fa56a1d472575da86a94dbc1edb78eda`(2026-02-11, Merge PR #55) |
| 取得日 | 2026-09-30 |
| sha256 | `dd1d451f909dbb8798f4a4de010c35e7dd9152f02bb2f7988442cdd138f29e39` |

## 配置

- `upstream/security-review.md` — 無改変の原本(差分確認用。編集禁止)
- `.claude/skills/llm-security-scan/references/upstream-security-review.md` — skill が参照する無改変コピー(`upstream/` と同一であること)

## 公式の拡張点(統合版の設計に使う)

- `docs/custom-security-scan-instructions.md` — 追加観点を "Data Exposure" カテゴリの後ろに追記する方式 → `rules/org-specific.md`
- `docs/custom-filtering-instructions.md` — 誤検知フィルタ指示の差し替え方式 → `rules/exclusions.md`

## 追従手順

1. upstream の最新ハッシュを取得し、`git diff <記録ハッシュ>..<最新> -- .claude/commands/security-review.md` を確認
2. 取り込む場合は `upstream/` を更新し、評価ケース(非公開の評価リポジトリ)で再評価する
3. 本表を更新

## Phase 1 動作確認(2026-09-30)

- 環境:Claude Code 2.1.285、公式 prompt を無改変のまま command として配置し、headless で実行(`claude -p`、claude-opus-5-5)
- 対象:scratchpad 上の最小リポジトリ(bare origin + feature ブランチで `pool.query` 文字列連結の SQLi を追加)
- 結果:`app.js:8` SQL Injection / High / confidence 9 を検出。無改変で実行可能 → **完了条件を満たす**

