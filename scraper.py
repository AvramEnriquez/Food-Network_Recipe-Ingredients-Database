from fractions import Fraction
from bs4 import BeautifulSoup
import unicodedata
import requests
import re

url = "https://www.foodnetwork.com/recipes/food-network-kitchen/halal-cart-chicken-11312197"

measurements = ([' ml ',' mL ',' milliliter ',' milliliters ',' millilitre ',' millilitres ',
' cc ',' l ',' L ',' liter ',' liters ',' litre ',' litres ',' teaspoon ',' teaspoons ',
' tablespoon ',' tablespoons ',' T ',' tbl ',' tbs ',' tbsp ',' fluid ounce ',' fluid ounces ',
' fl oz ',' gill ',' gills ',' cup ',' cups ',' c ',' pint ',' pints ',' p ',' pt ',' pts ',
' fl pt ',' fl pts ',' quart ',' quarts ',' q ',' qt ',' fl qt ',' fl qts ',' gallon ',
' gallons ',' g ',' gal ',' gals ',' mg ',' milligram ',' milligrams ',' milligramme ',
' milligrammes ',' g ',' gs ',' gram ',' grams ',' gramme ',' grammes ',' kg ',' kgs ',
' kilogram ',' kilograms ',' kilogramme ',' kilogrammes ',' pound ',' pounds ',' lb ',' lbs ',
' # ',' ounce ',' ounces ',' oz ', ' stick ', ' sticks '])
numdict = {
    "One" : 1,
    "Two" : 2,
    "Three" : 3,
    "Four" : 4,
    "Five" : 5,
    "Six" : 6,
    "Seven" : 7,
    "Eight" : 8,
    "Nine" : 9,
    "Ten" : 10,
}

def scraper(url):
    # Request HTML for URL then parse it
    result = requests.get(url)
    soup = BeautifulSoup(result.text, "html.parser")
    
    # Look for Food Network's ingredients checklist by looking for inputs that contain the following conditions 
    shopping_list = soup.find_all("input", {"class" : "o-Ingredients__a-Ingredient--Checkbox"}, {"type" : "checkbox"})

    # Item "value" contains ingredient + quantity
    scraped_ingred_quant = [item["value"] for item in shopping_list[1:]]

    return scraped_ingred_quant

def cleanup(scraped_ingred_quant):
    ingredient_list = []
    for item in scraped_ingred_quant:
        # Cleanup HTML encoding '\xa0'
        item = unicodedata.normalize('NFKD', item)
        # 'One' -> '1', 'Two' -> '2', 'Three' -> '3'
        for key, value in numdict.items():
            if key in item:
                item = item.replace(key, str(value))
        # If string contains a digit
        if any(char.isdigit() for char in item):
            # and if string contains a unit of measurement
            if any(unit in item for unit in measurements):
                # then split accordingly
                x_unit = ''
                for unit in measurements:
                    if unit in item:
                        # If multiple units exist in one string, iterate with earlier unit
                        # e.g. '5 tablespoons plus 3 ounces melted butter' <- Why do people do this?
                        # Keep iterating until it earliest unit is found
                        if item.index(unit) < item.index(x_unit) or item.index(x_unit) == 0:
                            x_unit = unit
                            list = item.split(x_unit, 1)
                            try:
                                # If ' ' exists, that means quantity is separated and requires addition
                                # e.g. 1 1/2 cups, 2 2/5 teaspoons
                                if ' ' in list[0]:
                                    num_list = list[0].split(' ', 1)
                                    total = sum(round(float(Fraction(x)), 2) for x in num_list)
                                    list[0] = str(total)
                                # Convert any fractions to floats
                                elif '/' in list[0]:
                                    list[0] = str(round(float(Fraction(list[0])), 2))
                                list[0] += x_unit
                            except ValueError:
                                # ValueError occurs if multiple units exist in one string and algorithm iterates that later one
                                # Not sure how else to work around this
                                continue
            else:
                # Else search for the first digit in the item
                num = (re.search(r'\d+', item).group())
                # and split accordingly
                list = item.split(num, 1)
                list[0] += num
            # Remove leading/trailing whitespace
            list = [s.strip() for s in list]
        else:
            list = ['', item]
        ingredient_list.append(list)
    return ingredient_list

scraped_ingred_quant = scraper(url)
ingredient_list = cleanup(scraped_ingred_quant)

if __name__ == "__main__":
    print(ingredient_list)