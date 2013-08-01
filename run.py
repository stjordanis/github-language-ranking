import os
import re
import shutil
import subprocess
import sys

from bs4 import BeautifulSoup
import requests

def get_page(url):
  return BeautifulSoup(requests.get("https://github.com" + url).text)

languages = []

languages_page = get_page("/languages")
list_items = languages_page.find(class_="all_languages").find("ul").find_all("li")
for list_item in list_items:
  link = list_item.find("a")
  if not link: continue

  language_page = get_page(link["href"])
  rank_text = language_page.find("h1").text
  match = re.search("is the #(\d+) most popular", rank_text)
  rank = 1 # Default to 1 to handle "the most".
  if match:
    rank = int(match.group(1))

  # Erase the line.
  print "\033[2K",
  print "\r{}/{} {} is #{}".format(len(languages), len(list_items), link.text, rank),
  sys.stdout.flush()

  languages.append((rank, link.text))

# Erase the line.
print "\033[2K",
print "\r",

languages.sort()
for rank, language in languages:
  print "#" + str(rank) + " " + language
