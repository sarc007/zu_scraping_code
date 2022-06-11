from urllib.parse import urlparse

import requests
import validators
from bs4 import BeautifulSoup
from validators import ValidationFailure

# from gensim.parsing.preprocessing import remove_stopwords


URL = "https://www.zu.ac.ae/main/en/index.aspx"
all_links = []
with open('.\\data\\urls_partial.txt', 'w', encoding='UTF8', newline='') as f:
    f.write('List of Links\n')

with open('.\\data\\urls.txt', 'w', encoding='UTF8', newline='') as f:
    f.write('List of Links\n')


def uri_validator(x):
    try:
        result = urlparse(x)
        return all([result.scheme, result.netloc])
    except:
        return False


def is_string_an_url(url_string: str) -> bool:
    result = validators.url(url_string)

    if isinstance(result, ValidationFailure):
        return False

    return result


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
            partial_link_ = partial_link
            while '../' in partial_link_:
                partial_link_ = partial_link_[3:]
            link = 'https://www.zu.ac.ae/main/en/' + partial_link_

    return link.strip()


def find_inner_links(part_data_, all_links_, partial_link):
    try:
        if uri_validator(partial_link) and is_string_an_url(partial_link):
            page = requests.get(partial_link)
            soup = BeautifulSoup(page.content, "html.parser")
            links = soup.find_all('a', href=True)
            for link in links:
                discovered_link = link_constructor(link['href'])
                if len(discovered_link) > 0 \
                        and not discovered_link + '\n' in all_links_ \
                        and 'zu.ac.ae' in discovered_link \
                        and uri_validator(discovered_link) and is_string_an_url(discovered_link):
                    print(f'all link length before set function: {len(all_links)}')
                    all_links_.append(discovered_link + '\n')
                    part_data_.append(discovered_link + '\n')
                    print(discovered_link)
                    if len(part_data_) % 2 == 0 and len(part_data_) > 0:
                        with open('.\\data\\urls_partial.txt', 'a', encoding='UTF8', newline='') as ft:
                            ft.writelines(part_data_)
                            part_data_ = []
                    find_inner_links(part_data_, all_links_, discovered_link)

    except TimeoutError:
        print(f'Link Removed, Check for Error : {partial_link}')
        all_links_.remove(all_links_.index(partial_link))


    except Exception as e:
        print(f' This link caused the following error : {e.__cause__}, error class: {e.__class__}, '
              f'error message {e.__context__}')
    finally:
        with open('.\\data\\urls_partial.txt', 'a', encoding='UTF8', newline='') as ft:
            ft.writelines(part_data_)
            part_data_ = []

part_data = []
find_inner_links(part_data, all_links, URL)

# print(link_constructor(link['href']))
print(f'all link length before set function: {len(all_links)}')
all_links = set(all_links)
print(f'all link length after set function : {len(all_links)}')
print(list(all_links))

with open('.\\data\\urls.txt', 'w', encoding='UTF8', newline='') as f:
    f.writelines(all_links)

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
