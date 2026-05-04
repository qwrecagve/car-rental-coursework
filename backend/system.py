import sqlite3
import os
import pyodbc
from datetime import datetime
from typing import List, Optional
from .models import Car, Customer, CarCreate, CustomerCreate

DB_PATH = os.path.join(os.path.dirname(__file__), "cars.db")
AZURE_CONN = os.getenv("AZURE_SQL_CONNECTIONSTRING")
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")

def get_db_connection():
    if ENVIRONMENT == "production" and AZURE_CONN:
        return pyodbc.connect(AZURE_CONN)
    
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def rows_to_dicts(cursor, rows):
    """pyodbc va sqlite uchun universial row->dict konvertori"""
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in rows]

def fetchone_to_dict(cursor, row):
    if row is None:
        return None
    columns = [col[0] for col in cursor.description]
    return dict(zip(columns, row))

db_init_error = None

def init_db():
    global db_init_error
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Azure SQL va SQLite farqini hisobga olamiz
        is_azure = (ENVIRONMENT == "production")
        
        # Mashinalar jadvali
        cursor.execute(f'''
            IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'cars')
            CREATE TABLE cars (
                car_id NVARCHAR(50) PRIMARY KEY,
                make NVARCHAR(100),
                model NVARCHAR(100),
                year INT,
                price_per_day FLOAT,
                image_url NVARCHAR(MAX),
                is_rented INT DEFAULT 0
            )
        ''' if is_azure else '''
            CREATE TABLE IF NOT EXISTS cars (
                car_id TEXT PRIMARY KEY,
                make TEXT,
                model TEXT,
                year INTEGER,
                price_per_day REAL,
                image_url TEXT,
                is_rented INTEGER DEFAULT 0
            )
        ''')
        
        # Mijozlar jadvali
        cursor.execute(f'''
            IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'customers')
            CREATE TABLE customers (
                customer_id INT PRIMARY KEY IDENTITY(1,1),
                name NVARCHAR(200),
                phone NVARCHAR(50),
                rented_car_id NVARCHAR(50),
                FOREIGN KEY (rented_car_id) REFERENCES cars (car_id)
            )
        ''' if is_azure else '''
            CREATE TABLE IF NOT EXISTS customers (
                customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                phone TEXT,
                rented_car_id TEXT,
                FOREIGN KEY (rented_car_id) REFERENCES cars (car_id)
            )
        ''')

        # Ijaralar tarixi
        cursor.execute(f'''
            IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'rentals')
            CREATE TABLE rentals (
                id INT PRIMARY KEY IDENTITY(1,1),
                car_id NVARCHAR(50),
                customer_id INT,
                rental_date NVARCHAR(50),
                days INT,
                total_price FLOAT
            )
        ''' if is_azure else '''
            CREATE TABLE IF NOT EXISTS rentals (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                car_id TEXT,
                customer_id INTEGER,
                rental_date TEXT,
                days INTEGER,
                total_price REAL
            )
        ''')
        
        # Boshlang'ich ma'lumotlar (agar bo'sh bo'lsa)
        check_query = "SELECT COUNT(*) FROM cars" if is_azure else "SELECT COUNT(*) FROM cars"
        cursor.execute(check_query)
        if cursor.fetchone()[0] == 0:
            initial_cars = [
                ('01A123AA', 'Chevrolet', 'Malibu', 2023, 500000.0, 'images/malibu-uz.jpg'),
                ('01B456BB', 'Chevrolet', 'Gentra', 2022, 300000.0, 'images/gentra.jpg'),
                ('01C789CC', 'Chevrolet', 'Cobalt', 2021, 250000.0, 'images/cobalt.jpg')
            ]
            for car in initial_cars:
                cursor.execute("INSERT INTO cars (car_id, make, model, year, price_per_day, image_url) VALUES (?, ?, ?, ?, ?, ?)", car)
        
        conn.commit()
        conn.close()
    except Exception as e:
        db_init_error = str(e)
        print("DATABASE INIT ERROR:", e)

# Bazani ishga tushirish
init_db()

def get_all_cars() -> List[Car]:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM cars")
    rows = rows_to_dicts(cursor, cursor.fetchall())
    conn.close()
    return [Car(**row) for row in rows]

def get_available_cars() -> List[Car]:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM cars WHERE is_rented = 0")
    rows = rows_to_dicts(cursor, cursor.fetchall())
    conn.close()
    return [Car(**row) for row in rows]

def get_rented_cars():
    conn = get_db_connection()
    cursor = conn.cursor()
    query = """
        SELECT c.car_id, c.make, c.model, c.year, c.price_per_day, c.image_url, c.is_rented,
               r.rental_date, r.days, r.total_price 
        FROM cars c
        JOIN rentals r ON c.car_id = r.car_id
        WHERE c.is_rented = 1
    """
    cursor.execute(query)
    rows = rows_to_dicts(cursor, cursor.fetchall())
    conn.close()
    return rows

