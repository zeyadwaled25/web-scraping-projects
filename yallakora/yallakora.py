import requests
from bs4 import BeautifulSoup
import csv

Date = input("Enter Date Formatted like MM/DD/YYYY: ")
page = requests.get(f"https://www.yallakora.com/match-center/?date={Date}")

def main(page):
  src = page.content
  soup = BeautifulSoup(src, "lxml")
  matchesDetails = []

  championships = soup.find_all("div", {'class': 'matchCard'})

  def getMatchInfo(championships):
    championshipTitle = championships.contents[1].find("h2").text.strip()
    allMatches = championships.contents[3].find_all("div", {'class': 'item'})

    for match in allMatches:
      teamA = match.find("div", {'class': 'teamA'}).text.strip()
      teamB = match.find("div", {'class': 'teamB'}).text.strip()

      result = match.find("div", {'class': 'MResult'})
      score_spans = result.find_all("span", {'class': 'score'})
      time = result.find("span", {'class': 'time'}).text.strip()

      score = f"'{score_spans[0].text.strip()} - {score_spans[1].text.strip()}'"
      time = f"'{time}'"

      matchesDetails.append({
        "نوع البطولة": championshipTitle,
        "الفريق الاول": teamA,
        "الفريق الثاني": teamB,
        "ميعاد المباراة": time,
        "النتيجه": score
      })

  for champ in championships:
    getMatchInfo(champ)

  keys = matchesDetails[0].keys()
  with open("yallakora.csv", "w", newline='', encoding="utf-8-sig") as f:
    writer = csv.DictWriter(f, keys)
    writer.writeheader()
    writer.writerows(matchesDetails)
  print("File created successfully. ✅")

main(page)