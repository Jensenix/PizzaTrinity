import unittest
import random
from unittest.mock import Mock, patch
from PizzaTrinity import (
    Pizza, PizzaError, InvalidToppingError, OutOfStockError,
    CustomerDatabase, Inventory, AuthManager, UIManager,
    ToppingStrategy, NormalStrategy, DailyDiscountStrategy, FreeToppingStrategy,
    DifficultyState, EasyState, MediumState, HardState,
    CustomerFactory, RegularCustomerFactory, VIPCustomerFactory,
    AbstractCustomer, Customer, VIPCustomer, ChallengeCustomer,
    CustomerManager, LevelManager, Quest, CompleteOrderQuest, ServeVIPQuest,
    DailyQuestManager, Boost, SlowTimeBoost, MoneyBoost, BoostShop,
    PizzaGame
)

class TestPizza(unittest.TestCase):
    def setUp(self):
        self.valid_pizza = Pizza("Medium", ["Cheese", "Pepperoni"])
    
    def test_pizza_creation_valid(self):
        self.assertEqual(self.valid_pizza.size, "Medium")
        self.assertEqual(len(self.valid_pizza.toppings), 2)
        self.assertIn("Cheese", self.valid_pizza.toppings)
    
    def test_pizza_invalid_size(self):
        with self.assertRaises(PizzaError):
            Pizza("ExtraLarge", ["Cheese"])
    
    def test_pizza_invalid_topping(self):
        with self.assertRaises(InvalidToppingError):
            Pizza("Small", ["InvalidTopping"])
    
    def test_pizza_price_calculation(self):
        expected_price = Pizza.base_price["Medium"] + Pizza.topping_prices["Cheese"] + Pizza.topping_prices["Pepperoni"]
        self.assertEqual(self.valid_pizza.price(), expected_price)
    
    def test_pizza_str_representation(self):
        self.assertEqual(str(self.valid_pizza), "Pizza Medium")

class TestToppingStrategy(unittest.TestCase):
    def setUp(self):
        self.test_price = 100000
        self.test_toppings = ["Cheese", "Pepperoni"]
    
    def test_normal_strategy(self):
        strategy = NormalStrategy()
        price, msg = strategy.apply_effect(self.test_price, self.test_toppings)
        self.assertEqual(price, self.test_price)
        self.assertEqual(msg, "Harga Normal")
    
    def test_daily_discount_strategy(self):
        strategy = DailyDiscountStrategy(0.2)
        price, msg = strategy.apply_effect(self.test_price, self.test_toppings)
        self.assertEqual(price, 80000)
        self.assertIn("20%", msg)
    
    def test_free_topping_strategy_with_toppings(self):
        strategy = FreeToppingStrategy()
        expected_price = self.test_price - Pizza.topping_prices["Cheese"]
        price, msg = strategy.apply_effect(self.test_price, self.test_toppings)
        self.assertEqual(price, expected_price)
        self.assertIn("Cheese", msg)
    
    def test_free_topping_strategy_no_toppings(self):
        strategy = FreeToppingStrategy()
        price, msg = strategy.apply_effect(self.test_price, [])
        self.assertEqual(price, self.test_price)
        self.assertEqual(msg, "Topping Gratis")

class TestDifficultyState(unittest.TestCase):
    def test_easy_state(self):
        state = EasyState()
        patience = state.get_patience_modifier(1)
        spawn_rate = state.get_spawn_rate(1)
        multiplier = state.get_score_multiplier()
        
        self.assertEqual(patience, 50)
        self.assertEqual(spawn_rate, 15)
        self.assertEqual(multiplier, 0.8)
    
    def test_medium_state(self):
        state = MediumState()
        patience = state.get_patience_modifier(1)
        spawn_rate = state.get_spawn_rate(1)
        multiplier = state.get_score_multiplier()
        
        self.assertEqual(patience, 40)
        self.assertEqual(spawn_rate, 10)
        self.assertEqual(multiplier, 1.0)
    
    def test_hard_state(self):
        state = HardState()
        patience = state.get_patience_modifier(1)
        spawn_rate = state.get_spawn_rate(1)
        multiplier = state.get_score_multiplier()
        
        self.assertEqual(patience, 20)
        self.assertEqual(spawn_rate, 6)
        self.assertEqual(multiplier, 1.5)
    
    def test_state_level_scaling(self):
        state = EasyState()
        patience_level1 = state.get_patience_modifier(1)
        patience_level3 = state.get_patience_modifier(3)
        
        self.assertGreater(patience_level1, patience_level3)

