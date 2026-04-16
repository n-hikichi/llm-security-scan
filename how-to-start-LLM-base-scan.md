# インストールと security scan(LLM base)の方法

**日付:** 2025年10月27日 15:58

## 条件

- Claude code CLI の利用を前提としている

## 概要

- Claude code の agent-skill[2] という機能を利用している
- この機能を利用して実装している

## 1. MCP Serena のセットアップ

### a. 事前に uv のインストール

uv は スキャン対象ディレクトリ で serena をインストールするために必要です。

```bash
$ curl -LsSf https://astral.sh/uv/install.sh | sh
```

### b. スキャン対象ディレクトリ で、serena をインストールして起動

次のコマンドにより、serena をインストールしてserver を起動する。（従ってこの段階で security 対象の repository は展開しておく必要がある。）

```bash
$ claude mcp add serena -- uvx --from git+https://github.com/oraios/serena \
  serena start-mcp-server --context ide-assistant --project $(pwd) \
  --open-web-dashboard false
```

### c. 確認コマンド

```bash
$ claude mcp list
```

または

```
> /mcp
```

## 2. Serena で prescan(onboarding[1]) する

### a. 具体的には

スキャン対象ディレクトリ で、claude を起動し、次の onboarding 処理を行う。時間を要する。

```
> mcp serena の onboarding 処理を行って。
```

### b. Context を消費しているので

claude code cli は再起動しておく。

## 3. Skill のインストール

### a. GitHub Releases から llm-security-scan.zip をダウンロードする

以下のリンクから最新の llm-security-scan.zip をダウンロードしてください：

https://github.com/n-hikichi/llm-security-scan/releases/latest

### b. スキャン対象ディレクトリ（claude 起動ディレクトリ） に展開する

### c. .claude/skills/ に llm-scan.zip が展開されていることを確認する

Claude へ次の指示で、llm-security-scan という skill が認識されていることを確認する。認識されていない場合は、再起動して、もう一度確認する。

```
> skill
```

英語で表示されていて、日本語で確認したい場合は、次の prompt を与える。

```
> 日本語で再提示して
```

## 4. LLM base の security scan の実行（登録した skill の起動）

### a. Claude へ次の指示で、security scan を開始する

あるいは選択肢を促された場合は、それに対応して指定する（例: "1." で進めて等）。時間を要する（10分近く?）。

```
> セキュリティスキャンを実行して
```

### b. npm audit の実行許可確認

"npm audit" の実行許可確認が発生した場合は、ここでは実行しない。（別フェーズで実行するので）

次のような選択肢が提示された場合, "1." と "2." の作業をするように指示して（例: >"1." と "2." の両方を進めて）

#### npm audit の実行を避けたい場合

以下の方法でレビューを続けられます:

1. package.json の目視確認のみでレポート作成
2. コードベースの静的解析に集中
3. ユーザーに手動で npm audit を実行してもらう

### c. セキュリティレポートが表示されたら

必要に応じて保存する。例えば、次のような prompt で。

```
> 得られたレポートをファイルに保存して。
```

---

## 注釈

### [1] MCP Serena での「onboarding作業」とは

プロジェクトやリポジトリを初めて Serena MCP で扱う際に行われる、初期理解・構造分析・インデックス生成・メモリ（知識ベース）作成など一連の初期化プロセス

### [2] Claude における agent-skill とは

Claude におけるサブタスクを実行する仕組み。context を消費せず、このサブタスク内で生成 AI でのタスクが自立的に動作する。Python/Javascript などのコードの実行も可能。実行空間は Anthropic の cloud 環境

### [3] スキャン対象の自動判定仕組み

**cwd（カレントディレクトリ）から探索する方式：**

