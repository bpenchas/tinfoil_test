# tinfoil_test

Minimal example: deploy a container to Tinfoil that runs a local model for inference and sends the output to the same model for checking. No external APIs — everything runs inside the confidential VM.

## What it does

`POST /generate` with a prompt →

1. **Local model** generates a response (TinyLlama 1.1B by default)
2. **Same model** reviews the response and says whether it's safe

## Local testing

```bash
pip install -r requirements.txt
python app.py
```

```bash
curl -X POST http://localhost:8000/generate \
  -H "Content-Type: application/json" \
  -d '{"prompt": "What is the capital of France?"}'
```

## Deploy to Tinfoil

1. Build and push the image (the model is downloaded at build time):
   ```bash
   docker build -t ghcr.io/you/tinfoil-test:v1 .
   docker push ghcr.io/you/tinfoil-test:v1
   # grab the sha256 digest from the push output
   ```
2. Set the `image` field in `tinfoil-config.yml` to the full `image:tag@sha256:...`
3. Push a tag to trigger deployment:
   ```bash
   git tag v1
   git push origin main --tags
   ```
