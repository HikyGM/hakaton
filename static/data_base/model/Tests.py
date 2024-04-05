from sqlalchemy import orm, Column, Integer, String, ForeignKey
from .db_session import SqlAlchemyBase


class Tests(SqlAlchemyBase):
    __tablename__ = 'tests'

    test_id = Column(Integer, primary_key=True, autoincrement=True)
    test_title_question = Column(String, nullable=True)
    test_answer_option_1 = Column(String, nullable=True)
    test_answer_option_2 = Column(String, nullable=True)
    test_answer_option_3 = Column(String, nullable=True)
    test_correct_option = Column(String, nullable=True)


    test_lesson_id = Column(Integer, ForeignKey("lessons.lessons_id"))
    test = orm.relationship('Lessons')


