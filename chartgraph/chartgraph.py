from flask import render_template

class Graph:
    def __init__(self):
        self.name = ''
        self.table = Table()
        self.table_data = ''

    def graph_from_rows(self, rows, label_index=0):
        labels = []
        data = []
        self.table_data = self.table.table_from_rows(rows)
        for row in rows:
            labels.append('"{0}"'.format(row[label_index]))
            for col in row[label_index+1:]:
                data.append(str(col))

        self.labels = ", ".join(labels)
        self.data = ", ".join(data)

    def render(self):
        c = {"name": self.name, "labels": self.labels, "data": self.data}
        return render_template("graph_bar.js", c=c) + self.table_data

class Table:
    def __init__(self):
        self.name = ''

    def table_from_rows(self, rows):
        return render_template("table.html", rows=rows)