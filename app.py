from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# TODO
# ---------------
# Secure python_flask eval execution by
#     1. blocking malicious keyword like os,eval,exec,bind,connect,python,socket,ls,cat,shell,bind
#     2. Implementing regex: r'0x[0-9A-Fa-f]+|\\u[0-9A-Fa-f]{4}|%[0-9A-Fa-f]{2}|\.[A-Za-z2O-9]{1,3}\b|[\\\\/]|\.'

BLOCKED_KEYWORDS = [
    "os", "eval", "exec", "bind", "connect", "python",
    "socket", "ls", "cat", "shell", "import", "__"
]


def is_blocked(user_input: str) -> bool:
    lowered = user_input.lower()
    return any(keyword in lowered for keyword in BLOCKED_KEYWORDS)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/execute", methods=["POST"])
def execute():
    feedback = request.form.get("feedback", "")

    if is_blocked(feedback):
        return render_template(
            "index.html",
            result="Error: blocked keyword detected in submission.",
            feedback=feedback,
        )

    try:
        # Intentionally vulnerable: the "sentiment score" is computed by
        # eval-ing whatever expression the user submits.
        output = eval(feedback)
        result = f"Thanks for your feedback! Sentiment score: {output}"
    except Exception as e:
        result = f"Error: {e}"

    return render_template("index.html", result=result, feedback=feedback)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
