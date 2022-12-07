import product
import dataProcessing


class Menu:

    def __init__(self, products: list[product.Product], is_small: bool) -> None:
        self.products = products
        self.is_small = is_small
        self.has_drink = False
        self.price = 0
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
        for item in products:
            if item.drink:
                self.has_drink = True
            self.price += item.price
            self.weight += item.weight
            self.kJ += item.kJ
            self.kcal += item.kcal
            self.fat += item.fat
            self.saturated_fats += item.saturated_fats
            self.carbons += item.carbons
            self.sugar += item.sugar
            self.fiber += item.fiber
            self.protein += item.protein
            self.salt += item.salt

    def __str__(self) -> str:
        representation = 'Menu: '
        for item in self.products[:-1]:
            representation += item.name + ', '
        representation += self.products[-1].name + ';'
        return representation

    def to_list(self) -> list:
        info = [item.name for item in self.products]
        info.append(self.is_small)
        return info

    def get_nutrition_data(self):
        return [self.weight, self.kJ, self.kcal, self.fat, self.saturated_fats,
                self.carbons, self.sugar, self.fiber, self.protein, self.salt]

    def get_nutrition_table(self) -> list:
        nutrition = self.get_nutrition_data()
        nutrition_per_100g = self.get_100g_data()
        return [[nutrition_per_100g[i], nutrition[i]] for i in range(len(nutrition))]

    def get_100g_data(self) -> list:
        factor = 100 / self.weight
        return [info * factor for info in self.get_nutrition_data()]
