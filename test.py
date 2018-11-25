import mysql.connector
import os
from flask import Flask
from flask import render_template

FLOWS_PER_IP = """
SELECT  inet_ntoa(dst_ip), count(last_switched) last_switched FROM goflow_records group by inet_ntoa(dst_ip)
"""

pw = os.environ.get("SQL_PASSWORD")
db = mysql.connector.connect(
    host="52.62.226.159",
    user="testgoflow",
    passwd=pw
)
app = Flask(__name__)

@app.route('/')
def test():
    cursor = db.cursor()
    cursor.execute("USE testgoflow")
    cursor.execute(FLOWS_PER_IP)
    r = cursor.fetchall()
    labels = []
    data = []
    for row in r:
        labels.append('"{0}"'.format(row[0]))
        data.append(str(row[1]))
    c = { "labels": ", ".join(labels), "data": ", ".join(data)}
    return render_template("test.html", items=c)