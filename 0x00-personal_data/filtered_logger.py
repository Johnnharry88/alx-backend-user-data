#!/usr/bin/env python3
"""Module that selects items using reges, porecess using log
fomatter, creates a logger, connects to a secure database,
reads and filters data"""
import re
from typing import List
import logging
import os
import mysql.connector


# PII FIELDS contains fields of user that considered personal data
PII_FIELDS = ('name', 'password', 'phone', 'ssn', 'email')


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """ Returns Obfscated log message"""
    for f in fields:
        message = re.sub(f+'=.*?'+separator,
                         f+'='+redaction+separator, message)
    return message


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """Filters values from records moving into log reords
        using filter_datum"""
        ms = super(RedactingFormatter, self).format(record)
        output = filter_datum(self.fields, self.REDACTION, ms, self.SEPARATOR)
        return output


def get_logger() -> logging.Logger:
    """Functions that returns an object of logging.Logger"""
    logger = logging.getLogger('user_data')
    logger.setLevel(logging.INFO)
    logger.propagate = False
    streamer = logging.StreamHandler()
    streamer.setFormatter(RedactingFormatter(PII_FIELDS))
    logger.addHandler(streamer)
    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """Connects to our database"""
    user = os.getenv('PERSONAL_DATA_DB_USERNAME', 'root')
    pasdkey = os.getenv('PERSONAL_DATA_DB_PASSWORD', "")
    host = os.getenv('PERSONAL_DATA_DB_HOST', 'localhost')
    db = os.getenv('PERSONAL_DATA_DB_NAME')
    connect = mysql.connector.connect(
        user=user,
        password=pasdkey,
        host=host,
        database=db,
        )
    return connect


def main():
    """Reads from Database"""
    db = get_db()
    logger = get_logger()
    cursor = db.cursor()
    cursor.execute('SELECT * FROM users;')
    fields = cursor.column_names
    for r in cursor:
        msg = "".join('{}={}; '.format(x, y) for x, y in zip(fields, r))
        logger.info(msg.strip())
    cursor.close()
    db.close()


if __name__ == "__main__":
    main()
