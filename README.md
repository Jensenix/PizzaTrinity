EN | [ID](docs/READMEid.md)

# 🍕 Python Pizza Shop Simulator

![Python](https://img.shields.io/badge/python-3.x-blue.svg)
![Type](https://img.shields.io/badge/type-school_project-green.svg)

Welcome to the Python Pizza Shop Simulator! This is a dynamic, text-based game where you take on the role of a pizza chef in a bustling and quirky restaurant. Your goal is to take orders from a variety of interesting customers, make their pizzas correctly, and serve them before their patience runs out!

This project is built entirely in Python and demonstrates key programming concepts like Object-Oriented Programming, multithreading, and user authentication in a fun, interactive command-line environment.

## 🕹️ Gameplay Demo

The entire game runs in your terminal. Here's a quick look at what you'll see:

**A customer arrives with a unique order and hints:**
```
──────────────────────────────────────
🍕 CUSTOMER ORDER
──────────────────────────────────────
👤 Nama       : Nenek Superhero [VIP]
⏳ Kesabaran  : 35 detik (Prioritas)
📦 Pesanan    : Pizza Medium
   - Exploding Peppers
   - Tomato Sauce
💡 Hint       :
   • BOOM! Careful, it bites!
   • Red like a superhero cape!
💰 Harga      : Rp 97,000
   Diskon 25.1% → Rp 72,629
──────────────────────────────────────
```

**You then select the correct toppings from the list to fulfill the order:**
```
[ TOPPING LIST ]
========================================
1. Cheese          | 6. Exploding Peppers
2. Pepperoni       | 7. Unicorn Glitter
3. Mushroom        | 8. Zombie Fingers
4. Olives          | 9. Invisible Onions
5. Tomato Sauce    | 10. Magic Dust
========================================

> Pilih 2 topping: 6 5

✔ Pesanan untuk Nenek Superhero selesai!
```

## ✨ Core Features

-   **Object-Oriented Design**: The game is built with clear, reusable classes like `Pizza`, `Customer`, and `VIPCustomer`, demonstrating a solid OOP structure.
-   **Multithreading**: A separate thread generates new customers in the background while you play, making the game dynamic and unpredictable. No two playthroughs are the same!
-   **Real-Time Challenge**: Customers have a 'Patience' timer that ticks down based on how long you take to make their order. Serve them quickly or they'll leave!
-   **VIP Customers**: Encounter special VIP customers who have higher priority but offer discounted prices. This feature showcases the use of **inheritance** by extending the base `Customer` class.
-   **User Authentication**: A simple but effective login and registration system ensures that player scores and status are tied to a specific user.
-   **Scoring System**: Earn points for each correctly fulfilled order and track your performance.
-   **Interactive Menus**: The game is navigated through a series of intuitive command-line menus.

## 🚀 How to Play

1.  **Run the Script**: Start the game from your terminal.
2.  **Login/Register**: Create a new user or log in with an existing one.
3.  **Start the Game**: From the main lobby, select "Start Game".
4.  **Wait for Customers**: New customers will arrive automatically every 20 seconds.
5.  **Serve a Customer**: From the game menu, select a customer by their number to view their order.
6.  **Read the Hints**: Use the customer's unique hints to figure out which toppings they want.
7.  **Make the Pizza**: Enter the numbers corresponding to the correct toppings to complete the order.
8.  **Earn Points**: Correct orders earn you points and increase your completed order count. Be fast and accurate to get the highest score!

## 🛠️ Technical Concepts Demonstrated

This project effectively demonstrates several important programming concepts:
-   **Object-Oriented Programming (OOP)**: Extensive use of classes and objects to model the game's components.
-   **Inheritance**: The `VIPCustomer` class inherits from and extends the `Customer` class.
-   **Encapsulation**: The `AuthManager` and `VIPCustomer` classes use private attributes (`_users`, `_discount`) to protect their internal state.
-   **Multithreading**: The `threading` module is used to run the customer generation process concurrently with the main game loop.
-   **Data Structures**: Use of lists and dictionaries to manage customers, pizza toppings, prices, and user data.

## ⚙️ Getting Started

No special libraries are needed to run this game, just a standard Python installation.

### Prerequisites
- Python 3.x

### Running the Game
1.  Save the code as a Python file (e.g., `pizza_game.py`).
2.  Open a terminal or command prompt.
3.  Navigate to the directory where you saved the file.
4.  Run the following command:
    ```sh
    python pizza_game.py
    ```
5.  Follow the on-screen instructions to play!
