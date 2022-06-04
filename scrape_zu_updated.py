import requests
from bs4 import BeautifulSoup
import csv

# from gensim.parsing.preprocessing import remove_stopwords


URL = "https://www.zu.ac.ae/main/en/index.aspx"
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


def find_inner_links(all_links_, partial_link):
    try:
        page = requests.get(partial_link)
        soup = BeautifulSoup(page.content, "html.parser")
        links = soup.find_all('a', href=True)
        print(f'all link length before set functin: {len(all_links)}')
        for link in links:
            discovered_link = link_constructor(link['href'])
            if len(discovered_link) > 0\
                    and discovered_link not in all_links_ \
                    and 'zu' in discovered_link:
                all_links_.append(discovered_link)
                print(discovered_link)
                find_inner_links(all_links_, discovered_link)

    except TimeoutError:
        print(f'Link Removed, Check for Error : {partial_link}')
        all_links_.remove(all_links_.index(partial_link))


    except:
        print(f' This link gave error : {partial_link}')


find_inner_links(all_links, URL)

# print(link_constructor(link['href']))
print(f'all link length before set functin: {len(all_links)}')
all_links = set(all_links)
print(f'all link length after set funcation : {len(all_links)}')
print(list(all_links))

with open('urls.csv', 'w', encoding='UTF8', newline='') as f:
    writer = csv.writer(f)

    # write the header
    # writer.writerow(header)

    # write multiple rows
    writer.writerows(all_links)
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
