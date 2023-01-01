import requests
from bs4 import BeautifulSoup

url = "https://www.foodnetwork.com/recipes/tyler-florence/fajitas-recipe-1906480"

result = requests.get(url)
soup = BeautifulSoup(result.text, "html.parser")

ingredients = soup.find(type = "application/ld+json")

target = ingredients.text
start = target.find("recipeIngredient\":") + len("recipeIngredient\":[\"")
end = target.find("\"],\"nutrition")

list = target[start:end].split('","')
print(list)