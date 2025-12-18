import sqlite3

def return_table_rows(sqlite_cursor: sqlite3.Cursor, table:str) -> list[tuple]:
    """Return a list of rows from a given table using a pre-defined Cursor"""

    sqlite_cursor.execute(f"SELECT * FROM {table}")

    rows: list[tuple] = sqlite_cursor.fetchall()

    return rows


def tag_id_mapping(sqlite_cursor:sqlite3.Cursor, table:str="tag") -> dict[int, int]:
    """Generate a mapping of old_tag_id: new_tag_id based on alphabetical sorting from existing tag names"""

    id_mapping: dict[int, int] = {}

    # Each tag row exists in the form (id, name, color, created_date)
    tags: list[tuple] = return_table_rows(sqlite_cursor=sqlite_cursor, table=table)

    # Create a mapping for name:existing_id
    name_tag_id: dict[str, int] = {tag[1]: tag[0] for tag in tags}

    # Define new alphabetical sorting order based on tag names
    sorted_tag_names: list[str] = sorted([tag_name for tag_name in name_tag_id.keys()])

    new_tag_id = 1

    # New sequential id numbers mapped to the old ones
    for name in sorted_tag_names:
        old_tag_id: int = name_tag_id.get(name)

        id_mapping[old_tag_id] = new_tag_id

        new_tag_id += 1

    return id_mapping


def generate_new_tag_rows(sqlite_cursor:sqlite3.Cursor, table:str="tag") -> list[tuple]:
    """Return table rows from (tag) updated with/sorted by new tag id numbers"""

    new_id_mapping: dict[int, int] = tag_id_mapping(sqlite_cursor=sqlite_cursor, table=table)

    tag_rows: list[tuple] = return_table_rows(sqlite_cursor=sqlite_cursor, table=table)

    updated_rows: list[tuple] = []

    # Create new tuple for each row with new tag id number
    for (old_id, name, color, created_date) in tag_rows:
        updated_row: tuple[int, str, str, str] = (new_id_mapping.get(old_id), name, color, created_date)
        updated_rows.append(updated_row)

    # Sort by the new id numbers
    sorted_rows: list[tuple] = sorted(updated_rows, key=lambda x: x[0])

    return sorted_rows


def generate_new_monitor_id_rows(sqlite_cursor:sqlite3.Cursor, table:str="monitor_tag") -> list[tuple]:
    """Return table rows from (monitor_tag) updated with/sorted by new tag id numbers"""

    new_id_mapping: dict[int, int] = tag_id_mapping(sqlite_cursor=sqlite_cursor, table='tag')

    # Each row of monitor_tag includes (id, monitor_id, tag_id, value)
    monitor_id_rows: list[tuple] = return_table_rows(sqlite_cursor=sqlite_cursor, table=table)

    rows_with_updated_tag_id: list[tuple] = []

    # Update the tag_id based on new mapping
    for (sorting_id, monitor_id, old_tag_id, value) in monitor_id_rows:
        new_row: tuple[int, int, int, str] = (sorting_id, monitor_id, new_id_mapping.get(old_tag_id), value)
        rows_with_updated_tag_id.append(new_row)


    # Sort the tuples based on the updated tag_id, third value in the tuple
    sorted_values: list[tuple] = sorted(rows_with_updated_tag_id, key=lambda x: x[2])

    final_output: list[tuple] = []

    new_sorting_id = 1

    # New sorting ID numbers will be based on lowest number (updated) tag_id
    # Monitor tags will not be grouped by creation date any longer
    for (old_sorting_id, monitor_id, updated_tag_id, value) in sorted_values:
        final_row: tuple[int, int, int, str] = (new_sorting_id, monitor_id, updated_tag_id, value)
        final_output.append(final_row)

        new_sorting_id += 1

    return final_output

def rewrite_tables(sqlite_cursor:sqlite3.Cursor) -> None:
    """Rewrite the tag and monitor_tag tables with new values"""
    #sqlite_cursor.execute("PRAGMA foreign_keys=OFF;")

    # tag table
    new_tag_table = generate_new_tag_rows(sqlite_cursor=sqlite_cursor, table='tag')

    # monitor_tag table
    new_monitor_tag_table = generate_new_monitor_id_rows(sqlite_cursor=sqlite_cursor, table='monitor_tag')

    sqlite_cursor.execute("DELETE FROM tag")
    sqlite_cursor.executemany("""INSERT INTO tag (id, name, color, created_date) VALUES (?, ?, ?, ?)""", new_tag_table)

    sqlite_cursor.execute("DELETE FROM monitor_tag")
    sqlite_cursor.executemany("INSERT INTO monitor_tag (id, monitor_id, tag_id, value) VALUES (?, ?, ?, ?)", new_monitor_tag_table)

    #sqlite_cursor.execute("PRAGMA foreign_keys=ON;")


def interactive(sqlite_cursor:sqlite3.Cursor) -> None:
    """Require user to view and confirm changes"""
    print("Existing tag rows (id, name, color, created_date):\n")
    existing_tag_rows = return_table_rows(sqlite_cursor=sqlite_cursor, table="tag")
    for row in existing_tag_rows:
        print(row)

    print("----------\n")

    print("Proposed update to tag rows (id, name, color, created_date):\n")
    proposed_tag_rows = generate_new_tag_rows(sqlite_cursor=sqlite_cursor, table="tag")
    for row in proposed_tag_rows:
        print(row)

    print('')

    user_choice = input("Would you like to commit these changes? (y/n)")

    if user_choice.lower() == 'y':
        rewrite_tables(sqlite_cursor)
    elif user_choice.lower() == 'n':
        print("Aborting Changes")

    else:
        print("Invalid selection, repeating")
        interactive(sqlite_cursor)


def execute(uptime_kuma_db:str, confirm:bool=True) -> None:
    """
    Perform updates, require user confirmation by default

    :param uptime_kuma_db: path to uptime kuma sqlite database
    :type uptime_kuma_db: str

    :param confirm: Option to display changes via and request user input
    :type confirm: bool

    """
    conn = sqlite3.connect(uptime_kuma_db)

    cursor = conn.cursor()

    if confirm:
        interactive(cursor)
    else:
        rewrite_tables(cursor)


    conn.commit()

    conn.close()
