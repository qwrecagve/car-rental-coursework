from models import Car, Customer
from system import CarRentalSystem

def main():
    system = CarRentalSystem()

    # Dastlabki ma'lumotlarni qo'shamiz (Test uchun)
    system.add_car(Car("01A111AA", "Chevrolet", "Malibu", 2022, 500000))
    system.add_car(Car("01B222BB", "Chevrolet", "Cobalt", 2021, 250000))
    system.add_car(Car("01C333CC", "Kia", "K5", 2023, 700000))
    system.add_car(Car("10D444DD", "BYD", "Chazor", 2024, 400000))

    system.add_customer(Customer(1, "Ali Valiyev"))
    system.add_customer(Customer(2, "Sardor Karimov"))
    system.add_customer(Customer(3, "Gulnoza Alimova"))

    while True:
        print("\n" + "="*40)
        print("       AVTOMOBIL IJARASI TIZIMI")
        print("="*40)
        print("1. Bo'sh avtomobillarni ko'rish")
        print("2. Mijozlar ro'yxatini ko'rish")
        print("3. Avtomobil ijaraga olish")
        print("4. Avtomobilni qaytarish")
        print("5. Dasturdan chiqish")
        print("="*40)

        choice = input("Tanlovingizni kiriting (1-5): ")

        if choice == '1':
            system.display_available_cars()
        elif choice == '2':
            system.display_all_customers()
        elif choice == '3':
            try:
                cust_id = int(input("Mijoz ID sini kiriting: "))
                car_id = input("Avtomobil ID (raqami)ni kiriting: ").strip()
                days = int(input("Necha kunga ijaraga olasiz? "))
                system.rent_car(cust_id, car_id, days)
            except ValueError:
                print("Iltimos, ID va kunlarni to'g'ri raqam formatida kiriting.")
        elif choice == '4':
            try:
                cust_id = int(input("Mijoz ID sini kiriting: "))
                car_id = input("Qaytarilayotgan Avtomobil ID (raqami)ni kiriting: ").strip()
                system.return_car(cust_id, car_id)
            except ValueError:
                print("Iltimos, ma'lumotlarni to'g'ri kiriting.")
        elif choice == '5':
            print("Dasturdan foydalanganingiz uchun rahmat. Xayr!")
            break
        else:
            print("Noto'g'ri tanlov. Iltimos, 1 dan 5 gacha bo'lgan raqamni tanlang.")

if __name__ == "__main__":
    main()
