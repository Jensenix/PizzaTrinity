import random
import threading
import time
from abc import ABC, abstractmethod

# === CUSTOM EXCEPTIONS ===
class PizzaError(Exception):
    pass

class InvalidToppingError(PizzaError):
    def __init__(self, toppings):
        self.toppings = toppings
        super().__init__(f"Topping tidak valid: {', '.join(toppings)}")

class OutOfStockError(PizzaError):
    def __init__(self, topping):
        self.topping = topping
        super().__init__(f"Stok {topping} habis!")

class UsernameError(PizzaError):
    def __init__(self, message):
        super().__init__(message)

class PasswordError(PizzaError):
    def __init__(self, message):
        super().__init__(message)

# === DATABASE KELAS  ===
class CustomerDatabase:
    __customers = [
        ("Alien Zog", "Beep boop, pizza or planetary destruction!"),
        ("Nenek Superhero", "Cepat, pizza ini untuk menyelamatkan dunia!"),
        ("Kucing Onar", "Meow, pizza harus punya tuna dan chaos!"),
        ("Zombie Bob", "Braaains... eh, maksudnya pizza!")
    ]
    __topping_hints = {
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
    __available_toppings = list({
        "Cheese": 10000, "Pepperoni": 12000, "Mushroom": 8000, "Olives": 9000, "Tomato Sauce": 7000,
        "Exploding Peppers": 15000, "Unicorn Glitter": 20000, "Zombie Fingers": 18000,
        "Invisible Onions": 5000, "Magic Dust": 25000
    }.keys())

    @classmethod
    def get_random_customer(kelas):
        return random.choice(kelas.__customers)

    @classmethod
    def get_topping_hint(kelas, topping):
        return kelas.__topping_hints.get(topping, "No hint available.")

    @classmethod
    def get_available_toppings(kelas):
        return kelas.__available_toppings.copy()

# === PIZZA ===
class Pizza:
    base_price = {"Small": 50000, "Medium": 75000, "Large": 100000}
    topping_prices = {
        "Cheese": 10000, "Pepperoni": 12000, "Mushroom": 8000, "Olives": 9000, "Tomato Sauce": 7000,
        "Exploding Peppers": 15000, "Unicorn Glitter": 20000, "Zombie Fingers": 18000,
        "Invisible Onions": 5000, "Magic Dust": 25000
    }

    def __init__(self, size, toppings):
        if size not in self.base_price:
            raise PizzaError("Ukuran pizza tidak valid!")
        invalid_toppings = [t for t in toppings if t not in self.topping_prices]
        if invalid_toppings:
            raise InvalidToppingError(invalid_toppings)
        self.size = size
        self.toppings = toppings

    def price(self):
        return self.base_price[self.size] + sum(self.topping_prices[t] for t in self.toppings)

    def __str__(self):
        return f"Pizza {self.size}"

# === ABSTRACT CUSTOMER ===
class AbstractCustomer(ABC):
    def __init__(self, level_manager):
        self.level_manager = level_manager
        self.name, self.quote = CustomerDatabase.get_random_customer()
        self.size = random.choice(list(Pizza.base_price.keys()))
        num_toppings = random.randint(2, 4)
        self.toppings = random.sample(CustomerDatabase.get_available_toppings(), num_toppings)
        self.pizza = Pizza(self.size, self.toppings)
        self.patience = level_manager.get_patience_modifier()
        self.time_left = self.patience

    def _display_common_order(self):
        print("")
        print("──────────────────────────────────────")
        print("CUSTOMER ORDER")
        print("──────────────────────────────────────")
        print(f"Nama      : {self.name}")
        print(f"Kesabaran : {self.time_left} detik")
        print(f"Pesanan   : {self.pizza}")
        for topping in self.toppings:
            print(f"   - {topping}")
        print("Hint      :")
        for topping in self.toppings:
            print(f"   • {CustomerDatabase.get_topping_hint(topping)}")
        print(f"Harga     : Rp {self.pizza.price():,}")

    @abstractmethod
    def display_chat(self):
        pass

    @abstractmethod
    def reduce_patience(self, elapsed_time):
        pass

    @abstractmethod
    def get_payment(self):
        pass

# === REGULAR CUSTOMER ===
class Customer(AbstractCustomer):
    def display_chat(self):
        self._display_common_order()

    def reduce_patience(self, elapsed_time):
        self.time_left -= int(elapsed_time)
        return self.time_left > 0

    def get_payment(self):
        return self.pizza.price()

# === VIP CUSTOMER ===
class VIPCustomer(AbstractCustomer):
    def __init__(self, level_manager):
        super().__init__(level_manager)
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
        self._display_common_order()
        discounted_price = self.pizza.price() * (1 - self._discount)
        print(f"Nama      : {self.name} [VIP]")
        print(f"Kesabaran : {self.time_left} detik (Prioritas)")
        print(f"Harga     : Rp {self.pizza.price():,}")
        print(f"   Diskon {self._discount*100:.1f}% → Rp {discounted_price:,.0f}")
        print("──────────────────────────────────────")

    def reduce_patience(self, elapsed_time):
        self.time_left -= int(elapsed_time * 0.5)
        return self.time_left > 0

    def get_payment(self):
        return int(self.pizza.price() * (1 - self._discount))

# === CHALLENGE CUSTOMER ===
class ChallengeCustomer(AbstractCustomer):
    def __init__(self, level_manager):
        super().__init__(level_manager)
        self.name = "CHALLENGE MASTER"
        self.size = "Large"
        self.toppings = random.sample(CustomerDatabase.get_available_toppings(), 8)
        self.pizza = Pizza(self.size, self.toppings)
        self.time_limit = 30
        self.start_time = None

    def display_chat(self):
        print("")
        print("FIRE" + "═" * 50)
        print("         CHALLENGE MODE")
        print("═" * 50)
        print(f"Nama      : {self.name}")
        print(f"WAKTU     : 30 detik TOTAL!")
        print(f"Pesanan   : {self.pizza}")
        for topping in self.toppings:
            print(f"   - {topping}")
        print("Hint      :")
        for topping in self.toppings:
            print(f"   • {CustomerDatabase.get_topping_hint(topping)}")
        print(f"Hadiah    : Rp 500,000 + 500 Score (jika berhasil!)")
        print("═" * 50)

    def reduce_patience(self, elapsed_time):
        return True

    def start_timer(self):
        self.start_time = time.time()

    def get_remaining_time(self):
        if self.start_time is None:
            return 30
        elapsed = time.time() - self.start_time
        return max(0, 30 - int(elapsed))

    def is_time_up(self):
        return self.get_remaining_time() <= 0

    def get_payment(self):
        return 500000

# === LEVEL MANAGER ===
class LevelManager:
    def __init__(self, level=1):
        self._level = level
        self._level_thresholds = {1: 0, 2: 5, 3: 15, 4: 30, 5: 50}
        self._patience_reduction = 5
        self._spawn_rate_reduction = 2
        self._base_spawn_rate = 10

    def get_level(self):
        return self._level

    def update_level(self, orders_completed):
        for level, threshold in sorted(self._level_thresholds.items(), reverse=True):
            if orders_completed >= threshold and self._level < level:
                self._level = level
                print(f"Selamat! Kamu naik ke Level {self._level}!")
                return True
        return False

    def get_patience_modifier(self):
        return max(10, 40 - (self._level - 1) * self._patience_reduction)

    def get_spawn_rate(self):
        return max(5, self._base_spawn_rate - (self._level - 1) * self._spawn_rate_reduction)

# === INVENTORY ===
class Inventory:
    def __init__(self, stock_data=None):
        default_stock = {topping: 10 for topping in Pizza.topping_prices.keys()}
        self._stock = stock_data if stock_data else default_stock
        self._max_stock = 20
        self._cost_per_stock = {
            "Cheese": 8000, "Pepperoni": 12000, "Mushroom": 6000, "Olives": 7000,
            "Tomato Sauce": 5000, "Exploding Peppers": 15000, "Unicorn Glitter": 25000,
            "Zombie Fingers": 18000, "Invisible Onions": 4000, "Magic Dust": 30000
        }

    def get_stock(self, topping):
        return self._stock.get(topping, 0)

    def get_restock_cost(self, topping):
        return self._cost_per_stock.get(topping, 5000)

    def use_topping(self, topping):
        if self._stock[topping] <= 0:
            raise OutOfStockError(topping)
        self._stock[topping] -= 1

    def restock(self, topping, amount, uang_saat_ini):
        if topping not in self._stock:
            raise InvalidToppingError([topping])
        cost = amount * self._cost_per_stock[topping]
        if uang_saat_ini < cost:
            raise ValueError(f"Uang tidak cukup! Perlu Rp {cost:,}.")
        if self._stock[topping] + amount > self._max_stock:
            raise ValueError(f"Stok maksimum {self._max_stock} untuk {topping}.")
        self._stock[topping] += amount
        return cost
    
    def display(self):
        print("\nINVENTARIS TOPPING")
        print("=" * 40)
        for topping, stock in self._stock.items():
            print(f"{topping:<15}: {stock} unit (Restok: Rp {self._cost_per_stock[topping]:,}/unit)")
        print("=" * 40)

    def get_state(self):
        return self._stock.copy()
    
    def suggest_restock(self, min_stock=2, restock_amount=5):
            for topping, stock in self._stock.items():
                if stock <= min_stock:
                    cost_per_unit = self._cost_per_stock[topping]
                    total_cost = cost_per_unit * restock_amount
                    yield {
                        'topping': topping,
                        'current': stock,
                        'suggest': restock_amount,
                        'cost_per_unit': cost_per_unit,
                        'total_cost': total_cost,
                        'message': f"{topping}: {stock} → +{restock_amount} = Rp {total_cost:,}"
                    }

# === CUSTOMER MANAGER ===
class CustomerManager:
    def __init__(self, level_manager):
        self.customers = []
        self.running = False
        self.level_manager = level_manager
        self.thread = None

    def start(self):
        self.running = True
        self.thread = threading.Thread(target=self._generate_loop)
        self.thread.daemon = True
        self.thread.start()

    def stop(self):
        self.running = False

    def _generate_loop(self):
        while self.running:
            if random.random() < 0.3:
                customer = VIPCustomer(self.level_manager)
            else:
                customer = Customer(self.level_manager)
            self.customers.append(customer)
            time.sleep(self.level_manager.get_spawn_rate())

    def remove_customer(self, index):
        if 0 <= index < len(self.customers):
            del self.customers[index]

# === UI MANAGER ===
class UIManager: 
    @staticmethod
    def print_topping_list(inventory):
        toppings = CustomerDatabase.get_available_toppings()
        left = toppings[:5]
        right = toppings[5:]
        print("\n[ DAFTAR TOPPING ]")
        print("=" * 50)
        for i in range(5):
            left_str = f"{left[i]} ({inventory.get_stock(left[i])})" if i < len(left) else ""
            right_str = f"{right[i]} ({inventory.get_stock(right[i])})" if i < len(right) else ""
            print(f"{i+1}. {left_str:<22} | {i+6}. {right_str:<22}")
        print("=" * 50)

    @staticmethod
    def display_status(username, level, score, orders, uang_saat_ini, time_left):
        print("PLAYER STATUS")
        print(f"User           : {username}")
        print(f"Level          : {level}")
        print(f"Score          : {score}")
        print(f"Uang Saat Ini  : Rp {uang_saat_ini:,}")
        print(f"Pesanan Selesai: {orders}")
        print(f"WAKTU TOTAL    : {time_left//60:02d}:{time_left%60:02d}")
        print("──────────────────────────────────────")

# === AUTH MANAGER ===
class AuthManager:
    def __init__(self):
        self._users = {}
        self._current_user = None

    def validate_username(self, username):
        if not username:
            raise UsernameError("Username tidak boleh kosong!")
        if not (5 <= len(username) <= 15):
            raise UsernameError("Username harus 5-15 karakter!")
        return True

    def validate_password(self, password):
        if not password:
            raise PasswordError("Password tidak boleh kosong!")
        if len(password) < 5:
            raise PasswordError("Password harus minimal 5 karakter!")
        return True

    def add_user(self, username, password):
        try:
            self.validate_username(username)
            self.validate_password(password)
            if username in self._users:
                raise UsernameError("Username sudah ada!")
            self._users[username] = password
            return True
        except (UsernameError, PasswordError) as e:
            raise

    def login(self, username, password):
        try:
            self.validate_username(username)
            self.validate_password(password)
            if username in self._users and self._users[username] == password:
                self._current_user = username
                return True
            raise UsernameError("Username atau password salah!")
        except (UsernameError, PasswordError) as e:
            raise

    def logout(self):
        self._current_user = None

    @property
    def current_user(self):
        return self._current_user

    def is_logged_in(self):
        return self._current_user is not None

# === MAIN GAME ===
class PizzaGame:
    GAME_TIME_LIMIT = 300  # 5 menit

    def __init__(self):
        self.auth = AuthManager()
        self.ui = UIManager()
        self.user_data = {}

    def _load_user_data(self, username):
        if username not in self.user_data:
            self.user_data[username] = {
                'uang_saat_ini': 0,
                'score': 0,
                'orders_completed': 0,
                'challenge_completed': False,
                'level': 1,
                'inventory_stock': {t: 10 for t in Pizza.topping_prices.keys()},
                'game_start_time': None
            }
        data = self.user_data[username]
        self.uang_saat_ini = data['uang_saat_ini']
        self._score = data['score']
        self.orders_completed = data['orders_completed']
        self.challenge_completed = data['challenge_completed']
        self.level_manager = LevelManager(data['level'])
        self.inventory = Inventory(data['inventory_stock'])
        self.customer_manager = CustomerManager(self.level_manager)
        self.game_start_time = data['game_start_time']

    def _save_user_data(self, username):
        if username in self.user_data:
            self.user_data[username].update({
                'uang_saat_ini': self.uang_saat_ini,
                'score': self._score,
                'orders_completed': self.orders_completed,
                'challenge_completed': self.challenge_completed,
                'level': self.level_manager.get_level(),
                'inventory_stock': self.inventory.get_state(),
                'game_start_time': self.game_start_time
            })

    def _add_score(self, points):
        self._score += points

    def _get_game_time_left(self):
        if self.game_start_time is None:
            return PizzaGame.GAME_TIME_LIMIT
        elapsed = time.time() - self.game_start_time
        return max(0, PizzaGame.GAME_TIME_LIMIT - int(elapsed))

    def _show_game_over_summary(self):
        print("\n" + "═" * 50)
        print("           WAKTU HABIS!")
        print("           GAME OVER")
        print("═" * 50)
        print(f"   Uang Didapat Sesinya : Rp {self.uang_saat_ini - 10000:,}")
        print(f"   Pesanan Selesai       : {self.orders_completed}")
        print(f"   Score                 : {self._score}")
        print(f"   Level                 : {self.level_manager.get_level()}")
        print("═" * 50)
        input("   Tekan Enter untuk kembali ke menu...")

    def _handle_topping_selection(self, customer, index):
        start_time = time.time()
        self.ui.print_topping_list(self.inventory)
        num_toppings = len(customer.toppings)
        print(f"\n> Pilih {num_toppings} topping (pisahkan spasi): ", end="")
        try:
            choices = list(map(int, input().split()))
            elapsed = time.time() - start_time

            if not customer.reduce_patience(elapsed):
                print(f"\n{customer.name} kehabisan kesabaran dan pergi!")
                self.customer_manager.remove_customer(index)
                return

            if len(choices) != num_toppings:
                print(f"Harus memilih tepat {num_toppings} topping!")
                return

            available = CustomerDatabase.get_available_toppings()
            selected = [available[i-1] for i in choices if 1 <= i <= len(available)]
            if len(selected) != num_toppings:
                print("Nomor topping tidak valid!")
                return

            for t in selected:
                self.inventory.use_topping(t)

            if sorted(selected) == sorted(customer.toppings):
                payment = customer.get_payment()
                print(f"\nPesanan untuk {customer.name} selesai! Mendapat Rp {payment:,}")
                self.customer_manager.remove_customer(index)
                self._add_score(100)
                self.uang_saat_ini += payment
                self.orders_completed += 1
                if self.level_manager.update_level(self.orders_completed):
                    print(f"Kesabaran: {self.level_manager.get_patience_modifier()} detik, spawn: {self.level_manager.get_spawn_rate()} detik.")
            else:
                print(f"\nTopping salah untuk {customer.name}!")

        except (ValueError, OutOfStockError, InvalidToppingError) as e:
            elapsed = time.time() - start_time
            if not customer.reduce_patience(elapsed):
                print(f"\n{customer.name} kehabisan kesabaran dan pergi!")
                self.customer_manager.remove_customer(index)
            else:
                print(f"Error: {str(e)}")

    def _restock_menu(self):
        while True:
            self.inventory.display()
            print(f"\nUang Saat Ini: Rp {self.uang_saat_ini:,}")
            
            # === TAMPILKAN SARAN RESTOK DARI GENERATOR ===
            print("\nSARAN RESTOK (otomatis):")
            print("-" * 50)
            has_suggestion = False
            for suggestion in self.inventory.suggest_restock(min_stock=2, restock_amount=5):
                has_suggestion = True
                print(f"   • {suggestion['message']}")
            if not has_suggestion:
                print("   Semua stok aman!")
            print("-" * 50)
            # ============================================

            print("\n> Restok (contoh: Cheese 3) | Kosongkan = kembali")
            print("> ", end="")
            inp = input().strip()
            if inp == "":
                print("Kembali ke menu utama.")
                break

            try:
                topping, amount = inp.split()
                amount = int(amount)
                if amount <= 0:
                    print("Jumlah harus > 0!")
                    continue

                cost = self.inventory.restock(topping, amount, self.uang_saat_ini)
                self.uang_saat_ini -= cost
                print(f"Restok {amount} {topping} berhasil! Biaya: Rp {cost:,}")

            except ValueError:
                print("Format salah! Contoh: Cheese 3")
            except Exception as e:
                print(f"Error: {str(e)}")

    def _challenge_mode(self):
        if self.challenge_completed:
            print("\nKamu sudah menyelesaikan Challenge Mode hari ini!")
            input("Tekan Enter untuk kembali...")
            return


        print("\n" + "🔥" * 20)
        print("       MEMULAI CHALLENGE MODE!")
        print("       8 TOPPING • 30 DETIK")
        print("🔥" * 20)
        input("Tekan Enter untuk mulai...")

        challenge = ChallengeCustomer(self.level_manager)
        challenge.display_chat()
        challenge.start_timer()

        self.ui.print_topping_list(self.inventory)
        print(f"\n> Pilih 8 topping (pisahkan spasi): ", end="")

        try:
            choices = list(map(int, input().split()))
            total_time = time.time() - challenge.start_time

            if total_time > 30:
                print(f"\nWAKTU HABIS! Kamu butuh {total_time:.1f} detik.")
                print("CHALLENGE GAGAL!")
                self.uang_saat_ini -= 50000
                print("Penalti: -Rp 50,000")
                input("\nTekan Enter...")
                return

            if len(choices) != 8:
                print("Harus pilih tepat 8 topping!")
                return

            available = CustomerDatabase.get_available_toppings()
            selected = [available[i-1] for i in choices if 1 <= i <= len(available)]
            if len(selected) != 8:
                print("Pilihan duplikat atau tidak lengkap!")
                return

            for t in selected:
                if self.inventory.get_stock(t) <= 0:
                    print(f"Stok {t} habis!")
                    return
                self.inventory.use_topping(t)

            if sorted(selected) == sorted(challenge.toppings):
                bonus = 500000
                score_bonus = 500
                print(f"\nSELAMAT! SELESAI DALAM {total_time:.1f} DETIK!")
                print(f"Bonus: Rp {bonus:,} | Score: +{score_bonus}")
                self.uang_saat_ini += bonus
                self._add_score(score_bonus)
                self.orders_completed += 1
                self.level_manager.update_level(self.orders_completed)
                self.challenge_completed = True
            else:
                print("\nTopping salah! Gagal.")
                self.uang_saat_ini -= 30000
                print("Penalti: -Rp 30,000")

        except Exception as e:
            print(f"Error: {str(e)}")
        finally:
            input("\nTekan Enter untuk kembali...")
    def _show_leaderboard(self):
        if self.auth.is_logged_in():
            self._save_user_data(self.auth.current_user)

        if not self.user_data:
            print("\nBelum ada data pemain yang tersimpan.")
            input("Tekan Enter untuk kembali...")
            return

        print("\n" + "═" * 40)
        print("          LEADERBOARD GLOBAL")
        print("═" * 40)

        sorted_players = sorted(
            self.user_data.items(),
            key=lambda item: item[1].get('score', 0),
            reverse=True
        )

        print(f"{'Rank':<6}{'User':<16}{'Score':<8}{'Uang':<12}{'Lvl':<4}")
        print("-" * 40)
        for rank, (username, data) in enumerate(sorted_players, start=1):
            if rank > 10:
                break
            score = data.get('score', 0)
            uang = data.get('uang_saat_ini', 0)
            level = data.get('level', 1)
            uang_str = f"Rp{uang:,}"
            print(f"{rank:<6}{username:<16}{score:<8}{uang_str:<12}{level:<4}")
        print("═" * 40)
        input("Tekan Enter untuk kembali...")

    def _lobby_menu(self):
        username = self.auth.current_user
        while self.auth.is_logged_in():
            time_left = self._get_game_time_left()
            print("\n" + "═" * 40)
            print(f"|{'PIZZA SHOP GAME':^38}|")
            print("═" * 40)
            print(f"    Selamat datang, {username}!")
            print(f"    WAKTU: {time_left//60:02d}:{time_left%60:02d}")
            print("──────────────────────────────────────")
            print("[ MENU UTAMA ]")
            print("1. Lihat Daftar Topping")
            print("2. Mulai Permainan (5 Menit)")
            print("3. Restok Topping")
            print("4. Challenge Mode")
            print("5. Lihat Statistik Lengkap")
            print("6. Leaderboard Semua Pemain")
            print("7. Logout")
            print("──────────────────────────────────────")
            choice = input("Pilih (1-6): ")

            if choice == "1":
                self.ui.print_topping_list(self.inventory)
                input("Tekan Enter...")
            elif choice == "2":
                self.game_start_time = time.time()
                self.customer_manager.start()
                self._game_loop()
            elif choice == "3":
                self._restock_menu()
            elif choice == "4":
                self._challenge_mode()
            elif choice == "5":
                print("\n" + "═" * 40)
                print("     STATISTIK LENGKAP")
                print("═" * 40)
                print(f"User            : {username}")
                print(f"Level           : {self.level_manager.get_level()}")
                print(f"Score           : {self._score}")
                print(f"Uang Saat Ini   : Rp {self.uang_saat_ini:,}")
                print(f"Pesanan Selesai : {self.orders_completed}")
                print("═" * 40)
                input("Tekan Enter untuk kembali...")
            elif choice == "6":
                self._show_leaderboard()
                
            elif choice == "7":
                self._save_user_data(username)
                print(f"Logout berhasil. Sampai jumpa, {username}!")
                self.auth.logout()
            else:
                print("Pilihan tidak valid!")

            
    def _game_loop(self):
        while self.customer_manager.running and self.auth.is_logged_in():
            time_left = self._get_game_time_left()
            if time_left <= 0:
                self.customer_manager.stop()
                self._show_game_over_summary()
                self.game_start_time = None
                self._lobby_menu()
                return

            if not self.customer_manager.customers:
                print(f"\nWAKTU: {time_left//60:02d}:{time_left%60:02d} | Belum ada pelanggan! Tekan Enter...")
                inp = input()
                if inp.strip() == "0":
                    self.customer_manager.stop()
                    self.game_start_time = None
                    self._lobby_menu()
                    return
                continue

            print(f"\n|{'═' * 38}|")
            print(f"|{'PIZZA SHOP GAME':^38}|")
            print(f"|{'═' * 38}|")
            print(f"|{'🦸 '+self.auth.current_user:^20} | 🌟Level {self.level_manager.get_level()}{'|':>6}")
            print(f"|{'─' *38 }|")
            print(f"| WAKTU {time_left//60:02d}:{time_left%60:02d}{'|':>27}")
            print(f"|{'─' *38 }|")
            print(f"| Pelanggan Aktif: {'|':>21}")
            for i, c in enumerate(self.customer_manager.customers, 1):
                status = "[VIP]" if isinstance(c, VIPCustomer) else ""
                print(f"|{i:<1}. {c.name:<16} {status:<5} {'(Time:':>6} {c.time_left}s) |")
            print(f"|{'─' *38 }|")

            try:
                inp = input("Pilih pelanggan | Back [0] | Refresh [ENTER]: ")
                if inp == "":
                    continue
                choice = int(inp)
                if choice == 0:
                    self.customer_manager.stop()
                    self.game_start_time = None
                    self._lobby_menu()
                    return
                elif 1 <= choice <= len(self.customer_manager.customers):
                    cust = self.customer_manager.customers[choice - 1]
                    cust.display_chat()
                    self._handle_topping_selection(cust, choice - 1)
                else:
                    print("Nomor tidak valid!")
            except ValueError:
                print("Masukkan angka!")

            self.ui.display_status(
                self.auth.current_user,
                self.level_manager.get_level(),
                self._score,
                self.orders_completed,
                self.uang_saat_ini,
                time_left
            )

    def run(self):
        print("PIZZA SHOP GAME - UANG DISIMPAN PER AKUN")
        while True:
            if not self.auth.is_logged_in():
                print("\n" + "═" * 40)
                print("        PIZZA SHOP GAME")
                print("═" * 40)
                print("──────────────────────────────────────")
                print("[ MENU LOGIN ]")
                print("1. Login")
                print("2. Daftar")
                print("3. Keluar")
                print("──────────────────────────────────────")
                choice = input("Pilih (1-3): ")
                if choice == "1":
                    username = input("Username: ")
                    password = input("Password: ")
                    try:
                        if self.auth.login(username, password):
                            print(f"✅ Login berhasil! Halo, {username}! ✅")
                            self._load_user_data(username)
                            self._lobby_menu()
                    except (UsernameError, PasswordError) as e:
                        print(f"{str(e)}")
                elif choice == "2":
                    username = input("Username baru: ")
                    password = input("Password baru: ")
                    try:
                        if self.auth.add_user(username, password):
                            print(f"✔️ User '{username}' berhasil dibuat. ✔️")
                    except (UsernameError, PasswordError) as e:
                        print(f"{str(e)}")
                elif choice == "3":
                    print("Terima kasih telah bermain!")
                    break
                else:
                    print("Pilihan tidak valid!")
            else:
                self._lobby_menu()

if __name__ == "__main__":
    game = PizzaGame()
    game.run()