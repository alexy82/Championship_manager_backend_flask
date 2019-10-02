"""
Base class for DB handlers
"""

import sqlalchemy

from app.core.utils.helpers import import_class_by_path
from configs import DATABASES


class DbBackendBase:
    """
    Base class
    """
    connections = {}

    def __init__(self):
        """
        Init method
        """
        for key, config in DATABASES.items():
            if key in self.connections:
                continue
            engine = import_class_by_path(config['ENGINE'])
            self.connections[key] = engine(config=config).create_engine()

    def get_connections(self):
        """
        Get list of active connections
        :return:
        """
        return self.connections

    def get_connection(self, name):
        """
        Get connection by name of config, if there is not exists then create one
        :param name: configuration name
        :return:
        """
        if name not in self.connections:
            config = DATABASES[name]
            engine = import_class_by_path(config['ENGINE'])
            self.connections[name] = engine(config=config).create_engine()
        return self.connections[name]


class BaseEngine:
    """
    Base Engine connection
    """
    config = {}

    def __init__(self, config=None):
        """
        Configuration from settings.py file
        :param config:
        """
        self.config = config

    def make_connection_string(self):
        """
        Make connection string by configured values
        :return: str
        """
        pass

    def create_engine(self):
        """
        Create engine for connections
        :return:
        """
        # return sqlalchemy.create_engine(self.make_connection_string(), **engine_options)
        engine_options = self.config.get('ENGINE_OPTIONS', {})
        return sqlalchemy.create_engine(self.make_connection_string(),
                                        **engine_options)


DB_CONNECTIONS = DbBackendBase()
