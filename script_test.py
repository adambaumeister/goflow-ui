from backends import Backend, FilterString

f = FilterString(value="src 127.0.0.1 dst 1.1.1.1")
print(f.strings)
