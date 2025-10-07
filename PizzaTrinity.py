import random
import threading
import time

class Pizza:
    base_price = {"Small": 50000, "Medium": 75000, "Large": 100000}
    topping_prices = {
        "Cheese": 10000, "Pepperoni": 12000, "Mushroom": 8000, "Olives": 9000, "Tomato Sauce": 7000,
        "Exploding Peppers": 15000, "Unicorn Glitter": 20000, "Zombie Fingers": 18000, 
        "Invisible Onions": 5000, "Magic Dust": 25000
    }

    def __init__(self, size, toppings):
        if size not in self.base_price:
            raise ValueError("Ukuran pizza tidak valid!")
        invalid_toppings = [t for t in toppings if t not in self.topping_prices]
        if invalid_toppings:
            raise ValueError(f"Topping tidak valid: {invalid_toppings}")
        self.size = size
        self.toppings = toppings

    def price(self):
        return self.base_price[self.size] + sum(self.topping_prices[t] for t in self.toppings)

    def __str__(self):
        return f"Pizza {self.size}"

class Customer:
    customers = [
        ("Alien Zog", "Beep boop, pizza or planetary destruction!"),
        ("Nenek Superhero", "Cepat, pizza ini untuk menyelamatkan dunia!"),
        ("Kucing Pembuat Onar", "Meow, pizza harus punya tuna dan chaos!"),
        ("Zombie Bob", "Braaains... eh, maksudnya pizza!")
    ]
    toppinghints = {
        "Cheese": "Melts like my heart in a rom-com!",
        "Pepperoni": "Round, spicy, like tiny UFOs!",
        "Mushroom": "Funky fungi from the forest!",
        "Olives": "Little green moons of joy!",
        "Tomato Sauce": "Red like a superhero cape!",
        "Exploding Peppers": "BOOM! Careful, it bites!",
        "Unicorn Glitter": "Sparkles like my dreams!",
        "Zombie Fingers": "Crunchy and... undead?",
        "Invisible Onions": "You can't see it, but it makes you cry!",
        "Magic Dust": "Tastes like wizardry!"
    }
    available_toppings = list(Pizza.topping_prices.keys())

    def __init__(self):
        self.name, self.quote = random.choice(self.customers)
        self.size = random.choice(list(Pizza.base_price.keys()))
        num_toppings = random.randint(2, 4)
        self.toppings = random.sample(self.available_toppings, num_toppings)
        self.pizza = Pizza(self.size, self.toppings)
        self.patience = random.randint(20, 40)
        self.time_left = self.patience

    def display_chat(self): 
        print("")  
        print("──────────────────────────────────────")  
        print("🍕 CUSTOMER ORDER")
        print("──────────────────────────────────────")
        print(f"👤 Nama      : {self.name}")
        print(f"⏳ Kesabaran : {self.time_left} detik")
        print(f"📦 Pesanan   : {self.pizza}")
        for topping in self.toppings:
            print(f"   - {topping}")
        print("💡 Hint      :")
        for topping in self.toppings:
            print(f"   • {self.toppinghints[topping]}")
        print(f"💰 Harga     : Rp {self.pizza.price():,}")

    def reduce_patience(self, elapsed_time):
        self.time_left -= int(elapsed_time)
        return self.time_left > 0

class VIPCustomer(Customer):
    def __init__(self):
        super().__init__()
        self._discount = random.uniform(0.1, 0.3)
        self.priority = True

    def get_discount(self):
        return self._discount

    def set_discount(self, discount):
        if 0 <= discount <= 0.5:
            self._discount = discount
        else:
            raise ValueError("Diskon harus antara 0 dan 50%!")

    def display_chat(self):
        discounted_price = self.pizza.price() * (1 - self._discount)
        print("──────────────────────────────────────")
        print("🍕 CUSTOMER ORDER")
        print("──────────────────────────────────────")
        print(f"👤 Nama      : {self.name} [VIP]")
        print(f"⏳ Kesabaran : {self.time_left} detik (Prioritas)")
        print(f"📦 Pesanan   : {self.pizza}")
        for topping in self.toppings:
            print(f"   - {topping}")
        print("💡 Hint      :")
        for topping in self.toppings:
            print(f"   • {self.toppinghints[topping]}")
        print(f"💰 Harga     : Rp {self.pizza.price():,}")
        print(f"   Diskon {self._discount*100:.1f}% → Rp {discounted_price:,.0f}")
        print("──────────────────────────────────────")

    def reduce_patience(self, elapsed_time):
        self.time_left -= int(elapsed_time * 0.5)
        return self.time_left > 0

class AuthManager:
    def __init__(self):
        self._users = {}
        self._current_user = None

    def add_user(self, username, password):
        if username in self._users:
            return False
        self._users[username] = password
        return True

    def login(self, username, password):
        if username in self._users and self._users[username] == password:
            self._current_user = username
            return True
        return False

    def logout(self):
        self._current_user = None

    @property
    def current_user(self):
        return self._current_user

    def is_logged_in(self):
        return self._current_user is not None

