# Synchronizer


Program that synchronizes two folders: source and replica. The program maintain a full, identical copy of source  folder at replica folder.


Takes four argument:
* --source - source folder path
* --replica - replica folder path
* --interval  - synchronization interval in seconds
* --log - log file path


Example of command:

python __init__.py --source="D:\synchronizer\source_folder" --replica="D:\synchronizer\replica_folder" --interval=60 --log="D:\synchronizer"