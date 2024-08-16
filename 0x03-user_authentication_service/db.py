#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound
from user import Base, User


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db")
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        '''takes email and hashed_password and returns User object'''
        new_user = User(email=email, hashed_password=hashed_password)
        session = self._session
        session.add(new_user)
        session.commit()
        return new_user

    def find_user_by(self, **kwargs) -> User:
        """
        A method that takes arbitrary keyword argument,
        with which it filters a query.
        """
        session = self._session
        try:
            query = session.query(User).filter_by(**kwargs).one()
            if not query:
                raise NoResultFound()
        except AttributeError as error:
            raise InvalidRequestError()
        return query

    def update_user(self, user_id: int, **kwargs) -> None:
        '''updates user object'''
        session = self._session
        try:
            query = self.find_user_by(id=user_id)
            user_attr = query.__dict__
            for attr, val in kwargs.items():
                if attr in user_attr:
                    setattr(query, attr, val)
                else:
                    raise ValueError()
            session.commit()
        except AttributeError as error:
            raise ValueError()
