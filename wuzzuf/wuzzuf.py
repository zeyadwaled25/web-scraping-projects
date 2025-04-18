import requests
from bs4 import BeautifulSoup
import csv
from itertools import zip_longest
import time

jobs = []
companies = []
locations = []
skills = []
dates = []
links = []
salaries = []
responsibilities = []

job = input("Enter Your Job: ").strip()
page_num = 0

while True:
  try:
    url = requests.get(f"https://wuzzuf.net/search/jobs/?a=hpb&q={job}&start={page_num}")
    content = url.content

    soup = BeautifulSoup(content, "lxml")
    page_limit = soup.find("strong").text

    if (page_num > int(page_limit) // 15):
      break

    job_title = soup.find_all("h2", {"class": "css-m604qf"})
    company_name = soup.find_all("div", {"class": "css-d7j1kk"})
    location_name = soup.find_all("span", {"class": "css-5wys0k"})
    skill = soup.find_all("div", {"class": "css-y4udm8"})
    new_posted = soup.find_all("div", {"class": "css-4c4ojb"})
    old_posted = soup.find_all("div", {"class": "css-do6t5g"})
    all_posted = [*new_posted, *old_posted]

    for div in skill:
        inner_div = div.find("div", {"class": None})
        if inner_div:
            skills.append(inner_div.text)


    for i in range(len(job_title)):
      jobs.append(job_title[i].text)
      companies.append(company_name[i].text)
      locations.append(location_name[i].text)
      dates.append(all_posted[i].text)
      links.append(job_title[i].find("a").attrs["href"])

    page_num += 1
    print(f"{page_num} - Page Switched")
    time.sleep(1)
  except Exception as e:
    print("Error Occurred:", e)
    break

# for link in links:
#   url = requests.get(link)
#   content = url.content
#   soup = BeautifulSoup(content, "lxml")
#   salary = soup.find_all("span", {"class": "css-4xky9y"})
#   salaries.append(salary[-1].text.strip())
#   req = soup.find_all("div", {"class": "css-1t5f0fr"})
#   respons_text = ""
#   for ol in req:
#     new_req = ol.find("ol")
#     for li in new_req.find_all("li"):
#       respons_text += li.text + " | "
#   responsibilities.append(respons_text)
#   time.sleep(1)

file_formated = zip_longest(jobs, companies, locations, skills, dates, links)

with open(f"{job}_wuzzuf.csv", "w", newline='', encoding="utf-8-sig") as fileExported:
  wr = csv.writer(fileExported)
  wr.writerow(["Job Title", "Company Name", "Location", "Skills", "Date", "Link"])
  wr.writerows(file_formated)

print("File created successfully. ✅")