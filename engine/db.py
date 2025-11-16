import csv
import sqlite3

conn = sqlite3.connect("jarvis.db")
cursor = conn.cursor()

query = "CREATE TABLE IF NOT EXISTS sys_command(id integer primary key, name VARCHAR(100), path VARCHAR(1000))"
cursor.execute(query)

# Insert system commands with proper duplicate handling
commands_to_insert = [
    ('one note', 'C:\\Program Files\\Microsoft Office\\root\\Office16\\ONENOTE.exe'),
    ('file explorer', 'C:\\Windows\\explorer.exe'),
    ('file explore', 'C:\\Windows\\explorer.exe'),
    ('Microsoft Edge', 'C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe'),
    ('firefox', 'C:\\Program Files\\Mozilla Firefox\\firefox.exe'),
    ('mozilla firefox', 'C:\\Program Files\\Mozilla Firefox\\firefox.exe'),
    ('chrome', 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe'),
    ('google chrome', 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe'),
    ('powerpoint', 'C:\\Program Files\\Microsoft Office\\root\\Office16\\powerpoint.exe'),
    ('power', 'C:\\Program Files\\Microsoft Office\\root\\Office16\\powerpoint.exe'),
    ('power point', 'C:\\Program Files\\Microsoft Office\\root\\Office16\\powerpoint.exe'),
    ('command prompt', 'C:\\windows\\system32\\cmd.exe'),
    ('notepad plus plus', 'C:\\Program Files\\Notepad++\\notepad++.exe'),
    # Microsoft Office applications
    ('ms word', 'C:\\Program Files\\Microsoft Office\\root\\Office16\\WINWORD.exe'),
    ('microsoft word', 'C:\\Program Files\\Microsoft Office\\root\\Office16\\WINWORD.exe'),
    ('word', 'C:\\Program Files\\Microsoft Office\\root\\Office16\\WINWORD.exe'),
    ('ms excel', 'C:\\Program Files\\Microsoft Office\\root\\Office16\\EXCEL.exe'),
    ('microsoft excel', 'C:\\Program Files\\Microsoft Office\\root\\Office16\\EXCEL.exe'),
    ('excel', 'C:\\Program Files\\Microsoft Office\\root\\Office16\\EXCEL.exe'),
    ('ms powerpoint', 'C:\\Program Files\\Microsoft Office\\root\\Office16\\POWERPNT.exe'),
    ('microsoft powerpoint', 'C:\\Program Files\\Microsoft Office\\root\\Office16\\POWERPNT.exe'),
    ('ms outlook', 'C:\\Program Files\\Microsoft Office\\root\\Office16\\OUTLOOK.exe'),
    ('microsoft outlook', 'C:\\Program Files\\Microsoft Office\\root\\Office16\\OUTLOOK.exe'),
    ('outlook', 'C:\\Program Files\\Microsoft Office\\root\\Office16\\OUTLOOK.exe'),
    ('ms access', 'C:\\Program Files\\Microsoft Office\\root\\Office16\\MSACCESS.exe'),
    ('microsoft access', 'C:\\Program Files\\Microsoft Office\\root\\Office16\\MSACCESS.exe'),
    ('access', 'C:\\Program Files\\Microsoft Office\\root\\Office16\\MSACCESS.exe'),
    ('ms publisher', 'C:\\Program Files\\Microsoft Office\\root\\Office16\\MSPUB.exe'),
    ('microsoft publisher', 'C:\\Program Files\\Microsoft Office\\root\\Office16\\MSPUB.exe'),
    ('publisher', 'C:\\Program Files\\Microsoft Office\\root\\Office16\\MSPUB.exe'),
    # Additional common applications
    ('notepad', 'C:\\Windows\\System32\\notepad.exe'),
    ('calculator', 'C:\\Windows\\System32\\calc.exe'),
    ('paint', 'C:\\Windows\\System32\\mspaint.exe'),
    ('task manager', 'C:\\Windows\\System32\\Taskmgr.exe'),
    ('control panel', 'C:\\Windows\\System32\\control.exe'),
    ('settings', 'C:\\Windows\\System32\\ms-settings:'),
    ('windows settings', 'C:\\Windows\\System32\\ms-settings:'),
    # Windows Store apps
    ('microsoft store', 'ms-windows-store:'),
    ('store', 'ms-windows-store:'),
    ('windows store', 'ms-windows-store:'),
    ('settings', 'ms-settings:'),
    ('calendar', 'outlookcal:'),
    ('mail', 'mailto:'),
    ('camera', 'microsoft.windows.camera:'),
    ('photos', 'microsoft.windows.photos:'),
    ('music', 'microsoft.zunemusic:'),
    ('video', 'microsoft.zunevideo:')
]

for name, path in commands_to_insert:
    # Check if command already exists
    cursor.execute("SELECT COUNT(*) FROM sys_command WHERE LOWER(name) = ?", (name.lower(),))
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO sys_command VALUES (null, ?, ?)", (name, path))

# Update any existing incorrect paths
cursor.execute("UPDATE sys_command SET path = 'C:\\Windows\\explorer.exe' WHERE name IN ('file explorer','file explore')")
cursor.execute("UPDATE sys_command SET path = 'C:\\Program Files\\Microsoft Office\\root\\Office16\\powerpoint.exe' WHERE name IN ('power','power point','powerpoint')")
cursor.execute("UPDATE sys_command SET name = 'notepad plus plus' WHERE name = 'notepad++'")
conn.commit()                                                       

query = "CREATE TABLE IF NOT EXISTS web_command(id integer primary key, name VARCHAR(100), url VARCHAR(1000))"
cursor.execute(query)

# Insert web commands with proper duplicate handling
web_commands_to_insert = [
    ('chat gpt', 'https://chatgpt.com/'),
    ('chatgpt', 'https://chatgpt.com/'),
    ('youtube', 'https://www.youtube.com/'),
    ('canva', 'https://www.canva.com/')
]

for name, url in web_commands_to_insert:
    # Check if command already exists
    cursor.execute("SELECT COUNT(*) FROM web_command WHERE LOWER(name) = ?", (name.lower(),))
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO web_command VALUES (null, ?, ?)", (name, url))

# Normalize any legacy naming
cursor.execute("UPDATE web_command SET name = 'chat gpt' WHERE LOWER(name) IN ('chatgpt','chat gpt','chat g p t','chat gpt')")
conn.commit()


# testing module
#app_name = "one note"
#cursor.execute('SELECT path FROM sys_command WHERE name IN (?)', (app_name,))
#results = cursor.fetchall()
#print(results[0][0])

# Create a table with the desired columns
#cursor.execute('''CREATE TABLE IF NOT EXISTS contacts (id integer primary key, name VARCHAR(200), mobile_no VARCHAR(255), email VARCHAR(255) NULL)''')


# Specify the column indices you want to import (0-based index)
# Example: Importing the 1st and 3rd columns
#desired_columns_indices = [0, 18]

# Read data from CSV and insert into SQLite table for the desired columns
#with open('contacts.csv', 'r', encoding='utf-8') as csvfile:
 #    csvreader = csv.reader(csvfile)
  #   for row in csvreader:
   #      selected_data = [row[i] for i in desired_columns_indices]
    #     cursor.execute(''' INSERT INTO contacts (id, 'name', 'mobile_no') VALUES (null, ?, ?);''', tuple(selected_data))

# Commit changes and close connection
#conn.commit()
#conn.close()

#query = "INSERT INTO contacts VALUES (null,'pawan', '1234567890', 'null')"
#cursor.execute(query)
#conn.commit()

#query = 'appa'
#query = query.strip().lower()
#cursor.execute("SELECT mobile_no FROM contacts WHERE LOWER(name) LIKE ? OR LOWER(name) LIKE ?", ('%' + query + '%', query + '%'))
#results = cursor.fetchall()
#print(results[0][0])



# cursor.execute("DROP TABLE IF EXISTS contacts")
# con.commit()
# cursor.execute('''CREATE TABLE IF NOT EXISTS contacts (id integer primary key, name VARCHAR(200), mobile_no VARCHAR(255), email VARCHAR(255) NULL)''')

# Specify the column indices you want to import (0-based index)
# Example: Importing the 1st and 3rd columns
# desired_columns_indices = [0, 20]

# Read data from CSV and insert into SQLite table for the desired columns
# with open('contacts.csv', 'r', encoding='utf-8') as csvfile:
#     csvreader = csv.reader(csvfile)
#     for row in csvreader:
#         selected_data = [row[i] for i in desired_columns_indices]
#         cursor.execute(''' INSERT INTO contacts (id, 'name', 'mobile_no') VALUES (null, ?, ?);''', tuple(selected_data))

# # Commit changes and close connection
# con.commit()
# con.close()

# query = "INSERT INTO contacts VALUES (null,'amma', '8792370079', 'null')"
# cursor.execute(query)
# conn.commit()