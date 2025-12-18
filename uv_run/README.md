# uv_run to Reorder Tags Within Uptime Kuma (SQLite)
___
**Did you create a backup of your db file yet?**

Install [uv](https://docs.astral.sh/uv/getting-started/installation/).

Copy the folder to your device and unzip.
 ```bash
curl -L -o reorder_uptime_kuma_tags.zip https://github.com/calebyourison/reorder_uptime_kuma_tags/releases/download/reorder_uptime_kuma_tags/uv_run.zip

unzip reorder_uptime_kuma_tags.zip
 ```

You can run the script with `uv run`

The script is looking for two variables: a path to the sqlite file and a True/False selection for user input confirmation (set to True for first time users, False for automation).

You can navigate into the directory or use its absolute path and chain everything into a one-liner:

```bash
    # Path to script folder                                   # Path to db file   # True/False user confirmation      
cd /some/path/to/reorder_uptime_kuma_tags && uv run main.py /some/path/to/kuma.db True
```
