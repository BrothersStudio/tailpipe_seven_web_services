import MySQLdb
import _mysql_exceptions
import os
import logging
from datetime import datetime


class mysqlInterview():

    logger = None

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.create_interviews_table()

    def create_conn(self):
        db = MySQLdb.connect(host=os.environ['MYSQL_ENDPOINT'],
                             user=os.environ['MYSQL_USER'],
                             passwd=os.environ['MYSQL_PASSWD'],
                             db=os.environ['MYSQL_DB']
                             )

        db.autocommit(True)
        return db.cursor()

    def create_interviews_table(self):

        conn = self.create_conn()

        try:
            conn.execute(
                """CREATE TABLE interviews 
                (message_id VARCHAR(200) NOT NULL, 
                level VARCHAR(3), 
                tag VARCHAR(20), 
                user VARCHAR(20), 
                message VARCHAR(612),
                PRIMARY KEY (message_id)
                )"""
            )
            self.logger.info('Interviews table successfully created.')
        except _mysql_exceptions.OperationalError as e:
            self.logger.info(e)
            self.logger.warning("Interviews table already exists, no action has been taken.")
        finally:
            conn.close()

    def insert_interview(self, level, tag, user, message):
        message_id = '{0}-{1}-{2}_{3}'.format(user, level, tag, str(datetime.now().strftime('%Y%m%d%H%M%S')))
        conn = self.create_conn()

        try:
            conn.execute("""INSERT INTO interviews (message_id, level, tag, user, message)
                        VALUES (%s, %s, %s, %s, %s);""", (message_id, level, tag, user, message))
        except Exception as e:
            print(e)
            self.logger.warning('Got Exception while inserting: {0}'.format(e))
            return False
        finally:
            conn.close()

        return True

    def select_interview(self, tag, level, user_id):
        conn = self.create_conn()

        try:
            conn.execute("""SELECT message FROM interviews
                            WHERE level = %s and tag = %s and (user <> %s OR user IS NULL)
                            ORDER BY RAND()
                            LIMIT 1""", (level, tag, user_id))
            response = conn.fetchall()

        except Exception as e:
            self.logger.warning('Got Exception while selecting: {0}'.format(e))
            return ()
        finally:
            conn.close()

        self.logger.info('Got raw response {0} from SELECT statement'.format(response))
        return response[0][0]


