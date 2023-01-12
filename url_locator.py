import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.common.exceptions import ElementClickInterceptedException

path = "/Applications/chromedriver.exe"
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

def locate_url():
    driver.get("https://www.foodnetwork.com/recipes/recipes-a-z/123")
    
    # get number of elements to click on
    letter_count = 0 
    letters_len = len(driver.find_elements(By.CLASS_NAME, "o-IndexPagination__a-Button "))

    # Loop through letters in list
    while (letter_count < letters_len):
        # Get letters by class_name and click
        letter = driver.find_elements(By.CLASS_NAME, "o-IndexPagination__a-Button ")
        letter[letter_count].click()

        time.sleep(1)
        
        # Loop through pages in each letter by clicking "Next" until it can no longer be clicked
        while True:
            try:
                # Find recipe URLs on each page
                all_recipe_urls = []
                recipe = driver.find_elements(By.CLASS_NAME, "m-PromoList__a-ListItem")
                recipe_url = [s.find_element(By.TAG_NAME, 'a').get_attribute('href') for s in recipe]
                
                all_recipe_urls += recipe_url

                # Click "Next" button
                page = driver.find_element(By.XPATH, "//*[contains(@class, 'o-Pagination__a-NextButton')]")
                page.click()

                time.sleep(1)
            except ElementClickInterceptedException:
                break

        letter_count += 1

    driver.quit()

    return all_recipe_urls

all_recipe_urls = locate_url()

if __name__ == "__main__":
    print(all_recipe_urls)