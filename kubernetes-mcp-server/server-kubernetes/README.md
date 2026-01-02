# Kubernetes MCP Server (minimal scaffold)

This small scaffold implements a Model Context Protocol (MCP) style server that translates a few natural-language commands into `kubectl` commands. It's intended as a safe starting point you can extend.

Prerequisites

- Node.js v18+ and npm (required)
- kubectl configured with kubeconfig (required for command execution)

Install Node.js (if not already installed)

**Windows:**
1. Download Node.js LTS from https://nodejs.org/en/
2. Run the installer and follow prompts (choose default options)
3. Restart your terminal/PowerShell after installation
4. Verify: `node --version` and `npm --version`

**macOS/Linux:**
```bash
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs
# or use Homebrew:
brew install node
```

Installation (local development)

```bash
# from server-kubernetes folder
cd server-kubernetes
npm install
# run server
node index.js
```

Or install globally (for CLI):

```bash
# from server-kubernetes folder
npm install -g .
# then:
mcp-k8s "Show me all pods in the production namespace with their status"
```

Safety

- Commands are not executed by default. Use the `--run` flag in the CLI or `?run=true` on the HTTP API and set `ALLOW_KUBECTL=1` to enable execution.

HTTP API

POST /command

Body: { "text": "Show me all pods in the production namespace with their status" }

Query: `?run=true` to execute (requires `ALLOW_KUBECTL=1` environment variable)

Examples (natural language)

- "Show me all pods in the production namespace with their status"
- "Scale the frontend deployment to 5 replicas and verify health"
- "Investigate why the payment service is crashing - check logs and events"

Extend

This parser is intentionally small. Replace or augment `parseCommand` in `index.js` with an LLM-based intent parser or more advanced NLP and integrate RBAC/authorization before allowing execution in production.