def get_active_customers() -> List[Customer]:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM customers WHERE rented_car_id IS NOT NULL")
    rows = rows_to_dicts(cursor, cursor.fetchall())
    conn.close()
    return [Customer(**row) for row in rows]

def get_all_registered_customers() -> List[Customer]:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM customers")
    rows = rows_to_dicts(cursor, cursor.fetchall())
    conn.close()
    return [Customer(**row) for row in rows]

def add_car(car: CarCreate):
    conn = get_db_connection()
    try:
        conn.execute("INSERT INTO cars (car_id, make, model, year, price_per_day, image_url) VALUES (?, ?, ?, ?, ?, ?)",
                     (car.car_id, car.make, car.model, car.year, car.price_per_day, car.image_url))
        conn.commit()
        return True
    except:
        return False
    finally:
        conn.close()

def delete_car(car_id: str):
    conn = get_db_connection()
    try:
        conn.execute("DELETE FROM cars WHERE car_id = ?", (car_id,))
        conn.commit()
        return True
    except:
        return False
    finally:
        conn.close()

def add_customer(customer: CustomerCreate):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO customers (name, phone) VALUES (?, ?)", (customer.name, customer.phone))
    conn.commit()
    new_id = cursor.lastrowid
    conn.close()
    return new_id

def rent_car(customer_id: int, car_id: str, days: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Mashina bo'shmi?
    cursor.execute("SELECT * FROM cars WHERE car_id = ? AND is_rented = 0", (car_id,))
    car = fetchone_to_dict(cursor, cursor.fetchone())
    if not car:
        conn.close()
        return {"error": "Mashina band yoki mavjud emas"}
    
    # Mijoz bormi?
    cursor.execute("SELECT * FROM customers WHERE customer_id = ?", (customer_id,))
    cust = fetchone_to_dict(cursor, cursor.fetchone())
    if not cust:
        conn.close()
        return {"error": "Mijoz topilmadi. Avval mijozni ro'yxatdan o'tkazing."}

    # Ijaraga berish
    cursor.execute("UPDATE cars SET is_rented = 1 WHERE car_id = ?", (car_id,))
    cursor.execute("UPDATE customers SET rented_car_id = ? WHERE customer_id = ?", (car_id, customer_id))
    
    total_price = car['price_per_day'] * days
    
    # Tarixga yozish
    today = datetime.now().strftime("%Y-%m-%d")
    cursor.execute("INSERT INTO rentals (car_id, customer_id, rental_date, days, total_price) VALUES (?, ?, ?, ?, ?)",
                   (car_id, customer_id, today, days, total_price))
    
    conn.commit()
    conn.close()
    
    return {
        "message": f"{car['make']} {car['model']} ijaraga berildi!",
        "total_price": total_price,
        "customer": cust['name']
    }

def get_earnings_report():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Bugungi sana
    now = datetime.now()
    current_month = now.strftime("%Y-%m")
    current_year = now.strftime("%Y")
    
    # 1 oylik tushum
    month_total = cursor.execute("SELECT SUM(total_price) FROM rentals WHERE rental_date LIKE ?", (f"{current_month}%",)).fetchone()[0] or 0
    
    # 1 yillik tushum
    year_total = cursor.execute("SELECT SUM(total_price) FROM rentals WHERE rental_date LIKE ?", (f"{current_year}%",)).fetchone()[0] or 0
    
    # Jami ijaralar soni
    total_rentals = cursor.execute("SELECT COUNT(*) FROM rentals").fetchone()[0]
    
    conn.close()
    
    return {
        "month_total": month_total,
        "year_total": year_total,
        "total_rentals": total_rentals
    }

def get_rental_history():
    conn = get_db_connection()
    cursor = conn.cursor()
    query = """
        SELECT r.id, r.car_id, r.customer_id, r.rental_date, r.days, r.total_price,
               c.make, c.model, cust.name as customer_name 
        FROM rentals r
        JOIN cars c ON r.car_id = c.car_id
        JOIN customers cust ON r.customer_id = cust.customer_id
        ORDER BY r.id DESC
    """
    cursor.execute(query)
    rows = rows_to_dicts(cursor, cursor.fetchall())
    conn.close()
    return rows

def return_car(customer_id: int, car_id: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Tekshirish
    cursor.execute("SELECT * FROM customers WHERE customer_id = ? AND rented_car_id = ?", (customer_id, car_id))
    res = cursor.fetchone()
    if not res:
        conn.close()
        return {"error": "Bunday ijara topilmadi"}
    
    # Qaytarish
    cursor.execute("UPDATE cars SET is_rented = 0 WHERE car_id = ?", (car_id,))
    cursor.execute("UPDATE customers SET rented_car_id = NULL WHERE customer_id = ?", (customer_id,))
    
    conn.commit()
    conn.close()
    return {"message": "Mashina muvaffaqiyatli qaytarildi!"}
