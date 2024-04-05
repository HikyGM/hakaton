from sqlalchemy import orm, Column, Integer, String, ForeignKey
from .db_session import SqlAlchemyBase


class Study(SqlAlchemyBase):
    __tablename__ = 'study'

    study_id = Column(Integer, primary_key=True, autoincrement=True)

    study_student_id = Column(Integer, ForeignKey("students.students_id"))
    student = orm.relationship('Students')

    study_course_id = Column(Integer, ForeignKey("courses.courses_id"))
    course = orm.relationship('Courses')

    study = orm.relationship("Mastering", back_populates='study')
