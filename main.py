from scripts import dataProcessing, product, scraper
import os.path

PRODUCT_LINK_PATH = 'product_links.txt'


def initialize() -> list[product.Product]:
    try:
        products = dataProcessing.load_products('products.csv')
    except FileNotFoundError:
        print('Error: Could not find products.csv')
        print('You can create a new products.csv file by scraping the data.')
        products = []
    except IndexError:
        print('Something went wrong!')
        print('Try to scrape the data again...')
        products = []
    return products


def scrape_data() -> list[product.Product]:
    if not os.path.exists(PRODUCT_LINK_PATH):
        print('Error: Could not find product_links.txt')
        return []

    data = scraper.scrape_multiple(PRODUCT_LINK_PATH)
    products = [dataProcessing.scraped_data_to_product(d) for d in data]
    dataProcessing.save_products(products, 'products.csv')
    return products


def add_product(products: list[product.Product]) -> list[product.Product]:
    url = input('Enter the url of the product: ')
    data = scraper.scrape(url)
    if len(data) == 0:
        print('Something went wrong. Please try again.')
        return products
    new_product = dataProcessing.scraped_data_to_product(data)
    products.append(new_product)
    dataProcessing.save_single_product(new_product, 'products.csv')



def menu_text_printer(section: str) -> None:
    if section == 'header':
        print('=' * 50)
        print('|\tMCDONALDS NUTRITION ANALYSING TOOL \t |')
        print('=' * 50)
        print()
    elif section == 'main':
        print('If you want to see the nutrition table of a specific product, type "nutrition"')
        print('If you want to scrape the data from the website, type "scrape"')
        print('If you want to exit the program, type "exit"')
        print()


def get_nutrition_table(products: list[product.Product]) -> None:
    print('0. Exit')
    for i in range(len(products)):
        print(f'{i + 1}. {products[i].name}')
    while True:
        try:
            user_input = int(input('Which product do you want to see the nutrition table of? ("0" for exit) '))
            if user_input < 0 or user_input > len(products):
                raise ValueError
            if user_input == 0:
                return
            dataProcessing.print_nutrition_table(products[user_input - 1])
        except ValueError:
            print('Error: Invalid input. Please try again.')


def main():
    products = initialize()
    menu_text_printer('header')
    while True:
        menu_text_printer('main')
        user_input = input('What do you want to do? ').lower()
        if user_input == 'nutrition':
            get_nutrition_table(products)
        elif user_input == 'scrape':
            products = scrape_data()
        elif user_input == 'exit':
            break
        else:
            print('Error: Invalid input. Please try again.')


if __name__ == '__main__':
    main()
