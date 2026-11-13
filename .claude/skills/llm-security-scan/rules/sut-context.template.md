# SUT context(スキャン対象の前提情報)— テンプレート

スキャン対象リポジトリのルートに `SECURITY_REVIEW_CONTEXT.md` として置く(または skill 引数でパスを渡す)。
**人が書く、信頼できる前提情報**であり、レビュー時は "Repository Context Research" の入力として扱う。
旧版の自動検出(`detect_project_type.py`)の代替。書かれていない項目は推定しない。
以下の値はすべて記入例。対象に合わせて書き換える。

## 書き方の注意(重要)

1. **確認できた事実だけを書く。** 推測や、「たぶんそうだ」は書かない。確認できない項目は、書かない(書かれていない項目は、推定されず、コードから読めることだけで判断される)。
2. **事実の直後に、「ただし、〜を意味しない」の 1 文を足す(ガード文)。** 前提情報は、読む側が、その事実を**広く解釈して、関連する確認を省く**ことがある。例: 「秘密情報は Secret Manager で管理している」と書くと、「接続文字列やトークンはログに出ない」と読まれて、ログ出力の確認が省かれることがある。**その事実が意味しないこと**を、すぐ後ろに書く。
3. **受容済みのリスクは、最小限に。** 広く書くほど、その周辺の確認が省かれる。理由と範囲(どのエンドポイントか)を書く。
4. **実環境と違ったら、書き直す。** ここに書いた事実は、レビューの前提になる。古くなった記述は、結論を誤らせる。

---

## Components

| path | role | runtime | trust of input |
|---|---|---|---|
| `frontend/` | end-user web client (例: Vue 3) | browser | untrusted (client-side; no authz expected here) |
| `backend/` | API server / BFF (例: Fastify) | Node.js | untrusted HTTP from Internet via reverse proxy |
| `worker/` | internal analysis service (例: FastAPI) | Python | internal only (called by backend with a service key) |

## Trust boundaries and deployment facts

- TLS termination: (例) reverse proxy / CDN → app server (plain HTTP inside is expected)
- API reachability: (例) every backend endpoint is reachable directly without the frontend (A2B); UI-side restrictions, Origin/Referer checks and "the client never sends this value" are not authorization
- Identity: (例) OIDC provider + server-side session cookie; CSRF token header on state-changing requests
- Tenancy: (例) one DB per tenant, resolved from Host header; or shared DB with `tenant_id` column
  - (ガード文の例) ただし、1 つの DB に複数の会社・組織が入るかは別の話。会社・組織の境界の検査は、テナントの分離とは別に確認する
- Roles: (例) `admin` = customer-company administrator (own company only), `user`
- Internal service calls: (例) backend → worker over private network with a shared service key
  - (ガード文の例) ただし、共有鍵があることは、内部サービスの認可・入力の検査が不要であることを意味しない
- Secrets: (例) secret manager via managed identity; `.env.*.example` files contain placeholders only
  - (ガード文の例) ただし、秘密情報を secret manager で管理していることは、接続文字列・トークン・鍵がログやレスポンスに出力されないことを意味しない。ログ出力の確認は、通常どおり行う

## Sensitive data classes

- (例) health data, conversation transcripts, employee identifiers

## Known accepted risks (do not re-report)

- (例) `/health` is unauthenticated by design; returns no data
