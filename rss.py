from bs4 import BeautifulSoup   # HTML parser
from lib.rfeed.rfeed import *   # RSS generator
from datetime import datetime
import os


# Get all the HTML files in the blog section
htmls = [x for x in os.listdir(os.getcwd() + "/blog") if x.endswith('.html')]
htmls.sort(reverse=True) # sort newest to oldest

items = []

# Generate an item for all blog posts. The description is the first paragraph.
for path in htmls:
    with open("blog/" + path) as file:
        soup = BeautifulSoup(file, "html.parser")

    name = soup.find("p", "author").text.strip("Author:").split(" (")[0]
    date = soup.find("p", "modified").text.strip("Last Modified: ")
    try:    # try to extract time as well as date from newer files
        dt = datetime.strptime(date, "%Y %b %d %H:%M")
    except:
        dt = datetime.strptime(date, "%Y %b %d")
    url  = "https://mchartigan.github.io/blog/" + path

    items.append(Item(
        title = soup.title.string,
        link = url,
        author = name,
        guid = Guid(url),
        pubDate = dt,
        description = soup.find_all("p")[0].text.strip()
    ))

# Generate main channel item
with open("index.html") as file:
    soup = BeautifulSoup(file, "html.parser")

date = soup.find("p", "modified").text.strip("Last Modified: ")
try:    # try to extract time as well as date from newer files
    dt = datetime.strptime(date, "%Y %b %d %H:%M")
except:
    dt = datetime.strptime(date, "%Y %b %d")

feed = Feed(
    title = soup.title.string,
    link = "https://mchartigan.github.io/",
    lastBuildDate = dt,
    language = "en-US",
    items = items,
    description = soup.find_all("p")[0].text.strip()
)

rss = feed.rss().replace("–", "--")     # replace hyphens with readable char
# write RSS feed to feed.xml
with open("feed.xml", "w") as file:
    file.write(rss)
