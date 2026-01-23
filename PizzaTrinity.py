import random
import threading
import time
import heapq
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

# === DATABASE KELAS ===
class CustomerDatabase:
    __customers = [
        ("Alien Zog", "Beep boop, pizza or planetary destruction!"),
        ("Nenek Superhero", "Cepat, pizza ini untuk meyelamatkan dunia!"),
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

#  STRATEGY PATTERN  
class ToppingStrategy(ABC):
    @abstractmethod
    def apply_effect(self, price, toppings):
        """Menerapkan efek dan mengembalikan (harga_baru, pesan_efek)."""
        pass

class NormalStrategy(ToppingStrategy):
    def apply_effect(self, price, toppings):
        return price, "Harga Normal"

class DailyDiscountStrategy(ToppingStrategy):
    def __init__(self, discount_rate):
        self.discount_rate = discount_rate
    
    def apply_effect(self, price, toppings):
        new_price = int(price * (1 - self.discount_rate))
        return new_price, f"Diskon Harian! (-{self.discount_rate*100:.0f}%)"

class FreeToppingStrategy(ToppingStrategy):
    def apply_effect(self, price, toppings):
        topping_price = 0
        topping_name = ""
        if toppings:
            first_topping = toppings[0]
            topping_price = Pizza.topping_prices.get(first_topping, 0)
            topping_name = first_topping
        
        new_price = price - topping_price
        return max(0, new_price), f"Topping Gratis: {topping_name}" if toppings else "Topping Gratis"

# === ABSTRACT FACTORY CUSTOMER ===
class CustomerFactory(ABC):
    @abstractmethod
    def create(self, level_manager):
        pass


class RegularCustomerFactory(CustomerFactory):
    def create(self, level_manager):
        return Customer(level_manager)


class VIPCustomerFactory(CustomerFactory):
    def create(self, level_manager):
        return VIPCustomer(level_manager)


# === PRIORITY QUEUE WRAPPER ===
class PrioritizedCustomer:
    def __init__(self, customer):
        self.customer = customer
        self.priority = 0 if isinstance(customer, VIPCustomer) else 1
        self.timestamp = time.time()

    def __lt__(self, other):
        return (self.priority, self.timestamp) < (other.priority, other.timestamp)

#  ABSTRACT CUSTOMER 
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
        print(f"Nama: {self.name}")
        print(f"Kesabaran : {self.time_left} detik")
        print(f"Pesanan : {self.pizza}")
        for topping in self.toppings:
            print(f" - {topping}")
        print("Hint:")
        for topping in self.toppings:
            print(f" • {CustomerDatabase.get_topping_hint(topping)}")
        # Base Price
        print(f"Harga Dasar: Rp {self.pizza.price():,}")


    @abstractmethod
    def display_chat(self, strategy): 
        pass

    @abstractmethod
    def reduce_patience(self, elapsed_time):
        pass

    @abstractmethod
    def get_payment(self, strategy): 
        pass

#  REGULAR CUSTOMER 
class Customer(AbstractCustomer):
    def display_chat(self, strategy): 
        self._display_common_order()
        price, effect_msg = strategy.apply_effect(self.pizza.price(), self.toppings)
        print(f"Harga Final: Rp {price:,.0f} ({effect_msg})")
        print("──────────────────────────────────────")

    def reduce_patience(self, elapsed_time):
        self.time_left -= int(elapsed_time)
        return self.time_left > 0

    def get_payment(self, strategy): 
        price, _ = strategy.apply_effect(self.pizza.price(), self.toppings)
        return price

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

    def display_chat(self, strategy): 
        self._display_common_order()
        base_price = self.pizza.price()
        discounted_price_raw = base_price * (1 - self._discount)
        final_price, effect_msg = strategy.apply_effect(discounted_price_raw, self.toppings)
        
        print(f"Nama: {self.name} [VIP]")
        print(f"Kesabaran : {self.time_left} detik (Prioritas)")
        print(f"Harga Dasar: Rp {base_price:,}")
        print(f" Diskon VIP {self._discount*100:.1f}% → Rp {discounted_price_raw:,.0f}")
        print(f" Strategi Harian: {effect_msg}")
        print(f"Harga Final: Rp {final_price:,.0f}")
        print("──────────────────────────────────────")

    def reduce_patience(self, elapsed_time):
        self.time_left -= int(elapsed_time * 0.5)
        return self.time_left > 0

    def get_payment(self, strategy): 
        base_price = self.pizza.price()
        discounted_price_raw = base_price * (1 - self._discount)
        final_price, _ = strategy.apply_effect(discounted_price_raw, self.toppings)
        return int(final_price)

#  CHALLENGE CUSTOMER 
class ChallengeCustomer(AbstractCustomer):
    def __init__(self, level_manager):
        super().__init__(level_manager)
        self.name = "CHALLENGE MASTER"
        self.size = "Large"
        self.toppings = random.sample(CustomerDatabase.get_available_toppings(), 8)
        self.pizza = Pizza(self.size, self.toppings)
        self.time_limit = 30
        self.start_time = None

    def display_chat(self, strategy=None): 
        print("")
        print("FIRE" + "═" * 50)
        print(" CHALLENGE MODE")
        print("═" * 50)
        print(f"Nama: {self.name}")
        print(f"WAKTU : 30 detik TOTAL!")
        print(f"Pesanan : {self.pizza}")
        for topping in self.toppings:
            print(f" - {topping}")
        print("Hint:")
        for topping in self.toppings:
            print(f" • {CustomerDatabase.get_topping_hint(topping)}")
        print(f"Hadiah: Rp 500,000 + 500 Score (jika berhasil!)")
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

    def get_payment(self, strategy=None):
        return 500000

#  STATE PATTERN  
class DifficultyState(ABC):
    @abstractmethod
    def get_patience_modifier(self, base_level):
        pass
    
    @abstractmethod
    def get_spawn_rate(self, base_level):
        pass

    @abstractmethod
    def get_score_multiplier(self):
        pass

class EasyState(DifficultyState):
    def get_patience_modifier(self, base_level):
        return max(20, 50 - (base_level - 1) * 5)
    
    def get_spawn_rate(self, base_level):
        return max(8, 15 - (base_level - 1) * 2)

    def get_score_multiplier(self):
        return 0.8 

class MediumState(DifficultyState):
    def get_patience_modifier(self, base_level):
        return max(10, 40 - (base_level - 1) * 5)
    
    def get_spawn_rate(self, base_level):
        return max(5, 10 - (base_level - 1) * 2)

    def get_score_multiplier(self):
        return 1.0

class HardState(DifficultyState):
    def get_patience_modifier(self, base_level):
        return max(5, 20 - (base_level - 1) * 3)
    
    def get_spawn_rate(self, base_level):
        return max(2, 6 - (base_level - 1) * 1)

    def get_score_multiplier(self):
        return 1.5 

# === LEVEL MANAGER (Context untuk State) ===
class LevelManager:
    def __init__(self, level=1, initial_state="Medium"):
        self._level = level
        self._level_thresholds = {1: 0, 2: 5, 3: 15, 4: 30, 5: 50}
        self.set_state(initial_state)

    def get_level(self):
        return self._level
    
    def set_state(self, state_name):
        state_name = state_name.lower()
        if state_name == "easy":
            self._state = EasyState()
        elif state_name == "medium":
            self._state = MediumState()
        elif state_name == "hard":
            self._state = HardState()
        else:
            raise ValueError("State kesulitan tidak valid!")
        self.state_name = state_name

    def update_level(self, orders_completed):
        for level, threshold in sorted(self._level_thresholds.items(), reverse=True):
            if orders_completed >= threshold and self._level < level:
                self._level = level
                print(f"Selamat! Kamu naik ke Level {self._level}!")
                return True
        return False

    def get_patience_modifier(self):
        return self._state.get_patience_modifier(self._level)

    def get_spawn_rate(self):
        return self._state.get_spawn_rate(self._level)
        
    def get_score_multiplier(self):
        return self._state.get_score_multiplier()

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
        self.queue = []
        self.running = False
        self.level_manager = level_manager
        self.spawn_thread = None
        self.timer_thread = None

        self.factories = [
            (0.3, VIPCustomerFactory()),
            (0.7, RegularCustomerFactory())
        ]

    def start(self):
        self.running = True
        self.spawn_thread = threading.Thread(target=self._spawn_loop, daemon=True)
        self.timer_thread = threading.Thread(target=self._timer_loop, daemon=True)
        self.spawn_thread.start()
        self.timer_thread.start()

    def stop(self):
        self.running = False

    # === SPAWN CUSTOMER VIA FACTORY ===
    def _spawn_loop(self):
        while self.running:
            r = random.random()
            acc = 0
            for chance, factory in self.factories:
                acc += chance
                if r <= acc:
                    customer = factory.create(self.level_manager)
                    heapq.heappush(self.queue, PrioritizedCustomer(customer))
                    break
            time.sleep(self.level_manager.get_spawn_rate())

    # === AUTO PATIENCE TIMER ===
    def _timer_loop(self):
        while self.running:
            time.sleep(1)
            expired = []

            for pc in self.queue:
                pc.customer.time_left -= 1 if not isinstance(pc.customer, VIPCustomer) else 0.5
                if pc.customer.time_left <= 0:
                    expired.append(pc.customer)

            for customer in expired:
                print(f"\n⏰ {customer.name} kehabisan kesabaran dan pergi!")
                self.remove_customer(customer)

    # === ACCESSORS ===
    def get_customers(self):
        return [pc.customer for pc in sorted(self.queue)]

    def remove_customer(self, customer):
        self.queue = [pc for pc in self.queue if pc.customer != customer]
        heapq.heapify(self.queue)


# AUTH MANAGER 
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

#  ADAPTER PATTERN 
class ExternalLogSystem:
    def log_transaction(self, id_number, customer_name, total_payment, is_success):
        """Menerima ID unik, Nama Pelanggan, Total Pembayaran, dan Status."""
        print(f"[EKSTERNAL LOG] ID: {id_number:05d} | Nama: {customer_name:<15} | Bayar: Rp {total_payment:,.0f} | Status: {'SUCCESS' if is_success else 'FAILED'}")

class OrderLoggerAdapter:
    def __init__(self, external_system):
        self._external_system = external_system
        self._log_counter = 1000 

    def log_order_completion(self, customer, payment, success=True):
        self._external_system.log_transaction(
            id_number=self._log_counter,
            customer_name=customer.name,
            total_payment=payment if success else 0,
            is_success=success
        )
        self._log_counter += 1

    def log_order_failure(self, customer):
        self._external_system.log_transaction(
            id_number=self._log_counter,
            customer_name=customer.name,
            total_payment=0,
            is_success=False
        )
        self._log_counter += 1

# =========================
# DAILY QUEST SYSTEM
# =========================

class Quest(ABC):
    def __init__(self, description, reward_money=0, reward_score=0):
        self.description = description
        self.reward_money = reward_money
        self.reward_score = reward_score
        self.completed = False

    @abstractmethod
    def check_progress(self, game):
        pass

    def give_reward(self, game):
        game.uang_saat_ini += self.reward_money
        game._add_score(self.reward_score)
        self.completed = True

class CompleteOrderQuest(Quest):
    def __init__(self, target):
        super().__init__(
            f"Selesaikan {target} pesanan",
            reward_money=50000,
            reward_score=100
        )
        self.target = target

    def check_progress(self, game):
        return game.orders_completed >= self.target


class ServeVIPQuest(Quest):
    def __init__(self):
        super().__init__(
            "Layani 1 pelanggan VIP",
            reward_money=75000,
            reward_score=150
        )
        self.served = False

    def mark_served(self):
        self.served = True

    def check_progress(self, game):
        return self.served

class DailyQuestManager:
    def __init__(self):
        self.quests = []

    def generate_daily_quests(self):
        self.quests = [
            CompleteOrderQuest(3),
            ServeVIPQuest()
        ]

    def check_all(self, game):
        for quest in self.quests:
            if not quest.completed and quest.check_progress(game):
                quest.give_reward(game)
                print(f"🎉 QUEST SELESAI: {quest.description}")



# =========================
# BOOST / ITEM SHOP SYSTEM
# =========================

class Boost(ABC):
    def __init__(self, name, price):
        self.name = name
        self.price = price

    @abstractmethod
    def apply(self, game):
        pass

class SlowTimeBoost(Boost):
    def __init__(self):
        super().__init__("Slow Time", 50000)

    def apply(self, game):
        game.level_manager.set_state("Easy")
        print("⏳ Waktu pelanggan melambat sementara!")


class MoneyBoost(Boost):
    def __init__(self):
        super().__init__("Money Boost", 75000)

    def apply(self, game):
        game.uang_saat_ini += 100000
        print("💰 Bonus uang langsung!")

class BoostShop:
    def __init__(self):
        self.items = [
            SlowTimeBoost(),
            MoneyBoost()
        ]

    def display(self):
        print("\nBOOST SHOP")
        print("-" * 30)
        for i, item in enumerate(self.items, 1):
            print(f"{i}. {item.name} - Rp {item.price:,}")
        print("0. Kembali")

    def buy(self, choice, game):
        if choice == 0:
            return
        item = self.items[choice - 1]
        if game.uang_saat_ini < item.price:
            print("❌ Uang tidak cukup!")
            return
        game.uang_saat_ini -= item.price
        item.apply(game)


# === UI MANAGER ===
class UIManager:
    def print_topping_list(self, inventory):
        print("\nDAFTAR TOPPING TERSEDIA")
        print("──────────────────────────────────────")
        toppings = list(Pizza.topping_prices.keys())
        for i, topping in enumerate(toppings, 1):
            stock = inventory.get_stock(topping)
            price = Pizza.topping_prices[topping]
            print(f"{i:>2}. {topping:<18} | Stok: {stock:<2} | Rp {price:,}")
        print("──────────────────────────────────────")

    def display_status(self, username, level, score, orders, uang, time_left):
        print("\nSTATUS PEMAIN")
        print("──────────────────────────────────────")
        print(f"User     : {username}")
        print(f"Level    : {level}")
        print(f"Score    : {score}")
        print(f"Pesanan  : {orders}")
        print(f"Uang     : Rp {uang:,}")
        print(f"Waktu    : {time_left//60:02d}:{time_left%60:02d}")
        print("──────────────────────────────────────")


#  MAIN GAME 
class PizzaGame:
    GAME_TIME_LIMIT = 300 # 5 menit
    BASE_STARTING_MONEY = 100000 # Uang awal

    def __init__(self):
        self.auth = AuthManager()
        self.ui = UIManager()
        self.user_data = {}
        self.topping_strategy = NormalStrategy() 
        self.strategy_name = "NORMAL" 
        self.topping_trend = {t: 0 for t in Pizza.topping_prices.keys()}
        
        self.external_logger = ExternalLogSystem()
        self.order_logger = OrderLoggerAdapter(self.external_logger)
        
        self.quest_manager = DailyQuestManager()
        self.quest_manager.generate_daily_quests()

        self.boost_shop = BoostShop()

    def _get_strategy_object(self, name):
        name = name.upper()
        if "DISKON HARIAN" in name:
            return DailyDiscountStrategy(random.uniform(0.1, 0.2)) 
        elif "TOPPING PERTAMA GRATIS" in name:
            return FreeToppingStrategy()
        return NormalStrategy()

    def _load_user_data(self, username):
        if username not in self.user_data:
            self.user_data[username] = {
                'uang_saat_ini': self.BASE_STARTING_MONEY,
                'score': 0,
                'orders_completed': 0,
                'challenge_completed': False,
                'level': 1,
                'difficulty_state': 'Medium', 
                'inventory_stock': {t: 10 for t in Pizza.topping_prices.keys()},
                'game_start_time': None,
                'strategy_name': 'NORMAL' 
            }
        data = self.user_data[username]
        self.uang_saat_ini = data['uang_saat_ini']
        self._score = data['score']
        self.orders_completed = data['orders_completed']
        self.challenge_completed = data['challenge_completed']
        self.difficulty_state = data.get('difficulty_state', 'Medium')
        self.level_manager = LevelManager(data['level'], self.difficulty_state) 
        self.inventory = Inventory(data['inventory_stock'])
        self.customer_manager = CustomerManager(self.level_manager)
        self.game_start_time = data['game_start_time']
        
        self.strategy_name = data.get('strategy_name', 'NORMAL') 
        self.topping_strategy = self._get_strategy_object(self.strategy_name)


    def _save_user_data(self, username):
        if username in self.user_data:
            self.user_data[username].update({
                'uang_saat_ini': self.uang_saat_ini,
                'score': self._score,
                'orders_completed': self.orders_completed,
                'challenge_completed': self.challenge_completed,
                'level': self.level_manager.get_level(),
                'difficulty_state': self.level_manager.state_name, 
                'inventory_stock': self.inventory.get_state(),
                'game_start_time': self.game_start_time,
                'strategy_name': self.strategy_name 
            })

    def _add_score(self, points):
        multiplier = self.level_manager.get_score_multiplier() 
        self._score += int(points * multiplier)

    def _update_daily_strategy(self):
        strategies = [
            (NormalStrategy(), "NORMAL"),
            (DailyDiscountStrategy(random.uniform(0.1, 0.2)), "DISKON HARIAN"),
            (FreeToppingStrategy(), "TOPPING PERTAMA GRATIS")
        ]
        self.topping_strategy, self.strategy_name = random.choice(strategies)
        print(f"\n📢 **Strategi Harian Baru: {self.strategy_name.upper()}!**")

    def _get_game_time_left(self):
        if self.game_start_time is None:
            return PizzaGame.GAME_TIME_LIMIT
        elapsed = time.time() - self.game_start_time
        return max(0, PizzaGame.GAME_TIME_LIMIT - int(elapsed))

    def _show_game_over_summary(self):
        print("\n" + "═" * 50)
        print(" WAKTU HABIS!")
        print(" GAME OVER")
        print("═" * 50)
        print(f" Uang Didapat (bersih) : Rp {self.uang_saat_ini - self.BASE_STARTING_MONEY:,}")
        print(f" Pesanan Selesai : {self.orders_completed}")
        print(f" Score : {self._score}")
        print(f" Level : {self.level_manager.get_level()}")
        print(f" Kesulitan : {self.level_manager.state_name.upper()}")
        print("═" * 50)
        input(" Tekan Enter untuk kembali ke menu...")

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
                self.order_logger.log_order_failure(customer) # Adapter Log
                self.customer_manager.remove_customer(customer)
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
                if isinstance(customer, VIPCustomer):
                    for q in self.quest_manager.quests:
                        if isinstance(q, ServeVIPQuest):
                            q.mark_served()
                for t in selected:
                    self.topping_trend[t] += 1
                payment = customer.get_payment(self.topping_strategy) 
                
                print(f"\nPesanan untuk {customer.name} selesai! Mendapat Rp {payment:,}")
                self.customer_manager.remove_customer(customer)
                self._add_score(100) 
                self.uang_saat_ini += payment
                self.orders_completed += 1
                self.quest_manager.check_all(self)
                self.order_logger.log_order_completion(customer, payment, True) 
                
                if self.level_manager.update_level(self.orders_completed):
                    print(f"Kesabaran: {self.level_manager.get_patience_modifier()} detik, spawn: {self.level_manager.get_spawn_rate()} detik.")
            else:
                print(f"\nTopping salah untuk {customer.name}!")
                self.order_logger.log_order_completion(customer, 0, False) 

        except (ValueError, OutOfStockError, InvalidToppingError) as e:
            elapsed = time.time() - start_time
            if not customer.reduce_patience(elapsed):
                print(f"\n{customer.name} kehabisan kesabaran dan pergi!")
                self.order_logger.log_order_failure(customer) 
                self.customer_manager.remove_customer(customer)
            else:
                print(f"Error: {str(e)}")

    def _show_daily_quests(self):
        print("\n" + "═" * 40)
        print("        DAILY QUEST")
        print("═" * 40)

        for i, quest in enumerate(self.quest_manager.quests, 1):
            status = "✅ SELESAI" if quest.completed else "❌ BELUM"
            print(f"{i}. {quest.description}")
            print(f"   Status : {status}")
            print(f"   Reward : Rp {quest.reward_money:,} | +{quest.reward_score} Score")
            print("-" * 40)

        input("Tekan Enter untuk kembali...")

    def _restock_menu(self):
        while True:
            self.inventory.display()
            print(f"\nUang Saat Ini: Rp {self.uang_saat_ini:,}")
            
            # TAMPILKAN SARAN RESTOK DARI GENERATOR
            print("\nSARAN RESTOK (otomatis):")
            print("-" * 50)
            has_suggestion = False
            for suggestion in self.inventory.suggest_restock(min_stock=2, restock_amount=5):
                has_suggestion = True
                print(f" • {suggestion['message']}")
            if not has_suggestion:
                print(" Semua stok aman!")
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

    def _difficulty_menu(self):
        while True:
            print("\n[ PENGATURAN KESULITAN ]")
            print("──────────────────────────────────────")
            print(f"Kesulitan Saat Ini: {self.level_manager.state_name.upper()}")
            print("1. Easy (Kesabaran: TINGGI, Spawn: LAMBAT, Score: 0.8x)")
            print("2. Medium (Default, Score: 1.0x)")
            print("3. Hard (Kesabaran: RENDAH, Spawn: CEPAT, Score: 1.5x)")
            print("0. Kembali")
            choice = input("Pilih (0-3): ")
            if choice == "0":
                break
            try:
                if choice == "1":
                    self.level_manager.set_state("Easy")
                    print("✅ Kesulitan diatur ke Easy.")
                elif choice == "2":
                    self.level_manager.set_state("Medium")
                    print("✅ Kesulitan diatur ke Medium.")
                elif choice == "3":
                    self.level_manager.set_state("Hard")
                    print("✅ Kesulitan diatur ke Hard.")
                else:
                    print("Pilihan tidak valid!")
            except ValueError as e:
                print(f"Error: {str(e)}")


    def _challenge_mode(self):
        if self.challenge_completed:
            print("\nKamu sudah menyelesaikan Challenge Mode hari ini!")
            input("Tekan Enter untuk kembali...")
            return

        print("\n" + "🔥" * 20)
        print(" MEMULAI CHALLENGE MODE!")
        print(" 8 TOPPING • 30 DETIK")
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
                self.order_logger.log_order_completion(challenge, 0, False)
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
                    self.order_logger.log_order_completion(challenge, 0, False)
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
                self.order_logger.log_order_completion(challenge, bonus, True)
            else:
                print("\nTopping salah! Gagal.")
                self.uang_saat_ini -= 30000
                print("Penalti: -Rp 30,000")
                self.order_logger.log_order_completion(challenge, 0, False)

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
        print("LEADERBOARD GLOBAL")
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

    def _show_topping_trend(self):
        print("\n" + "═" * 40)
        print("        TREN TOPPING")
        print("═" * 40)

        sorted_trend = sorted(
            self.topping_trend.items(),
            key=lambda x: x[1],
            reverse=True
        )

        print(f"{'Rank':<6}{'Topping':<20}{'Jumlah':<8}")
        print("-" * 40)

        for i, (topping, count) in enumerate(sorted_trend, start=1):
            print(f"{i:<6}{topping:<20}{count:<8}")

        print("═" * 40)
        input("Tekan Enter untuk kembali...")


    def _lobby_menu(self):
        username = self.auth.current_user
        while self.auth.is_logged_in():
            time_left = self._get_game_time_left()
            self._save_user_data(username) 

            print("\n" + "═" * 40)
            print(f"|{'PIZZA SHOP GAME':^38}|")
            print("═" * 40)
            print(f"Selamat datang, {username}!")
            print(f"Kesulitan: {self.level_manager.state_name.upper()}")
            print(f"Strategi Harian: {self.strategy_name.upper()}") 
            print(f"WAKTU: {time_left//60:02d}:{time_left%60:02d}")
            print("──────────────────────────────────────")
            print("[ MENU UTAMA ]")
            print("1. Lihat Daftar Topping")
            print("2. Mulai Permainan (5 Menit)")
            print("3. Restok Topping")
            print("4. Challenge Mode (Sekali per sesi)")
            print("5. Atur Kesulitan Permainan (State Pattern)") 
            print("6. Lihat Statistik Lengkap")
            print("7. Tren Topping (Paling Laris)")
            print("8. Leaderboard Semua Pemain")
            print("9. Boost Shop")
            print("10. Daily Quest")
            print("11. Logout")
            print("──────────────────────────────────────")
            choice = input("Pilih (1-8): ")

            if choice == "1":
                self.ui.print_topping_list(self.inventory)
                input("Tekan Enter...")
            elif choice == "2":
                self._update_daily_strategy() 
                self.game_start_time = time.time()
                self.customer_manager.start()
                self._game_loop()
            elif choice == "3":
                self._restock_menu()
            elif choice == "4":
                self._challenge_mode()
            elif choice == "5": 
                self._difficulty_menu() 
            elif choice == "6":
                print("\n" + "═" * 40)
                print(" STATISTIK LENGKAP")
                print("═" * 40)
                self.ui.display_status(
                    username,
                    self.level_manager.get_level(),
                    self._score,
                    self.orders_completed,
                    self.uang_saat_ini,
                    self._get_game_time_left()
                )
                print("═" * 40)
                input("Tekan Enter untuk kembali...")
            elif choice == "7":
                self._show_topping_trend()
            elif choice == "8":
                self._show_leaderboard()
            elif choice == "9":
                self.boost_shop.display()
                choice = int(input("Pilih item: "))
                self.boost_shop.buy(choice, self)
            elif choice == "10":
                self._show_daily_quests()
            elif choice == "11":
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

            if not self.customer_manager.get_customers():
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
            print(f"|{'Kesulitan: '+self.level_manager.state_name.upper():<38}|") 
            print(f"|{'Strategi: '+self.strategy_name.upper():<38}|")
            print(f"|{'─' *38 }|")
            print(f"| WAKTU {time_left//60:02d}:{time_left%60:02d}{'|':>27}")
            print(f"|{'─' *38 }|")
            print(f"| Pelanggan Aktif: {'|':>21}")
            customers = self.customer_manager.get_customers()
            for i, c in enumerate(customers, 1):
                status = "[VIP]" if isinstance(c, VIPCustomer) else ""
                print(f"|{i}. {c.name:<16} {status:<5} (Time: {int(c.time_left)}s) |")
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
                elif 1 <= choice <= len(self.customer_manager.get_customers()):
                    cust = self.customer_manager.get_customers()[choice - 1]
                    cust.display_chat(self.topping_strategy) 
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
                print("PIZZA SHOP GAME")
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
                        print(f"❌ {str(e)} ❌")
                elif choice == "2":
                    username = input("Username baru: ")
                    password = input("Password baru: ")
                    try:
                        if self.auth.add_user(username, password):
                            print(f"✔️ User '{username}' berhasil dibuat. ✔️")
                    except (UsernameError, PasswordError) as e:
                        print(f"❌ {str(e)} ❌")
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
