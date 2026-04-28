from models import Car, Customer

class CarRentalSystem:
    def __init__(self):
        self.cars = []
        self.customers = []

    def add_car(self, car):
        self.cars.append(car)

    def add_customer(self, customer):
        self.customers.append(customer)

    def display_available_cars(self):
        print("\n--- Bo'sh avtomobillar ro'yxati ---")
        available_cars = [car for car in self.cars if not car.is_rented]
        if not available_cars:
            print("Hozircha bo'sh avtomobillar yo'q.")
        else:
            for car in available_cars:
                print(car)

    def display_all_customers(self):
        print("\n--- Mijozlar ro'yxati ---")
        if not self.customers:
            print("Hozircha mijozlar ro'yxatga olinmagan.")
        else:
            for customer in self.customers:
                print(customer)

    def find_car(self, car_id):
        for car in self.cars:
            if car.car_id == car_id:
                return car
        return None

    def find_customer(self, customer_id):
        for customer in self.customers:
            if customer.customer_id == customer_id:
                return customer
        return None

    def rent_car(self, customer_id, car_id, days):
        car = self.find_car(car_id)
        customer = self.find_customer(customer_id)

        if not car:
            print("Bunday ID (raqamli) mashina topilmadi.")
            return
        if not customer:
            print("Bunday ID raqamli mijoz topilmadi.")
            return

        if car.is_rented:
            print(f"Kechirasiz, bu mashina hozirda band ({car.make} {car.model}).")
        else:
            car.is_rented = True
            customer.rented_cars.append(car)
            total_price = car.price_per_day * days
            print(f"\n✅ Muaffaqiyatli! {customer.name} '{car.make} {car.model}' mashinasini {days} kunga ijaraga oldi.")
            print(f"Jami to'lov: {total_price:,.0f} so'm.")

    def return_car(self, customer_id, car_id):
        car = self.find_car(car_id)
        customer = self.find_customer(customer_id)

        if not car or not customer:
            print("Xato: Mashina yoki Mijoz topilmadi.")
            return

        if car in customer.rented_cars:
            car.is_rented = False
            customer.rented_cars.remove(car)
            print(f"\n✅ {customer.name} '{car.make} {car.model}' mashinasini qaytardi. Rahmat!")
        else:
            print("Bu mijoz ushbu mashinani ijaraga olmagan.")
