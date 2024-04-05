from sqlalchemy import orm, Column, Integer, String, ForeignKey
from .db_session import SqlAlchemyBase


class Mastering(SqlAlchemyBase):
    __tablename__ = 'mastering'

    mastering_id = Column(Integer, primary_key=True, autoincrement=True)

    mastering_rating = Column(Integer, nullable=True)

    mastering_lesson_id = Column(Integer, ForeignKey("lessons.lessons_id"))
    lesson = orm.relationship('Lessons')

    mastering_study_id = Column(Integer, ForeignKey("study.study_id"))
    study = orm.relationship('Study')




