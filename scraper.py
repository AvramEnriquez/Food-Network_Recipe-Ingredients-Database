import requests
import re
from bs4 import BeautifulSoup

url = "https://www.foodnetwork.com/recipes/rabbit-stroganoff-recipe-1915633"

def scraper(url):
    # Request HTML for URL then parse it
    result = requests.get(url)
    soup = BeautifulSoup(result.text, "html.parser")
    
    # Look for Food Network's ingredients checklist by looking for inputs that contain the following conditions 
    shopping_list = soup.find_all("input", {"class" : "o-Ingredients__a-Ingredient--Checkbox"}, {"type" : "checkbox"})

    # Item "value" contains ingredient + quantity
    ingredients_quantity = [item["value"] for item in shopping_list[1:]]

    return ingredients_quantity

ingredients_quantity = scraper(url)

measurements = ([' ml ',' mL ',' milliliter ',' milliliters ',' millilitre ',' millilitres ',
' cc ',' l ',' L ',' liter ',' liters ',' litre ',' litres ',' teaspoon ',' teaspoons ',
' tablespoon ',' tablespoons ',' T ',' tbl ',' tbs ',' tbsp ',' fluid ounce ',' fluid ounces ',
' fl oz ',' gill ',' gills ',' cup ',' cups ',' c ',' pint ',' pints ',' p ',' pt ',' pts ',
' fl pt ',' fl pts ',' quart ',' quarts ',' q ',' qt ',' fl qt ',' fl qts ',' gallon ',
' gallons ',' g ',' gal ',' gals ',' mg ',' milligram ',' milligrams ',' milligramme ',
' milligrammes ',' g ',' gs ',' gram ',' grams ',' gramme ',' grammes ',' kg ',' kgs ',
' kilogram ',' kilograms ',' kilogramme ',' kilogrammes ',' pound ',' pounds ',' lb ',' lbs ',
' # ',' ounce ',' ounces ',' oz ', ' stick ', ' sticks ', ' clove ', ' cloves '])

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

for item in ingredients_quantity:
    for key, value in numdict.items():
        if key in item:
            item = item.replace(key, str(value))
    if any(char.isdigit() for char in item):
        if any(unit in item for unit in measurements):
            for unit in measurements:
                if unit in item:
                    list = item.split(unit, 1)
                    list[0] += unit
        else:
            # Search for integer in the item
            num = (re.search(r'\d+', item).group())
            list = item.split(num, 1)
            list[0] += num
        list = [s.replace('\xa0', ' ') for s in list]
        list = [s.strip() for s in list]
        print(list)
    else:
        list = ['', item]
        print(list)
