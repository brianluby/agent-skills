# Go verification

Prefer repository task runners and preserve declared build tags, `GOOS`/`GOARCH`, CGO policy, and module/workspace layout.

## Focused loop

```sh
gofmt -w <changed-go-files>
go test ./path/to/package
go test ./path/to/package -run '^TestName$'
go vet ./path/to/package
```

Use `gofmt -d` or a repository formatter check when edits must remain non-mutating. Run `go test -race` for changed synchronization, goroutines, caches, pools, handlers, or shared state; the race detector is platform-dependent and not proof of race freedom.

## Escalation

```sh
go test ./...
go vet ./...
go test -race ./...
go test ./... -count=1
```

Additional checks:

- Fuzz parsers, protocol handlers, and security-sensitive boundary code when fuzz targets exist.
- Run benchmarks with stable inputs and compare statistically; do not claim performance from a single timing.
- Inspect `go.mod` and `go.sum` after dependency changes. Use `go mod tidy -diff` when supported before applying tidy.
- Run generated-code checks only through documented generators; review generated diffs.
- Test supported build tags and cross-platform files explicitly when touched.
- For public APIs, verify examples and compatibility with downstream interface assertions.

Never hide test cache effects, silently change toolchains, or claim checks that could not run.