1. **スキャンの起点**: ユーザーが `claude` コマンドを実行したディレクトリが起点
2. **プロジェクト検出**: そのディレクトリ（または上位ディレクトリ）から `package.json` を検索
3. **トップレベル判定**: `package.json` が見つかった場所をプロジェクトのトップレベルと判定
4. **プロジェクト型判定**: package.json の dependencies を解析して、以下を自動判定
   - 言語: JavaScript / TypeScript
   - フレームワーク: Vue.js / React / Express.js / Next.js など
   - 型: クライアントサイド / サーバーサイド / ハイブリッド
5. **スキャン実行**: 判定結果に応じた適切なセキュリティチェックリストを適用

**つまり、ユーザーが対象ディレクトリで Claude を起動すれば、スキャン対象が自動で決まる**という仕組み。

---

# 付録 A 生成 AI know how - ハルシネーションの可能性

**日付:** 2025年10月28日 13:08

## Claude の Agent-skill でのハルシネーション発生例

Claude の Agent-skill で、次のような状況でハルシネーションが発生した。

Skill の知識として、次はこのような security scan を推奨と記述したが、それも実行してしまった。

- 依存環境を scan する npm audit が有効

### 対策

⇒推奨環境の記述自体を削除

---

# 付録 B Claudeのインストール方法

**日付:** 2025年11月14日 11:46

## Ubuntu への install 例, claude code CLI

Ubuntu の場合、binary version がお勧め。

- Javascript 版もあるが、Javascript の target である場合、conflict する可能性を排除したいため

### claude/binary version の install に関して

claude/binary version の install に関して検索した。生成 AI 検索リンクと コマンド例を次に示す。これを参考にインストールする。

- https://www.perplexity.ai/search/claude-binary-version-noinsta-2yfMkxYgTW.PeLQ5bHntZg#0

```bash
$ curl -fsSL https://claude.ai/install.sh | bash
```

## Claude code CLI の認証（最初に利用する場合）

基本的に次のような手順。ここで "b." の browser と "c." の browser が同じものを用いるのが良さそう。

Chromium を install すると、認証ステップが楽。長い URL を chromium で open するが `chromium '長い URL'` という script file を作成すると、うまくいく。

### a. Chromium を install する

### b. Claude を起動すると、最初に認証するための URL が表示される

その URL をアクセスすると、email が届く。

- i. その URL をアクセスすると認証用の長い token が得られる

### c. Email には、認証用 token を生成する URL が含まれている

- i. 生成 URL を click すると、長い token が得られる
- ii. その長い token を、Claude code CLI 側に paste する

### d. 認証の時、普通は email を参照しないで進められる

## 付録 claude code の利用状況確認 command, ccusage

Ccusage を install しておくと、利用状況が確認出来ます。

使い過ぎると、精度の低いモデルに自動的に切り替わったりして、精度が下がることがあります。

次の URL を参考に ccusage を install する。

- https://zenn.dev/ryoppippi/articles/6c9a8fe6629cd6

---

# 付録 C 実行例

**日付:** 2025年11月14日 12:04

## サンプル実行例

実際にここにある "LLM base scan, LLM 起動"を、herensme-sv に対して適用した例を示す。

### 1. "付録 B Claude のインストール" セッションに従う

claude code CLI を install する

### 2. テスト対象の heresme-sv を git clone(Download)する

download する例

```bash
$ gh repo clone MicrosSoftwareInc/heresme-sv
```

### 3. Claude code CLI の動作確認

source code の README.md がある場所で claude を起動する。

初回 claude 起動時、最後に示す screen shot のような browser が起動されるので、認証する。

その後の認証のknow how は "付録B. Claudeの..." を参照のこと。

### 4. llm-security-scan.zip をダウンロードして展開する

GitHub Releases から最新版をダウンロード：

```bash
$ curl -L https://github.com/n-hikichi/llm-security-scan/releases/latest/download/llm-security-scan.zip -o llm-security-scan.zip
$ unzip llm-security-scan.zip
```

または、ブラウザで以下のリンクから直接ダウンロード：
https://github.com/n-hikichi/llm-security-scan/releases/latest

ダウンロード後、repository のルートディレクトリで展開します：

```bash
$ unzip llm-security-scan.zip
```

