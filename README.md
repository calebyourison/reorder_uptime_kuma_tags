# Reorder Tags Within Uptime Kuma (SQLite)
___

For those who enjoy and highly recommend [Uptime Kuma](https://github.com/louislam/uptime-kuma), this script is a Band-Aid approach to a [feature request](https://github.com/louislam/uptime-kuma/issues/1308) that will likely be implemented at some point in the future.

When creating tags they are displayed in their order of creation.  
When adding tags to monitors, the order in which they are added determines the display order.
There is currently no option to sort or reorder them.

**For installations running SQLite**, this script will perform a single database update and reorder the tags *alphabetically*.
The script will need to be run again in the event that further tags have been created and/or added to monitors.
For installations running MariaDB, a similar approach is likely possible, but not covered in this project.

**BACKUP YOUR DB FILE BEFORE ATTEMPTING ANY CHANGES.  
REVERTING TO THE ORIGINAL SQLITE FILE MAY BE NEEDED IF THE CHANGES ARE UNDESIRABLE OR DATA GETS CORRUPTED**

## Usage
___
**Did you create a backup of your db file yet?**

<u>Stop the Uptime Kuma process entirely first</u>.  Then copy the db file to a local path. Save a copy in a protected directory until you are certain everything worked as desired.
Once the changes have been applied, the db file should be copied back into the Uptime Kuma directory and then restarted. 
If the changes fail for some reason, revert to the protected copy.

The recommended way to use this script, especially for those unfamiliar with Python, is the `uv` approach.
Please see the [README](https://github.com/calebyourison/reorder_uptime_kuma_tags/blob/master/uv_run/README.md) for details on how to run it via this method.

For those with active Python environments, the `reorder_tags.py` script can instead be copied into your IDE and run via the `execute()` function.   

The function requires a local path to the db file.  
Optionally, one can disable the confirm parameter if running this script via automation as it requires user response.

**...Did you create a backup of your db file yet?**

```bash
my_db_file = 'some/path/to/file.db'

execute(my_db_file, confirm=True)
```
The `tag` table appears to determine the order in which tags are displayed in full list form (ie settings and homepage dropdown).
The `monitor_tag` table appears to determine the order in which tags are displayed on individual monitors.

If experimenting, the existing tables can be retrieved and displayed.

General List `tag`
````bash
conn = sqlite3.connect("/path/to/file.db")
cursor = conn.cursor()

tag_table = return_table_rows(cursor, "tag")

for row in tag_table:
    print(row)

# (Tag_ID, Name, Color, Creation Date)    
(3, 'My_website', '#4B5563', '2025-07-13 15:25:30')
(4, 'A_server', '#4B5563', '2025-07-13 17:34:31')
(5, 'Docker_Host', '#2563EB', '2025-07-13 19:20:54')
...

# Tag_ID determines the display order for the general list
````
Monitor Tags `monitor_tag`
```bash
conn = sqlite3.connect("/path/to/file.db")
cursor = conn.cursor()

monitor_tag_table = return_table_rows(cursor, "monitor_tag")

for row in monitor_tag_table:
    print(row)

# (ID, Monitor_ID, Tag_ID, Value) 
(11, 11, 3, '')
(13, 13, 3, '')
(16, 15, 4, '')
...

# ID determines the display order for tags added to individual monitors
```

The script identifies an *alphabetical* order for tags based on the tag names present in the `tag` table.
From there, it generates a mapping for {old_id: new_id} so that it can reorder the entries in both the `tag` table as well as the `monitor_tag` table.

It's highly recommend to perform periodic backups of your database.  You can run this script during that process if desired.

This works especially if using Docker and the container is stopped for a short while so the volume can be copied. 

