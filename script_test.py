from backends import Schema
import re

s = Schema()
s.add_filter("src 53")
print(s.build_filter_string())
