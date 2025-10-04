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
        return f"Pizza {self.size} dengan topping: {', '.join(self.toppings)}"

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
        "Magic Dust": "Poof! Tastes like wizardry!"
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

    def display_bubble_chat(self):   
        print(f"                     ______________________________________________________________________")
        print(f"                    // {self.name}: {self.quote}                                           ")
        print(f"  _______           | {self.pizza}                                                            ")
        print(f" ༼ つ ◕_◕ ༽つ 🍕    | Hint: {', '.join(self.toppinghints[t] for t in self.toppings)}        ")
        print(f" |        |         | Patience: {self.time_left} seconds left!                               ")
        print(f"                    |_____________________________________________________________________")
        print(f"Total Harga: Rp {self.pizza.price():,}")

    def reduce_patience(self, elapsed_time):
        self.time_left -= int(elapsed_time)
        return self.time_left > 0

class VIPCustomer(Customer):  # Inheritance dari Customer
    def __init__(self):
        super().__init__()  # Memanggil __init__ dari Customer
        self._discount = random.uniform(0.1, 0.3)  # Diskon 10%-30% (enkapsulasi)
        self.priority = True  # Prioritas pelayanan

    # Enkapsulasi: Getter untuk discount
    def get_discount(self):
        return self._discount

    # Enkapsulasi: Setter untuk discount
    def set_discount(self, discount):
        if 0 <= discount <= 0.5:
            self._discount = discount
        else:
            raise ValueError("Diskon harus antara 0 dan 50%!")

    # Polymorphism: Override display_bubble_chat
    def display_bubble_chat(self):
        discounted_price = self.pizza.price() * (1 - self._discount)
        print(f"                     ______________________________________________________________________")
        print(f"                    // {self.name} [VIP]: {self.quote} (Diskon {self._discount*100:.1f}%)   ")
        print(f"  _______           | {self.pizza}                                                            ")
        print(f" ༼ つ ◕_◕ ༽つ 💎    | Hint: {', '.join(self.toppinghints[t] for t in self.toppings)}        ")
        print(f" |        |         | Patience: {self.time_left} seconds left! (Prioritas VIP)              ")
        print(f"                    |_____________________________________________________________________")
        print(f"Total Harga Asli: Rp {self.pizza.price():,}")
        print(f"Harga Setelah Diskon: Rp {discounted_price:,.0f}")

    def reduce_patience(self, elapsed_time):
        # VIP memiliki kesabaran lebih lama (50% tambahan)
        self.time_left -= int(elapsed_time * 0.5)
        return self.time_left > 0

