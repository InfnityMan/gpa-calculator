# Import Libraries
import gpa_calculator_database_manager as gpadm
from flask import Flask, render_template, request, jsonify, redirect, url_for, session

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.secret_key = 'your_secret_key_here'


@app.route('/add_account', methods=['GET'])
def add_account():
    student_email = request.args.get('email')
    student_password = request.args.get('password')
    name = request.args.get('name')
    school = request.args.get('school')

    gpadm.add_account(student_email, student_password, name, school)

    return redirect(url_for('logged_in', email=student_email, password=student_password))


@app.route('/gpa_calculator')
def gpa_calculator_page():
    return render_template("gpa_calculator.html")


@app.route('/login')
def login():
    return render_template('login_page.html')


@app.route("/")
def hello_world():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    else:
        return render_template("gpa_calculator.html")


@app.route("/logging_in", methods=['GET'])
def logged_in():
    email = request.args.get('email')
    password = request.args.get('password')

    login_info = gpadm.login(email, password)

    if login_info is not None:
        session['user_id'] = login_info[0]
        session['name'] = login_info[3]
        return jsonify({'status': 'success'})
    else:
        return jsonify({'status': 'failure'})


@app.route("/get_grades", methods=['GET'])
def get_grades():
    grades = gpadm.get_all_grades(session['user_id'])
    return jsonify(grades)


@app.route("/add_grades", methods=['GET'])
def add_grades():
    subject = request.args.get('subject')
    grade = request.args.get('grade')
    weighted = request.args.get('weighted')
    studentGrade = request.args.get('studentGrade')

    gpadm.add_grade(session['user_id'], subject, grade, weighted, studentGrade)
    updated_grades = gpadm.get_all_grades(session['user_id'])
    return jsonify(updated_grades)


@app.route("/update_grades", methods=['GET'])
def update_grades():
    subject = request.args.get('subject')
    grade = request.args.get('grade')

    gpadm.update_grade(session['user_id'], subject, grade)
    updated_grades = gpadm.get_all_grades(session['user_id'])
    return jsonify(updated_grades)


@app.route("/delete_grades", methods=['GET'])
def delete_grades():
    subject = request.args.get('subject')

    gpadm.delete_grade(session['user_id'], subject)
    updated_grades = gpadm.get_all_grades(session['user_id'])
    return jsonify(updated_grades)


@app.route("/signup_page")
def signup_page():
    return render_template("signup_page.html")


@app.route("/log_out")
def log_out():
    session['user_id'] = None
    session['email'] = None
    session['password'] = None
    return redirect(url_for('hello_world'))


@app.route("/get_name", methods=['GET'])
def get_name():
    return session['name']


if __name__ == '__main__':
    app.run()
