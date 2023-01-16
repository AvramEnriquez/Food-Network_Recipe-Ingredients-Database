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

def insert():
    # Create url_table
    url_table = 'url_table'
    try:
        cur.execute(f"""
            CREATE TABLE {url_table} (
                url VARCHAR
            );
            """)
        print(f"Table {url_table} created successfully.")
        from url_locator import all_recipe_urls
        for url in all_recipe_urls:
            cur.execute(f"""
                INSERT INTO url_table (
                    url
                )
                VALUES (
                    '{url}'
                );
                """)
            conn.commit()
        
        # Pull URLs into list
        cur.execute("""
            SELECT 
                *
            FROM 
                url_table;
            """)
        url_tuples = cur.fetchall()
        url_list = list(map(list, zip(*url_tuples)))[0]
    except psycopg2.errors.DuplicateTable:
        print(f"Table {url_table} already exists.")
        conn.commit()

        # Pull URLs into list
        cur.execute("""
            SELECT 
                *
            FROM 
                url_table;
            """)
        url_tuples = cur.fetchall()
        url_list = list(map(list, zip(*url_tuples)))[0]

    conn.commit()

    return url_list

url_list = insert()

cur.close()
conn.close()