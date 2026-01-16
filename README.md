## de-gig API

Simple Express + MongoDB API (TypeScript) to serve freelancers data. On first `docker compose up`, it seeds MongoDB from `freelancers.json`.

### Run (Docker)

```bash
docker compose up --build -d
# wait a few seconds for seeding to complete
curl "http://localhost:3002/freelancers?limit=10&page=1" | jq
```

### Local dev (optional)

```bash
npm install
npm run start:dev   # ts-node ESM loader, watches source
```

Build + run locally:

```bash
npm run build
npm start
```

- `limit` max is 10 (default 10) - enforced guard, cannot exceed 10 rows per request
- `page` starts at 1

Environment (optional via `.env` or compose overrides):
- `PORT` (default `3002`)
- `MONGO_URL` (default `mongodb://mongo:27017/de_gig`)
- `FREELANCERS_PATH` (default `/app/freelancers.json`)

Health check:

```bash
curl http://localhost:3002/healthz
```

### Notes
- MongoDB listens on host port `27019` (maps to container port `27017`).
- MongoDB data persists via the `mongo_data` volume.
- Seeding only occurs if the `freelancers` collection is empty.
