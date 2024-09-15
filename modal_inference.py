from modal import App, web_endpoint, Image, Secret

app = App("llama-inference")

@app.function(
    image=Image.debian_slim().pip_install("openai"),
    secrets=[Secret.from_name("openai-api-key")]
)
@web_endpoint(method="POST")
def llm_inference(prompt):
    import os
    from openai import OpenAI

    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    client.base_url = "https://your-modal-endpoint.modal.run/v1"

    completion = client.chat.completions.create(
        model="meta-llama/Meta-Llama-3-8B-Instruct",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
    )

    return completion.choices[0].message.content

if __name__ == "__main__":
    app.serve()