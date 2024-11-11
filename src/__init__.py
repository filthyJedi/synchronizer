import time
import argparse
import schedule
import log
from synchronization_logic import *


def synchronization_process():
    scan_folder(source_folder_path, source_folder_dict)
    scan_folder(replica_folder_path, replica_folder_dict)
    synchronize(source_folder_path, replica_folder_path, source_folder_dict, replica_folder_dict)
    logger.info('Synchronized')


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Script that synchronize two folders"
    )
    parser.add_argument("--source", required=True, type=str)
    parser.add_argument("--replica", required=True, type=str)
    parser.add_argument("--interval", required=True, type=int)
    parser.add_argument("--log", required=True, type=str)
    args = parser.parse_args()

    source_folder_path = args.source
    replica_folder_path = args.replica
    synchronization_interval = args.interval
    log_file_path = args.log

    log.create_logger(log_file_path)

    ensure_dir_exist(source_folder_path)
    ensure_dir_exist(replica_folder_path)

    source_folder_dict = dict()
    replica_folder_dict = dict()


synchronization_process()
schedule.every(synchronization_interval).seconds.do(synchronization_process)
while True:
    schedule.run_pending()
    time.sleep(1)