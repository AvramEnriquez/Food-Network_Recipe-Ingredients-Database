from selenium import webdriver
path = "/Applications/chromedriver.exe"
driver = webdriver.Chrome(path)

def launchBrowser():
    driver.get("https://www.youtube.com/watch?v=Xjv1sY630Uc")
    print(driver.title)
    driver.quit()

drive = launchBrowser()

# for letter in list:
#     for page in letter:
#         for recipe in page:
#             # Grab URL until no more URLs
#         # Click Next until Next is disabled
#     # Click next letter