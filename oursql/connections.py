import sys

import umysql
import pymysql.connections

from .utils import setdocstring
from .cursors import Cursor

class Connection(pymysql.connections.Connection):
    @setdocstring(pymysql.connections.Connection.__init__)
    def __init__(self, *args, **kwargs):
        if 'cursorclass' not in kwargs:
            kwargs['cursorclass'] = Cursor
        self._umysql_conn = umysql.Connection()
        super(Connection, self).__init__(*args, **kwargs)

    @setdocstring(pymysql.connections.Connection.set_charset)
    def set_charset(self, charset):
        if charset:
            self._umysql_conn.query("SET NAMES %s", (charset,))
            self.charset = charset

    @setdocstring(pymysql.connections.Connection.autocommit)
    def autocommit(self, value):
        self._umysql_conn.query("SET AUTOCOMMIT = %s", (value,))

    @setdocstring(pymysql.connections.Connection.commit)
    def commit(self):
        self._umysql_conn.query('COMMIT')

    @setdocstring(pymysql.connections.Connection.close)
    def close(self):
        self._umysql_conn.close()

    def _connect(self):
        self._umysql_conn.connect(self.host, self.port, self.user,
                                  self.password, self.db, False, self.charset)

    def query(self, sql, args):
        try:
            return self._umysql_conn.query(sql, args)
        except umysql.SQLError, e:
            exc, value, tb = sys.exc_info()
            self.errorhandler(None, exc, value)

