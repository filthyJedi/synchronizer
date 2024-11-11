# Synchronizer


Program that synchronizes two folders: source and replica. The program maintain a full, identical copy of source  folder at replica folder.


Takes four argument:
* --source - source folder path, should be absolute
* --replica - replica folder path, should be absolute
* --interval  - synchronization interval in seconds
* --log - log file path, should be absolute


Example of command:

python __init__.py --source="D:\synchronizer\source_folder" --replica="D:\synchronizer\replica_folder" --interval=60 --log="D:\synchronizer"