from flask import Flask, render_template, request, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey


app = Flask(__name__)
app.config["SECRET_KEY"] = "survey"
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False

debug = DebugToolbarExtension(app)

question_number = 0

@app.route("/")
def survey():
    """Showing survey form."""

    return render_template("survey.html", title=satisfaction_survey.title,
        instructions=satisfaction_survey.instructions)


@app.route("/questions/<int:quest>")
def question(quest):
    """Showing one question from survey."""
    # if(quest == len(satisfaction_survey.questions)):

    """Check if on the right question"""
    if int(len(session["responses"])) != int(quest):
        flash("Please answer")
        return redirect(f"/questions/{len(session['responses'])}")
    else:
        return render_template("question.html", question=satisfaction_survey.questions[quest].question, choices=satisfaction_survey.questions[quest].choices, quest=quest)


@app.route("/answers", methods=["POST"])
def answers():
    """Receiving answers."""
    current = session["responses"]
    current.append(request.form["choice_made"])
    session["responses"] = current

    quest = int(request.form["question_number"])


    """Check if limit of questions has been reached"""
    if quest == len(satisfaction_survey.questions) - 1:
        return redirect('/thankyou')
    else:
        quest += 1
        return redirect(f"/questions/{quest}")


@app.route('/thankyou')
def thank_you():
    """Render thank you page"""

    return render_template('thankyou.html')


@app.route("/setup", methods=["POST"])
def setup():
    """Creating our session storage"""

    session["responses"] = []
    
    return redirect("/questions/0")
