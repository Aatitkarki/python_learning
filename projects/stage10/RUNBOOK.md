# Local deployment and recovery answer

Run from the repository root. This is a local teaching stack. The API and database ports bind to loopback. A real deployment additionally needs identity-provider integration, HTTPS/reverse proxy, durable shared rate limits, release locks, monitoring, access reviews, and tested migrations.

## Prepare and start

```bash
python tools/create_local_env.py
# Inspect .env privately; do not paste credentials into a report.
docker compose config --quiet
docker compose up --build -d
docker compose ps
curl --fail http://127.0.0.1:8000/ready
```

If your installation uses a standalone Compose executable, use `docker-compose` instead of `docker compose`. Install/start a Docker engine first; a CLI binary alone is insufficient. The credential helper refuses to replace an existing `.env`.

Open `http://127.0.0.1:8000/docs` to inspect the API. The authentication header is `Authorization: Bearer <tenant-key>`. Use the tenant A key from your own `.env`. The notebook/API tests demonstrate requests without exposing a real credential.

For a local Python API instead of containers:

```bash
set -a
source .env
set +a
python -m uvicorn projects.api:app --host 127.0.0.1 --port 8000
```

The default local database is `work/course.db`. To use the Compose database from local Python, set DATABASE_URL as in INTEGRATIONS.md. The seed fixtures are loaded only when `COURSE_SEED=1`.

## Check persistence and safe failures

Create a record, restart the API with `docker compose restart api`, and confirm the same count/total. A missing or invalid credential should return 401; invalid request shape 422; unauthorized/missing financial periods 404; per-process quota exhaustion 429. `/health` is liveness; `/ready` checks database access.

Stop the database in this disposable lab with `docker compose stop database`, verify `/ready` returns 503, and record behavior of data endpoints. Restart with `docker compose start database`. The API converts SQLite/PostgreSQL database exceptions to a generic 503 without returning internal paths or connection details. Verify timeout behavior separately; a health response alone does not prove every operation is bounded. Do not log DSNs, keys, or raw sensitive documents while debugging.

## Backup and restore into a separate database

Do this only against your disposable course database. Keep the backup under ignored work/ and protect it as data.

```bash
mkdir -p work/backups
docker compose exec -T database pg_dump -U learner -d learning -Fc > work/backups/learning.dump
docker compose exec -T database createdb -U learner learning_restore
docker compose exec -T database pg_restore -U learner -d learning_restore --no-owner < work/backups/learning.dump
docker compose exec -T database psql -U learner -d learning_restore -c 'SELECT COUNT(*) FROM financials;'
```

The seeded financials count is six. Also compare document counts, record sums, and a known query. Use a new restore database name on subsequent drills instead of dropping an existing database casually. A backup of the application tables must be coordinated with external document storage and index/model versions.

## Migrations and rollback

Treat schema setup in `Store` as initial teaching scaffolding. For real migrations, record numbered versions, test upgrade on a copy of data, and use an expand-contract sequence: add compatible structures, deploy compatible application, backfill, switch reads, then remove old structures in a later release. Test the previous app against the new schema before claiming rollback support.

Save image digest, dependency lock, schema version, prompt/model/index versions, and evaluation report per release. If readiness or hard evaluation gates fail, stop promotion and switch traffic back to the known-good compatible image. Do not reverse a data migration without a rehearsed procedure and backup.

## Coolify deployment exercise

After the local drill, use a private repository and your own authorized host. Point the build at `projects/stage10/Dockerfile` with repository-root context. Supply secrets in the platform, connect a private PostgreSQL service/volume, configure `/ready`, choose the API port, enable HTTPS for the intended domain, and keep database/model ports private. Run migrations and smoke checks before routing traffic. Record deploy and rollback steps and actually rehearse them.

The supplied GitHub Actions workflow tests and builds but deliberately does not deploy to an unspecified account. Add a deployment job for your own environment after you have a concrete release, secrets, backup/rollback policy, and successful integration evidence.
