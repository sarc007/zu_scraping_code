import ast


file = open(".\data\ZU_version_.json", "r")

contents = file.read()
dictionary = ast.literal_eval(contents)

file.close()

print(type(dictionary))
