from scraper import ingredient_list
import psycopg2

"""CONNECTING TO DATABASE"""
# Insert database name, username, password, server address, and port here
DB_NAME = ('postgres')
DB_USER = ('postgres')
DB_PASS = ('')
DB_HOST = ('localhost')
DB_PORT = ('5432')

try:
    conn = psycopg2.connect(
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASS,
        host=DB_HOST,
        port=DB_PORT)
    print("\nDatabase connected successfully!")
except:
    print("Database failed to connect.")

# Create recipe, ingredients, and quantities tables
tables = ['recipe_table','ingredient_table']
for table_name in tables:
    try:
        cur = conn.cursor()

        cur.execute(f"""
            CREATE TABLE {table_name} (
                id SERIAL PRIMARY KEY NOT NULL,
                "name" VARCHAR
            );
            """)
        print(f"Table {table_name} created successfully.")
    except psycopg2.errors.DuplicateTable:
        print(f"Table {table_name} already exists.")
    conn.commit()  # Commit the change

quantity_table = 'quantity_table'
try:
    cur.execute(f"""
        CREATE TABLE {quantity_table} (
            "unit" VARCHAR,
            "quantity#" VARHCAR,
            "recipe_id" INT,
            "ingredient_id" INT
        );
        """)
    print(f"Table {quantity_table} created successfully.")
except psycopg2.errors.DuplicateTable:
    print(f"Table {quantity_table} already exists.")
conn.commit()  # Commit the change

def insert():
    for list in ingredient_list:
        name = list[1]
    
        cur.execute(f"""
            INSERT INTO ingredient_table (
                "name"
            )
            VALUES (
                '{name}'
            );
            """)
        conn.commit() 

table = insert()
