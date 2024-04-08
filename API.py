from static.data_base.model import db_session
from flask import Flask, jsonify, request

from static.data_base.model.Students import Students
from static.data_base.model.Study import Study
from static.data_base.model.Courses import Courses
from static.data_base.model.Lessons import Lessons
from static.data_base.model.Tests import Tests
from static.data_base.model.Mastering import Mastering

app = Flask(__name__)


@app.route('/api/mastering', methods=['GET'])
def get_mastering():
    session = db_session.create_session()
    response = session.query(Mastering).all()
    if response:
        return jsonify([item.to_dict(
            only=['mastering_id', 'mastering_rating', 'mastering_lesson_id', 'mastering_study_id']) for item in
            response])
    else:
        return jsonify({'error': 'An empty table'})


@app.route('/api/tests', methods=['GET'])
def get_tests():
    session = db_session.create_session()
    response = session.query(Tests).all()
    if response:
        return jsonify([item.to_dict(
            only=['test_id', 'test_title_question', 'test_answer_option_1', 'test_answer_option_2',
                  'test_answer_option_3', 'test_correct_option', 'test_lesson_id']) for item in response])
    else:
        return jsonify({'error': 'An empty table'})


@app.route('/api/lessons', methods=['GET'])
def get_lessons():
    session = db_session.create_session()
    response = session.query(Lessons).all()
    if response:
        return jsonify([item.to_dict(
            only=['lessons_id', 'lessons_title', 'lessons_type', 'lessons_url_file', 'lesson_course_id']) for item in
            response])
    else:
        return jsonify({'error': 'An empty table'})


@app.route('/api/courses', methods=['GET'])
def get_courses():
    session = db_session.create_session()
    response = session.query(Courses).all()
    if response:
        return jsonify([item.to_dict(
            only=['courses_id', 'courses_title']) for item in response])
    else:
        return jsonify({'error': 'An empty table'})


@app.route('/api/students', methods=['GET'])
def get_students():
    session = db_session.create_session()
    response = session.query(Students).all()
    if response:
        return jsonify([item.to_dict(
            only=['students_id', 'student_id_telegram', 'student_id_chat', 'student_first_name', 'student_last_name',
                  'student_login']) for item in response])
    else:
        return jsonify({'error': 'An empty table'})


@app.route('/api/study', methods=['GET'])
def get_study():
    session = db_session.create_session()
    response = session.query(Study).all()
    if response:
        return jsonify([item.to_dict(
            only=['study_id', 'study_student_id', 'study_course_id']) for item in response])
    else:
        return jsonify({'error': 'An empty table'})


@app.route('/api/<string:table>/<int:_id>', methods=['GET'])
def get_student(table, _id):
    if table not in ('students', 'study', 'courses', 'lessons', 'tests', 'mastering',):
        return jsonify({'errors': f"The table {table} was not found"})
    session = db_session.create_session()
    response = session.query(eval(table.capitalize())).filter(
        eval(f'{table.capitalize()}.{table}_id') == _id).first()
    if response:
        return jsonify(response.to_dict())
    else:
        return jsonify({'error': 'Not found'})


@app.route('/api/<string:table>/<int:_id>', methods=['DELETE'])
def delete_student(table, _id):
    if table not in ('students', 'study', 'courses', 'lessons', 'tests', 'mastering',):
        return jsonify({'errors': f"The table {table} was not found"})
    session = db_session.create_session()
    response = session.query(eval(table.capitalize())).filter(
        eval(f'{table.capitalize()}.{table}_id') == _id).first()
    if response:
        session.delete(response)
        session.commit()
        return jsonify({'success': 'OK'})
    else:
        return jsonify({'error': 'Not found'})


@app.route('/api/update_student', methods=['PUT'])
def update_student():
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in
                 ['student_id_telegram', 'student_id_chat',
                  'student_first_name', 'student_last_name',
                  'student_login', 'student_password', 'student_password_repeat']):
        return jsonify({'error': 'Bad request'})
    no_value = {key: 'No value' for key, value in request.json.items() if not value}
    if no_value:
        return jsonify(no_value)
    res = request.json
    session = db_session.create_session()

    check_login = session.query(Students).filter(Students.student_login == res['student_login']).first()
    errors = {}
    if check_login:
        errors['login'] = 'Login is used'
    if res['student_password'] != res['student_password_repeat']:
        errors['password'] = "Passwords don't match"
    if errors:
        return jsonify(errors)

    new_student = Students(
        student_id_telegram=res['student_id_telegram'],
        student_id_chat=res['student_id_chat'],
        student_first_name=res['student_first_name'],
        student_last_name=res['student_last_name'],
        student_login=res['student_login'],
    )
    new_student.set_password(res['student_password'])
    session.add(new_student)
    session.commit()

    return jsonify({'success': 'OK'})


@app.route('/api/students', methods=['POST'])
def create_student():
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in
                 ['student_first_name', 'student_last_name',
                  'student_login', 'student_password']):
        return jsonify({'error': 'Bad request'})
    no_value = {key: 'No value' for key, value in request.json.items() if not value}
    if no_value:
        return jsonify(no_value)
    res = request.json
    session = db_session.create_session()
    new_student = Students(
        student_id_telegram='',
        student_id_chat='',
        student_first_name=res['student_first_name'],
        student_last_name=res['student_last_name'],
        student_login=res['student_login'],
    )
    new_student.set_password(res['student_password'])
    session.add(new_student)
    session.commit()
    return jsonify([new_student.to_dict()])


@app.route('/api/courses', methods=['POST'])
def create_course():
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif 'courses_title' not in request.json:
        return jsonify({'error': 'Bad request'})
    no_value = {key: 'No value' for key, value in request.json.items() if not value}
    if no_value:
        return jsonify(no_value)
    res = request.json
    session = db_session.create_session()

    check_title = session.query(Courses).filter(Courses.courses_title == res['courses_title']).first()
    errors = {}
    if check_title:
        errors['title'] = 'Title is used'
    if errors:
        return jsonify(errors)

    new_course = Courses(courses_title=res['courses_title'])
    session.add(new_course)
    session.commit()
    return jsonify({'success': 'OK'})


@app.route('/api/lessons', methods=['POST'])
def create_lesson():
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(
            key in request.json for key in ['lessons_title', 'lessons_type', 'lessons_url_file', 'lesson_course_id']):
        return jsonify({'error': 'Bad request'})
    no_value = {key: 'No value' for key, value in request.json.items() if not value}
    if no_value:
        return jsonify(no_value)
    res = request.json
    session = db_session.create_session()

    check_title = session.query(Lessons).filter(Lessons.lessons_title == res['lessons_title']).first()
    check_course = session.query(Courses).filter(Courses.courses_id == res['lesson_course_id']).first()
    errors = {}
    if check_title:
        errors['title'] = 'Title is used'
    if check_course:
        errors['course_id'] = 'Not found'
    if errors:
        return jsonify(errors)

    new_lesson = Lessons(
        lessons_title=res['lessons_title'],
        lessons_type=res['lessons_type'],
        lessons_url_file=res['lessons_url_file'],
        lesson_course_id=res['lesson_course_id']

    )
    session.add(new_lesson)
    session.commit()
    return jsonify({'success': 'OK'})


if __name__ == '__main__':
    db_session.global_init("static/data_base/data_base.db")
    app.run(port=8080)
