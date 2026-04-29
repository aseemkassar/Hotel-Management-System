import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime
import os

class HotelManagementSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Mannat Hotel Management System")
        self.root.geometry("1200x700")
        self.root.state('zoomed')  # Maximize window
        
        # Database setup
        self.setup_database()
        
        # Background image (download a hotel image and place it as 'hotel_bg.jpg')
        self.create_background()
        
        # Main frame with styling
        self.main_frame = tk.Frame(root, bg='#2c3e50')
        self.main_frame.place(relx=0.5, rely=0.5, anchor='center')
        
        self.create_widgets()
        
    def setup_database(self):
        self.conn = sqlite3.connect('hotel_management.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS bookings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                guest_name TEXT NOT NULL,
                room_no INTEGER NOT NULL,
                room_type TEXT NOT NULL,
                check_in DATE NOT NULL,
                check_out DATE NOT NULL,
                total_amount REAL NOT NULL,
                status TEXT DEFAULT 'Active'
            )
        ''')
        self.conn.commit()
    
    def create_background(self):
        # Background image setup (hotel_bg.jpg file chahiye)
        try:
            # Agar image file hai to use karo, nahi to gradient banayenge
            self.bg_image = tk.PhotoImage(file="hotel_bg.jpg")
            self.bg_label = tk.Label(self.root, image=self.bg_image)
            self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        except:
            # Gradient background if no image
            self.create_gradient_bg()
    
    def create_gradient_bg(self):
        # Beautiful gradient background
        canvas = tk.Canvas(self.root, width=1200, height=700)
        canvas.place(x=0, y=0)
        
        # Gradient colors
        colors = ['#667eea', '#764ba2']
        for i in range(100):
            r1, g1, b1 = self.hex_to_rgb(colors[0])
            r2, g2, b2 = self.hex_to_rgb(colors[1])
            r = r1 + (r2-r1) * i / 99
            g = g1 + (g2-g1) * i / 99
            b = b1 + (b2-b1) * i / 99
            canvas.create_rectangle(i*12, 0, (i+1)*12, 700, 
                                  fill=f'#{int(r):02x}{int(g):02x}{int(b):02x}', outline='')
    
    def hex_to_rgb(self, hex_color):
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    
    def create_widgets(self):
        # Title
        title_label = tk.Label(self.main_frame, text="Mannat Hotel Management", 
                              font=('Arial', 28, 'bold'), 
                              fg='#ecf0f1', bg='#2c3e50')
        title_label.pack(pady=20)
        
        # Navigation tabs
        self.notebook = ttk.Notebook(self.main_frame)
        self.notebook.pack(pady=20, padx=20, fill='both', expand=True)
        
        # Check-in Tab
        self.checkin_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.checkin_frame, text="📥 Check-In")
        self.create_checkin_tab()
        
        # Check-out Tab
        self.checkout_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.checkout_frame, text="📤 Check-Out")
        self.create_checkout_tab()
        
        # Rooms Status Tab
        self.rooms_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.rooms_frame, text="🛏️ Rooms Status")
        self.create_rooms_tab()
        
        # Bookings Tab
        self.bookings_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.bookings_frame, text="📋 All Bookings")
        self.create_bookings_tab()
    
    def create_checkin_tab(self):
        # Stylish input frame
        input_frame = tk.Frame(self.checkin_frame, bg='#34495e', relief='raised', bd=2)
        input_frame.pack(pady=20, padx=20, fill='x')
        
        # Labels and Entries
        tk.Label(input_frame, text="Guest Name:", font=('Arial', 12, 'bold'), 
                fg='white', bg='#34495e').grid(row=0, column=0, padx=10, pady=10, sticky='w')
        self.guest_name = tk.Entry(input_frame, font=('Arial', 12), width=25, relief='solid', bd=2)
        self.guest_name.grid(row=0, column=1, padx=10, pady=10)
        
        tk.Label(input_frame, text="Room No:", font=('Arial', 12, 'bold'), 
                fg='white', bg='#34495e').grid(row=1, column=0, padx=10, pady=10, sticky='w')
        self.room_no = tk.Entry(input_frame, font=('Arial', 12), width=25, relief='solid', bd=2)
        self.room_no.grid(row=1, column=1, padx=10, pady=10)
        
        tk.Label(input_frame, text="Room Type:", font=('Arial', 12, 'bold'), 
                fg='white', bg='#34495e').grid(row=2, column=0, padx=10, pady=10, sticky='w')
        self.room_type = ttk.Combobox(input_frame, values=['Deluxe', 'Premium', 'Suite', 'Presidential'], 
                                     font=('Arial', 12), width=22, state='readonly')
        self.room_type.grid(row=2, column=1, padx=10, pady=10)
        
        tk.Label(input_frame, text="Check-in Date:", font=('Arial', 12, 'bold'), 
                fg='white', bg='#34495e').grid(row=3, column=0, padx=10, pady=10, sticky='w')
        self.checkin_date = tk.Entry(input_frame, font=('Arial', 12), width=25, relief='solid', bd=2)
        self.checkin_date.insert(0, datetime.now().strftime("%Y-%m-%d"))
        self.checkin_date.grid(row=3, column=1, padx=10, pady=10)
        
        tk.Label(input_frame, text="Check-out Date:", font=('Arial', 12, 'bold'), 
                fg='white', bg='#34495e').grid(row=4, column=0, padx=10, pady=10, sticky='w')
        self.checkout_date = tk.Entry(input_frame, font=('Arial', 12), width=25, relief='solid', bd=2)
        self.checkout_date.grid(row=4, column=1, padx=10, pady=10)
        
        # Calculate Amount
        tk.Button(input_frame, text="💰 Calculate Amount", command=self.calculate_amount,
                 bg='#27ae60', fg='white', font=('Arial', 10, 'bold'),
                 relief='flat', cursor='hand2').grid(row=5, column=0, columnspan=2, pady=20)
        
        self.total_amount_var = tk.StringVar(value="₹0")
        tk.Label(input_frame, textvariable=self.total_amount_var, font=('Arial', 16, 'bold'),
                fg='#f39c12', bg='#34495e').grid(row=6, column=0, columnspan=2, pady=10)
        
        # Check-in Button
        tk.Button(input_frame, text="✅ CHECK-IN GUEST", command=self.checkin_guest,
                 bg='#3498db', fg='white', font=('Arial', 14, 'bold'),
                 relief='flat', cursor='hand2', height=2, width=20).grid(row=7, column=0, columnspan=2, pady=20)
    
    def create_checkout_tab(self):
        tk.Label(self.checkout_frame, text="Enter Room Number to Check-out:", 
                font=('Arial', 16, 'bold'), fg='#ecf0f1', bg='#2c3e50').pack(pady=40)
        
        checkout_frame = tk.Frame(self.checkout_frame, bg='#34495e', relief='raised', bd=2)
        checkout_frame.pack(pady=20)
        
        self.checkout_room = tk.Entry(checkout_frame, font=('Arial', 14), width=15, relief='solid', bd=2)
        self.checkout_room.pack(pady=20, padx=20)
        
        tk.Button(checkout_frame, text="🚪 CHECK-OUT", command=self.checkout_guest,
                 bg='#e74c3c', fg='white', font=('Arial', 14, 'bold'),
                 relief='flat', cursor='hand2', height=2, width=15).pack(pady=20)
    
    def create_rooms_tab(self):
        # Treeview for rooms status
        columns = ('Room No', 'Type', 'Status', 'Guest', 'Check-out')
        self.rooms_tree = ttk.Treeview(self.rooms_frame, columns=columns, show='headings', height=15)
        
        for col in columns:
            self.rooms_tree.heading(col, text=col)
            self.rooms_tree.column(col, width=150)
        
        scrollbar = ttk.Scrollbar(self.rooms_frame, orient='vertical', command=self.rooms_tree.yview)
        self.rooms_tree.configure(yscrollcommand=scrollbar.set)
        
        self.rooms_tree.pack(pady=20, padx=20, fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        tk.Button(self.rooms_frame, text="🔄 Refresh Rooms", command=self.refresh_rooms,
                 bg='#f39c12', fg='white', font=('Arial', 12, 'bold'),
                 relief='flat', cursor='hand2').pack(pady=10)
        
        self.refresh_rooms()
    
    def create_bookings_tab(self):
        columns = ('ID', 'Guest', 'Room', 'Type', 'Check-in', 'Check-out', 'Amount', 'Status')
        self.bookings_tree = ttk.Treeview(self.bookings_frame, columns=columns, show='headings', height=15)
        
        for col in columns:
            self.bookings_tree.heading(col, text=col)
            self.bookings_tree.column(col, width=120)
        
        scrollbar = ttk.Scrollbar(self.bookings_frame, orient='vertical', command=self.bookings_tree.yview)
        self.bookings_tree.configure(yscrollcommand=scrollbar.set)
        
        self.bookings_tree.pack(pady=20, padx=20, fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        tk.Button(self.bookings_frame, text="🔄 Refresh Bookings", command=self.refresh_bookings,
                 bg='#9b59b6', fg='white', font=('Arial', 12, 'bold'),
                 relief='flat', cursor='hand2').pack(pady=10)
        
        self.refresh_bookings()
    
    def calculate_amount(self):
        room_rates = {'Deluxe': 5000, 'Premium': 8000, 'Suite': 12000, 'Presidential': 20000}
        room_type = self.room_type.get()
        if room_type and room_type in room_rates:
            days = 1  # Default 1 day
            try:
                checkout = datetime.strptime(self.checkout_date.get(), "%Y-%m-%d")
                checkin = datetime.strptime(self.checkin_date.get(), "%Y-%m-%d")
                days = (checkout - checkin).days
            except:
                pass
            total = room_rates[room_type] * days
            self.total_amount_var.set(f"₹{total:,}")
            return total
        return 0
    
    def checkin_guest(self):
        if not all([self.guest_name.get(), self.room_no.get(), self.room_type.get(), 
                   self.checkin_date.get(), self.checkout_date.get()]):
            messagebox.showerror("Error", "Please fill all fields!")
            return
        
        total = self.calculate_amount()
        try:
            self.cursor.execute('''
                INSERT INTO bookings (guest_name, room_no, room_type, check_in, check_out, total_amount)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (self.guest_name.get(), int(self.room_no.get()), self.room_type.get(),
                  self.checkin_date.get(), self.checkout_date.get(), total))
            self.conn.commit()
            messagebox.showinfo("Success", "✅ Guest checked-in successfully!")
            self.clear_checkin_fields()
            self.refresh_rooms()
            self.refresh_bookings()
        except Exception as e:
            messagebox.showerror("Error", f"Check-in failed: {str(e)}")
    
    def checkout_guest(self):
        room_no = self.checkout_room.get()
        if not room_no:
            messagebox.showerror("Error", "Enter Room Number!")
            return
        
        self.cursor.execute("UPDATE bookings SET status='Checked-out' WHERE room_no=? AND status='Active'", 
                          (room_no,))
        if self.cursor.rowcount > 0:
            self.conn.commit()
            messagebox.showinfo("Success", f"✅ Room {room_no} checked-out!")
            self.refresh_rooms()
            self.refresh_bookings()
            self.checkout_room.delete(0, tk.END)
        else:
            messagebox.showerror("Error", "Room not found or already checked-out!")
    
    def refresh_rooms(self):
        for item in self.rooms_tree.get_children():
            self.rooms_tree.delete(item)
        
        self.cursor.execute('''
            SELECT room_no, room_type, status, guest_name, check_out 
            FROM bookings WHERE status='Active'
        ''')
        for row in self.cursor.fetchall():
            self.rooms_tree.insert('', 'end', values=row)
    
    def refresh_bookings(self):
        for item in self.bookings_tree.get_children():
            self.bookings_tree.delete(item)
        
        self.cursor.execute("SELECT * FROM bookings ORDER BY id DESC")
        for row in self.cursor.fetchall():
            self.bookings_tree.insert('', 'end', values=row)
    
    def clear_checkin_fields(self):
        self.guest_name.delete(0, tk.END)
        self.room_no.delete(0, tk.END)
        self.checkin_date.delete(0, tk.END)
        self.checkout_date.delete(0, tk.END)
        self.total_amount_var.set("₹0")

if __name__ == "__main__":
    root = tk.Tk()
    app = HotelManagementSystem(root)
    root.mainloop()
