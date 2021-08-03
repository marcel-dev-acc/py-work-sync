import env

import os
import json

def list_folder(folder_path: str):
    """FOR WINDOWS:
    Lists all folders within a local host by walking through the tree.
    """
    folder_contents_obj = {}
    folder_contents = os.listdir(folder_path)
    # List all items in the folder
    for item in folder_contents:
        item_is_file = os.path.isfile(
            os.path.join(
                folder_path,
                item
            )
        )
        # Identify if item is a sub-folder
        sub_folder_contents_obj = None
        if not item_is_file:
            sub_folder_contents_obj = list_folder(
                os.path.join(
                    folder_path,
                    item
                )
            )
        # Calculate the file sizes
        file_size = 0
        if item_is_file:
            file_size = os.path.getsize(
                os.path.join(
                    folder_path,
                    item
                )
            )
        # Create folder tree object
        folder_contents_obj[item] = {
            "type": "file" if item_is_file else "folder",
            "size": file_size,
        }
        # Add sub-folders into object
        if sub_folder_contents_obj is not None:
            for sub_item in sub_folder_contents_obj:
                folder_contents_obj[item][sub_item] = sub_folder_contents_obj[sub_item]


    # print(json.dumps(folder_contents_obj, indent=4))
    return folder_contents_obj


if __name__ == "__main__":
    folder_contents_list = list_folder(
        os.environ.get("LOCAL_HOST_FOLDER")
    )
    with open(os.path.join(os.getcwd(), "local_tree.json"), "w") as file:
        file.write(json.dumps(folder_contents_list, indent=4))
    print("Finished")