class TestCustomerFactory(unittest.TestCase):
    def setUp(self):
        self.mock_level_manager = Mock()
        self.mock_level_manager.get_patience_modifier.return_value = 30
    
    def test_regular_factory_creates_customer(self):
        factory = RegularCustomerFactory()
        customer = factory.create(self.mock_level_manager)
        
        self.assertIsInstance(customer, Customer)
        self.assertEqual(customer.level_manager, self.mock_level_manager)
    
    def test_vip_factory_creates_vip_customer(self):
        factory = VIPCustomerFactory()
        customer = factory.create(self.mock_level_manager)
        
        self.assertIsInstance(customer, VIPCustomer)
        self.assertTrue(hasattr(customer, '_discount'))

class TestInventory(unittest.TestCase):
    def setUp(self):
        self.inventory = Inventory()
        self.test_topping = "Cheese"
    
    def test_initial_stock(self):
        stock = self.inventory.get_stock(self.test_topping)
        self.assertEqual(stock, 10)
    
    def test_use_topping_success(self):
        initial_stock = self.inventory.get_stock(self.test_topping)
        self.inventory.use_topping(self.test_topping)
        final_stock = self.inventory.get_stock(self.test_topping)
        self.assertEqual(final_stock, initial_stock - 1)
    
    def test_use_topping_out_of_stock(self):
        # Deplete stock completely
        for _ in range(10):
            self.inventory.use_topping(self.test_topping)
        
        with self.assertRaises(OutOfStockError):
            self.inventory.use_topping(self.test_topping)
    
    def test_restock_success(self):
        # Use some topping first
        self.inventory.use_topping(self.test_topping)
        
        cost = self.inventory.restock(self.test_topping, 5, 100000)
        expected_cost = 5 * self.inventory._cost_per_stock[self.test_topping]
        
        self.assertEqual(cost, expected_cost)
        self.assertEqual(self.inventory.get_stock(self.test_topping), 14)
    
    def test_restock_insufficient_funds(self):
        with self.assertRaises(ValueError):
            self.inventory.restock(self.test_topping, 5, 1000)  # Too little money
    
    def test_restock_exceeds_max(self):
        with self.assertRaises(ValueError):
            self.inventory.restock(self.test_topping, 20, 1000000)  # Exceeds max stock

class TestAuthManager(unittest.TestCase):
    def setUp(self):
        self.auth = AuthManager()
    
    def test_add_user_success(self):
        result = self.auth.add_user("testuser", "password123")
        self.assertTrue(result)
        self.assertIn("testuser", self.auth._users)
    
    def test_add_duplicate_user(self):
        self.auth.add_user("testuser", "password123")
        with self.assertRaises(Exception):
            self.auth.add_user("testuser", "differentpass")
    
    def test_login_success(self):
        self.auth.add_user("testuser", "password123")
        result = self.auth.login("testuser", "password123")
        self.assertTrue(result)
        self.assertEqual(self.auth.current_user, "testuser")
    
    def test_login_invalid_credentials(self):
        with self.assertRaises(Exception):
            self.auth.login("nonexistent", "wrongpass")
    
    def test_username_validation(self):
        with self.assertRaises(Exception):
            self.auth.validate_username("")  # Empty username
        
        with self.assertRaises(Exception):
            self.auth.validate_username("ab")  # Too short
    
    def test_password_validation(self):
        with self.assertRaises(Exception):
            self.auth.validate_password("")  # Empty password
        
        with self.assertRaises(Exception):
            self.auth.validate_password("123")  # Too short

