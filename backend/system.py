from typing import List, Dict, Any
from .models import Car, Customer

# Oddiy ro'yxat ko'rinishidagi ma'lumotlar bazasi (Test uchun)
cars_db: List[Car] = [
    Car(car_id="01A111AA", make="Chevrolet", model="Malibu", year=2022, price_per_day=500000, 
        image_url="images/malibu.png"),
    Car(car_id="01B222BB", make="Chevrolet", model="Cobalt", year=2021, price_per_day=250000, 
        image_url="images/cobalt.png"),
    Car(car_id="01C333CC", make="Kia", model="K5", year=2023, price_per_day=700000, 
        image_url="images/k5.png"),
    Car(car_id="10D444DD", make="BYD", model="Chazor", year=2024, price_per_day=400000, 
        image_url="images/chazor.png"),
    Car(car_id="01E555EE", make="Chevrolet", model="Gentra", year=2024, price_per_day=300000, 
        image_url="images/gentra.png")
]

customers_db: List[Customer] = [
    Customer(customer_id=1, name="Ali Valiyev"),
    Customer(customer_id=2, name="Sardor Karimov"),
    Customer(customer_id=3, name="Gulnoza Alimova")
]

def get_all_cars():
    return cars_db

def get_available_cars():
    return [c for c in cars_db if not c.is_rented]

def get_all_customers():
    return customers_db

def rent_car(customer_id: int, car_id: str, days: int) -> Dict[str, Any]:
    car = next((c for c in cars_db if c.car_id == car_id), None)
    customer = next((c for c in customers_db if c.customer_id == customer_id), None)

    if not car:
        return {"success": False, "message": "Bunday raqamli mashina topilmadi."}
    if not customer:
        return {"success": False, "message": "Bunday ID li mijoz topilmadi."}
    if car.is_rented:
        return {"success": False, "message": "Kechirasiz, bu mashina hozirda band."}

    car.is_rented = True
    customer.rented_cars.append(car)
    total_price = car.price_per_day * days
    
    return {
        "success": True, 
        "message": f"Muaffaqiyatli! Jami to'lov: {total_price:,.0f} so'm.",
        "total_price": total_price
    }

def return_car(customer_id: int, car_id: str) -> Dict[str, Any]:
    car = next((c for c in cars_db if c.car_id == car_id), None)
    customer = next((c for c in customers_db if c.customer_id == customer_id), None)

    if not car or not customer:
        return {"success": False, "message": "Mashina yoki Mijoz topilmadi."}

    rented_car = next((c for c in customer.rented_cars if c.car_id == car_id), None)
    if rented_car:
        car.is_rented = False
        # Mijozning mashinalari ro'yxatidan o'chiramiz
        customer.rented_cars = [c for c in customer.rented_cars if c.car_id != car_id]
        return {"success": True, "message": "Mashina muvaffaqiyatli qaytarildi. Rahmat!"}
    
    return {"success": False, "message": "Bu mijoz ushbu mashinani ijaraga olmagan."}
