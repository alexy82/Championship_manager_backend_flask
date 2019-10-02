"""
MySQL Handlers
"""
from app.core.db.backends.base import BaseEngine


class MySQLDB(BaseEngine):
    """
    Engine to connect to mysql
    """

    def make_connection_string(self):
        """
        Make connection string
        :return:
        """
        connection_str = 'mysql+mysqldb://{username}:{password}@{host}:{port}/{name}'.format(
            username=self.config.get('USERNAME', ''),
            password=self.config.get('PASSWORD', ''),
            host=self.config.get('HOST', '127.0.0.1'),
            port=self.config.get('PORT', '1433'),
            name=self.config.get('NAME', ''))
        return connection_str