class TestQuestSystem(unittest.TestCase):
    def setUp(self):
        self.mock_game = Mock()
        self.mock_game.orders_completed = 5
        self.mock_game.uang_saat_ini = 100000
        self.mock_game._add_score = Mock()
    
    def test_complete_order_quest_success(self):
        quest = CompleteOrderQuest(3)
        result = quest.check_progress(self.mock_game)
        self.assertTrue(result)
        
        quest.give_reward(self.mock_game)
        self.assertEqual(self.mock_game.uang_saat_ini, 150000)
        self.mock_game._add_score.assert_called_with(100)
    
    def test_complete_order_quest_not_complete(self):
        quest = CompleteOrderQuest(10)
        result = quest.check_progress(self.mock_game)
        self.assertFalse(result)
    
    def test_serve_vip_quest(self):
        quest = ServeVIPQuest()
        self.assertFalse(quest.check_progress(self.mock_game))
        
        quest.mark_served()
        self.assertTrue(quest.check_progress(self.mock_game))
    
    def test_daily_quest_manager(self):
        manager = DailyQuestManager()
        manager.generate_daily_quests()
        
        self.assertEqual(len(manager.quests), 2)
        self.assertIsInstance(manager.quests[0], CompleteOrderQuest)
        self.assertIsInstance(manager.quests[1], ServeVIPQuest)

class TestBoostSystem(unittest.TestCase):
    def setUp(self):
        self.mock_game = Mock()
        self.mock_game.level_manager = Mock()
        self.mock_game.uang_saat_ini = 100000
    
    def test_slow_time_boost(self):
        boost = SlowTimeBoost()
        self.assertEqual(boost.name, "Slow Time")
        self.assertEqual(boost.price, 50000)
        
        boost.apply(self.mock_game)
        self.mock_game.level_manager.set_state.assert_called_with("Easy")
    
    def test_money_boost(self):
        boost = MoneyBoost()
        self.assertEqual(boost.name, "Money Boost")
        self.assertEqual(boost.price, 75000)
        
        boost.apply(self.mock_game)
        self.assertEqual(self.mock_game.uang_saat_ini, 200000)
    
    def test_boost_shop(self):
        shop = BoostShop()
        self.assertEqual(len(shop.items), 2)
        self.assertIsInstance(shop.items[0], SlowTimeBoost)
        self.assertIsInstance(shop.items[1], MoneyBoost)
    
    def test_boost_shop_purchase_success(self):
        shop = BoostShop()
        initial_money = self.mock_game.uang_saat_ini
        
        shop.buy(1, self.mock_game)  # Buy SlowTimeBoost
        
        self.assertEqual(self.mock_game.uang_saat_ini, initial_money - 50000)
        self.mock_game.level_manager.set_state.assert_called_with("Easy")
    
    def test_boost_shop_purchase_insufficient_funds(self):
        shop = BoostShop()
        self.mock_game.uang_saat_ini = 1000  # Very low
        
        with patch('builtins.print') as mock_print:
            shop.buy(1, self.mock_game)
            mock_print.assert_called_with("❌ Uang tidak cukup!")

class TestCustomerManager(unittest.TestCase):
    def setUp(self):
        self.mock_level_manager = Mock()
        self.mock_level_manager.get_spawn_rate.return_value = 2
        self.manager = CustomerManager(self.mock_level_manager)
    
    def test_initialization(self):
        self.assertEqual(len(self.manager.factories), 2)
        self.assertIsInstance(self.manager.factories[0][1], VIPCustomerFactory)
        self.assertIsInstance(self.manager.factories[1][1], RegularCustomerFactory)
        self.assertEqual(self.manager.factories[0][0], 0.3)  # 30% VIP
        self.assertEqual(self.manager.factories[1][0], 0.7)  # 70% Regular
    
    @patch('random.random')
    def test_spawn_customer_vip(self, mock_random):
        mock_random.return_value = 0.1  # Should trigger VIP
        
        with patch.object(self.manager.factories[0][1], 'create') as mock_create:
            mock_create.return_value = Mock()
            
            self.manager._spawn_loop()
            
            mock_create.assert_called_once_with(self.mock_level_manager)
            self.assertEqual(len(self.manager.queue), 1)
    
    def test_remove_customer(self):
        mock_customer = Mock()
        prioritized_customer = Mock()
        prioritized_customer.customer = mock_customer
        
        self.manager.queue.append(prioritized_customer)
        self.manager.remove_customer(mock_customer)
        
        self.assertEqual(len(self.manager.queue), 0)
    
    def test_get_customers_sorted(self):
        mock_regular = Mock(spec=Customer)
        mock_vip = Mock(spec=VIPCustomer)
        
        self.manager.queue = [
            Mock(customer=mock_regular, priority=1, timestamp=2),
            Mock(customer=mock_vip, priority=0, timestamp=1)
        ]
        
        with patch('heapq.nsmallest'):
            customers = self.manager.get_customers()
            self.assertIsInstance(customers, list)

