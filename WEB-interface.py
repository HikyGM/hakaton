import requests as requests
from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Домашняя страница', content='content/home.html')


@app.route('/students', methods=['GET'])
def get_students():
    res = requests.get('http://127.0.0.1:8080/api/students')
    if res.status_code == 200:
        # return res.json()
        students = []
        for item in res.json():
            new_student = {'student_id_telegram': item['student_id_telegram'],
                           'student_id_chat': item['student_id_chat'],
                           'student_first_name': item['student_first_name'],
                           'student_last_name': item['student_last_name'],
                           'student_login': item['student_login'],
                           'students_id': item['students_id']}
            students.append(new_student)
        return render_template('index.html', title='Домашняя страница', content='content/students.html', students=students)
    else:
        return {'error': 'An empty table'}


@app.route('/add-student', methods=['GET', 'POST'])
def add_user():
    if request.method == 'GET':
        return render_template('index.html', title='Добавление пользователя', content='content/add-student.html',
                               answer='')
    if request.method == 'POST':
        if 8 <= len(request.form['password']) <= 20:
            res = requests.post('http://127.0.0.1:8080/api/students', json={
                'student_first_name': request.form['first_name'],
                'student_last_name': request.form['last_name'],
                'student_login': request.form['login'],
                'student_password': request.form['password']
            })
            if res.status_code == 200:
                return render_template('index.html', title='Добавление пользователя',
                                       content='content/add-student.html', answer='Студент успешно добавлен!')
            else:
                return {'error': 'An empty table'}
        else:
            return render_template('index.html', title='Добавление пользователя', content='content/add-student.html',
                                   answer='Пароль должен быть от 8 до 20 символов')


if __name__ == '__main__':
    app.run(debug=True)
