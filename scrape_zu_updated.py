import requests
from bs4 import BeautifulSoup
import csv

# from gensim.parsing.preprocessing import remove_stopwords


URL = "https://www.zu.ac.ae/main/en/index.aspx"
page = requests.get(URL)

soup = BeautifulSoup(page.content, "html.parser")

links = soup.find_all('a', href=True)
# print(links)
print("length - ", len(links))
all_links = []


def link_constructor(partial_link):
    link = ''
    if partial_link[:4] == 'http' and 'javascript' not in partial_link:
        return partial_link.strip()
    elif partial_link[:9] == '/main/en/':
        link = 'https://www.zu.ac.ae' + partial_link
    elif partial_link[:10] == 'javascript':
        pass
    else:
        if URL != 'https://www.zu.ac.ae/main/en/' + partial_link:
            link = 'https://www.zu.ac.ae/main/en/' + partial_link
    return link.strip()


for link in links:
    if len(link_constructor(link['href'])) > 0:
        all_links.append(link_constructor(link['href']))
        # print(link_constructor(link['href']))
print(f'all link length before set functin: {len(all_links)}')
all_links = set(all_links)
print(f'all link length after set funcation : {len(all_links)}')
print(all_links)
# print(type(link['href']))
# break
# if 'href=' in link.contents:
#     print(link)


# sum_fall_dt = 'summer_fall_date'
# # open the file in the write mode
# f = open('zayed_csv.csv', 'w', encoding='utf-8')
#
# # create the csv writer
# writer = csv.writer(f)
#
# # write a row to the csv file
# writer.writerow(soup)
#
# # close the file
# f.close()
