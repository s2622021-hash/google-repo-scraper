import json
import sqlite3
import time

import requests
from bs4 import BeautifulSoup

# Make the database (the saved list) and a table inside it
conn = sqlite3.connect("repos.db")
cur = conn.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS repos (name TEXT, language TEXT, stars INTEGER)")
cur.execute("DELETE FROM repos")  # start fresh each time

# Visit the first 3 pages of Google's project list
for page in range(1, 4):
    url = f"https://github.com/orgs/google/repositories?page={page}"
    response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    soup = BeautifulSoup(response.text, "html.parser")

    # The project list is stored inside a hidden data block on the page.
    # Look through the data blocks until we find the one with the projects.
    repos = []
    for tag in soup.find_all("script", {"type": "application/json"}):
        try:
            data = json.loads(tag.string)
            repos = data["payload"]["orgReposPageRoute"]["repositories"]
            break
        except Exception:
            continue

    print(f"Page {page}: found {len(repos)} projects")

    for repo in repos:
        name = repo["name"]
        language = repo["primaryLanguage"]["name"] if repo.get("primaryLanguage") else "Unknown"
        stars = repo["starsCount"]

        cur.execute("INSERT INTO repos VALUES (?, ?, ?)", (name, language, stars))

    time.sleep(1)  # wait 1 second so we are polite to the website

conn.commit()
conn.close()
print("Done! Data saved to repos.db")