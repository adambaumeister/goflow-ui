from backends import Schema

s = Schema()
s.add_filter("dst 152.83.247.1")
print(s.build_filter_string())
