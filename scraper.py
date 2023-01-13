# from url_locator import all_recipe_urls as urls
from fractions import Fraction
from bs4 import BeautifulSoup
import unicodedata
import requests
import re

urls = ['https://www.foodnetwork.com/recipes/apple-studded-brown-butter-streusel-coffee-cake-2124530']

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

    # Look for Food Network's recipe name by looking for meta element that contains the following condition
    scraped_recipe_name = soup.find("meta", {"property" : "og:title"})
    # Item content contains name
    recipe_name = scraped_recipe_name["content"]
    recipe_name = recipe_name.replace("'","")

    # Look for Food Network's ingredients checklist by looking for input elements that contain the following conditions 
    shopping_list = soup.find_all("input", {"class" : "o-Ingredients__a-Ingredient--Checkbox"}, {"type" : "checkbox"})
    # Item "value" contains ingredient + quantity
    scraped_ingred_quant = [item["value"] for item in shopping_list[1:]]

    return recipe_name, scraped_ingred_quant

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
                    if unit in item and item.index(unit) <= 5:
                        # If multiple units exist in one string, iterate with earlier unit
                        # e.g. '5 tablespoons plus 3 ounces melted butter' <- Why do people do this?
                        # Keep iterating until earliest unit is found
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
                                list.insert(1, x_unit)
                            except ValueError:
                                # ValueError occurs if multiple units exist in one string and algorithm iterates the later one
                                # Not sure how else to work around this
                                continue
                    elif unit in item and item.index(unit) > 5:
                        # Else search for the first digit in the item
                        num = (re.search(r'\d+', item).group())
                        # If '/' exists, e.g. 1/2 onion
                        if '/' in item and item.index('/') <= 5:
                            num = num + item[item.index(num) + 1] + item[item.index(num) + 2]
                        # and split accordingly
                        list = item.split(num, 1)
                        list[0] = str(round(float(Fraction(num)), 2))
                        list.insert(1, '')
            else:
                # Else search for the first digit in the item
                num = (re.search(r'\d+', item).group())
                # If '/' exists, e.g. 1/2 onion
                if '/' in item and item.index('/') <= 5:
                    num = num + item[item.index(num) + 1] + item[item.index(num) + 2]
                # and split accordingly
                list = item.split(num, 1)
                list[0] = str(round(float(Fraction(num)), 2))
                list.insert(1, '')
        else:
            list = ['', '', item]
        # Remove leading/trailing whitespace and quotes in string
        list = [s.strip() for s in list]
        list = [s.replace("'","") for s in list]
        ingredient_list.append(list)
    return ingredient_list

def url_cycler():
    # Cycle through URls and create a list of tuples
    # Each tuple contains (recipe name, [list of ingredients]) 
    for url in urls:
        try:
            recipe_name = scraper(url)[0]
            scraped_ingred_quant = scraper(url)[1]
            ingredient_list = cleanup(scraped_ingred_quant)
            yield recipe_name, ingredient_list
        # If error, continue. Running into URLs with NoneType
        except:
            continue

name_and_ingredients = url_cycler()

if __name__ == "__main__":
    print(list(name_and_ingredients))