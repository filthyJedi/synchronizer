import os
from element import Element
import shutil
import hashlib

source_folder_path = "D:\python_projects\synchronizer\source_folder"
replica_folder_path = "D:\python_projects\synchronizer\\replica_folder"

source_folder_dict = dict()
replica_folder_dict = dict()


def scan_folder(folder_path, folder_dictionary):
    for item in os.scandir(folder_path):
        # relative_path = item.path.replace(folder_path, '')
        is_dir = item.is_dir()
        file = Element(item.path, os.path.getsize(item.path), is_dir)
        folder_dictionary[file.path] = file
        if is_dir:
            scan_folder(item.path, folder_dictionary)


def hash_compare(path1, path2):
    p = open(path1, 'rb').read()
    o = open(path2, 'rb').read()
    hash1 = hashlib.md5(open(path1, 'rb').read()).hexdigest()
    hash2 = hashlib.md5(open(path2, 'rb').read()).hexdigest()
    return hash1 == hash2


def replica_clean_up(source_dict, replica_dict):
    for replica_item_key, replica_item_value in replica_dict.items():
        source_item_value = source_dict.get(replica_item_key.replace(replica_folder_path, source_folder_path))
        if source_item_value is None:
            try:
                shutil.rmtree(replica_item_value.path)
            except FileNotFoundError:
                print(f"File '{replica_item_value.path}' not found.")
            except Exception:
                print('some exeption')

def synchronize(source_dict, replica_dict):
    for source_item_key, source_item_value in source_dict.items():
        replica_item_value = replica_dict.get(source_item_key.replace(source_folder_path, replica_folder_path))
        if replica_item_value is None:
            if source_item_value.is_dir:
                path_for_copy_dir = source_item_value.path.replace(source_folder_path, replica_folder_path)
                os.mkdir(path_for_copy_dir)
            else:
                replica_path = source_item_value.path.replace(source_folder_path, replica_folder_path)
                shutil.copyfile(source_item_value.path, replica_path)

        else:
            if source_item_value.is_dir:
                continue
            if source_item_value.size != replica_item_value.size:
                replica_path = source_item_value.path.replace(source_folder_path, replica_folder_path)
                shutil.copyfile(source_item_value.path, replica_path)
            elif not hash_compare(source_item_value.path, replica_item_value.path):
                replica_path = source_item_value.path.replace(source_folder_path, replica_folder_path)
                shutil.copyfile(source_item_value.path, replica_path)

    replica_clean_up(source_dict, replica_dict)


scan_folder(source_folder_path, source_folder_dict)
scan_folder(replica_folder_path, replica_folder_dict)
print(source_folder_dict)
for k, v in source_folder_dict.items():
    print(v.path)
print(replica_folder_dict)
synchronize(source_folder_dict, replica_folder_dict)
