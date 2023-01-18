from scraper import unique_name_and_ingredients
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

cur = conn.cursor()

# Create recipe_table
recipe_table = 'recipe_table'
try:
    cur.execute(f"""
        CREATE TABLE {recipe_table} (
            recipe VARCHAR,
            ingredient VARCHAR,
            quantity VARCHAR,
            unit VARCHAR
        );
        """)
    print(f"Table {recipe_table} created successfully.")
except psycopg2.errors.DuplicateTable:
    print(f"Table {recipe_table} already exists.")
conn.commit()  # Commit the change

def insert():
    for tuple in unique_name_and_ingredients:
        recipe_name = tuple[0]
        for list in tuple[1]:
            try:
                quantity = list[0]
                unit = list[1]
                ingredient = list[2]

                cur.execute(f"""
                    INSERT INTO recipe_table (
                        recipe,
                        ingredient,
                        quantity,
                        unit
                    )
                    VALUES (
                        '{recipe_name}',
                        '{ingredient}',
                        '{quantity}',
                        '{unit}'
                    );
                    """)
                conn.commit()
            except:
                print(tuple)
                continue

table = insert()

cur.close()
conn.close()