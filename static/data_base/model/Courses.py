from sqlalchemy import orm, Column, Integer, String, ForeignKey
from sqlalchemy_serializer import SerializerMixin

from .db_session import SqlAlchemyBase


class Courses(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'courses'

    courses_id = Column(Integer, primary_key=True, autoincrement=True)
    courses_title = Column(String)

    course_study = orm.relationship("Study", back_populates='course')
    course_lesson = orm.relationship("Lessons", back_populates='lesson')

