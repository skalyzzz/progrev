import random
import string
import datetime
 dependabot/pip/jinja2-2.11.3
import random
import string
from functools import wraps

import sqlalchemy

import hashlib

import sqlalchemy
from flask import current_app
from flask_login import UserMixin
 database
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app.data import db_session

from app.data import db_session
from app.data.db_session import SqlAlchemyBase
from app.data.users_friends import UsersFriends
from modules import constants


dependabot/pip/jinja2-2.11.3
def generate_alternative_id():
    """Создаёт альтернативный id для пользователя, представляющий собой строку
    из 10-20 случайных символов (чисел, букв, нижних подчёркиваний)"""
    size = random.randint(10, 20)
    alt_id = ''.join(
        random.choice(string.ascii_letters + string.digits + '_') for _ in
        range(size)).lower()
    return alt_id


def create_alternative_id():
    """Создаёт уникальный альтернативный id для пользователя."""
    session = db_session.create_session()
    alt_id = generate_alternative_id()
    query = session.query(Users).exists().where(
        Users.alternative_id == alt_id)
    while session.query(query).scalar():
        alt_id = generate_alternative_id()
    return alt_id


class Users(SqlAlchemyBase, SerializerMixin):
    """Модель пользователей."""
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True,
                           index=True)
    # Альтернативный id нужен для того, чтобы при смене пароля у пользователя
    # все его входы становились недействительными (т.к. при обращении к API
    # используется именно alternative_id, а при смене пароля он генерируется
    # заново)
    alternative_id = sqlalchemy.Column(sqlalchemy.String, index=True)

def create_alternative_id(size):
    alt_ids = set()
    session = db_session.create_session()
    for user in session.query(Users).all:
        alt_ids.add(user.alternative_id)
    alt_id = ''.join(
        random.choice(string.ascii_letters + string.digits + '_' * 13) for _ in
        range(size))
    while alt_id in alt_ids:
        alt_id = ''.join(
            random.choice(string.ascii_letters + string.digits + '_' * 13)
            for _ in range(size))
    return alt_id


def create_api_key(email, created_date, password):
    secret_key = current_app.config['SECRET_KEY']
    hash_object = hashlib.sha256(bytes(email + secret_key + str(created_date) +
                                       password, encoding='utf-8'))
    return hash_object.hexdigest()


class Users(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    alternative_id = sqlalchemy.Column(sqlalchemy.String)
database
    first_name = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    second_name = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    email = sqlalchemy.Column(sqlalchemy.String,
                              index=True, unique=True, nullable=False)
    phone_number = sqlalchemy.Column(sqlalchemy.Integer, unique=True,
                                     nullable=True)
    age = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    city = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    additional_inf = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    # Подтверждён ли email пользователя
    is_confirmed = sqlalchemy.Column(sqlalchemy.Boolean, default=False)
    hashed_password = sqlalchemy.Column(sqlalchemy.String, nullable=True)
dependabot/pip/jinja2-2.11.3
    avatar = sqlalchemy.Column(sqlalchemy.String, nullable=True,
                               default=constants.USER_DEFAULT_AVATAR)

    api_key = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    avatar = sqlalchemy.Column(sqlalchemy.String, nullable=True)
 database
    created_date = sqlalchemy.Column(sqlalchemy.DateTime,
                                     default=datetime.datetime.now)
    messages = orm.relation('Messages', backref='message_sender')
    chats = orm.relation('Chats', secondary='chat_participants',
                         backref='chat_member')
    incoming_friend_requests = orm.relation(
        'UsersFriends', backref='inviter',
        foreign_keys=[UsersFriends.invitee_id]
    )
    outgoing_friend_requests = orm.relation(
        'UsersFriends', backref='invitee',
        foreign_keys=[UsersFriends.inviter_id]
    )

 dependabot/pip/jinja2-2.11.3
    @property
    def friends(self):
        """Свойство возвращает всех друзей пользователя в виде FriendsList
        (друзья - пользователи, заявки в друзья которых принял текущий
        пользователь, либо пользователи, которые приняли заявку в друзья от
        текущего)"""
        session = db_session.create_session()
        friends_list = FriendsList()
        users_query = session.query(Users)
        for friend in self.incoming_friend_requests:
            if friend.is_accepted:
                user = users_query.filter(Users.id == friend.inviter_id).first()
                friends_list.append(user)
        for friend in self.outgoing_friend_requests:
            if friend.is_accepted:
                user = users_query.filter(Users.id == friend.invitee_id).first()
                friends_list.append(user)
        return friends_list

    def set_attributes(self, password):
        self.hashed_password = generate_password_hash(password)
        self.alternative_id = create_alternative_id()

    messages = orm.relation('Messages', backref='message_sender')
    chats = orm.relation('Chats', secondary='chat_participants',
                         backref='chat_member')
    friends = orm.relation('UsersFriends', backref='inviter',
                           foreign_keys=[UsersFriends.inviter_id])

    def set_attributes(self, password):
        self.hashed_password = generate_password_hash(password)
        self.api_key = create_api_key(self.email, self.created_date, password)
        self.alternative_id = create_alternative_id(random.randint(10, 20))
 database

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)

dependabot/pip/jinja2-2.11.3
    @wraps(SerializerMixin.to_dict)
    def to_dict(self, *args, **kwargs):
        result = super().to_dict(*args, **kwargs)
        if 'alternative_id' in result:
            result['user_id'] = result['alternative_id']
            del result['alternative_id']
        return result


class FriendsList(list):
    """Список друзей пользователя. При проверке наличия элемента в себе,
    проверяет, есть ли в списке пользователь с таким же id, как и у переданного
    пользователя."""

    def __contains__(self, user: Users):
        return any(friend.id == user.id for friend in self)
=======
    def get_id(self):
        return self.alternative_id
database
