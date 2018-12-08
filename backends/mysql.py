from .default import Backend
import mysql.connector
from chartgraph import Graph
import re

class Mysql_backend(Backend):
    def __init__(self, OPTIONS):
        super().__init__()
        print("Got this far")
        self.required_opts = ['host', 'user', 'passwd', 'db']
        self.parse_options(OPTIONS)
        self.columns = {}

        self.db = mysql.connector.connect(
            host=self.OPTIONS['host'],
            user=self.OPTIONS['user'],
            passwd=self.OPTIONS['passwd']
        )

        self.filter_map = {
            "\d+\-\d+\-\d+": TimeFilter
        }
        self.schema = Schema()

        self.filters = []

    def get_columns(self):
        return self.schema.get_columns()

    def add_filter(self, op, value):
        for regex, f in self.filter_map.items():
            if re.match(regex, value):
                filter = f(op, value)
                self.schema.add_filter(filter)

    def get_int_columns(self):
        return self.schema.get_int_columns()

    def topn_graph(self, field, limit=10):
        db = self.db
        self.schema.limit = limit
        FLOWS_PER_IP = self.schema.topn(field)

        cursor = db.cursor()
        cursor.execute("USE testgoflow")
        cursor.execute(FLOWS_PER_IP)
        r = cursor.fetchall()
        g = Graph()
        g.name = "topn_{0}".format(field)
        g.graph_from_rows(r, 0)
        return g

    def topn_sum_graph(self, field, sum_by, limit=10):
        db = self.db
        self.schema.limit = limit
        FLOWS_PER_IP = self.schema.topn_sum(field, sum_by)

        cursor = db.cursor()
        cursor.execute("USE testgoflow")
        cursor.execute(FLOWS_PER_IP)
        r = cursor.fetchall()
        g = Graph()
        g.name = "TopN {0}".format(field)
        g.graph_from_rows(r, 0)
        return g

class TimeFilter:
    def __init__(self, op, value):
        self.op = op
        self.value = value

    def get_query_string(self):
        return "last_switched {0} \"{1}\"".format(self.op, self.value)

class Column:
    """
    Column

    Column handling class.
    Governs how query strings are built and helper functons for returned data.
    """
    def __init__(self, name, display_name=None):
        self.name = name
        self.display_name = display_name
        self.type = 'text'

    def get_display_name(self):
        return self.display_name

    def select(self):
        return "{0}".format(self.name)


class IP4Column(Column):
    def __init__(self, name, display_name=None):
        super().__init__(name, display_name)
        self.type = "ip"

    def select(self):
        return "inet_ntoa({0})".format(self.name)

class IntColumn(Column):
    def __init__(self, name, display_name=None):
        super().__init__(name, display_name)
        self.type = 'int'

    def select(self):
        return "{0}".format(self.name)

class Schema:
    """
    Schema

    Defines the backend schema
    Changes to the backend (naming, etc.) should be reflected here.
    """
    def __init__(self):
        # Default
        self.limit = 10

        # Columns
        self.columns = {
            "last_switched": Column("last_switched", "Last Switched"),
            "src_ip": IP4Column("src_ip", "Source IP"),
            "src_port": Column("src_port", "Source Port"),
            "dst_ip": IP4Column("dst_ip", "Destination IP"),
            "dst_port": Column("dst_port", "Destination Port"),
            "in_bytes": IntColumn("in_bytes", "Input bytes"),
        }

        # Supported queries
        self.QUERIES = {
            "TOPN": self.topn
        }

        self.filters = []

    def add_filter(self, filter):
        self.filters.append(filter)
        print(self.build_filter_string())

    def build_filter_string(self):
        s = 'WHERE '
        l = []
        for f in self.filters:
            l.append(f.get_query_string())

        if len(l) > 0:
            return s + " AND ".join(l)
        else:
            return ''

    def get_columns(self):
        result = {}
        for col_name, col in self.columns.items():
            result[col_name] = col.get_display_name()

        return result

    def get_int_columns(self):
        result = {}
        for col_name, col in self.columns.items():
            if col.type is "int":
                result[col_name] = col.get_display_name()

        return result

    def topn(self, column):
        count = "last_switched"
        q = """
        SELECT {0}, count({1}) AS c FROM goflow_records {2} GROUP BY {0} ORDER BY c DESC
        """.format(self.columns[column].select(), count, self.build_filter_string())
        return self.query_boilerplate(q)

    def topn_sum(self, column, sum_by):
        q = """
        SELECT {0}, sum({1}) AS c FROM goflow_records {2} GROUP BY {0} ORDER BY c DESC
        """.format(self.columns[column].select(), sum_by, self.build_filter_string())
        return self.query_boilerplate(q)

    def query_boilerplate(self, q):
        q = q + """LIMIT {0}""".format(self.limit)
        return q
