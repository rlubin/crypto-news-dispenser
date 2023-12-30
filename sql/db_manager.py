import datetime
import os
import sqlite3
import logging


class Db_manager:

    def __init__(self):
        self.db_path = os.path.abspath(os.getenv('DB_PATH'))
        self.sql_setup_path = os.path.abspath(os.getenv('SQL_SETUP_PATH'))
        self.setup()

    def execute_scripts_from_file(self, con, filename):
        cur = con.cursor()
        # con.set_trace_callback(print)

        fd = open(filename, 'r')
        sqlFile = fd.read()
        fd.close()

        # all SQL commands (split on ';')
        sqlCommands = sqlFile.split(';')

        for command in sqlCommands:
            try:
                logging.info(command)
                cur.execute(command)
            except Exception as error:
                logging.error(f"Command skipped: {error}")

    def setup(self):
        con = sqlite3.connect(self.db_path)
        cur = con.cursor()
        # con.set_trace_callback(print)

        try:
            res = cur.execute(
                "SELECT name FROM sqlite_master WHERE type='table'")
            tables = res.fetchone()

            # if table doesn't exist create
            if tables is None or "articles" not in tables:
                logging.info("articles table does not exist, creating...")
                self.execute_scripts_from_file(con, self.sql_setup_path)

        except Exception as error:
            logging.error(error)

        con.close()

    def does_article_exist(self, article_name, article_url):
        con = sqlite3.connect(self.db_path)
        cur = con.cursor()
        # con.set_trace_callback(print)
        rows = []

        try:
            cmd = "SELECT * FROM articles WHERE articleName=? AND articleUrl=?"
            cur.execute(cmd, (article_name, article_url))
            rows = cur.fetchall()

        except Exception as error:
            logging.error(error)

        con.close()

        if len(rows) > 0:
            return True

        return False

    def add_article(self, article_name, article_url):
        con = sqlite3.connect(self.db_path)
        cur = con.cursor()
        # con.set_trace_callback(print)

        try:
            cmd = "INSERT INTO articles (articleName, articleUrl, linkTime) VALUES (?, ?, ?)"
            date_string = datetime.datetime.now().isoformat()
            cur.execute(cmd, (article_name, article_url, date_string))
            con.commit()

        except Exception as error:
            logging.error(error)

        con.close()
