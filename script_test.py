from backends import Schema

s = Schema()
s.add_filter("src 127.0.0.1")
print(s.build_filter_string())