class TestLevelManager(unittest.TestCase):
    def setUp(self):
        self.level_manager = LevelManager()
    
    def test_initial_level(self):
        self.assertEqual(self.level_manager.get_level(), 1)
        self.assertIsInstance(self.level_manager._state, MediumState)
    
    def test_set_state(self):
        self.level_manager.set_state("Easy")
        self.assertIsInstance(self.level_manager._state, EasyState)
        self.assertEqual(self.level_manager.state_name, "easy")
        
        self.level_manager.set_state("Hard")
        self.assertIsInstance(self.level_manager._state, HardState)
        self.assertEqual(self.level_manager.state_name, "hard")
    
    def test_set_invalid_state(self):
        with self.assertRaises(ValueError):
            self.level_manager.set_state("Invalid")
    
    def test_update_level(self):
        result = self.level_manager.update_level(5)
        self.assertTrue(result)
        self.assertEqual(self.level_manager.get_level(), 2)
        
        result = self.level_manager.update_level(4)
        self.assertFalse(result)
        self.assertEqual(self.level_manager.get_level(), 2)
    
    def test_state_delegation(self):
        self.level_manager.set_state("Easy")
        
        patience = self.level_manager.get_patience_modifier()
        spawn_rate = self.level_manager.get_spawn_rate()
        multiplier = self.level_manager.get_score_multiplier()
        
        self.assertIsInstance(patience, int)
        self.assertIsInstance(spawn_rate, int)
        self.assertIsInstance(multiplier, float)

class TestPizzaGame(unittest.TestCase):
    def setUp(self):
        self.game = PizzaGame()
    
    def test_initialization(self):
        self.assertIsInstance(self.game.auth, AuthManager)
        self.assertIsInstance(self.game.ui, UIManager)
        self.assertIsInstance(self.game.topping_strategy, NormalStrategy)
        self.assertEqual(self.game.strategy_name, "NORMAL")
        self.assertIsInstance(self.game.quest_manager, DailyQuestManager)
        self.assertIsInstance(self.game.boost_shop, BoostShop)
    
    def test_get_strategy_object(self):
        strategy = self.game._get_strategy_object("normal")
        self.assertIsInstance(strategy, NormalStrategy)
        
        strategy = self.game._get_strategy_object("diskon harian")
        self.assertIsInstance(strategy, DailyDiscountStrategy)
        
        strategy = self.game._get_strategy_object("topping pertama gratis")
        self.assertIsInstance(strategy, FreeToppingStrategy)
    
    def test_load_user_data_new_user(self):
        username = "newuser"
        self.game._load_user_data(username)
        
        self.assertIn(username, self.game.user_data)
        self.assertEqual(self.game.uang_saat_ini, PizzaGame.BASE_STARTING_MONEY)
        self.assertEqual(self.game._score, 0)
        self.assertEqual(self.game.orders_completed, 0)
    
    def test_save_user_data(self):
        username = "testuser"
        self.game._load_user_data(username)
        self.game.uang_saat_ini = 150000
        self.game._score = 500
        
        self.game._save_user_data(username)
        
        saved_data = self.game.user_data[username]
        self.assertEqual(saved_data['uang_saat_ini'], 150000)
        self.assertEqual(saved_data['score'], 500)
    
    def test_add_score_with_multiplier(self):
        self.game.level_manager = Mock()
        self.game.level_manager.get_score_multiplier.return_value = 1.5
        
        self.game._add_score(100)
        self.assertEqual(self.game._score, 150)
    
    def test_update_daily_strategy(self):
        initial_strategy = self.game.topping_strategy
        self.game._update_daily_strategy()
        
        self.assertIsInstance(self.game.topping_strategy, ToppingStrategy)
        self.assertIn(self.game.strategy_name, ["NORMAL", "DISKON HARIAN", "TOPPING PERTAMA GRATIS"])
    
    def test_get_game_time_left(self):
        time_left = self.game._get_game_time_left()
        self.assertEqual(time_left, PizzaGame.GAME_TIME_LIMIT)
        
        self.game.game_start_time = time.time() - 60  
        time_left = self.game._get_game_time_left()
        self.assertEqual(time_left, PizzaGame.GAME_TIME_LIMIT - 60)

if __name__ == '__main__':
    unittest.main()
