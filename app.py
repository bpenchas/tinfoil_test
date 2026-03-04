"""Inference + checker example using Tinfoil's inference API."""

import os
from flask import Flask, jsonify, request
from tinfoil import TinfoilAI

app = Flask(__name__)

client = TinfoilAI(
    api_key=os.getenv("TINFOIL_API_KEY")
)

MODEL_NAME = os.getenv("MODEL_NAME", "deepseek-r1-0528")


def chat(messages, max_tokens=256):
    """Run a chat-style completion using Tinfoil's inference API."""
    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=messages,
        max_tokens=max_tokens,
    )
    return response.choices[0].message.content


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
        max_tokens=256,
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
        max_tokens=64,
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
