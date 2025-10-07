EN | [ID](docs/READMEid.md) | [中文](docs/READMEcn.md)
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
👤 Nama      : Nenek Superhero [VIP]
⏳ Kesabaran : 35 detik (Prioritas)
📦 Pesanan   : Pizza Medium
   - Exploding Peppers
   - Tomato Sauce
💡 Hint      :
   • BOOM! Careful, it bites!
   • Red like a superhero cape!
💰 Harga     : Rp 97,000
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
-   **Multithreading**: A separate thread generates new customers in the background while you play, making the game dynamic and unpredictable.
-   **Real-Time Challenge**: Customers have a 'Patience' timer that ticks down based on how long you take to make their order. Serve them quickly or they'll leave!
-   **VIP Customers**: Encounter special VIP customers who have higher priority and offer discounts, showcasing the use of **inheritance**.
-   **User Authentication**: A simple login and registration system ensures player scores are tied to a specific user.
-   **Scoring System**: Earn points for each correctly fulfilled order and track your performance.
-   **Interactive Menus**: The game is navigated through a series of intuitive command-line menus.

## 🛠️ Technical Concepts Demonstrated

-   **Object-Oriented Programming (OOP)**: Extensive use of classes and objects to model the game's components.
-   **Inheritance**: The `VIPCustomer` class inherits from and extends the `Customer` class.
-   **Encapsulation**: The `AuthManager` and `VIPCustomer` classes use private attributes to protect their internal state.
-   **Multithreading**: The `threading` module runs the customer generation process concurrently with the main game loop.
-   **Data Structures**: Use of lists and dictionaries to manage customers, toppings, prices, and user data.

## 🏛️ Architecture & Class Diagram

The game is architected around the `PizzaGame` class, which manages the main loop and game state. It utilizes an `AuthManager` for user sessions and dynamically generates `Customer` objects, which can also be specialized `VIPCustomer` objects.

<img width="1126" height="897" alt="Class Diagram Trinity" src="https://github.com/user-attachments/assets/afc46696-962a-44d2-a2a1-2b26ee6793dc" />

## 🚀 How to Play

1.  **Run the Script**: Start the game from your terminal.
2.  **Login/Register**: Create a new user or log in with an existing one.
3.  **Start the Game**: From the main lobby, select "Start Game".
4.  **Wait for Customers**: New customers will arrive automatically every 20 seconds.
5.  **Serve a Customer**: From the game menu, select a customer by their number to view their order.
6.  **Read the Hints**: Use the customer's unique hints to figure out which toppings they want.
7.  **Make the Pizza**: Enter the numbers corresponding to the correct toppings to complete the order.
8.  **Earn Points**: Correct orders earn you points. Be fast and accurate to get the highest score!

## ⚙️ Getting Started

No special libraries are needed to run this game, just a standard Python installation.

### Prerequisites
- Python 3.x

### Running the Game
1.  Save the code as a Python file (e.g., `PizzaTrinity.py`).
2.  Open a terminal or command prompt.
3.  Navigate to the directory where you saved the file.
4.  Run the following command:
    ```sh
    python PizzaTrinity.py
    ```
5.  Follow the on-screen instructions to play!

## 👥 Author & Contributors

<table border="0" cellspacing="10" cellpadding="5">
  <tr>
    <td align="center" style="border: 1px solid #555; padding: 10px;">
      <a href="https://github.com/Serthons">
        <img src="https://github.com/Serthons.png" width="100" height="100" alt="Jess2Jes" style="border-radius: 50%;"/>
      </a>
      <br/>
      <a href="https://github.com/Serthons">Serthons</a>
    </td>
    <td align="center" style="border: 1px solid #555; padding: 10px;">
      <a href="https://github.com/Jensenix">
        <img src="https://github.com/Jensenix.png" width="100" height="100" alt="Hans" style="border-radius: 50%;"/>
      </a>
      <br/>
      <a href="https://github.com/Jensenix">Jensenix</a>
    </td>
    <td align="center" style="border: 1px solid #555; padding: 10px;">
      <a href="https://github.com/vincentlawi">
        <img src="https://github.com/vincentlawi.png" width="100" height="100" alt="StevNard"/>
      </a>
      <br/>
      <a href="https://github.com/vincentlawi">vincentlawi</a>
    </td>
  </tr>
</table>