- `.claude/skills/llm-security-scan/` に展開されていることを確認する

### 5. これ以降は進める

"LLM base scan の自動..." セクションに従って、進める。

- Security scan 本体は、10分近くかかる

### サンプル実行スクリーンショット

（Claude Login ページのスクリーンショット）

---

# 付録 D LLM ポータビリティと柔軟性

**日付:** 2026年3月10日

## LLM架構の多様性

本ツール「llm-security-scan」は、現在 **Claude AI** を LLM エンジンとして実装していますが、その設計上の特性から、**他の大規模言語モデル (LLM) への移植は技術的に容易** です。

## 現在の実装（Claude ベース）

```
Claude Code CLI
    ↓
Agent-Skill (Python実行環境)
    ↓
プロジェクト分析・脆弱性検出
    ↓
セキュリティレポート生成
```

## 他の LLM への移植可能性

### a. 技術的な理由

1. **Agent-Skill の独立性**
   - Agent-Skill は Anthropic クラウド環境で実行される独立した Python 実行空間
   - LLM エンジンの選択が本質的に分離されている
   - 別の LLM への接続は、API 呼び出し部分の置き換えで対応可能

2. **プロンプト設計の汎用性**
   - セキュリティチェックリスト（cli-security-prompt.md、sv-security-prompt.md）
   - 大多数の先進 LLM（Claude、GPT-4、Codex など）で同等に機能
   - 言語モデルの能力レベルが近い場合、プロンプトの再調整で対応可能

### b. 移植可能な LLM の例

#### OpenAI Codex（OpenCode 経由）

```bash
# 現在（Claude ベース）
claude mcp add serena -- uvx --from git+https://github.com/oraios/serena ...

# 移植例（Codex ベース）
opencode mcp add serena -- ...
# または直接 OpenAI API を利用
```

- **適性**: 高い。Codex は同等以上のコード理解能力を持つ
- **実装工数**: 中程度（API キー管理、エラーハンドリング）

#### Google Gemini

```python
# API 呼び出しの置き換え例
from anthropic import Anthropic  # 現在
# ↓
import google.generativeai as genai  # Gemini への置き換え
```

- **適性**: 中程度。マルチモーダル対応により潜在的に有利
- **実装工数**: 中程度

#### Meta Llama（オンプレミス）

- **適性**: 中程度。十分な能力があるが、セキュリティ分析の専門性では劣る可能性
- **実装工数**: 高い（インフラ構築）

### c. 一般的な移植手順

1. **Agent-Skill 内の LLM API 置き換え**
   ```python
   # 現在の実装
   from anthropic import Anthropic
   client = Anthropic(api_key=...)

   # 新しい LLM への置き換え
   import openai  # または別のプロバイダ
   client = openai.OpenAI(api_key=...)
   ```

2. **API インターフェースの統一化**
   - リクエスト形式の標準化（roles, content など）
   - エラーハンドリングの一般化

3. **プロンプトの微調整**
   - LLM ごとの得意な指示形式への最適化
   - 例：Claude は詳細なシステムプロンプトに強い傾向

4. **テストと検証**
   - 複数のサンプルプロジェクトでのスキャン実施
   - 出力品質と検出率の比較

## 今後の拡張方向

- **マルチ LLM サポート**: ユーザーが LLM を選択できる仕組み
- **LLM 比較モード**: 複数の LLM でスキャンし、結果を比較
- **ハイブリッド戦略**: 分析フェーズごとに最適な LLM を選択

## 設計上の考慮

このツールが LLM ポータブルになっている理由：

1. **プロンプトベースの設計** - 硬くコード化された検査ルールではなく、LLM の指示理解力に依存
2. **API 中立的な構造** - 各 LLM の API の差異が吸収される層がある
3. **Skill 機構の独立性** - Claude Code CLI から疎結合されている

逆に、非常に特定の LLM 機能（例：Claude の vision capabilities など）に依存する場合は移植難度が上がります。

