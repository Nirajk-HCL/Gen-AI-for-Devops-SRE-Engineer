# Kubernetes MCP Server - AI Coding Agent Instructions

## Project Overview
Go-based Model Context Protocol (MCP) server providing native Kubernetes/OpenShift cluster management without external CLI dependencies. Supports STDIO, HTTP, and SSE transport modes. Multi-platform distribution via native binaries, npm, PyPI, and container images.

## Architecture & Key Concepts

### Toolset-Based Architecture
Tools are organized into **toolsets** that group related functionality:
- **Tool definitions** live in `pkg/api/` using `ServerTool` struct
- **Toolsets** in `pkg/toolsets/` (subdirs: `config/`, `core/`, `helm/`, `kiali/`, `kubevirt/`)
- **Registration** happens via `toolsets.Register()` at package init
- Each toolset implements `api.Toolset` interface with `GetName()`, `GetTools()`, `GetPrompts()`

### Go Package Layout
- `cmd/kubernetes-mcp-server/` - main entry using Cobra CLI framework
- `pkg/api/` - tool definitions, interfaces, parameter parsing utilities
- `pkg/kubernetes/` - Kubernetes client management, auth, and access control
- `pkg/mcp/` - MCP protocol implementation (STDIO/HTTP/SSE support)
- `pkg/http/` - HTTP server and authorization middleware  
- `pkg/helm/` - Helm chart operations
- `pkg/output/` - formatting and rendering (table/yaml)
- `internal/test/` - shared test utilities and helpers

### Distribution Chain
Changes to Go code automatically propagate to all distribution methods:
- **Native binaries**: `make build-all-platforms` creates platform-specific executables
- **npm wrapper** (`npm/`): includes prebuilt binaries, downloads on install
- **Python wrapper** (`python/`): script downloads correct binary from GitHub releases
- **Container image**: `Dockerfile` packages binary
- Usually no changes needed to npm/python unless version/packaging updates required

## Development Workflows

### Building & Testing
```bash
make build              # Format, tidy, lint, build binary
make build-all-platforms # Build for all OS/arch combinations
make test               # Run test suite (downloads envtest on first run)
make lint               # golangci-lint static analysis
```

### Local Development Environment
```bash
make local-env-setup    # Kind cluster + Keycloak + build
./kubernetes-mcp-server --port 8008 --config _output/config.toml
# Or use MCP inspector:
npx @modelcontextprotocol/inspector@latest $(pwd)/kubernetes-mcp-server
```

### Adding New MCP Tools
1. Define handler function implementing tool logic
2. Create `ServerTool` struct with schema and handler in `pkg/api/`
3. Add to appropriate toolset in `pkg/toolsets/` (or create new toolset)
4. Register toolset if new: `toolsets.Register(NewMyToolset())` in package init
5. Run `make test` and `make update-readme-tools` to update docs

### Distribution Publishing
```bash
make npm-copy-binaries  # Copy binaries to npm packages
make npm-publish        # Publish to npmjs.com
make python-publish     # Publish to pypi.org
```

## Testing Patterns (CRITICAL)

### Required Approach
- **Use testify/suite**: organize tests with `suite.Suite` embedding
- **Black-box testing**: test public API only, no mocks, real implementations
- **Behavior over implementation**: test outcomes, not internal state
- **One assertion per subtest**: each `s.Run()` tests one specific behavior

### Test Structure Example
```go
type MyTestSuite struct {
    suite.Suite
}

func (s *MyTestSuite) TestFeature() {
    s.Run("valid input scenarios", func() {
        s.Run("handles simple case correctly", func() {
            result := functionUnderTest(input)
            s.Equal("expected", result)
        })
    })
    s.Run("edge cases", func() {
        s.Run("returns error for nil input", func() {
            _, err := functionUnderTest(nil)
            s.Error(err, "expected error for nil input")
        })
    })
}

func TestMyFeature(t *testing.T) {
    suite.Run(t, new(MyTestSuite))
}
```

### Error Handling in Tests
- Use `s.Require().NoError(err)` for setup operations that must succeed
- Use `s.Error(err)` or `s.NoError(err)` for testing error conditions
- Always check and handle errors—never ignore them in production code

### Good Examples
- `internal/test/unstructured_test.go` - testify/suite patterns
- `pkg/mcp/kubevirt_test.go` - behavior-based MCP testing
- `pkg/kubernetes/manager_test.go` - setup/teardown with subtests

## Project Conventions

### Parameter Parsing
Use helpers from `pkg/api/params.go` for tool argument extraction:
- `RequiredString(params, "key")` - returns error if missing/invalid
- `OptionalString(params, "key", "default")` - returns default if missing
- `OptionalBool(params, "key", false)` - handles boolean parameters
- `ParseInt64(value)` - converts JSON numbers (float64) to int64

### Build Configuration
- Go modules target **Go 1.25** (see `go.mod`)
- LD_FLAGS inject version info: `CommitHash`, `Version`, `BuildTime`, `BinaryName`
- `GIT_TAG_VERSION` (without `-dirty` suffix) used for npm/PyPI versioning
- Platform matrix: `OSES = darwin linux windows`, `ARCHS = amd64 arm64`

### Kubeconfig Handling
Server resolves config in order: `--kubeconfig` flag → `KUBECONFIG` env → `~/.kube/config` → in-cluster config. Supports multi-cluster (multiple contexts) unless `--disable-multi-cluster` set.

### Read-Only & Safety Modes
- `--read-only`: disables all write operations (create/update/delete)
- `--disable-destructive`: allows updates but prevents deletes
- `--stateless`: disables tool/prompt change notifications (for serverless/LB)

## Key Files Reference
- [pkg/toolsets/toolsets.go](../pkg/toolsets/toolsets.go) - toolset registration system
- [pkg/api/kubernetes.go](../pkg/api/kubernetes.go) - KubernetesClient interface
- [Makefile](../Makefile) - all build, test, lint targets with help descriptions
- [AGENTS.md](../AGENTS.md) - comprehensive project guide (source of this doc)
- [docs/GETTING_STARTED_KUBERNETES.md](../docs/GETTING_STARTED_KUBERNETES.md) - ServiceAccount setup
- [internal/test/](../internal/test/) - reusable test helpers and utilities

## Common Patterns
- **Tool handlers** receive `ToolHandlerParams` with `GetArguments()` method
- **Client access** via `params.GetClient()` returns `api.KubernetesClient`
- **Output rendering** use `output` package for table/yaml formatting
- **OpenShift detection** toolsets receive `api.Openshift` to conditionally enable tools
- **Resource operations** use dynamic client with `unstructured.Unstructured` for generic K8s resources
