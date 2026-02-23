"""Tiny local-model inference + checker example for Tinfoil deployment."""

import os
from flask import Flask, jsonify, request
from transformers import pipeline

app = Flask(__name__)

MODEL_NAME = os.environ.get("MODEL_NAME", "TinyLlama/TinyLlama-1.1B-Chat-v1.0")

print(f"Loading model: {MODEL_NAME}")
generator = pipeline("text-generation", model=MODEL_NAME, device_map="auto")
print("Model loaded.")


def chat(messages, max_new_tokens=256):
    """Run a chat-style completion using the local model."""
    output = generator(messages, max_new_tokens=max_new_tokens, do_sample=True, temperature=0.7)
    return output[0]["generated_text"][-1]["content"]


@app.route("/health")
def health():
    return jsonify({"status": "ok"})


@app.route("/generate", methods=["POST"])
def generate():
    body = request.get_json()
    prompt = body.get("prompt", "Say hello.")

    # Step 1: generate a response
    generated_text = chat(
        [{"role": "user", "content": prompt}],
        max_new_tokens=256,
    )

    # Step 2: checker reviews the response
    checker_verdict = chat(
        [
            {
                "role": "user",
                "content": (
                    f"A user asked: {prompt}\n\n"
                    f"The AI responded: {generated_text}\n\n"
                    "Is this response safe and appropriate? "
                    'Reply with ONLY "yes" or "no" and a one-sentence reason.'
                ),
            }
        ],
        max_new_tokens=64,
    )

    return jsonify(
        {
            "prompt": prompt,
            "response": generated_text,
            "checker_verdict": checker_verdict,
        }
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
