import csv
from tabulate import tabulate
import product
import mcMenu

ANGABEN = ['Portionsgröße(g)', 'Brennwert(kJ)', 'Brennwert(kcal)', 'Fett(g)', 'davon gesättigte Fettsäuren(g)',
           'Kohlenhydrate(g)', 'davon Zucker(g)', 'Ballaststoffe(g)', 'Eiweiß(g)', 'Salz(g)']


def print_nutrition_table(item: product.Product) -> None:
    print('Here are the nutrition facts for the product: ', item.name)
    nutrition_data = item.get_nutrition_table()
    for i in range(len(nutrition_data)):
        nutrition_data[i].insert(0, ANGABEN[i])
    print(tabulate(nutrition_data, headers=['Angabe', 'Menge pro 100g', 'Menge pro Portion'], tablefmt='orgtbl'))


def print_nutrition_table_menu(menu: mcMenu.Menu) -> None:
    print('Here are the nutrition facts for the menu:')
    print(menu)
    nutrition_data = menu.get_nutrition_table()
    for i in range(len(nutrition_data)):
        nutrition_data[i].insert(0, ANGABEN[i])
    print(tabulate(nutrition_data, headers=['Angabe', 'Menge pro 100g', 'Menge pro Portion'], tablefmt='orgtbl'))


# save products to a csv file
def save_products(products: list[product.Product], path: str) -> None:
    product_data = [item.to_list() for item in products]
    with open(path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(product_data)


# load products from a csv file
def load_products(path: str) -> list[product.Product]:
    with open(path, 'r') as f:
        csv_data = list(csv.reader(f))
    products = []
    for datum in csv_data:
        new_product = product.Product(datum)
        new_product.menuType = datum[11]
        new_product.drink = bool(datum[12])
        new_product.price = datum[13]
        new_product.is_side_small = bool(datum[14])
        products.append(new_product)
    return products


def scraped_data_to_product(data: list) -> product.Product:
    product_data = [data[0]]
    for i in range(10):
        product_data.append(data[i*2 + 2])
    new_product = product.Product(product_data)
    return new_product


def save_single_product(item: product.Product, path: str) -> None:
    with open(path, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(item.to_list())


def add_product_properties(products: list[product.Product]):
    classics = ['Big Rösti', 'Grand BBQ Cheese', 'Big Tasty® Bacon', 'McCrispy® Homestyle', 'Big Mac®',
                 'Hamburger Royal TS', 'Hamburger Royal Käse', 'McChicken® Classic', 'Fresh Vegan TS', 'McRib®',
                 'Filet-o-Fish®', '9 Spicy Chicken McNuggets', '6 Spicy Chicken McNuggets', '9 Chicken McNuggets®',
                 '6 Chicken McNuggets®', 'McWrap Chicken Sweet-Chili', 'McWrap® Chicken Caesar']

    sides = ['Pommes Frites groß', 'Riffelkartoffeln', 'Snack Salad Classic', 'Coca-Cola Classic 0,5l',
                'Coca-Cola Light Taste 0,5l', 'Coca-Cola Zero Sugar 0,5l', 'Lipton Ice Tea Peach 0,5l', 'Fanta 0,5l',
                'Sprite 0,5l', 'ViO Mineralwasser Still 0,5l', 'Adelholzener Apfelschorle 0,5l', 'Orangensaft 0,25l',
                'Café Grande', 'Cappuccino Grande', 'Latte Macchiato Grande', 'Dark Chocolate grande',
                'Milchshake Schokogeschmack 0,4l', 'Milchshake Erdbeergeschmack 0,4l',
                'Milchshake Vanillegeschmack 0,4l']

    extras = ['Buttermilk Ranch Dip 25 ml', 'Dip HEATWAVE 25 ml', 'Sour Cream-Schnittlauch Dip 25ml', 'Ketchup 20ml',
              'Mayonnaise 20ml', 'Dip Cocktail 25ml', 'Curry Sauce 25ml', 'Süßsauer Sauce 25ml', 'Barbecue Sauce 25ml',
              'Chili Sauce 25ml', 'Senf Sauce 25ml', 'Balsamico Dressing 30ml', 'Caesar Dressing 50ml']

    drinks = ['Coca-Cola Classic 0,5l', 'Coca-Cola Classic 0,4l', 'Coca-Cola Classic 0,25l',
              'Coca-Cola Light Taste 0,5l', 'Coca-Cola Light Taste 0,4l', 'Coca-Cola Light Taste 0,25l',
              'Coca-Cola Zero Sugar 0,5l', 'Coca-Cola Zero Sugar 0,4l', 'Coca-Cola Zero Sugar 0,25l',
              'Lipton Ice Tea Peach 0,5l', 'Lipton Ice Tea Peach 0,4l', 'Lipton Ice Tea Peach 0,25l',
              'Fanta 0,5l', 'Fanta 0,4l', 'Fanta 0,25l',
              'Sprite 0,5l', 'Sprite 0,4l', 'Sprite 0,25l',
              'ViO Mineralwasser Still 0,5l', 'Adelholzener Apfelschorle 0,5l', 'Orangensaft 0,25l',
              'Red Bull 0,25l', 'Café Grande', 'Café Regular', 'Café Small', 'Cappuccino Grande', 'Cappuccino Regular',
              'Cappuccino Small', 'Latte Macchiato Grande', 'Latte Macchiato Regular', 'Caramel Macchiato Grande 0,4l',
              'Caramel Macchiato Regular 0,3l', 'Espresso Grande', 'Espresso Small', 'Espresso Macchiato grande',
              'Espresso Macchiato small', 'Chai Latte Grande', 'Chai Latte Regular',
              'Dark Chocolate grande', 'Dark Chocolate regular', 'Dark Chocolate small',
              'Milchshake Schokogeschmack 0,4l', 'Milchshake Schokogeschmack 0,25l', 'Milchshake Erdbeergeschmack 0,4l',
              'Milchshake Erdbeergeschmack 0,25l', 'Milchshake Vanillegeschmack 0,4l',
              'Milchshake Vanillegeschmack 0,25l',
              'Heißes Kakaogetränk grande', 'Heißes Kakaogetränk small', 'Earl Grey Tee Regular', 'Grüner Tee Regular',
              'Fresh Mint Tee Regular', 'McMilchshake Erdbeer Schoko-Sauce 0,4l',
              'McMilchshake Erdbeer Schoko-Sauce 0,25l', 'McMilchshake Schoko Karamell-Sauce 0,4l',
              'McMilchshake Schoko Karamell-Sauce 0,25l',
              'McFrappé Choc 0,4l', 'McFrappé Choc 0,3l']

    sides_small = []

    for classic in classics:
        product.get_product_by_name(classic, products).menuType = 'classic'
    for side in sides:
        product.get_product_by_name(side, products).menuType = 'side'
    for extra in extras:
        product.get_product_by_name(extra, products).menuType = 'extra'
    for drink in drinks:
        product.get_product_by_name(drink, products).drink = True
    for side in sides_small:
        product.get_product_by_name(side, products).is_side_small = True
