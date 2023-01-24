from flask import Flask, render_template, redirect, request, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)
app.config['SECRET_KEY'] = 'key40'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

RESPONSES_KEY = 'responses'


@app.route('/')
def show_survey():
    return render_template('start.html', survey=survey)


@app.route('/start', methods=['POST'])
def start_survey():

    session[RESPONSES_KEY] = []

    return redirect('/questions/0')


@ app.route('/questions/<int:q>')
def handle_question(q):
    responses = session.get(RESPONSES_KEY)

    if (responses is None):
        return redirect('/')

    if (len(responses) == len(survey.questions)):
        return redirect('/complete')

    if (len(responses) != q):
        flash('Invalid question id!')
        return redirect(f'/questions/{len(responses)}')

    question = survey.questions[q]
    return render_template('questions.html', question=question, q=q)


@ app.route('/answer', methods=['POST'])
def handle_answer():
    answer = request.form['answer']

    responses = session[RESPONSES_KEY]
    responses.append(answer)
    session[RESPONSES_KEY] = responses

    if (len(responses) == len(survey.questions)):
        return redirect('/complete')
    else:
        return redirect(f"/questions/{len(responses)}")


@ app.route('/complete')
def complete():
    return render_template('completion.html')
