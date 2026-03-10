# LLM Security Scan

Claude AI を活用した JavaScript/Node.js プロジェクト向けの包括的なセキュリティスキャンツール。

## 概要

LLM Security Scan は、Claude AI の高度な言語理解能力を活用して、JavaScript/Node.js プロジェクトの脆弱性を自動検出するセキュリティスキャンスキルです。従来のルールベースのセキュリティツールとは異なり、文脈を理解した分析により誤検知を削減し、より実用的なセキュリティ提案を提供します。

## 主な特徴

- **AI駆動の分析** - Claude AI による文脈を理解したセキュリティ分析
- **自動プロジェクト判定** - `package.json` から JavaScript/Vue.js/Express.js などを自動認識
- **包括的なチェック** - XSS、SQL インジェクション、認証・認可、依存関係脆弱性など
- **MCP Serena 統合** - コードベースの効率的な探索と分析
- **詳細なレポート生成** - 重大度別の脆弱性リスト、修正提案、コード例付き

## 対応プロジェクト

### v1.0.0 対応

| 言語 | フレームワーク | プロジェクト型 |
|------|-------------|-------------|
| **JavaScript** | Vue.js, React, Angular | クライアント / サーバー / ハイブリッド |
| **TypeScript** | Next.js, Nuxt.js, Remix | クライアント / サーバー / ハイブリッド |
| **Node.js** | Express.js, NestJS, Koa, Fastify | サーバー |

### 今後の拡張予定

- Python（Django, Flask）
- Java（Spring, Jakarta）
- Go

## クイックスタート

### 1. 前提条件

- Claude Code CLI がインストール済み
- 対象プロジェクトが git clone 済み
- uv がインストール可能

### 2. セットアップ（3ステップ）

**ステップ 1: uv のインストール**

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**ステップ 2: MCP Serena のセットアップ**

スキャン対象ディレクトリで以下を実行：

```bash
claude mcp add serena -- uvx --from git+https://github.com/oraios/serena \
  serena-mcp-server --context ide-assistant --project $(pwd) \
  --enable-webdashboard=false
```

その後、Claude CLI を再起動

**ステップ 3: Skill のインストール**

```bash
# GitHub Releases から llm-security-scan.zip をダウンロード
curl -L https://github.com/n-hikichi/llm-security-scan/releases/latest/download/llm-security-scan.zip \
  -o llm-security-scan.zip

# 展開
unzip llm-security-scan.zip

# Skill が認識されたか確認
> skill
```

### 3. スキャン実行

スキャン対象ディレクトリで Claude CLI を起動：

```bash
cd /path/to/your/project
claude
```

Claude に以下を指示：

```
セキュリティスキャンを実行して
```

スキャン完了後（約10分）、以下で結果をファイルに保存できます：

```
得られたレポートをファイルに保存して。
```

## 検出される脆弱性

### クライアントサイド（Vue.js/React など）

- **認証・認可** - トークン管理、ストレージセキュリティ
- **XSS 対策** - 入力エスケープ、DOM 操作
- **API 通信** - HTTPS、認証ヘッダー
- **依存関係** - 既知の脆弱性、パッケージバージョン
- **データ保護** - localStorage/sessionStorage の使用

### サーバーサイド（Express.js/NestJS など）

- **認証・認可** - JWT、パスワードハッシュ、セッション管理
- **データベース** - SQL インジェクション、接続セキュリティ
- **入力検証** - サニタイゼーション、型チェック
- **CORS とヘッダー** - セキュリティヘッダー設定
- **エラーハンドリング** - 情報漏洩対策

## ドキュメント

- **[getting-started.md](getting-started.md)** - 初心者向けガイド（スライド形式）
- **[how-to-start-LLM-base-scan.md](how-to-start-LLM-base-scan.md)** - 詳細なセットアップガイド
- **[ChangeLog.md](ChangeLog.md)** - バージョン履歴

## よくある質問

**Q: スキャン結果をファイルに保存できますか？**

A: はい。スキャン完了後に「レポートをファイルに保存して」と指示すると Markdown ファイルが生成されます。

**Q: 同じプロジェクトを複数回スキャンできますか？**

A: はい。何度でも実行可能です。2回目以降はスキャンが高速化されます。

**Q: Python/Java プロジェクトもスキャンできますか？**

A: 現在は JavaScript/Node.js が公式対応です。他言語への拡張は技術的に実現可能で、今後対応予定です。

**Q: スキャン結果の信頼性は？**

A: Claude AI による分析なので、最終確認はチーム内で行うことをお勧めします。

## トラブルシューティング

### "skill が認識されない"

Claude CLI を再起動してみてください。

### "MCP Serena の初期化が遅い"

初回のみ時間がかかります（5-10 分）。完了まで待ってください。

### "Authentication エラー"

Claude Code CLI の認証を確認してください：

```bash
gh auth status
```

## 技術仕様

- **実装言語** - Python（検出スクリプト）、Markdown（セキュリティプロンプト）
- **AI エンジン** - Claude API
- **コード分析** - MCP Serena（オプション）
- **出力形式** - Markdown（ターミナル表示 + ファイル保存可能）

## ライセンス

このプロジェクトはオープンソースです。

## サポート

- GitHub Issues で質問・報告してください
- ドキュメントの改善提案も歓迎します

## 関連リソース

- [Claude Code CLI](https://github.com/anthropics/claude-code)
- [MCP Serena](https://github.com/oraios/serena)
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)

---

**さあ、セキュアな開発を始めましょう！**
