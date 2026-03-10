# LLM Security Scan へようこそ
## 初心者向けガイド

---

# 目次

- LLM Security Scan とは
- 従来のセキュリティスキャンとの違い
- 必要な準備
- セットアップ手順（5分でできる）
- 実行フロー
- 期待される成果物
- Q&A

---

# LLM Security Scan とは

**LLM Security Scan** = Claude AI を活用したセキュリティスキャンツール

## 特徴
- **プロジェクト型の自動判断** - リポジトリ構造から JavaScript/Vue.js/Express.js を自動認識
- **生成AI駆動の分析** - ルールベースではなく、Claude の言語理解能力で文脈を考慮した検出
- **MCP Serena との連携** - コードベースのディープな分析が可能
- **入出力が明確** - 入力：リポジトリ、出力：詳細レポート（ターミナル表示 + ファイル保存可能）

---

# 従来のセキュリティスキャンとの違い

| 項目 | 従来のツール | LLM Security Scan |
|------|------------|------------------|
| 分析方式 | ルールベース | AI ベース（Claude） |
| 検出能力 | パターンマッチング | 文脈を理解した分析 |
| 誤検知 | 多い | 少ない |
| カスタマイズ | 難しい | Claude で調整可能 |
| 学習時間 | 短い | 中程度（初期セットアップ） |

---

# 必要な準備

## 前提条件
- Claude Code CLI がインストール済み
- 対象プロジェクトが git clone 済み
- uv（Python パッケージマネージャ）がインストール可能

## 所要時間
- セットアップ：**約 15-20 分**
- 初回スキャン：**約 10 分**（プロジェクト規模による）
- 2 回目以降：**約 5-10 分**

---

# セットアップ手順（ステップ 1/3）

## ステップ 1: uv をインストール

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

※ 一度だけ実行すればOK

---

# セットアップ手順（ステップ 2/3）

## ステップ 2: MCP Serena をセットアップ

スキャン対象ディレクトリで以下を実行：

```bash
claude mcp add serena -- uvx --from git+https://github.com/oraios/serena \
  serena-mcp-server --context ide-assistant --project $(pwd) \
  --enable-webdashboard=false
```

その後、Claude CLI を再起動

---

# セットアップ手順（ステップ 3/3）

## ステップ 3: Skill をインストール

1. GitHub Releases から `llm-security-scan.zip` をダウンロード
   ```bash
   curl -L https://github.com/n-hikichi/llm-security-scan/releases/latest/download/llm-security-scan.zip \
     -o llm-security-scan.zip
   ```

2. 展開する
   ```bash
   unzip llm-security-scan.zip
   ```

3. Claude Code に skill が認識されたか確認
   ```
   > skill
   ```

---

# 実行フロー

## スキャン開始から結果取得まで

```
1. Claude CLI 起動（プロジェクトディレクトリで）
   ↓
2. "セキュリティスキャンを実行して" と指示
   ↓
3. MCP Serena が初期化（初回のみ）
   ↓
4. Claude AI がコードを分析
   ↓
5. セキュリティレポート生成
   ↓
6. 結果をファイルに保存（オプション）
```

⏱️ **所要時間：約 10 分**

---

# スキャンで検出される項目

## セキュリティ脆弱性
- ✅ XSS（クロスサイトスクリプティング）
- ✅ SQL インジェクション
- ✅ 認証・認可の問題
- ✅ 依存関係の脆弱性
- ✅ 暗号化関連の問題

## コード品質
- ✅ セキュリティアンチパターン
- ✅ 危険な関数の使用
- ✅ 設定ファイルの問題

---

# 入力と出力の流れ

## 入力（何をスキャンするか）

```
Git リポジトリ（ローカルで展開済み）
  ↓
LLM Security Scan が自動判断
  ├─ package.json で JavaScript/Node.js を検出
  ├─ Vue.js/React/Express.js のプレームワークを判断
  └─ プロジェクト構造から対応言語を認識
```

**自動判断：** リポジトリから言語・フレームワークを自動判定

---

# 出力と結果の取得方法

## 出力（スキャン結果をどこで見るか）

