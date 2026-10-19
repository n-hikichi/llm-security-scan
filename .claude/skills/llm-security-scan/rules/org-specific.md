# 自社の追加観点

公式 prompt の "SECURITY CATEGORIES TO EXAMINE" の **Data Exposure カテゴリの直後**に差し込むカテゴリ。
ここに載せるのは「公式が拾わない、または除外してしまう、自社の脅威モデル」だけ。公式と重複する観点は書かない。
出典:旧 prompt set の差分分析と、自社製品コードでの評価(評価ケースと結果は非公開)。
対象ごとに変わる事実(ロールの意味、TLS 終端、テナント方式、扱うデータの種類)は、ここには書かず、対象リポジトリ側の `SECURITY_REVIEW_CONTEXT.md` に書く(`sut-context.template.md`)。

このファイルは 2 部構成。prompt に差し込むのは区切り線 `---` より後の「差し込む本文」だけ。本文は英語の公式 prompt に入るので英語で書く。
**本文を変えたら、下の対訳も合わせて直すこと。**

## 対訳(人が読むためのもの。prompt には入らない)

**テナント・会社の境界(マルチテナント SaaS)**
- user_id、company_id、dept_id、session_id をキーにしたクエリで、呼び出し元のテナント・会社の範囲による絞り込みがなく、テナント A の利用者がテナント B の行を読み書きできるもの
- 「admin」に会社・テナントをまたぐ無条件のアクセスを与える権限チェック。`SECURITY_REVIEW_CONTEXT.md` にテナント横断の特権ロールが明示されていない限り、admin は自分のテナント・会社の範囲に限られる管理者として扱う
- リクエスト間で共有される可変の状態(モジュールレベルの変数、シングルトンのインスタンスフィールド、user_id だけをキーにしたキャッシュ)が、別のリクエストや別のテナントのデータを返しうるもの。例外を握りつぶした結果、前のリクエストの結果が残ったまま返される経路を含む
- ネットワーク由来の値(Host、X-Forwarded-*、クライアント IP)を信用してテナントの解決や認可を行い、認証済みセッションとサーバー側で結び付けていないもの

**トークンの扱い**
- JWT や署名付きトークンを、署名を検証しない方法(`jwt.decode()` など)で読み、その中身を認証・認可に使うもの
- 資格情報、セッショントークン、個人データをブラウザの永続ストレージ(localStorage、sessionStorage、IndexedDB)に保存するもの

**ログイン・ID 連携のフロー**
- OIDC / OAuth のコールバックが、ログインを開始したブラウザと結び付いていないもの(相関 Cookie などを login state と照合していない)。攻撃者の未使用の code と state を使ったログイン CSRF・セッション固定が成立する
- コールバック時に選ばれるリダイレクト URI やテナントを、ログイン開始時に記録した値と照合していないもの

**リポジトリに入った秘密実体**
- 秘密鍵、秘密鍵付きの証明書、実際の値が入った `.env`、パスワード入りの接続文字列や URL、サービスの資格情報がリポジトリに commit されているもの。自己署名や「開発用」であっても報告する(履歴は残り、リポジトリは共有されうるため)
- このカテゴリは追跡されている**すべてのファイル**が対象。テストコード、フィクスチャ、スクリプト、文書、コメントアウトされた行を含む。公式の除外 2・11・16(ディスク上の秘密、テスト専用ファイル、文書ファイル)はこのカテゴリには適用しない
- 秘密が未使用・期限切れ・コメントアウト済み・攻撃経路が示せない、という理由で重大度や確信度を下げない。所見は「秘密実体が存在すること」そのもの。確信度は「実在する秘密実体か(プレースホルダではないか)」で付ける。重大度は最低 Medium。ローカル以外のホスト(データベース、クラウドサービス、外部 API)の資格情報は High

**安全に関わる判定の完全性(人に関する健康・安全・適合性の判定を出力するサービス)**
- 対象にそのようなサービスが含まれることは `SECURITY_REVIEW_CONTEXT.md` の "Sensitive data classes" や役割欄で示す。含まれなければこのカテゴリは出番がない
- 判定の処理で、上流の失敗(LLM 呼び出し、DB 参照、パースエラー、データ欠落)が既定値・空値・「正常」の値に置き換えられ、リクエストが成功として返るもの。高リスクの対象が低リスクと報告されうる
- これらは別カテゴリ `judgment_fail_open` として報告する。攻撃者が起こすものではなく完全性の所見であり、脆弱性の件数とは別に数える

## 差し込む本文

---

**Tenant / Company Boundary (multi-tenant SaaS):**
- Queries keyed by user_id, company_id, dept_id, or session_id that do not also constrain by the caller's tenant/company scope, letting a caller in tenant A read or modify rows of tenant B
- Role checks that grant an "admin" unconditional access across companies or tenants. Unless SECURITY_REVIEW_CONTEXT.md explicitly declares a cross-tenant super-user role, treat an admin as scoped to its own tenant/company
- Mutable state shared across requests (module-level or singleton instance fields, caches keyed only by user_id) that can return another request's or another tenant's data — including fail-open paths where a caught exception leaves a previous request's result in place and returns it
- Tenant resolution or authorization that trusts network-derived values (Host, X-Forwarded-*, client IP) without a server-side binding to the authenticated session

**Token Handling:**
- Reading a JWT or signed token with a non-verifying decode (e.g. `jwt.decode()` without signature verification) and using its claims for authentication or authorization
- Storing credentials, session tokens, or personal data in browser persistent storage (localStorage, sessionStorage, IndexedDB) where any XSS or shared device exposes them

**Login / Federation Flows:**
- OIDC / OAuth callback handlers that do not bind the callback to the browser that started the login (no correlation cookie or equivalent compared against the login state), enabling login CSRF / session fixation with an attacker's unconsumed code+state
- Redirect URI or tenant selected at callback time that is not checked against the value recorded when the login started

**Committed Secret Material:**
- Private keys, certificates with private keys, `.env` files with real values, connection strings or URLs with embedded passwords, or service credentials committed to the repository — report these even when the key is self-signed or "for development", since repository history is retained and the repository may be shared or cloned
- This category applies to EVERY tracked file: test code, fixtures, scripts, documentation, and commented-out lines included. HARD EXCLUSIONS 2, 11 and 16 (secrets on disk, test-only files, documentation files) do NOT apply to this category
- Do not lower severity or confidence for this category because the secret is unused, expired, commented out, or has no demonstrated attack path. The finding is the presence of the secret material itself: confidence reflects whether it is real secret material (not a placeholder), and severity is at least Medium; credentials for a non-local host (database, cloud service, third-party API) are High

**Safety-Critical Judgment Integrity (services whose output is a health, safety, or eligibility judgment about a person):**
- Applies when SECURITY_REVIEW_CONTEXT.md (component roles or "Sensitive data classes") shows that the target produces such judgments; otherwise this category has nothing to match
- Code paths in that judgment logic where an upstream failure (LLM call, DB lookup, parse error, missing data) is replaced by a default, empty, or "normal" value and the request still returns a success response, so that a high-risk case can be reported as low-risk
- Report these as a separate category `judgment_fail_open`; they are integrity findings, not attacker-triggered exploits, and are tracked separately from the main vulnerability count
