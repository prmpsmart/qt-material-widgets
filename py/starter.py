from os import mkdir, walk, makedirs, path, getcwd


f = r"C:\Users\Administrator\Coding_Projects\Python\Dev_Workspace\Qt_Material_Widgets\cpp\qt-material-widgets-master\components"
try:
    mkdir("examples")
    mkdir("components")
except:
    ...

for a, b, c in walk(f):
    for ba in b:
        g = path.join(a, ba).replace(f, "components")
        # g = path.join("components", g)
        try:
            makedirs(g)
        except:
            ...