| 出力先 | 用途 | 操作 |
|------|------|------|
| **ターミナル（Claude CLI）** | リアルタイム確認 | スキャン実行中に自動表示 |
| **ファイル保存** | 記録・共有・監視 | `> レポートをファイルに保存して` で Markdown ファイル生成 |

## 例：出力ファイル
```
security-report-2026-03-10.md
```

---

# 期待される成果物

## スキャン完了後、以下を得られます

### セキュリティレポート
```
- 検出された脆弱性リスト
- 重大度別の分類（Critical / High / Medium / Low）
- 具体的な修正方法の提案
- 影響範囲の説明
```

### ファイルに保存
```bash
> 得られたレポートをファイルに保存して。
```

---

# 対応言語とプロジェクト型

## 公式対応

| 言語 | フレームワーク | サポート |
|------|-------------|---------|
| **JavaScript** | Vue.js, React, Express.js | ✅ 完全対応 |
| **TypeScript** | Next.js, Nuxt.js | ✅ 完全対応 |
| **Node.js** | NestJS, Koa, Fastify | ✅ 完全対応 |

## 拡張可能性

| 言語 | 対応可能性 |
|------|---------|
| **Python** | ⚠️ 現在は未対応（拡張検討中） |
| **Java** | ⚠️ 現在は未対応（拡張検討中） |
| **Go** | ⚠️ 現在は未対応（拡張検討中） |
| **その他言語** | Claude AI の分析能力で対応可能（カスタム実装） |

**注：** 他の言語を使用している場合は、GitHub Issues で対応希望を報告してください

---

# よくある質問（Q&A）

### Q1: スキャン中、npm audit の実行を聞かれた場合？
**A:** 別フェーズで実行するため「実行しない」を選択

### Q2: スキャン結果の信頼性は？
**A:** Claude AI による分析なので、最終確認はチーム内で行うことをお勧め

### Q3: 同じプロジェクトを再スキャンできる？
**A:** はい、何回でも実行可能（2回目以降は高速化）

### Q4: スキャン結果をテキストファイルに保存できる？
**A:** はい、スキャン完了後に「レポートをファイルに保存して」と指示

### Q5: Python/Java プロジェクトもスキャンできる？
**A:** 現在は JavaScript/Node.js が公式対応。他言語は技術的に検討中

### Q6: 出力結果はどこで見られる？
**A:** 2つの方法
  - リアルタイム：Claude CLI のターミナル画面
  - 保存：Markdown ファイルとして生成・保存可能

---

# トラブルシューティング

## よくある問題と対処法

### 問題 1: "skill が認識されない"
**対処法：** Claude CLI を再起動してみる

### 問題 2: "MCP Serena の初期化が遅い"
**対処法：** 初回のみ時間がかかります（5-10 分）。完了まで待つ

### 問題 3: "Authentication エラー"
**対処法：** Claude Code CLI の認証を確認
```bash
gh auth status
```

---

# 次のステップ

## スキャン後の活動

1. **レポート確認**
   - 検出された脆弱性を確認
   - 優先度を決定

2. **修正計画**
   - チーム内で修正方針を検討
   - スケジュール作成

3. **修正実施**
   - 脆弱性を修正
   - 修正後に再スキャン（確認用）

4. **運用体制**
   - 定期的なスキャン（週 1 回など）
   - CI/CD パイプライン組み込みも可能

---

# まとめ

## LLM Security Scan の利点

✅ セットアップが簡単（15-20 分）
✅ AI による高度な分析
✅ カスタマイズ可能な結果
✅ 継続的なセキュリティ向上
✅ コスト効率的

---

# リソース

## 詳細情報
- 📖 [詳細ガイド](https://github.com/n-hikichi/llm-security-scan/blob/main/how-to-start-LLM-base-scan.md)
- 🔗 [GitHub リポジトリ](https://github.com/n-hikichi/llm-security-scan)
- 📝 [ChangeLog](https://github.com/n-hikichi/llm-security-scan/blob/main/ChangeLog.md)

## サポート
- GitHub Issues で質問・報告可能
- Claude Code CLI `/help` コマンドで基本情報確認可能

---

# ご質問はありませんか？

**さあ、セキュアな開発を始めましょう！**

