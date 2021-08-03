import env
from ssh import SSHHandler

import os
import json

def list_folder(handler, folder_path: str):
    """FOR LINUX:
    Lists all folders on the remote host by walking through the tree.
    """
    folder_contents_obj = {}
    # SSH handler
    ss = handler
    # Get remote file sizes
    command = "ls -l"  # fetches files and folder statistics
    response = ss._exec(
        "{} {}".format(
            command,
            folder_path
        )
    )
    # print(json.dumps(response, indent=4))

    stdout = response.get("stdout")
    if not stdout:
        return None
    
    # Get remote folder size on linux
    remote_base_folder_size = 0
    for line in stdout:
        sudo_file = line.replace("\n", "")
        clean_file_line = []
        for stdout_item in sudo_file.split(" "):
            if stdout_item:
                clean_file_line.append(stdout_item)
        if len(clean_file_line) != 9:
            continue
        item = clean_file_line[8]  # hard coded
        size = clean_file_line[4]  # hard coded for ls -l
        command = "file"  # validates if path is a file
        response = ss._exec(
            "{} {}".format(
                command,
                "{}/{}".format(folder_path, item)
            )
        )
        # print(json.dumps(response, indent=4))
        file_type_stdout = response.get("stdout")
        if not file_type_stdout:
            continue
        sudo_file_type_array = file_type_stdout[0].replace("\n", "").replace(":", "").split(" ")
        if "directory" in sudo_file_type_array:
            sub_folder_contents_obj = list_folder(
                ss,
                "{}/{}".format(folder_path, item)
            )
            folder_contents_obj[item] = {
                "type": "folder",
                "size": 0,
            }
            if sub_folder_contents_obj:
                for sub_item in sub_folder_contents_obj:
                    folder_contents_obj[item][sub_item] = sub_folder_contents_obj[sub_item]
        else:
            folder_contents_obj[item] = {
                "type": "file",
                "size": int(size),
            }

    # print(json.dumps(folder_contents_obj, indent=4))
    return folder_contents_obj

if __name__ == "__main__":
    ss = SSHHandler()
    ss._client()
    folder_contents_list = list_folder(
        ss,
        os.environ.get("REMOTE_HOST_FOLDER")
    )
    with open(os.path.join(os.getcwd(), "remote_tree.json"), "w") as file:
        file.write(json.dumps(folder_contents_list, indent=4))
    print("Finished")