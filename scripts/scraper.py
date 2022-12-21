from selenium import webdriver
import csv
from scripts import progressbar, dataProcessing


def get_page_html(url):  # opens and renders a page and returns the html code as a string
    driver = webdriver.Chrome()
    driver.get(url)
    code = driver.page_source
    driver.close()
    return code


def get_multiple_page_html(urls: list[str]) -> list[str]:
    driver = webdriver.Chrome()
    htmls = []
    print('Loading pages...')
    for index, url in enumerate(urls):
        progressbar.printProgressBar(index, len(urls), prefix='Progress:', suffix='Complete', length=50)
        driver.get(url)
        htmls.append(driver.page_source)
    print()
    driver.close()
    return htmls


def scrape_value(datum):  # take a table field and return the value stored in it
    if '<span>' in datum:
        scraped_datum = datum.split('<span>')[1].split('</span>')[0].split('\n')[1].strip(' ')
    else:
        scraped_datum = datum.split('<span aria-hidden="true">')[1].split('</span>')[0].split('\n')[1].strip(' ')
    if scraped_datum == '':
        return 100
    else:
        return float(scraped_datum)


def get_item_data(code):  # get the tables single data fields and run them through the scrapeValue function
    item_data = []
    name = code.split('<title>')[1].split('</title>')[0]
    item_data.append(name)
    table = code.partition('<table>')[2].partition('</table>')[0]
    rows = table.split('</tr>')

    rows_without_head = []
    for row in rows:
        rows_without_head.append(row.partition('</th>')[2])

    data_in_rows = []
    for row in rows_without_head:
        data_in_rows.append(row.split('</td>'))

    # data is stored in data_in_rows [1] to [10]
    # in there, the values are at indices [0] and [1]
    for i in range(1, 11):
        datum1 = data_in_rows[i][0].partition('>')[2]
        datum2 = data_in_rows[i][1].partition('>')[2]
        item_data.append(scrape_value(datum1))
        item_data.append(scrape_value(datum2))
    return item_data


def save_data(data, path):  # saves the data to a csv file
    with open(path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(data)


def scrape(url):  # basically the main function
    try:
        code = get_page_html(url)
        data = get_item_data(code)
        return data
    except IndexError:
        print('Error: Could not scrape data from ' + url)
        return []


def scrape_multiple(path: str) -> list:
    with open(path, 'r') as f:
        urls = f.read().splitlines()
    if len(urls) == 0:
        print('No urls found in product_links.txt')
        print('Please add some urls to the file and try again.')
        print()
        return []
    htmls = get_multiple_page_html(urls)
    data = []
    errors = []

    print('Scraping data...')
    for i, html in enumerate(htmls):
        progressbar.printProgressBar(i, len(htmls), prefix='Progress:', suffix='Complete', length=50)
        try:
            data.append(get_item_data(html))
        except IndexError:
            errors.append(urls[i])
    print('Errors:', end=' ')
    if len(errors) == 0:
        print('None')
    else:
        print()
        for error in errors:
            print(error)
    return data


# scrape one product and insert it into a specific line of a csv file
def scrape_and_insert(url, line, path):
    data = scrape(url)
    with open(path, 'r') as f:
        csv_data = list(csv.reader(f))
    csv_data.insert(line, dataProcessing.scraped_data_to_product(data).to_list())
    save_data(csv_data, path)


def scrape_and_append(url, path):
    data = scrape(url)
    with open(path, 'r') as f:
        csv_data = list(csv.reader(f))
    csv_data.append(data)
    save_data(csv_data, path)
