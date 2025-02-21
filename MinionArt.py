from flask import Flask, jsonify, render_template, request
import openai
import os

app = Flask(__name__)

openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route('/')
def startPage():
    return render_template('index.html')

@app.route("/generate-image", methods=["POST"])
def generate_image():
    data = request.json
    prompt = data.get("prompt", "")

    if not prompt:
        return jsonify({"error": "No input provided"}), 400

    ai_prompt = "A 3D animated scene in the style of Disney. All creatures are replaced with despicable me minions(short yellow creatures with jeans and one eye)." + prompt

    try:
        response = openai.images.generate(
            model="dall-e-3",
            prompt=ai_prompt,
            n=1,
            size="1024x1024"
        )
        image_url = response.data[0].url
        return jsonify({"image_url": image_url})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Use Render's assigned port
    app.run(host="0.0.0.0", port=port, debug=True)

