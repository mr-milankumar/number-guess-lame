from flask import Flask, render_template, request, session, redirect, url_for
import random

app = Flask(__name__)

# REQUIRED for sessions
app.secret_key = "super-secret-key"  # change later for production


def start_new_game(level):
    session["difficulty"] = level
    session["attempts"] = 0
    session["game_over"] = False
    session["guess_history"] = []

    if level == "easy":
        session["secret_number"] = random.randint(1, 20)
        session["max_attempts"] = 10
    elif level == "medium":
        session["secret_number"] = random.randint(1, 50)
        session["max_attempts"] = 7
    elif level == "hard":
        session["secret_number"] = random.randint(1, 100)
        session["max_attempts"] = 5


@app.route("/", methods=["GET", "POST"])
def index():
    message = ""

    # -----------------------------
    # START GAME (difficulty chosen)
    # -----------------------------
    if request.method == "POST" and "difficulty" in request.form:
        start_new_game(request.form["difficulty"])
        return redirect(url_for("index"))

    # -----------------------------
    # HANDLE GUESS
    # -----------------------------
    if request.method == "POST" and "guess" in request.form:
        if not session.get("game_over", True):
            guess = int(request.form["guess"])
            session["attempts"] += 1
            session["guess_history"].append(guess)

            if guess > session["secret_number"]:
                message = "⬆️ Too high!"
            elif guess < session["secret_number"]:
                message = "⬇️ Too low!"
            else:
                message = f"🎉 Correct! You guessed it in {session['attempts']} attempts."
                session["game_over"] = True

            if (
                session["attempts"] >= session["max_attempts"]
                and not session["game_over"]
            ):
                message = f"❌ Game Over! The number was {session['secret_number']}."
                session["game_over"] = True

    return render_template(
        "index.html",
        message=message,
        difficulty=session.get("difficulty"),
        attempts=session.get("attempts", 0),
        max_attempts=session.get("max_attempts", 0),
        game_over=session.get("game_over", False),
        guess_history=session.get("guess_history", []),
    )


@app.route("/restart", methods=["POST"])
def restart():
    if "difficulty" in session:
        start_new_game(session["difficulty"])
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run()
