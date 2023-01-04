from pint import UnitRegistry
from scraper import ingredient_list

ureg = UnitRegistry()
Q_ = ureg.Quantity
# Define one stick (of butter) = 1/2 cup (of butter)
ureg.define('stick = sticks = 0.5 * cup')

print(ingredient_list)

Ingredient = input("Ingredient: ")
Quant = input("Quantity: ")
Unit = input("Unit (if no unit e.g. 1 onion leave blank): ")

QuantUnit = Quant + Unit

for set in ingredient_list:
    if set[1] == Ingredient:
        if len(set[0]):
            print(Q_(set[0]), set[1])
            if Q_(QuantUnit) <= Q_(set[0]):
                print("Have less than or equal to")