# Reorder Tags Within Uptime Kuma (SQLite)
___

For those who enjoy and highly recommend [Uptime Kuma](https://github.com/louislam/uptime-kuma), this script is a Band-Aid approach to a [feature request](https://github.com/louislam/uptime-kuma/issues/1308) that will likely be implemented at some point in the future.

When creating tags they are displayed in their order of creation.  
When adding tags to monitors, the order in which they are added determines the display order.
There is currently no option to sort or reorder them.

**For installations running SQLite**, this script will perform a single database update and reorder the tags alphabetically.
The script will need to be run again in the event that further tags have been created and/or added to monitors.
For installations running MariaDB, a similar approach is likely possible, but not covered in this project.

**BACKUP YOUR DB FILE BEFORE ATTEMPTING ANY CHANGES.  
REVERTING TO THE ORIGINAL SQLITE FILE MAY BE NEEDED IF THE CHANGES ARE UNDESIRABLE OR DATA GETS CORRUPTED**

## Usage
___
**Did you create a backup your db file yet?**

Ideally, stop the process entirely first.  Then copy the db file to a local path.

The recommended way to use this script, especially for those unfamiliar with Python, is the `uv` approach.
Please see the [README]() for details on how to run it via this method.

For those with active Python environments, the `reorder_tags.py` script can be copied into your IDE and run via the `execute()` function.
The function requires a local path to the db file.  
Optionally, one can disable the confirm parameter if running this script via automation as it requires user response.

```bash
my_db_file = 'some/path/to/file.db'

execute(my_db_file, confirm=True)
```

The script is fairly basic.  
The process identifies an alphabetical order for tags based on the name present in the `tag` table.
From their, it generates a mapping for {new_id:old_id} so that it can reorder the entries in both the `tag` table as well as the `monitor_tag` table.

It's highly recommend to perform periodic backups of your database.  You can run this script during that process if desired.

This works especially well with Docker if the container is stopped for a short while so the volume can be copied. 

