import os
import json

def comparison():
    folder_root = os.getcwd()
    with open(os.path.join(folder_root, "local_tree.json"), "r") as file:
        local_contents = json.loads(file.read())

    with open(os.path.join(folder_root, "remote_tree.json"), "r") as file:
        remote_contents = json.loads(file.read())

    if local_contents == remote_contents:
        return "Matched"
    else:
        return "Not matched"

if __name__ == "__main__":
    result = comparison()
    print(result)