class PizzaGame:
    def __init__(self):
        self.auth_manager = AuthManager()
        self.running = False
        self.customer_thread = None
        self.customers = []
        self.score = 0
        self.orders_completed = 0

    def generate_customers(self):
        while self.running and self.auth_manager.is_logged_in():
            if random.random() < 0.3:
                new_customer = VIPCustomer()
            else:
                new_customer = Customer()
            self.customers.append(new_customer)
            time.sleep(20)

    def print_topping_info(self):
        print("\n[ TOPPING LIST ]")
        available_toppings = list(Pizza.topping_prices.keys())
        left = available_toppings[:5]
        right = available_toppings[5:]
        print("=" * 40)
        for i in range(5):
            left_str = left[i] if i < len(left) else ""
            right_str = right[i] if i < len(right) else ""
            print(f"{i+1}. {left_str:<15} | {i+6}. {right_str:<15}")
        print("=" * 40)

    def display_player_status(self):
        print("🏆 PLAYER STATUS")
        print(f"User   : {self.auth_manager.current_user}")
        print(f"Score  : {self.score}")
        print(f"Pesanan: {self.orders_completed} selesai")
        print("--------------------------------------")

    def select_toppings(self, customer, customer_index):
        start_time = time.time()
        self.print_topping_info()
        num_toppings = len(customer.toppings)
        print(f"\n> Pilih {num_toppings} topping: ", end="")
        try:
            choices = list(map(int, input().split()))
            end_time = time.time()
            elapsed_time = end_time - start_time
            
            if not customer.reduce_patience(elapsed_time):
                print(f"\n{customer.name} kehabisan kesabaran dan pergi!")
                self.customers.pop(customer_index)
                return
            
            if len(choices) != num_toppings:
                print(f"Harus memilih tepat {num_toppings} topping!")
                return
            
            available_toppings = list(Pizza.topping_prices.keys())
            selected_toppings = [available_toppings[i - 1] for i in choices if 1 <= i <= len(available_toppings)]
            if len(selected_toppings) != num_toppings:
                print("Pilihan nomor topping tidak valid!")
                return
            
            if sorted(selected_toppings) == sorted(customer.toppings):
                print(f"\n✔ Pesanan untuk {customer.name} selesai!")
                self.customers.pop(customer_index)
                self.score += 100
                self.orders_completed += 1
            else:
                print(f"\nMaaf, topping yang dipilih tidak sesuai dengan pesanan {customer.name}!")
                
        except (ValueError, IndexError):
            end_time = time.time()
            elapsed_time = end_time - start_time
            if not customer.reduce_patience(elapsed_time):
                print(f"\n{customer.name} kehabisan kesabaran dan pergi!")
                self.customers.pop(customer_index)
            else:
                print("Masukkan nomor topping yang valid!")

    def lobby_menu(self):
        while self.auth_manager.is_logged_in():
            print("")
            print("╔══════════════════════════════════╗")
            print("║          PIZZA SHOP GAME         ║")
            print("╚══════════════════════════════════╝")
            print(f"            Welcome, {self.auth_manager.current_user}           ")
            print("--------------------------------------")
            print("[ MAIN MENU ]")
            print("▸ 1. Cek Hint Topping")
            print("▸ 2. Start Game")
            print("▸ 3. Logout")
            print("--------------------------------------")
            choice = input("Pilih opsi (1-3): ")

            if choice == "1":
                self.print_topping_info()
            elif choice == "2":
                self.running = True
                self.customers = []
                self.customer_thread = threading.Thread(target=self.generate_customers)
                self.customer_thread.daemon = True
                self.customer_thread.start()
                self.game_menu()
            elif choice == "3":
                print(f"Logout berhasil. Sampai jumpa, {self.auth_manager.current_user}!")
                self.auth_manager.logout()
            else:
                print("Opsi tidak valid!")

    def game_menu(self):
        while self.running and self.auth_manager.is_logged_in():
            print(f"\n╔══════════════════════════════════╗")
            print(f"║          PIZZA SHOP GAME         ║")
            print(f"╚══════════════════════════════════╝")
            print(f"            Welcome, {self.auth_manager.current_user}           ")
            print("--------------------------------------")
            print("Daftar Pelanggan Aktif:")
            for i, customer in enumerate(self.customers, 1):
                print(f"{i}. {customer.name} (Kesabaran: {customer.time_left} detik)")
            try:
                choice = int(input("Pilih nomor pelanggan untuk melayani pesanan [0] (mulai kembali)| [Enter] (Refresh)"))
                if choice == 0:
                    self.lobby_menu()
                elif 1 <= choice <= len(self.customers):
                    selected_customer = self.customers[choice - 1]
                    selected_customer.display_chat()
                    self.select_toppings(selected_customer, choice - 1)
                else:
                    print("Pilihan tidak valid!")
            except ValueError:
                print("Masukkan nomor yang valid!")
            self.display_player_status()

    def run(self):
        while True:
            if not self.auth_manager.is_logged_in():
                print("\n╔══════════════════════════════════╗")
                print("║          PIZZA SHOP GAME         ║")
                print("╚══════════════════════════════════╝")
                print("--------------------------------------")
                print("[ LOGIN MENU ]")
                print("▸ 1. Login")
                print("▸ 2. Tambah User")
                print("▸ 3. Keluar")
                print("--------------------------------------")
                choice = input("Pilih opsi (1-3): ")
                
                if choice == "1":
                    username = input("Username: ")
                    password = input("Password: ")
                    if self.auth_manager.login(username, password):
                        print(f"Login berhasil! Selamat datang, {self.auth_manager.current_user}!")
                        self.lobby_menu()
                    else:
                        print("Username atau password salah!")
                elif choice == "2":
                    username = input("Masukkan username baru: ")
                    password = input("Masukkan password baru: ")
                    if self.auth_manager.add_user(username, password):
                        print(f"User '{username}' berhasil ditambahkan.")
                    else:
                        print(f"Username '{username}' sudah ada!")
                elif choice == "3":
                    self.running = False
                    print("Terima kasih telah bermain!")
                    break
                else:
                    print("Opsi tidak valid!")
            else:
                self.lobby_menu()

if __name__ == "__main__":
    game = PizzaGame()
    game.run()