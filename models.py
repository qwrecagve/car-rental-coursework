class Car:
    def __init__(self, car_id, make, model, year, price_per_day):
        self.car_id = car_id
        self.make = make
        self.model = model
        self.year = year
        self.price_per_day = price_per_day
        self.is_rented = False

    def __str__(self):
        status = "Band" if self.is_rented else "Bo'sh"
        return f"[{self.car_id}] {self.make} {self.model} ({self.year}) - Kuniga: {self.price_per_day:,.0f} so'm. Holati: {status}"

class Customer:
    def __init__(self, customer_id, name):
        self.customer_id = customer_id
        self.name = name
        self.rented_cars = []

    def __str__(self):
        # Ijaraga olingan avtomobillar raqamlarini ko'rsatish
        rented_ids = ", ".join([car.car_id for car in self.rented_cars]) if self.rented_cars else "Yo'q"
        return f"Mijoz: {self.name} (ID: {self.customer_id}). Ijaradagi mashinalari: {rented_ids}"
