from flask import Flask, render_template
from datetime import datetime
import sqlite3

app = Flask(__name__)


@app.route('/')
def index():
    # return render_template('index.html')

    database_contents = ''

    conn = sqlite3.connect('sqlite/library.db')
    try:
        c = conn.cursor()
        rows = c.execute('SELECT * FROM book_book')
        for row in rows:
            database_contents += f"<p>{row}</p>\n"
        return '<h1>Database Content test:</h1>' + database_contents
    finally:
        conn.close()
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')

