import sqlalchemy

from .db_session import SqlAlchemyBase


class Stickers(SqlAlchemyBase):
 dependabot/pip/jinja2-2.11.3
    """Модель стикеров."""

database
    __tablename__ = 'stickers'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    image_path = sqlalchemy.Column(sqlalchemy.String)
