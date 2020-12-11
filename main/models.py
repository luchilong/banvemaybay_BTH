# from sqlalchemy import Column, String, Boolean, Enum, Integer
# from sqlalchemy.orm import relationship
# from flask_login import UserMixin
# from enum import Enum as UserEnum
#
#
# class Base(db.Model):
#     __abstract__ = True
#
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     name = Column(String(50), nullable=False)
#
#
# class UserRole(UserEnum):
#     USER = 1
#     ADMIN = 2
#
#
# class User(Base, UserMixin):
#     email = Column(String(50))
#     username = Column(String(50), nullable=False, unique=True)
#     password = Column(String(50), nullable=False)
#     active = Column(Boolean, default=True)
#     user_role = Column(Enum(UserRole), default=UserRole.USER)
#
#     receipts = relationship('Receipt', backref='customer', lazy=True)
#
# if __name__ == '__main__':
#     db.create_all()