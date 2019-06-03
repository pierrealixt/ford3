from bs4 import BeautifulSoup
import requests
import unicodedata
import csv
import time


TIMESTAMP = int(time.time())
CSV_FIELDNAMES = [
    'saqa_id',
    'name',
    'type',
    'field_study',
    'subfield_study']


def scrape_qualification_link(link):
    href = link.get('href')
    if href[0:25] == 'viewQualification.php?id=':
        return href[25:]


def get_results_page(data):
    response = requests.post(
        'http://regqs.saqa.org.za/search.php',
        data=data)
    return response.content


def get_qualification_page(saqa_id):
    url = 'http://regqs.saqa.org.za/viewQualification.php?id={saqa_id}'.format(
        saqa_id=saqa_id)
    response = requests.get(url)
    return response.content


def get_text(node):
    return unicodedata.normalize('NFKD', node.get_text()).rstrip()


def scrape_qualification_page(html):
    html = BeautifulSoup(html, 'html.parser')

    tables = html.find_all('table')
    info = tables[5]

    tds_id_title = info.find_all('tr')[1].find_all('td')
    tds_info = info.find_all('tr')[7].find_all('td')

    return {
        'saqa_id': get_text(tds_id_title[0]),
        'name': get_text(tds_id_title[1]),
        'type': get_text(tds_info[0]),
        'field_study': get_text(tds_info[1]).split(' - ')[1],
        'subfield_study': get_text(tds_info[2])
    }


def init_csv():
    csv_filename = 'saqa_qualifications_{}.csv'.format(TIMESTAMP)
    with open(csv_filename, 'w') as csvfile:
        writer = csv.DictWriter(
            csvfile,
            delimiter=';',
            fieldnames=CSV_FIELDNAMES)
        writer.writeheader()

    return csv_filename


def write_to_csv(csv_filename, qualification):
    with open(csv_filename, 'a') as csvfile:
        writer = csv.DictWriter(
            csvfile,
            delimiter=';',
            fieldnames=CSV_FIELDNAMES)
        writer.writerow(qualification)


def scrape_qualification_pages(ids):
    csv_filename = init_csv()

    for saqa_id in ids:
        try:
            print(saqa_id)
            html = get_qualification_page(saqa_id)
            qualif = scrape_qualification_page(html)
            write_to_csv(csv_filename, qualif)
        except IndexError:
            continue


def save_ids(ids):
    txt_filename = 'saqa_ids_{}.txt'.format(TIMESTAMP)
    with open(txt_filename, 'w') as txtfile:
        txtfile.write(str(ids))


def get_offset_from_page(page):
    if page == 0:
        return 0
    else:
        return (page * 60) + 1


def get_form_data(offset):
    """
    Returns form data with updated offset.
    """
    return {
      "GO": "Go",
      "searchResultsATfirst": offset,
      "cat": "qual",
      "view": "table",
      "QUALIFICATION_TITLE": "",
      "QUALIFICATION_ID": "",
      "NQF_LEVEL_ID": "",
      "NQF_LEVEL_G2_ID": "",
      "ABET_BAND_ID": "",
      "SUBFIELD_ID": "",
      "QUALIFICATION_TYPE_ID": "",
      "ORIGINATOR_ID": "",
      "FIELD_ID": "",
      "ETQA_ID": "",
      "SEARCH_TEXT": "",
      "ACCRED_PROVIDER_ID": "",
      "NQF_SUBFRAMEWORK_ID": ""
    }


def scrape_results_page(html):
    """
    Scrape a results page. Get saqa_ids from HTML links.
    """
    html = BeautifulSoup(html, 'html.parser')

    links = html.find_all('a')

    saqa_ids = [
        scrape_qualification_link(link)
        for link in links
    ]

    saqa_ids = [x for x in saqa_ids if x]
    return saqa_ids


def get_saqa_ids(page):
    """
    :page: int
    Return a list of saqa_ids from a page.
    """
    offset = get_offset_from_page(page)

    data_form = get_form_data(offset)

    results_page = get_results_page(data_form)

    saqa_ids = scrape_results_page(results_page)

    return saqa_ids


def scrape_saqa_ids():
    """
    Scrape saqa_ids.
    :returns: list of string
    """

    # use a set to avoid duplicates
    saqa_ids = set()

    page = 0
    while (1):
        len_ids = len(saqa_ids)
        print(page, len_ids)

        page_saqa_ids = get_saqa_ids(page)
        saqa_ids.update(page_saqa_ids)

        # loop until there is no more ids to scrape
        if len(saqa_ids) == len_ids:
            break

        page += 1

    saqa_ids = list(saqa_ids)
    save_ids(saqa_ids)

    return saqa_ids


def main():
    print('Scraping saqa_ids from SAQA search results...')

    ids = scrape_saqa_ids()

    print('Scraped {} saqa_ids', len(ids))
    print('Scraping SAQA qualifications...')

    scrape_qualification_pages(ids)


if __name__ == '__main__':
    main()
