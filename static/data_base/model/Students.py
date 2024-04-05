from sqlalchemy import orm, Column, Integer, String, ForeignKey
from sqlalchemy_serializer import SerializerMixin

from .db_session import SqlAlchemyBase
from werkzeug.security import generate_password_hash, check_password_hash


class Students(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'students'

    students_id = Column(Integer, primary_key=True, autoincrement=True)
    student_id_telegram = Column(Integer, nullable=True)
    student_id_chat = Column(Integer, nullable=True)
    student_first_name = Column(String, nullable=True)
    student_last_name = Column(String, nullable=True)
    student_login = Column(String, nullable=True, unique=True)
    student_password = Column(String, nullable=True)

    student = orm.relationship("Study", back_populates='student')

    def set_password(self, password):
        self.student_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.student_password, password)
