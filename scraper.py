import requests
import re
from bs4 import BeautifulSoup

url = "https://www.foodnetwork.com/recipes/haggis-recipe-2126047"

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

print(ingredients_quantity)

measurements = ([' ml ',' mL ',' milliliter ',' milliliters ',' millilitre ',' millilitres ',
' cc ',' l ',' L ',' liter ',' liters ',' litre ',' litres ',' teaspoon ',' teaspoons ',
' tablespoon ',' tablespoons ',' T ',' tbl ',' tbs ',' tbsp ',' fluid ounce ',' fluid ounces ',
' fl oz ',' gill ',' gills ',' cup ',' cups ',' c ',' pint ',' pints ',' p ',' pt ',' pts ',
' fl pt ',' fl pts ',' quart ',' quarts ',' q ',' qt ',' fl qt ',' fl qts ',' gallon ',
' gallons ',' g ',' gal ',' gals ',' mg ',' milligram ',' milligrams ',' milligramme ',
' milligrammes ',' g ',' gs ',' gram ',' grams ',' gramme ',' grammes ',' kg ',' kgs ',
' kilogram ',' kilograms ',' kilogramme ',' kilogrammes ',' pound ',' pounds ',' lb ',' lbs ',
' # ',' ounce ',' ounces ',' oz '])

for item in ingredients_quantity:
    # If int exists in string then pull int
    if any(char.isdigit() for char in item):
        for unit in measurements:
            if unit in item:
                quantity = (re.search(r'\d+', item).group()) + unit
                print(quantity)
    else:
        # Else put 0
        print(0)
