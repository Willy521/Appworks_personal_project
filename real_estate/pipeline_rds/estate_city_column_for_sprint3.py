# estate_city_column_for_sprint3

import pymysql
from dotenv import load_dotenv
from decouple import config

# 環境變數
load_dotenv()
password = config('DATABASE_PASSWORD')
password_bytes = password.encode('utf-8')


# connect to db
def connect_db():
    try:
        conn = pymysql.connect(
            host='appworks.cwjujjrb7yo0.ap-southeast-2.rds.amazonaws.com',
            port=3306,
            user='admin',
            password=password_bytes,
            database='estate_data_hub',
            charset='utf8mb4'
        )
        print("Have connected to db")
        return conn
    except Exception as e:
        print(f"error: {e}")
        return None


def update_city_column(conn):
    try:
        cursor = conn.cursor()

        # Check if the city column exists
        cursor.execute("SHOW COLUMNS FROM real_estate LIKE 'city';")
        result = cursor.fetchone()

        # If city column does not exist, then add it
        if not result:
            cursor.execute("ALTER TABLE real_estate ADD city VARCHAR(255);")
            print("Added 'city' column to the table.")

        # Update city column based on address column
        sql = """
        UPDATE real_estate
        SET city = CASE
            WHEN LOCATE('市', address) > 0 THEN SUBSTRING(address, 1, LOCATE('市', address))
            WHEN LOCATE('縣', address) > 0 THEN SUBSTRING(address, 1, LOCATE('縣', address))
            ELSE ''
            END;
        """
        cursor.execute(sql)
        conn.commit()

        print("City column updated successfully!")
        cursor.close()

    except Exception as e:
        print(f"Error while updating city column: {e}")


def create_sprint3_demo_table(conn):
    try:
        cursor = conn.cursor()
        sql = """
        CREATE TABLE IF NOT EXISTS sprint3_demo AS 
        SELECT id, city, district, address, zoning, transaction_date, build_case, buildings_and_number 
        FROM real_estate;
        """
        cursor.execute(sql)
        print("Created 'sprint3_demo' table successfully!")
        cursor.close()
    except Exception as e:
        print(f"Error while creating 'sprint3_demo' table: {e}")


def main():
    conn = connect_db()
    if conn:
        update_city_column(conn)
        create_sprint3_demo_table(conn)
        conn.close()


if __name__ == "__main__":
    main()
