[EN](../README.md) | ID
# 🍕 Simulator Toko Pizza dengan Python

![Python](https://img.shields.io/badge/python-3.x-blue.svg)
![Type](https://img.shields.io/badge/type-proyek_sekolah-green.svg)

Selamat datang di Simulator Toko Pizza Python! Ini adalah game berbasis teks yang dinamis di mana Anda berperan sebagai koki pizza di sebuah restoran yang ramai dan unik. Tujuan Anda adalah menerima pesanan dari berbagai pelanggan yang menarik, membuat pizza mereka dengan benar, dan melayani mereka sebelum kesabaran mereka habis!

Proyek ini sepenuhnya dibangun dengan Python dan mendemonstrasikan konsep-konsep utama pemrograman seperti Pemrograman Berbasis Objek (PBO), *multithreading*, dan autentikasi pengguna dalam lingkungan baris perintah (command-line) yang seru dan interaktif.

## 🕹️ Demo Gameplay

Seluruh permainan berjalan di terminal Anda. Berikut adalah cuplikan dari apa yang akan Anda lihat:

**Seorang pelanggan datang dengan pesanan dan petunjuk unik:**
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

**Anda kemudian memilih topping yang benar dari daftar untuk menyelesaikan pesanan:**
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

## ✨ Fitur Utama

-   **Desain Berbasis Objek**: Game ini dibangun dengan kelas-kelas yang jelas dan dapat digunakan kembali seperti `Pizza`, `Customer`, dan `VIPCustomer`, menunjukkan struktur PBO yang solid.
-   **Multithreading**: Sebuah *thread* terpisah menghasilkan pelanggan baru di latar belakang saat Anda bermain, membuat permainan menjadi dinamis dan tidak dapat diprediksi. Tidak ada permainan yang sama!
-   **Tantangan Real-Time**: Pelanggan memiliki timer 'Kesabaran' yang terus berkurang berdasarkan berapa lama Anda membuat pesanan mereka. Layani dengan cepat atau mereka akan pergi!
-   **Pelanggan VIP**: Temui pelanggan VIP khusus yang memiliki prioritas lebih tinggi tetapi menawarkan harga diskon. Fitur ini menampilkan penggunaan konsep **Pewarisan (Inheritance)**.
-   **Autentikasi Pengguna**: Sistem login dan registrasi yang sederhana namun efektif memastikan bahwa skor dan status pemain terikat pada pengguna tertentu.
-   **Sistem Skor**: Dapatkan poin untuk setiap pesanan yang diselesaikan dengan benar dan lacak performa Anda.
-   **Menu Interaktif**: Permainan ini dinavigasi melalui serangkaian menu baris perintah yang intuitif.

## 🚀 Cara Bermain

1.  **Jalankan Skrip**: Mulai permainan dari terminal Anda.
2.  **Login/Daftar**: Buat pengguna baru atau masuk dengan pengguna yang sudah ada.
3.  **Mulai Bermain**: Dari lobi utama, pilih "Start Game".
4.  **Tunggu Pelanggan**: Pelanggan baru akan datang secara otomatis setiap 20 detik.
5.  **Layani Pelanggan**: Dari menu permainan, pilih pelanggan berdasarkan nomornya untuk melihat pesanan mereka.
6.  **Baca Petunjuk (Hint)**: Gunakan petunjuk unik dari pelanggan untuk mencari tahu topping apa yang mereka inginkan.
7.  **Buat Pizza**: Masukkan nomor yang sesuai dengan topping yang benar untuk menyelesaikan pesanan.
8.  **Dapatkan Poin**: Pesanan yang benar memberi Anda poin dan menambah jumlah pesanan yang diselesaikan. Jadilah cepat dan akurat untuk mendapatkan skor tertinggi!

## 🛠️ Konsep Teknis yang Didemonstrasikan

Proyek ini secara efektif mendemonstrasikan beberapa konsep pemrograman penting:
-   **Pemrograman Berbasis Objek (PBO/OOP)**: Penggunaan kelas dan objek secara ekstensif untuk memodelkan komponen-komponen permainan.
-   **Pewarisan (Inheritance)**: Kelas `VIPCustomer` mewarisi dan memperluas fungsionalitas dari kelas `Customer`.
-   **Enkapsulasi (Encapsulation)**: Kelas `AuthManager` dan `VIPCustomer` menggunakan atribut privat (`_users`, `_discount`) untuk melindungi data internal mereka.
-   **Multithreading**: Modul `threading` digunakan untuk menjalankan proses pembuatan pelanggan secara bersamaan dengan loop utama permainan.
-   **Struktur Data**: Penggunaan *list* dan *dictionary* untuk mengelola pelanggan, topping pizza, harga, dan data pengguna.

## ⚙️ Cara Memulai

Tidak ada *library* khusus yang diperlukan untuk menjalankan game ini, hanya instalasi Python standar.

### Prasyarat
-   Python 3.x

### Menjalankan Game
1.  Simpan kode sebagai file Python (contoh: `pizza_game.py`).
2.  Buka terminal atau *command prompt*.
3.  Arahkan ke direktori tempat Anda menyimpan file tersebut.
4.  Jalankan perintah berikut:
    ```sh
    python pizza_game.py
    ```
5.  Ikuti petunjuk di layar untuk bermain!
