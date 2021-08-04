import env
from ssh import SSHHandler

import os
import json

def loop_validation(
    handler: object,
    head: str,
    contents: dict,
    target_contents: dict
) -> None:
    """The loop validation method handles recursive checking of files
    and folders for their existence on the remote host."""
    ss = handler
    arch_head = head
    arch_head_list = arch_head.split("/")[1:]
    for _item in contents:
        # Skip all informational fields
        if _item in ["type", "size"]:
            continue
        remote_value = target_contents
        if remote_value:
            for lookup in arch_head_list:
                remote_value = remote_value.get(lookup)
        if contents[_item]["type"] == "folder":
            # This is a folder

            # Validate folder exists on remote
            if not remote_value or _item not in remote_value:
                print("Item {} not in folder".format(_item))
                # Create folder as it does not exist on remote host
                ss._exec(
                    "mkdir -p {}{}/{}".format(
                        os.environ["REMOTE_HOST_FOLDER"],
                        arch_head,
                        _item
                    )
                )

            # Check sub folders recursively as defined by local host
            loop_validation(
                handler=ss,
                head="{}/{}".format(arch_head, _item),
                contents=contents[_item],
                target_contents=target_contents
            )
        else:
            # This is a file

            # Validate file exists on remote
            if  not remote_value or _item not in remote_value:
                print("Item {} not in folder".format(_item))
                # Copy file as it does not exist on remote host
                local_sub_path = "{}{}".format("\\", "\\")
                for _folder in arch_head_list:
                    local_sub_path = local_sub_path + _folder + "{}{}".format("\\", "\\")
                local_file_path = "{}{}{}".format(
                    os.environ["LOCAL_HOST_FOLDER"],
                    local_sub_path,
                    _item
                )
                with open(local_file_path, "r") as file:
                    file_contents = file.read()
                ss._open(
                    dest="{}{}".format(
                        os.environ["REMOTE_HOST_FOLDER"],
                        arch_head
                    ),
                    filename=_item,
                    contents=file_contents
                )

    return None


def forward_sync(handler):
    """The sync method takes a source and target and
    moves the file to the location"""
    # Set the SSH handler
    ss = handler

    folder_root = os.getcwd()

    with open(os.path.join(folder_root, "local_tree.json"), "r") as file:
        local_contents = json.loads(file.read())

    with open(os.path.join(folder_root, "remote_tree.json"), "r") as file:
        remote_contents = json.loads(file.read())

    loop_validation(
        handler=ss,
        head="",
        contents=local_contents,
        target_contents=remote_contents
    )

if __name__ == "__main__":
    ss = SSHHandler()
    ss._client()

    forward_sync(ss)