from sqlalchemy import orm, Column, Integer, String, ForeignKey
from sqlalchemy_serializer import SerializerMixin

from .db_session import SqlAlchemyBase


class Lessons(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'lessons'

    lessons_id = Column(Integer, primary_key=True, autoincrement=True)
    lessons_title = Column(String, nullable=True)
    lessons_type = Column(String, nullable=True)
    lessons_url_file = Column(String, nullable=True)


    lesson_course_id = Column(Integer, ForeignKey("courses.courses_id"))
    lesson = orm.relationship('Courses')

    test = orm.relationship("Tests", back_populates='test')
    mastering = orm.relationship("Mastering", back_populates='lesson')


