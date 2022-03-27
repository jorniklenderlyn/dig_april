import sqlalchemy
from dataBot.datacode.mySQL.func_db.db_session import SqlAlchemyBase


class DigTelegramUser(SqlAlchemyBase):
    __tablename__ = "DigTelegramUser"

    id = sqlalchemy.Column(sqlalchemy.Integer, autoincrement=True, primary_key=True)
    user_id = sqlalchemy.Column(sqlalchemy.Text)
    user_name = sqlalchemy.Column(sqlalchemy.Text)
    dirt_map = sqlalchemy.Column(sqlalchemy.Text)
    diamonds = sqlalchemy.Column(sqlalchemy.Integer)
    efficiency = sqlalchemy.Column(sqlalchemy.Integer)
    fortune = sqlalchemy.Column(sqlalchemy.Integer)
    level = sqlalchemy.Column(sqlalchemy.Integer)
    time = sqlalchemy.Column(sqlalchemy.DateTime)
