import csv


class Product:

    def __init__(self, data: list) -> None:
        try:
            self.name = data[0]
            self.weight = float(data[1])
            self.kJ = float(data[2])
            self.kcal = float(data[3])
            self.fat = float(data[4])
            self.saturated_fats = float(data[5])
            self.carbons = float(data[6])
            self.sugar = float(data[7])
            self.fiber = float(data[8])
            self.protein = float(data[9])
            self.salt = float(data[10])
        except IndexError:
            print('Error: Could not create Product object. Please check if the input is valid.')
            self.name = ''
            self.weight = 0
            self.kJ = 0
            self.kcal = 0
            self.fat = 0
            self.saturated_fats = 0
            self.carbons = 0
            self.sugar = 0
            self.fiber = 0
            self.protein = 0
            self.salt = 0

        self.menuType = ''
        self.drink = False
        self.price = 0
        self.is_side_small = False

    def __str__(self) -> str:
        return self.name

    def to_list(self) -> list:
        return [self.name, self.weight, self.kJ, self.kcal, self.fat, self.saturated_fats,
                self.carbons, self.sugar, self.fiber, self.protein, self.salt, self.menuType, self.drink,
                self.price, self.is_side_small]

    def get_nutrition_table(self) -> list:
        nutrition = self.to_list()[1:11]
        nutrition_per_100g = self.get_100g_data()
        return [[nutrition_per_100g[i], nutrition[i]] for i in range(len(nutrition))]

    def get_100g_data(self) -> list:
        factor = 100 / self.weight
        return [info * factor for info in self.to_list()[1:11]]


# get a Product from a list by its name
def get_product_by_name(name: str, products: list[Product]) -> Product:
    for product in products:
        if product.name == name:
            return product
    return None


# get a list of all products of a specific menu type
def get_products_by_menu_type(menu_type: str, products: list[Product]) -> list[Product]:
    return [product for product in products if product.menuType == menu_type]

