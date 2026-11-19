import sqlite3

# Open the saved list
conn = sqlite3.connect("repos.db")
cur = conn.cursor()

# SELECT means "show me what is stored". Here, the most popular projects come first.
cur.execute("SELECT name, language, stars FROM repos ORDER BY stars DESC")
rows = cur.fetchall()

print(f"Total projects saved: {len(rows)}")
print()
for name, language, stars in rows:
    print(f"{name} | {language} | {stars} stars")

conn.close()