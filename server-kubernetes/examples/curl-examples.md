## Examples (curl)

# 1) Parse command (no execution)
curl -s -X POST http://localhost:3000/command -H 'Content-Type: application/json' -d '{"text":"Show me all pods in the production namespace with their status"}'

# 2) Execute (requires ALLOW_KUBECTL=1 and kubectl configured)
curl -s -X POST 'http://localhost:3000/command?run=true' -H 'Content-Type: application/json' -d '{"text":"Scale the frontend deployment to 5 replicas and verify health"}'
