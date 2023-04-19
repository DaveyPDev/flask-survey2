from flask import Flask, request, render_template, redirect, flash, session, abort

from flask_debugtoolbar import DebugToolbarExtension

from surveys import satisfaction_survey as survey

app = Flask(__name__)

app.config['SECRET_KEY'] = 'applecore'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

RESPONSES_KEY = 'responses'

# @app.route('/404')
# def page_not_found():
#     abort(404)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.route('/')
def home_page():
    
    return render_template('survey_start.html', survey=survey)


@app.route('/begin', methods=["POST"])
def start_survey():

    session["responses"] = []

    return redirect('/questions/0')


# @app.route('/questions/0')
# def question():
    
#     return 


@app.route('/questions/<int:question_id>')
def show_question(question_id):

    responses = session.get('responses')
    if (responses is None):
        return redirect('/')
    if (len(responses) == len(survey.questions)):
        return redirect('/complete')
    if (len(responses) != question_id):
        return redirect(f'/questions/{len(responses)}')
    
    question = survey.questions[question_id]
    return render_template('question.html', question_num=question_id, question=question)


@app.route('/answer', methods=["POST"])
def handle_answers():

    choice = request.form['answer']
    responses = session['responses']
    responses.append(choice)
    session['responses'] = responses

    if len(responses) < len(survey.questions):
        return redirect(f'/questions/{len(responses)}')

    else:
        return redirect('/complete')

@app.route('/complete')
def complete():
    
    return render_template('complete.html')
    