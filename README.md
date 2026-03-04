# tinfoil_test

A minimal example of running an inference + checker pipeline inside a Tinfoil confidential enclave.

## What it does

```
User prompt → LLM 1 (Generator) → LLM 2 (Checker) → Response
```

`POST /generate` triggers a two-step pipeline:

1. **LLM 1 (Generator)**: Takes the user's prompt and generates a response using DeepSeek R1
2. **LLM 2 (Checker)**: Reviews the generated response and evaluates whether it's safe and appropriate

Both LLM calls use Tinfoil's inference API, which runs inside a confidential VM with hardware-level encryption. Your prompts and responses never leave the secure enclave.

## Example

```bash
curl -s -X POST https://ppa.rinberg-lab.containers.tinfoil.dev/generate \
  -H "Content-Type: application/json" \
  -d '{"prompt": "What is 2 + 2?"}' | jq .
```

Response:
```json
{
  "prompt": "What is 2 + 2?",
  "response": "The sum of 2 + 2 is **4**.",
  "checker_verdict": "Yes. The response correctly answers a simple math question..."
}
```

## Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/health` | GET | Health check, returns `{"status": "ok"}` |
| `/generate` | POST | Run the inference + checker pipeline |

## Local testing

```bash
export TINFOIL_API_KEY=your_key_here
pip install -r requirements.txt
python app.py
```

```bash
curl -X POST http://localhost:8000/generate \
  -H "Content-Type: application/json" \
  -d '{"prompt": "What is the capital of France?"}'
```

## Deploy to Tinfoil

1. Build and push the Docker image:
   ```bash
   docker build -t ghcr.io/bpenchas/tinfoil-test:v1 .
   docker push ghcr.io/bpenchas/tinfoil-test:v1
   # Note the sha256 digest from the push output
   ```

2. Update `tinfoil-config.yml` with the image digest:
   ```yaml
   image: "ghcr.io/bpenchas/tinfoil-test@sha256:..."
   ```

3. Commit and push a tag to trigger the GitHub Actions workflow:
   ```bash
   git add tinfoil-config.yml
   git commit -m "pin image digest"
   git push
   git tag v1
   git push origin v1
   ```

The workflow runs `tinfoilsh/pri-build-action` which creates a Sigstore attestation and deploys the container to a Tinfoil enclave.

## Configuration

See `tinfoil-config.yml`:

- **Model**: `deepseek-r1-0528` (configurable via `MODEL_NAME` env var)
- **Secrets**: `TINFOIL_API_KEY` (required for inference API access)
- **Resources**: 4 CPUs, 16GB RAM
