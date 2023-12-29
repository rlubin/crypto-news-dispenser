import datetime
import sqlite3


def execute_scripts_from_file(db_path, filename):
    con = sqlite3.connect(db_path)
    cur = con.cursor()
    # con.set_trace_callback(print)

    fd = open(filename, 'r')
    sqlFile = fd.read()
    fd.close()

    # all SQL commands (split on ';')
    sqlCommands = sqlFile.split(';')

    for command in sqlCommands:
        try:
            cur.execute(command)
        except Exception as error:
            print("Command skipped: ", error)


def db_setup(db_path):
    con = sqlite3.connect(db_path)
    cur = con.cursor()
    # con.set_trace_callback(print)

    try:
        res = cur.execute("SELECT name FROM sqlite_master")
        tables = res.fetchone()

        # if table doesn't exist create
        if "articles" not in tables:
            print("articles table does not exist, creating...")
            execute_scripts_from_file("setup.sql")

    except Exception as error:
        print(error)

    con.close()


def does_article_exist(db_path, article_name, article_url):
    con = sqlite3.connect(db_path)
    cur = con.cursor()
    # con.set_trace_callback(print)
    rows = []

    try:
        cmd = "SELECT * FROM articles WHERE articleName=? AND articleUrl=?"
        cur.execute(cmd, (article_name, article_url))
        rows = cur.fetchall()
    except Exception as error:
        print(error)

    con.close()

    if len(rows) > 0:
        return True
    return False


def add_article(db_path, article_name, article_url):
    con = sqlite3.connect(db_path)
    cur = con.cursor()
    # con.set_trace_callback(print)

    try:
        cmd = "INSERT INTO articles (articleName, articleUrl, linkTime) VALUES (?, ?, ?)"
        date_string = datetime.datetime.now().isoformat()
        cur.execute(cmd, (article_name, article_url, date_string))
        con.commit()
    except Exception as error:
        print(error)

    con.close()
