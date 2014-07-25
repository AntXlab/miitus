from __future__ import absolute_import
from sqlalchemy.ext.declarative import declarative_base
from .utils import Singleton

class Preparation(Singleton):
    """
    everything declarative
    """
    def __init__(self):
        super(Preparation, self).__init__()

        self.__sql_base = declarative_base()

    @property
    def Base(self):
        """
        get declarative_base of sqlalchemy
        """
        return self.__sql_base

