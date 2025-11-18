from flask import Flask, jsonify, render_template, request
from post_generator import generate_post, few_shot


app = Flask(__name__)

PROJECT_NAME = "PerLink"
LENGTH_OPTIONS = ["Short", "Medium", "Long"]
LANGUAGE_OPTIONS = ["English", "Hinglish"]


def get_available_tags():
    tags = few_shot.get_tags() or []
    return sorted(tags)


@app.route("/")
def index():
    return render_template(
        "index.html",
        project_name=PROJECT_NAME,
        tags=get_available_tags(),
        lengths=LENGTH_OPTIONS,
        languages=LANGUAGE_OPTIONS,
    )


@app.route("/generate", methods=["POST"])
def generate():
    data = request.get_json(silent=True) or {}
    length = data.get("length")
    language = data.get("language")
    tag = data.get("tag")

    missing = [field for field, value in {"length": length, "language": language, "tag": tag}.items() if not value]
    if missing:
        return jsonify({"error": f"Missing fields: {', '.join(missing)}"}), 400

    if length not in LENGTH_OPTIONS or language not in LANGUAGE_OPTIONS or tag not in get_available_tags():
        return jsonify({"error": "Invalid selection. Please refresh and try again."}), 400

    try:
        post = generate_post(length, language, tag)
    except Exception as exc:  # pragma: no cover - surface readable error to UI
        return jsonify({"error": f"Unable to generate post: {exc}"}), 500

    return jsonify({"post": post})


if __name__ == "__main__":
    app.run(debug=True)
