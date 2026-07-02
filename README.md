<div align="center">

# 👑 Mannat Hotel Management System

### *Where Every Stay Becomes a Story* ✨

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Tkinter](https://img.shields.io/badge/Tkinter-GUI-FF6B6B?style=for-the-badge&logo=python&logoColor=white)
![MySQL](https://img.shields.io/badge/MySQL-Database-4479A1?style=for-the-badge&logo=mysql&logoColor=white)
![Status](https://img.shields.io/badge/Status-Active-00C851?style=for-the-badge)

</div>

---

## 📖 Overview

> **Mannat Hotel Management System** is a fully-featured, premium desktop application built with Python. Designed to streamline hotel operations — from luxury room bookings to seamless guest checkouts — all wrapped in a stunning dark-themed UI.

Whether you're managing a boutique hotel or a luxury resort, this system handles everything with elegance and precision. 🏰

---

## ✨ Features

| Feature | Description |
|--------|-------------|
| 📥 **Guest Check-In** | Register guests with full details, room category & auto billing |
| 📤 **Guest Check-Out** | One-click checkout with instant room status update |
| 🖼️ **Dynamic Room Preview** | Full-screen background changes based on selected room type |
| 💰 **Auto Billing Engine** | Calculates total based on room category × nights stayed |
| 📧 **Automated Email Alerts** | Premium styled confirmation & checkout emails sent instantly |
| 📊 **Live Data Dashboard** | Real-time booking table with search, view & delete options |
| 🗄️ **MySQL Integration** | Persistent data storage with full CRUD operations |
| 🎨 **Luxury Dark UI** | Modern, elegant dark theme with gold accents |

---

## 🛠️ Tech Stack

```
💻 Language     →   Python 3.10+
🎨 GUI          →   Tkinter + ttk
🗄️ Database     →   MySQL (mysql-connector-python)
📧 Email        →   smtplib + MIME (Gmail SMTP)
🖼️ Images       →   Pillow (PIL)
🧵 Threading    →   Python threading (async email)
```

---

## 📁 Project Structure

```
Hotel Management/
│
├── 📄 hotel.py                  # Main application file
├── 🖼️ deluxe.jpg               # Deluxe room background
├── 🖼️ premium.jpg              # Premium room background
├── 🖼️ suite.jpg                # Suite room background
├── 🖼️ presidential.jpg         # Presidential room background
├── 🖼️ default_room.jpg         # Default background image
└── 📘 README.md                 # Project documentation
```
---

## ⚙️ Installation & Setup

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/aseemkassar/hotel-management-system.git
cd hotel-management-system
```

### 2️⃣ Install Required Libraries
```bash
pip install mysql-connector-python Pillow
```

### 3️⃣ Setup MySQL Database
```bash
# Start MySQL server and make sure these credentials match your setup:
Host     : localhost
Port     : 3306
User     : root
Password : aseem
```

### 4️⃣ Configure Email (Optional)
```python
# In hotel.py, update these lines:
self.sender_email    = "aseemmwn2006@gmail.com"
self.sender_password = "*************"
```
> 💡 Use a **Gmail App Password**, not your regular Gmail password.  
> Generate it from: Google Account → Security → 2-Step Verification → App Passwords

### 5️⃣ Run the Application
```bash
python hotel_project.py
```

---

## 🖥️ Screenshots

| Check-In Panel | Check-Out Panel | Live Dashboard |
|:-:|:-:|:-:|
| 📥 Guest registration form with dynamic room preview | 📤 Room number based live background change | 📊 Real-time booking data table |

---

## 🏨 Room Categories & Pricing

| 🛏️ Category | 💰 Rate per Night |
|-------------|------------------|
| 🥈 Deluxe | ₹5,000 |
| 🥇 Premium | ₹8,000 |
| 💎 Suite | ₹12,000 |
| 👑 Presidential | ₹20,000 |

> Custom rates can also be set manually per booking.

---

## 📧 Email Notifications

Guests automatically receive beautiful styled emails for:

- ✅ **Booking Confirmation** — with full reservation details & hotel amenities
- 👋 **Checkout Confirmation** — with a thank you note & discount code for next visit

---

## 🚀 Future Enhancements

- [ ] 📱 Mobile-responsive web version
- [ ] 📊 Revenue analytics & monthly reports
- [ ] 🔐 Admin login & role-based access
- [ ] 🌐 Online booking portal integration
- [ ] 🧾 PDF invoice generation
- [ ] 💳 Online payment gateway

---

## 👨‍💻 Developed By

<div align="center">

### 🌟 Mohd Aseem

*Data Analyst*

[![GitHub](https://img.shields.io/badge/GitHub-Follow-181717?style=for-the-badge&logo=github)](https://github.com/yourusername)

</div>

---

<div align="center">

**⭐ If you found this project helpful, please give it a star!**

*Made with ❤️ and lots of ☕ by Mohd Aseem*

</div>
