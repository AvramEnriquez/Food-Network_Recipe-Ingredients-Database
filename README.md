# Food Network_Recipe Ingredients Database
 WIP Project to pull recipe names and ingredients from the Food Network and store them in a database
 
 Makes use of Selenium and BeautifulSoup modules to scrape URLs from the Food Network website and Pint module to match and compare varying units of measurement. Also makes use of psycopg2 module to upload URLs, recipe names, ingredients, and units/quantity into databases. 
 
 Currently finding that the most difficult thing about this is that different authors upload recipes differently.
 Examples:
 - "1 - 4 ounce peach"
 - "75g/2 3/4 ounce butter"
 - "2 cups (450 g) butter"
 - "2 1/2 onions"
 

UPDATE: Made too many requests on their website, project is currently on hold.
