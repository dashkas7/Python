from flask import Flask, redirect, render_template, request, session, url_for, jsonify
import os
from models import db, Quiz, Question, db_add_new_data, User
from random import shuffle
from sqlalchemy import not_

BASE_DIR = os.path.dirname(__file__)
DB_DIR = os.path.join(BASE_DIR, 'db')
os.makedirs(DB_DIR, exist_ok=True)
DB_PATH = os.path.join(DB_DIR, 'db_quiz.db')

app = Flask(
    __name__,
    template_folder=os.path.join(BASE_DIR, 'templates'),
    static_folder=os.path.join(BASE_DIR, 'static')
)
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_PATH}'
app.config['SECRET_KEY'] = 'secretkeysecretkeysecretkey1212121'

db.init_app(app)

html_config = {'admin': True, 'debug': False}


with app.app_context():
    db_add_new_data()
    quizes = Quiz.query.all()
    print("Все квизы:", quizes)
    quiz = quizes[0]
    q = quiz.questions
    print("Вопросы первого квиза:", q)
    print("Первый вопрос и его квизы:", q[0], q[0].quizes)



@app.route('/')
def index():
    return render_template('base.html', html_config=html_config)


@app.route('/quiz/', methods=['POST', 'GET'])
def view_quiz():
    if request.method == 'GET':
        session['quiz_id'] = -1
        quizes = Quiz.query.all()
        return render_template('start.html', quizes=quizes, html_config=html_config)

  
    session['quiz_id'] = int(request.form.get('quiz'))
    session['question_n'] = 0
    session['question_id'] = 0
    session['right_answers'] = 0
    return redirect(url_for('view_question'))


@app.route('/question/', methods=['POST', 'GET'])
def view_question():
    if not session.get('quiz_id') or session['quiz_id'] == -1:
        return redirect(url_for('view_quiz'))

    quiz = Quiz.query.get(session['quiz_id'])
    if not quiz:
        return redirect(url_for('view_quiz'))

    if request.method == 'POST':
        question = Question.query.get(session['question_id'])
        if question and question.answer == request.form.get('ans_text'):
            session['right_answers'] += 1
        session['question_n'] += 1

  
    if session['question_n'] >= len(quiz.questions):
        session['quiz_id'] = -1
        return redirect(url_for('view_result'))

    question = quiz.questions[session['question_n']]
    session['question_id'] = question.id
    answers = [question.answer, question.wrong1, question.wrong2, question.wrong3]
    shuffle(answers)

    return render_template('question.html',
                           answers=answers,
                           question=question,
                           html_config=html_config)


@app.route('/questions/')
def view_questions():
    questions = Question.query.all()
    return render_template('questions.html', questions=questions, html_config=html_config)


@app.route('/result/')
def view_result():
    return render_template('result.html',
                           right=session.get('right_answers', 0),
                           total=session.get('question_n', 0),
                           html_config=html_config)



@app.route('/quizes_view/', methods=['POST', 'GET'])
def view_quiz_edit():
    if request.method == 'POST':
        quiz_name = request.form.get('quiz')
        if quiz_name and len(quiz_name) > 3:
            user = User.query.first()
            if not user:
                user = User('admin')
                db.session.add(user)
                db.session.commit()
            quiz = Quiz(quiz_name, user)
            db.session.add(quiz)
            db.session.commit()
        else:
            question = request.form.get('question')
            answer = request.form.get('answer')
            wrong1 = request.form.get('wrong1')
            wrong2 = request.form.get('wrong2')
            wrong3 = request.form.get('wrong3')
            if all([question, answer, wrong1, wrong2, wrong3]):
                q = Question(question, answer, wrong1, wrong2, wrong3)
                db.session.add(q)
                db.session.commit()
        return redirect(url_for('view_quiz_edit'))

    quizes = Quiz.query.all()
    questions = Question.query.all()
    return render_template('quizes_view.html',
                           html_config=html_config,
                           quizes=quizes,
                           questions=questions,
                           len=len)
@app.route('/quiz_edit/<int:id>/', methods=['GET', 'POST'])
def quiz_edit(id):
    quiz = Quiz.query.get_or_404(id)

    if request.method == 'POST':
        new_name = request.form.get('name')
        if new_name and len(new_name) > 3:
            quiz.name = new_name

        add_q = [int(v) for k, v in request.form.items() if k.startswith('add_q')]
        del_q = [int(v) for k, v in request.form.items() if k.startswith('del_q')]

        if add_q:
            qs = Question.query.filter(Question.id.in_(add_q)).all()
            for q in qs:
                if q not in quiz.questions:
                    quiz.questions.append(q)

        
        if del_q:
            qs = Question.query.filter(Question.id.in_(del_q)).all()
            for q in qs:
                if q in quiz.questions:
                    quiz.questions.remove(q)

        db.session.commit()
        return redirect(url_for('view_quiz_edit'))


    current_ids = [q.id for q in quiz.questions]
    available_questions = Question.query.filter(~Question.id.in_(current_ids)).all()

    return render_template(
        'quiz_edit.html',
        quiz=quiz,
        available_questions=available_questions,
        html_config=html_config
    )


@app.route('/quiz_menu/')
def quiz_menu():
    quizes = Quiz.query.all()
    return render_template('quiz_menu.html', quizes=quizes, html_config=html_config)


@app.route('/question_edit/<int:id>/', methods=['GET', 'POST'])
def question_edit(id):
    q = Question.query.get_or_404(id)

    if request.method == 'POST':
        q.question = request.form.get('question')
        q.answer = request.form.get('answer')
        q.wrong1 = request.form.get('wrong1')
        q.wrong2 = request.form.get('wrong2')
        q.wrong3 = request.form.get('wrong3')

        db.session.commit()
        return redirect(url_for('view_quiz_edit'))

    return render_template('question_edit.html', q=q, html_config=html_config)


@app.route('/quiz_delete/<int:id>/')
def quiz_delete(id):
    Quiz.query.filter_by(id=id).delete()
    db.session.commit()
    return redirect('/quizes_view/')


@app.route('/question_delete/<int:id>/')
def question_delete(id):
    Question.query.filter_by(id=id).delete()
    db.session.commit()
    return redirect('/quizes_view/')


@app.errorhandler(404)
def page_not_found(e):
    return '<h1 style="color:red; text-align:center"> Упс..... </h1>', 404


@app.route('/api/quizes/', methods=['GET'])
def api_get():
    quizes = Quiz.query.all()
    payload = [{'name': q.name, 'id': q.id, 'user_id': q.user_id} for q in quizes]
    return jsonify(payload)


@app.route('/api/quizes/', methods=['POST'])
def api_post():
    user = User.query.first()
    if not user:
        user = User('admin')
        db.session.add(user)
        db.session.commit()
    quiz = Quiz('Quiz123', user)
    db.session.add(quiz)
    db.session.commit()
    return jsonify({"id": quiz.id})


@app.route('/api/quizes/<int:id>/', methods=['GET'])
def api_get_id(id):
    quiz = db.session.query(Quiz).get_or_404(id)
    return jsonify(dict(name=quiz.name, user_id=quiz.user_id))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5555)
