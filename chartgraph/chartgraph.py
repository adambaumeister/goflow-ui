from flask import render_template

class Graph:
    def __init__(self):
        self.name = ''

    def graph_from_rows(self, rows, label_index=0):
        labels = []
        data = []
        for row in rows:
            labels.append('"{0}"'.format(row[label_index]))
            for col in row[label_index+1:]:
                if type(col) is int:
                    data.append(str(col))
                else:
                    data.append(col)

        self.labels = ", ".join(labels)
        self.data = ", ".join(data)

    def render(self):
        c = {"name": self.name, "labels": self.labels, "data": self.data}
        return render_template("graph_bar.js", c=c)


