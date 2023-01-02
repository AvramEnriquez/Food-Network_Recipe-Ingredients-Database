import requests
from bs4 import BeautifulSoup

url = "https://www.foodnetwork.com/recipes/tyler-florence/fajitas-recipe-1906480"

def scraper(url):
    # Request HTML for URL then parse it
    result = requests.get(url)
    soup = BeautifulSoup(result.text, "html.parser")
    
    # Look for Food Network's ingredients checkbox by looking for inputs that contain the following conditions 
    shopping_list = soup.find_all("input", {"class" : "o-Ingredients__a-Ingredient--Checkbox"}, {"type" : "checkbox"})

    ingredients = []
    ingredients = [item["value"] for item in shopping_list[1:]]  # Item "value" contains ingredient + quantity

    return ingredients

print(scraper(url))