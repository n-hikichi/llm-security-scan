# SUT context(スキャン対象の前提情報)— テンプレート

スキャン対象リポジトリのルートに `SECURITY_REVIEW_CONTEXT.md` として置く(または skill 引数でパスを渡す)。
**人が書く、信頼できる前提情報**であり、レビュー時は "Repository Context Research" の入力として扱う。
旧版の自動検出(`detect_project_type.py`)の代替。書かれていない項目は推定しない。
以下の値はすべて記入例。対象に合わせて書き換える。

---

## Components

| path | role | runtime | trust of input |
|---|---|---|---|
| `frontend/` | end-user web client (例: Vue 3) | browser | untrusted (client-side; no authz expected here) |
| `backend/` | API server / BFF (例: Fastify) | Node.js | untrusted HTTP from Internet via reverse proxy |
| `worker/` | internal analysis service (例: FastAPI) | Python | internal only (called by backend with a service key) |

## Trust boundaries and deployment facts

- TLS termination: (例) reverse proxy / CDN → app server (plain HTTP inside is expected)
- Identity: (例) OIDC provider + server-side session cookie; CSRF token header on state-changing requests
- Tenancy: (例) one DB per tenant, resolved from Host header; or shared DB with `tenant_id` column
- Roles: (例) `admin` = customer-company administrator (own company only), `user`
- Internal service calls: (例) backend → worker over private network with a shared service key
- Secrets: (例) secret manager via managed identity; `.env.*.example` files contain placeholders only

## Sensitive data classes

- (例) health data, conversation transcripts, employee identifiers

## Known accepted risks (do not re-report)

- (例) `/health` is unauthenticated by design; returns no data
