import os

dirs = [
    os.path.join("data","raw"),
    os.path.join("data","processed"),
    "notebooks",
    "saved_models",
    "src"
]

#for all objsts in previous list we want to create a folders (directories) and since these folders are empty
#and we want to initialize git also, we will keep an empty git file here. pass means that
#when we open the file we wont do anything, just open it and store empty gitkeep file there

for dir_ in dirs:
    os.makedirs(dir_, exist_ok = True)
    with open(os.path.join(dir_,".gitkeep"), "w") as f:
        pass

#we create __init__.py inside source folder because we want to make sure we keep the source as python package

files = [
    "dvc.yaml",
    "params.yaml",
    ".gitignore",
    os.path.join("src","__init__.py")
]

for file_ in files:
    with open(file_, "w") as f:
        pass