class PizzaGame:
    def __init__(self):
        self.users = {}  # Menyimpan username: password
        self.current_user = None
        self.customers = []  # Menyimpan daftar pelanggan aktif
        self.running = False
        self.customer_thread = None

    def add_user(self, username, password):
        if username in self.users:
            print(f"Username '{username}' sudah ada!")
            return False
        self.users[username] = password
        print(f"User '{username}' berhasil ditambahkan.")
        return True

    def login(self, username, password):
        if username in self.users and self.users[username] == password:
            self.current_user = username
            print(f"Login berhasil! Selamat datang, {username}!")
            return True
        print("Username atau password salah!")
        return False

    def generate_customers(self):
        while self.running and self.current_user:
            if not self.customers:
                print("\nSemua pelanggan kehabisan kesabaran!")
            # 30% peluang untuk VIPCustomer
            if random.random() < 0.3:
                new_customer = VIPCustomer()
            else:
                new_customer = Customer()
            self.customers.append(new_customer)
            time.sleep(20)  # Tunggu 20 detik sebelum pelanggan baru

    def print_topping_info(self):
        print("\nInformasi Topping:")
        for topping, hint in Customer.toppinghints.items():
            price = Pizza.topping_prices[topping]
            print(f"- {topping}: Rp {price:,} ({hint})")

    def select_toppings(self, customer, customer_index):
        start_time = time.time()  # Catat waktu mulai
        print("\nDaftar Topping Tersedia:")
        available_toppings = list(Pizza.topping_prices.keys())
        # Membagi topping: 4 kiri, 4 tengah, 2 kanan
        left = available_toppings[:4]
        middle = available_toppings[4:8]
        right = available_toppings[8:]
        
        # Menentukan panjang maksimum untuk alignment
        max_len = max(len(topping) for topping in available_toppings)
        
        # Mencetak header
        print("-" * (3 * (max_len + 5)))
        
        # Mencetak topping dengan nomor menggunakan f-string
        for i in range(4):
            left_str = f"{i + 1} {left[i]:<{max_len}}" if i < len(left) else " " * (max_len + 4)
            middle_str = f"{i + 5} {middle[i]:<{max_len}}" if i < len(middle) else " " * (max_len + 4)
            right_str = f"{i + 9} {right[i]:<{max_len}}" if i < len(right) else " " * (max_len + 4)
            print(f"{left_str:<{max_len + 5}} {middle_str:<{max_len + 5}} {right_str:<{max_len + 5}}")

        num_toppings = len(customer.toppings)
        print(f"\nPilih {num_toppings} topping untuk {customer.name} (masukkan nomor, pisahkan dengan spasi):")
        try:
            choices = list(map(int, input().split()))
            end_time = time.time()  # Catat waktu selesai
            elapsed_time = end_time - start_time  # Hitung waktu yang dihabisan
            
            # Kurangi kesabaran pelanggan yang dipilih
            if not customer.reduce_patience(elapsed_time):
                print(f"\n{customer.name} kehabisan kesabaran dan pergi!")
                self.customers.pop(customer_index)
                return
            
            if len(choices) != num_toppings:
                print(f"Harus memilih tepat {num_toppings} topping!")
                return
            
            selected_toppings = [available_toppings[i - 1] for i in choices if 1 <= i <= len(available_toppings)]
            if len(selected_toppings) != num_toppings:
                print("Pilihan nomor topping tidak valid!")
                return
            
            # Periksa apakah topping yang dipilih cocok dengan topping pelanggan
            if sorted(selected_toppings) == sorted(customer.toppings):
                print(f"\nSelamat! Pesanan untuk {customer.name} berhasil diselesaikan!")
                self.customers.pop(customer_index)  # Hapus pelanggan yang dilayani
            else:
                print(f"\nMaaf, topping yang dipilih tidak sesuai dengan pesanan {customer.name}!")
                
        except (ValueError, IndexError):
            end_time = time.time()  # Catat waktu selesai meskipun error
            elapsed_time = end_time - start_time
            if not customer.reduce_patience(elapsed_time):
                print(f"\n{customer.name} kehabisan kesabaran dan pergi!")
                self.customers.pop(customer_index)
            else:
                print("Masukkan nomor topping yang valid!")

    def lobby_menu(self):
        while self.current_user and not self.running:
            print(f"\n=== Lobby (User: {self.current_user}) ===")
            print("1. Cek Hint Topping")
            print("2. Start Game")
            print("3. Logout")
            choice = input("Pilih opsi (1-3): ")

            if choice == "1":
                self.print_topping_info()
            elif choice == "2":
                self.running = True
                self.customers = []  # Kosongkan pelanggan saat mulai game
                self.customer_thread = threading.Thread(target=self.generate_customers)
                self.customer_thread.daemon = True
                self.customer_thread.start()
                self.game_menu()
            elif choice == "3":
                print(f"Logout berhasil. Sampai jumpa, {self.current_user}!")
                self.current_user = None
            else:
                print("Opsi tidak valid!")

    def game_menu(self):
        while self.running and self.current_user:
            print(f"\n=== Menu Game (User: {self.current_user}) ===")
            print("Daftar Pelanggan Aktif:")
            for i, customer in enumerate(self.customers, 1):
                print(f"{i}. {customer.name} (Kesabaran: {customer.time_left} detik)")
            try:
                choice = int(input("Pilih nomor pelanggan untuk melayani pesanan (0 untuk lanjut ke opsi menu): "))
                if choice == 0:
                    pass  # Lanjut ke opsi menu
                elif 1 <= choice <= len(self.customers):
                    selected_customer = self.customers[choice - 1]
                    selected_customer.display_bubble_chat()
                    self.select_toppings(selected_customer, choice - 1)
                else:
                    print("Pilihan tidak valid!")
            except ValueError:
                print("Masukkan nomor yang valid!")
             
    def run(self):
        while True:
            if not self.current_user:
                print("\n=== Menu Login ===")
                print("1. Login")
                print("2. Tambah User")
                print("3. Keluar")
                choice = input("Pilih opsi (1-3): ")
                
                if choice == "1":
                    username = input("Username: ")
                    password = input("Password: ")
                    if self.login(username, password):
                        self.lobby_menu()
                elif choice == "2":
                    username = input("Masukkan username baru: ")
                    password = input("Masukkan password baru: ")
                    self.add_user(username, password)
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
