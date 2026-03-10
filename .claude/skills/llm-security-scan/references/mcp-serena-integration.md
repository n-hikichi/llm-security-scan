# MCP Serena 統合ガイド

このスキルは MCP Serena と統合することで、より効果的なセキュリティスキャンを実施できます。

## MCP Serena とは

MCP Serena は、IDE アシスタント向けの Model Context Protocol (MCP) サーバーで、
ソースコードの静的解析とシンボル情報の提供を行います。

## 統合のメリット

1. **効率的なコード探索**: Symbol Overview により、ファイル全体を読み込まずに構造を把握
2. **的確な脆弱性検出**: 関数やクラスの定義箇所を素早く特定
3. **依存関係の追跡**: import/require 文の解析により、依存関係を把握

## セットアップ手順

### 1. MCP Serena のインストール

```bash
# uvx を使用してインストール
pip install uv  # uv がインストールされていない場合

# Serena の MCP サーバーを追加
claude mcp add serena -- $HOME/.local/bin/uvx --from git+https://github.com/oraios/serena serena start-mcp-server --context ide-assistant --project $(pwd)
```

### 2. MCP サーバーの起動確認

```bash
# MCP サーバーの一覧を確認
claude mcp list

# 出力例:
# Name     Status   PID
# serena   running  12345
```

### 3. Claude Code CLI 内での確認

Claude Code CLI を起動後、以下のコマンドで MCP ツールが利用可能か確認:

```
> /mcp
```

利用可能な MCP ツールの一覧が表示されます。

### 4. Onboarding (初期化処理)

プロジェクトのソースコードを事前解析させることで、スキャンの精度が向上します:

```
> mcp serena 向けの onboarding 処理を行ってください
```

この処理により、Serena がプロジェクト全体のシンボル情報を構築します。

## セキュリティスキャンでの活用

MCP Serena が有効な場合、以下の機能を活用できます:

### Symbol Overview の取得

特定のファイルの構造を把握:

```
> src/auth/login.js の Symbol Overview を取得してください
```

### 関数定義の検索

特定の関数の実装箇所を検索:

```
> authenticateUser 関数の定義を検索してください
```

### 依存関係の分析

モジュールの import/require を追跡:

```
> jwt トークン関連のモジュールを使用しているファイルを検索してください
```

## トラブルシューティング

### MCP サーバーが起動しない

```bash
# プロセスを確認
ps aux | grep serena

# 必要に応じて再起動
claude mcp restart serena
```

### Onboarding が完了しない

大規模なプロジェクトの場合、解析に時間がかかることがあります。
以下のコマンドで進捗を確認:

```
> mcp serena の解析状況を確認してください
```

### Symbol Overview が取得できない

ファイルパスが正しいか確認してください。相対パスまたは絶対パスで指定できます。

## 参考リンク

- MCP Serena リポジトリ: https://github.com/oraios/serena
- Model Context Protocol: https://modelcontextprotocol.io/
