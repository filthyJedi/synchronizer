import hashlib
import os
import shutil
from element import Element
import logging

logger = logging.getLogger('synchronize_logger')


def ensure_dir_exist(folder_path):
    if not os.path.exists(folder_path):
        os.mkdir(folder_path)


# scan specified folder and list all elements it contains
def scan_folder(folder_path, folder_dictionary):
    for item in os.scandir(folder_path):
        is_dir = item.is_dir()
        file = Element(item.path, os.path.getsize(item.path), is_dir)
        folder_dictionary[file.path] = file
        if is_dir:
            scan_folder(item.path, folder_dictionary)


# compare two files by their hash
def hash_compare(path1, path2):
    hash1 = hashlib.md5(open(path1, 'rb').read()).hexdigest()
    hash2 = hashlib.md5(open(path2, 'rb').read()).hexdigest()
    return hash1 == hash2


# delete elements, that not exist in source folder, from replica folder
def replica_clean_up(source_folder_path, replica_folder_path, source_dict, replica_dict):
    for replica_item_key, replica_item_value in replica_dict.items():
        source_item_value = source_dict.get(replica_item_key.replace(replica_folder_path, source_folder_path))
        if source_item_value is None:
            try:
                if replica_item_value.is_dir:
                    shutil.rmtree(replica_item_value.path)
                else:
                    os.remove(replica_item_value.path)
                logger.info(f'Deleted file "{replica_item_value.path}"')
            except FileNotFoundError:
                pass
            except Exception:
                logger.exception('Error while element deletion')


# copy elements from source to replica folder and remove excess
def synchronize(source_folder_path, replica_folder_path, source_dict, replica_dict):
    for source_item_key, source_item_value in source_dict.items():

        replica_item_value = replica_dict.get(source_item_key.replace(source_folder_path, replica_folder_path))
        replica_copy_path = source_item_value.path.replace(source_folder_path, replica_folder_path)

        if replica_item_value is None:
            if source_item_value.is_dir:
                path_for_creation_dir = source_item_value.path.replace(source_folder_path, replica_folder_path)
                os.mkdir(path_for_creation_dir)
                logger.info(f'Created directory "{path_for_creation_dir}"')
            else:
                shutil.copyfile(source_item_value.path, replica_copy_path)
                logger.info(f'Copied file "{replica_copy_path}"')
        else:
            if source_item_value.is_dir:
                continue
            if source_item_value.size != replica_item_value.size:
                shutil.copyfile(source_item_value.path, replica_copy_path)
                logger.info(f'Copied file "{replica_copy_path}"')
            elif not hash_compare(source_item_value.path, replica_item_value.path):
                shutil.copyfile(source_item_value.path, replica_copy_path)
                logger.info(f'Copied file "{replica_copy_path}"')

    replica_clean_up(source_folder_path, replica_folder_path, source_dict, replica_dict)