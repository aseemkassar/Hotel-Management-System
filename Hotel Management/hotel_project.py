import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from datetime import datetime, timedelta
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import threading
from email.utils import formataddr
from PIL import Image, ImageTk
import os

# ✅ Script jis folder mein hai, wahaan se images load hongi
# Chahe aap script kisi bhi directory se run karo
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

class HotelManagementSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("👑 Mannat Hotel - Elite Premium Suite")
        self.root.geometry("1450x950")
        self.root.state('zoomed')
        
        self.bg_dark = '#0f172a'
        self.bg_panel = '#1e293b'
        self.bg_field = '#334155'
        self.fg_light = '#f8fafc'
        self.fg_muted = '#94a3b8'
        self.btn_accent = '#f1f5f9'
        self.btn_accent_fg = '#0f172a'
        self.btn_red = '#ef4444'
        self.btn_blue = '#3b82f6'

        self.sender_email = "aseemmwn2006@gmail.com"
        self.sender_password = "tzqladbmrfhwvzxp"

        self.conn = self.connect_db()
        if not self.conn:
            return

        self.cursor = self.conn.cursor()
        self.create_tables()
        self.setup_styles()
        self.setup_ui()
        self.refresh_status()

    def connect_db(self):
        try:
            return mysql.connector.connect(
                host="localhost", port=3306, user="root",
                password="aseem", auth_plugin='mysql_native_password'
            )
        except:
            messagebox.showerror("Database Error", "Please ensure MySQL server is running (mysqld --console)")
            return None

    def create_tables(self):
        self.cursor.execute("CREATE DATABASE IF NOT EXISTS hotel_db")
        self.cursor.execute("USE hotel_db")
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS bookings (
                id INT AUTO_INCREMENT PRIMARY KEY,
                guest_name VARCHAR(100),
                phone VARCHAR(15),
                email VARCHAR(100),
                room_no INT UNIQUE,
                room_type VARCHAR(50),
                check_in DATE,
                check_out DATE,
                total_amount DECIMAL(10,2),
                status VARCHAR(20) DEFAULT 'Active'
            )
        """)
        self.conn.commit()

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TNotebook', background=self.bg_dark, borderwidth=0)
        style.configure('TNotebook.Tab', font=('Segoe UI', 11, 'bold'), padding=[25, 10], background=self.bg_panel, foreground=self.fg_light)
        style.map('TNotebook.Tab', background=[('selected', self.btn_accent)], foreground=[('selected', self.btn_accent_fg)])
        
        style.configure('Treeview', background=self.bg_panel, fieldbackground=self.bg_panel, foreground=self.fg_light, font=('Segoe UI', 11), rowheight=35)
        style.configure('Treeview.Heading', background=self.bg_dark, foreground=self.fg_light, font=('Segoe UI', 12, 'bold'))
        style.map('Treeview', background=[('selected', self.btn_blue)], foreground=[('selected', self.fg_light)])

    def send_email_async(self, guest_email, subject, msg_body):
        def email_thread():
            if not guest_email or "@" not in guest_email:
                return
            try:
                msg = MIMEMultipart()
                msg['From'] = formataddr(("✨ Mannat Hotel ✨", self.sender_email))
                msg['To'] = guest_email
                msg['Subject'] = subject
                msg.attach(MIMEText(msg_body, 'plain', 'utf-8'))
                server = smtplib.SMTP('smtp.gmail.com', 587)
                server.starttls()
                server.login(self.sender_email, self.sender_password)
                server.sendmail(self.sender_email, guest_email, msg.as_string())
                server.quit()
            except Exception as e:
                print(f"Background Email Error: {e}")
        threading.Thread(target=email_thread, daemon=True).start()

    def setup_ui(self):
        self.main_frame = tk.Frame(self.root, bg=self.bg_dark)
        self.main_frame.pack(fill='both', expand=True)

        header = tk.Frame(self.main_frame, bg=self.bg_panel, height=80, bd=0)
        header.pack(fill='x', side='top', padx=30, pady=(20, 10))
        tk.Label(header, text="M A N N A T   H O T E L   &   L U X U R Y   S U I T E S", font=('Helvetica', 22, 'bold'), fg=self.fg_light, bg=self.bg_panel).pack(pady=15)

        notebook = ttk.Notebook(self.main_frame)
        notebook.pack(fill='both', expand=True, padx=30, pady=(10, 30))

        self.checkin_frame = tk.Frame(notebook, bg=self.bg_dark)
        self.checkout_frame = tk.Frame(notebook, bg=self.bg_dark)
        self.status_frame = tk.Frame(notebook, bg=self.bg_dark)

        notebook.add(self.checkin_frame, text="  📥 GUEST CHECK-IN  ")
        notebook.add(self.checkout_frame, text="  📤 GUEST CHECK-OUT  ")
        notebook.add(self.status_frame, text="  📊 LIVE DATA & ACTIONS  ")

        self.create_checkin_tab()
        self.create_checkout_tab()
        self.create_status_tab()

        self.root.bind('<Return>', lambda e: self.save_booking())

    
    def create_checkin_tab(self):
        
        self.bg_canvas = tk.Canvas(
            self.checkin_frame,
            highlightthickness=0,
            bg=self.bg_dark
        )
        self.bg_canvas.place(x=0, y=0, relwidth=1, relheight=1)

        
        self.bg_canvas.bind("<Configure>", self._on_canvas_resize)

        
        overlay = tk.Frame(
            self.checkin_frame,
            bg='#0f172a',        
            padx=40,
            pady=20,
            bd=0
        )
        
        overlay.place(relx=0.5, rely=0.5, anchor='center')

        
        tk.Label(
            overlay,
            text="LUXURY REGISTRATION",
            font=('Helvetica', 15, 'bold'),
            fg=self.fg_light,
            bg='#0f172a'
        ).grid(row=0, column=0, columnspan=2, pady=(0, 20))

        
        self.room_preview_label = tk.Label(
            overlay,
            text="",
            font=('Segoe UI', 10, 'italic'),
            fg=self.fg_muted,
            bg='#0f172a'
        )

        field_data = [
            ("Guest Full Name *", "guest_name"),
            ("Contact Number", "phone"),
            ("Email Address *", "email"),
            ("Room Number *", "room_no"),
            ("Room Category *", "room_type"),
            ("Custom Rate per Night (Optional)", "custom_rate"),
            ("Check-In Date (YYYY-MM-DD)", "checkin_date"),
            ("Check-Out Date (YYYY-MM-DD)", "checkout_date")
        ]

        self.entries = {}
        for idx, (label_text, key) in enumerate(field_data):
            lbl = tk.Label(
                overlay,
                text=label_text,
                font=('Segoe UI', 10, 'bold'),
                fg=self.fg_muted,
                bg='#0f172a'
            )
            lbl.grid(row=idx + 1, column=0, sticky='w', pady=6, padx=(0, 20))

            if key == "room_type":
                entry = ttk.Combobox(
                    overlay,
                    values=['Deluxe', 'Premium', 'Suite', 'Presidential'],
                    width=33,
                    state='readonly',
                    font=('Segoe UI', 11)
                )
                
                entry.bind("<<ComboboxSelected>>", self.on_room_category_change)
            else:
                entry = tk.Entry(
                    overlay,
                    font=('Segoe UI', 11),
                    width=35,
                    bg=self.bg_field,
                    fg=self.fg_light,
                    insertbackground=self.fg_light,
                    bd=0,
                    relief='flat'
                )
                if key in ["checkin_date", "checkout_date", "custom_rate"]:
                    entry.bind("<KeyRelease>", lambda e: self.calculate_total())
                    if key == "checkin_date":
                        entry.insert(0, datetime.now().strftime("%Y-%m-%d"))
                    elif key == "checkout_date":
                        entry.insert(0, (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d"))

            entry.grid(row=idx + 1, column=1, pady=6)
            self.entries[key] = entry

        self.total_label = tk.Label(
            overlay,
            text="Estimated Total: ₹0",
            font=('Helvetica', 14, 'bold'),
            fg=self.fg_light,
            bg='#0f172a'
        )
        self.total_label.grid(row=10, column=0, columnspan=2, pady=12)

        save_btn = tk.Button(
            overlay,
            text="CONFIRM RESERVATION",
            command=self.save_booking,
            font=('Helvetica', 11, 'bold'),
            bg=self.btn_accent,
            fg=self.btn_accent_fg,
            activebackground='#cbd5e1',
            activeforeground='#000000',
            bd=0,
            cursor='hand2',
            height=2,
            width=35
        )
        save_btn.grid(row=11, column=0, columnspan=2, pady=5)

        
        self._bg_photo = None
        self._current_bg_file = None

    def _on_canvas_resize(self, event):
        """Canvas size badalne par background image bhi resize ho"""
        if self._current_bg_file:
            self._render_bg_image(self._current_bg_file, event.width, event.height)

    def on_room_category_change(self, event):
        """Room category badalne par background image aur total dono update"""
        self.calculate_total()

        category = self.entries["room_type"].get().lower()
        
        image_mapping = {
            'deluxe':       os.path.join(BASE_DIR, 'hotel.jpg'),
            'premium':      os.path.join(BASE_DIR, 'hotel1.jpg'),
            'suite':        os.path.join(BASE_DIR, 'hotel2.jpg'),
            'presidential': os.path.join(BASE_DIR, 'hotel5.jpg'),
        }
        image_file = image_mapping.get(category, os.path.join(BASE_DIR, 'default_room.jpg'))
        self.update_room_image(image_file)

    
    def update_room_image(self, filename):
        """Diye gaye filename se poori tab ka background set karo"""
        self._current_bg_file = filename
        w = self.bg_canvas.winfo_width()
        h = self.bg_canvas.winfo_height()

        
        if w < 10 or h < 10:
            
            self.bg_canvas.after(100, lambda: self.update_room_image(filename))
            return

        self._render_bg_image(filename, w, h)

    def _render_bg_image(self, filename, width, height):
        """Image ko canvas ke exact size me stretch karke render karo"""
        try:
            if os.path.exists(filename):
                img = Image.open(filename)
            else:
                
                img = Image.new('RGB', (width, height), color='#1e293b')

            img = img.resize((width, height), Image.Resampling.LANCZOS)
            self._bg_photo = ImageTk.PhotoImage(img)

            
            self.bg_canvas.delete("bg_img")
            self.bg_canvas.create_image(
                0, 0,
                anchor='nw',
                image=self._bg_photo,
                tags="bg_img"
            )
            
            self.bg_canvas.tag_lower("bg_img")

        except Exception as e:
            print(f"Background image error: {e}")
            self.bg_canvas.config(bg=self.bg_dark)

    

    def create_checkout_tab(self):
        
        self.co_bg_canvas = tk.Canvas(self.checkout_frame, highlightthickness=0, bg=self.bg_dark)
        self.co_bg_canvas.place(x=0, y=0, relwidth=1, relheight=1)
        self.co_bg_canvas.bind("<Configure>", self._on_co_canvas_resize)
        self._co_bg_photo = None
        self._co_current_file = None

        
        panel = tk.Frame(self.checkout_frame, bg='#0f172a', padx=60, pady=40, bd=0)
        panel.place(relx=0.5, rely=0.5, anchor='center')

        tk.Label(panel, text="DEPARTURE & SETTLEMENT", font=('Helvetica', 18, 'bold'),
                 fg=self.fg_light, bg='#0f172a').pack(pady=(0, 8))

        
        self.co_preview_label = tk.Label(panel, text="", font=('Segoe UI', 11, 'italic'),
                                          fg='#94a3b8', bg='#0f172a')
        self.co_preview_label.pack(pady=(0, 15))

        tk.Label(panel, text="Enter Assigned Room Number:", font=('Segoe UI', 12),
                 fg=self.fg_muted, bg='#0f172a').pack(pady=5)

        self.checkout_entry = tk.Entry(panel, font=('Segoe UI', 22, 'bold'), width=12,
                                        justify='center', bg=self.bg_field, fg=self.fg_light,
                                        insertbackground=self.fg_light, bd=0)
        self.checkout_entry.pack(pady=15)

        
        self.checkout_entry.bind("<KeyRelease>", self._on_checkout_room_type)

        out_btn = tk.Button(panel, text="PROCESS CHECK-OUT & BILL", command=self.checkout_room,
                            font=('Helvetica', 11, 'bold'), bg=self.btn_red, fg=self.fg_light,
                            activebackground='#b91c1c', activeforeground='white',
                            bd=0, cursor='hand2', height=2, width=32)
        out_btn.pack(pady=15)

    def _on_co_canvas_resize(self, event):
        """Checkout canvas resize hone par image bhi resize ho"""
        if self._co_current_file:
            self._render_co_bg_image(self._co_current_file, event.width, event.height)

    def _on_checkout_room_type(self, event):
        """Room number type karte hi DB se room_type fetch karo aur background set karo"""
        room_no_str = self.checkout_entry.get().strip()
        if not room_no_str.isdigit():
            
            self.co_bg_canvas.delete("co_bg_img")
            self._co_current_file = None
            self.co_bg_canvas.config(bg=self.bg_dark)
            self.co_preview_label.config(text="")
            return
        try:
            room_no = int(room_no_str)
            self.cursor.execute(
                "SELECT guest_name, room_type FROM hotel_db.bookings WHERE room_no=%s AND status='Active'",
                (room_no,)
            )
            row = self.cursor.fetchone()
            if row:
                guest_name, room_type = row[0], row[1]
                self.co_preview_label.config(
                    text=f"🛏  {room_type}  |  👤 {guest_name}",
                    fg='#f8fafc'
                )
                
                co_image_mapping = {
                    'Deluxe':       os.path.join(BASE_DIR, 'deluxe.jpg'),
                    'Premium':      os.path.join(BASE_DIR, 'premium.jpg'),
                    'Suite':        os.path.join(BASE_DIR, 'suite.jpg'),
                    'Presidential': os.path.join(BASE_DIR, 'presidential.jpg'),
                }
                img_file = co_image_mapping.get(room_type, os.path.join(BASE_DIR, 'default_room.jpg'))
                self._update_co_bg_image(img_file)
            else:
                
                self.co_bg_canvas.delete("co_bg_img")
                self._co_current_file = None
                self.co_bg_canvas.config(bg=self.bg_dark)
                self.co_preview_label.config(text="❌  No active booking found for this room", fg='#ef4444')
        except Exception:
            pass

    def _update_co_bg_image(self, filename):
        """Checkout tab ka background image set karo"""
        self._co_current_file = filename
        w = self.co_bg_canvas.winfo_width()
        h = self.co_bg_canvas.winfo_height()
        if w < 10 or h < 10:
            self.co_bg_canvas.after(100, lambda: self._update_co_bg_image(filename))
            return
        self._render_co_bg_image(filename, w, h)

    def _render_co_bg_image(self, filename, width, height):
        """Image ko canvas ke exact size mein render karo"""
        try:
            if os.path.exists(filename):
                img = Image.open(filename)
            else:
                img = Image.new('RGB', (width, height), color='#1e293b')
            img = img.resize((width, height), Image.Resampling.LANCZOS)
            self._co_bg_photo = ImageTk.PhotoImage(img)
            self.co_bg_canvas.delete("co_bg_img")
            self.co_bg_canvas.create_image(0, 0, anchor='nw',
                                            image=self._co_bg_photo, tags="co_bg_img")
            self.co_bg_canvas.tag_lower("co_bg_img")
        except Exception as e:
            print(f"Checkout bg image error: {e}")
            self.co_bg_canvas.config(bg=self.bg_dark)

    def create_status_tab(self):
        action_bar = tk.Frame(self.status_frame, bg=self.bg_dark, pady=10)
        action_bar.pack(fill='x', side='top', padx=20)

        tk.Label(action_bar, text="💡 Double-Click any row to view Full Guest Details", font=('Segoe UI', 11, 'italic'), fg=self.fg_muted, bg=self.bg_dark).pack(side='left', padx=10)

        btn_view = tk.Button(action_bar, text="👁️ VIEW DETAILS", command=self.view_selected_guest, bg=self.btn_blue, fg=self.fg_light, font=('Helvetica', 10, 'bold'), bd=0, width=15, height=2, cursor='hand2')
        btn_view.pack(side='right', padx=10)

        btn_del = tk.Button(action_bar, text="🗑️ DELETE RECORD", command=self.delete_selected_guest, bg=self.btn_red, fg=self.fg_light, font=('Helvetica', 10, 'bold'), bd=0, width=15, height=2, cursor='hand2')
        btn_del.pack(side='right', padx=10)

        btn_ref = tk.Button(action_bar, text="🔄 REFRESH", command=self.refresh_status, bg=self.bg_field, fg=self.fg_light, font=('Helvetica', 10, 'bold'), bd=0, width=12, height=2, cursor='hand2')
        btn_ref.pack(side='right', padx=10)

        tree_frame = tk.Frame(self.status_frame, bg=self.bg_dark)
        tree_frame.pack(fill='both', expand=True, padx=20, pady=(0, 20))

        cols = ("ID", "Room No", "Guest Name", "Category", "Check-In", "Check-Out", "Total Amount", "Status")
        self.tree = ttk.Treeview(tree_frame, columns=cols, show='headings', selectmode='browse')

        v_scroll = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        h_scroll = ttk.Scrollbar(tree_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=v_scroll.set, xscrollcommand=h_scroll.set)

        self.tree.grid(row=0, column=0, sticky='nsew')
        v_scroll.grid(row=0, column=1, sticky='ns')
        h_scroll.grid(row=1, column=0, sticky='ew')

        tree_frame.grid_columnconfigure(0, weight=1)
        tree_frame.grid_rowconfigure(0, weight=1)

        for col in cols:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=140, anchor='center')

        self.tree.bind("<Double-1>", lambda e: self.view_selected_guest())

    def calculate_total(self):
        try:
            rtype = self.entries["room_type"].get()
            cin = datetime.strptime(self.entries["checkin_date"].get(), "%Y-%m-%d")
            cout = datetime.strptime(self.entries["checkout_date"].get(), "%Y-%m-%d")
            custom_rate_str = self.entries["custom_rate"].get().strip()

            nights = max((cout - cin).days, 1)
            if custom_rate_str:
                per_night_rate = float(custom_rate_str)
            else:
                rates = {'Deluxe': 5000, 'Premium': 8000, 'Suite': 12000, 'Presidential': 20000}
                per_night_rate = rates.get(rtype, 0)

            total = per_night_rate * nights
            if total > 0:
                self.total_label.config(text=f"Estimated Total: ₹{total:,}", fg=self.fg_light)
            return total
        except:
            self.total_label.config(text="Status: Enter Valid Dates/Rates...", fg=self.fg_muted)
            return 0

    def view_selected_guest(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Selection Required", "Please select a guest row from the table first.")
            return

        values = self.tree.item(selected_item, 'values')
        booking_id = values[0]

        self.cursor.execute("SELECT guest_name, phone, email, room_no, room_type, check_in, check_out, total_amount, status FROM hotel_db.bookings WHERE id=%s", (booking_id,))
        row = self.cursor.fetchone()

        if row:
            detail_msg = (
                f"MANNAT HOTEL GUEST PROFILE\n\n"
                f"👤 Name: {row[0]}\n"
                f"📞 Contact: {row[1]}\n"
                f"📧 Email: {row[2]}\n"
                f"🚪 Room Number: {row[3]}\n"
                f"🛏️ Category: {row[4]}\n"
                f"📅 Check-In: {row[5]}\n"
                f"📅 Check-Out: {row[6]}\n"
                f"💰 Total Amount Paid: ₹{row[7]:,}\n"
                f"📌 Booking Status: {row[8]}"
            )
            messagebox.showinfo("Full Guest Profile", detail_msg)

    def delete_selected_guest(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Selection Required", "Please select a row to delete.")
            return

        values = self.tree.item(selected_item, 'values')
        booking_id = values[0]
        guest_name = values[2]

        confirm = messagebox.askyesno("Confirm Permanent Deletion", f"Are you sure you want to completely erase {guest_name}'s record from hotel_db?")
        if confirm:
            self.cursor.execute("DELETE FROM hotel_db.bookings WHERE id=%s", (booking_id,))
            self.conn.commit()
            messagebox.showinfo("Erased", "Record deleted successfully.")
            self.refresh_status()

    def save_booking(self):
        try:
            guest = self.entries["guest_name"].get().strip()
            phone = self.entries["phone"].get().strip()
            email = self.entries["email"].get().strip()
            room_no_str = self.entries["room_no"].get().strip()
            room_type = self.entries["room_type"].get()
            check_in = self.entries["checkin_date"].get().strip()
            check_out = self.entries["checkout_date"].get().strip()

            if not all([guest, email, room_no_str, room_type]):
                messagebox.showerror("Validation Error", "Name, Email, Room No, and Room Category are required.")
                return

            room_no = int(room_no_str)
            total = self.calculate_total()
            if total == 0:
                messagebox.showerror("Calculation Error", "Please verify dates or custom rates entry.")
                return

            self.cursor.execute("SELECT * FROM hotel_db.bookings WHERE room_no=%s AND status='Active'", (room_no,))
            if self.cursor.fetchone():
                messagebox.showerror("Allocation Conflict", f"Room {room_no} is currently occupied.")
                return

            self.cursor.execute("""
                INSERT INTO hotel_db.bookings
                (guest_name, phone, email, room_no, room_type, check_in, check_out, total_amount)
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
            """, (guest, phone, email, room_no, room_type, check_in, check_out, total))
            self.conn.commit()

            sub = "🎉 Booking Confirmed! Welcome to Mannat Hotel 👑"
            body = (
                f"╔══════════════════════════════════════╗\n"
                f"      👑  MANNAT HOTEL & LUXURY SUITES  👑\n"
                f"╚══════════════════════════════════════╝\n\n"
                f"🌟 Dear {guest},\n\n"
                f"Congratulations! Your luxury reservation has been\n"
                f"successfully confirmed. We are beyond delighted\n"
                f"to welcome you to our family! 🥂✨\n\n"
                f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                f"        🏨  YOUR RESERVATION DETAILS\n"
                f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
                f"  🚪 Room Number   :  {room_no}\n"
                f"  🛏️  Room Category :  {room_type}\n"
                f"  📅 Check-In      :  {check_in}\n"
                f"  📅 Check-Out     :  {check_out}\n"
                f"  💰 Total Amount  :  ₹{total:,}\n\n"
                f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
                f"🎁 What awaits you at Mannat Hotel:\n\n"
                f"  ✅ World-class luxury accommodation\n"
                f"  ✅ 24/7 Dedicated concierge service 🛎️\n"
                f"  ✅ Fine dining & rooftop experience 🍽️\n"
                f"  ✅ Complimentary welcome drink on arrival 🍾\n"
                f"  ✅ Premium spa & wellness facilities 💆\n\n"
                f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
                f"📞 Need help before your arrival?\n"
                f"   Our front desk is available 24/7 just for you!\n\n"
                f"🌸 We promise to make your stay absolutely\n"
                f"   unforgettable & filled with golden memories! 💛\n\n"
                f"See you soon! 🚀💫\n\n"
                f"With warm regards & excitement,\n"
                f"🌟 Guest Relations Team\n"
                f"👑 Mannat Hotel Resort & Luxury Suites\n"
                f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                f"   \'Where Every Stay Becomes a Story\' 💛"
            )
            self.send_email_async(email, sub, body)

            messagebox.showinfo("Success", f"Booking recorded successfully for {guest}!")
            self.refresh_status()
            self.clear_form()

        except ValueError:
            messagebox.showerror("Format Error", "Room Number and Custom Rate must contain numerical digits only.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def checkout_room(self):
        try:
            room_no_str = self.checkout_entry.get().strip()
            if not room_no_str:
                messagebox.showerror("Error", "Please enter a Room Number.")
                return

            room_no = int(room_no_str)
            self.cursor.execute("SELECT guest_name, email FROM hotel_db.bookings WHERE room_no=%s AND status='Active'", (room_no,))
            res = self.cursor.fetchone()

            if res:
                guest_name, email = res[0], res[1]
                self.cursor.execute("UPDATE hotel_db.bookings SET status='Checked-out' WHERE room_no=%s AND status='Active'", (room_no,))
                self.conn.commit()

                sub = "💖 Thank You for Staying at Mannat Hotel! Safe Travels 🌟"
                body = (
                    f"╔══════════════════════════════════════╗\n"
                    f"      👑  MANNAT HOTEL & LUXURY SUITES  👑\n"
                    f"╚══════════════════════════════════════╝\n\n"
                    f"💖 Dear {guest_name},\n\n"
                    f"It was an absolute honour and privilege\n"
                    f"to have you as our guest! 🌸\n\n"
                    f"Your check-out from Room {room_no} has been\n"
                    f"successfully processed. 🏨✅\n\n"
                    f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                    f"         ✈️  BON VOYAGE, DEAR GUEST!\n"
                    f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
                    f"🌟 We truly hope you had a magnificent,\n"
                    f"   relaxing & memorable stay with us!\n\n"
                    f"😊 Your happiness is our greatest reward.\n"
                    f"   Thank you for choosing Mannat Hotel as\n"
                    f"   your home away from home! 🏡💛\n\n"
                    f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
                    f"🎁 Before you go, here\'s a little gift:\n\n"
                    f"  🌹 Use code MANNAT10 for 10% off\n"
                    f"     on your next booking with us!\n\n"
                    f"  ⭐ We\'d love to hear about your experience!\n"
                    f"     Your feedback means the world to us.\n\n"
                    f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
                    f"🚗 Safe travels wherever you go next!\n"
                    f"   May your journey be smooth & beautiful! ✈️🗺️\n\n"
                    f"We can\'t wait to welcome you back! 🤗👑\n\n"
                    f"With love & gratitude,\n"
                    f"🌟 Guest Relations Team\n"
                    f"👑 Mannat Hotel Resort & Luxury Suites\n"
                    f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                    f"   \'Where Every Stay Becomes a Story\' 💛"
                )
                self.send_email_async(email, sub, body)
                messagebox.showinfo("Success", f"Room {room_no} Checked-Out Successfully.")
            else:
                messagebox.showerror("Not Found", f"No Active booking found for Room {room_no}.")

            self.refresh_status()
            self.checkout_entry.delete(0, 'end')
            # ✅ Checkout ke baad background aur preview clear karo
            self.co_bg_canvas.delete("co_bg_img")
            self._co_current_file = None
            self.co_bg_canvas.config(bg=self.bg_dark)
            self.co_preview_label.config(text="")
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid numerical Room Number.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def refresh_status(self):
        try:
            self.tree.delete(*self.tree.get_children())
            self.cursor.execute("SELECT id,room_no,guest_name,room_type,check_in,check_out,total_amount,status FROM hotel_db.bookings ORDER BY id DESC")
            for row in self.cursor.fetchall():
                self.tree.insert("", "end", values=(row[0], row[1], row[2], row[3], row[4], row[5], f"₹{row[6]:,.0f}", row[7]))
        except Exception as e:
            print(f"Refresh error: {e}")

    def clear_form(self):
        self.entries["guest_name"].delete(0, 'end')
        self.entries["phone"].delete(0, 'end')
        self.entries["email"].delete(0, 'end')
        self.entries["room_no"].delete(0, 'end')
        self.entries["room_type"].set('')
        self.entries["custom_rate"].delete(0, 'end')
        self.entries["checkin_date"].delete(0, 'end')
        self.entries["checkin_date"].insert(0, datetime.now().strftime("%Y-%m-%d"))
        self.entries["checkout_date"].delete(0, 'end')
        self.entries["checkout_date"].insert(0, (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d"))
        self.total_label.config(text="Estimated Total: ₹0", fg=self.fg_light)
        # ✅ Background clear — default hotel view dikhao
        default_img = os.path.join(BASE_DIR, 'default_room.jpg')
        self.update_room_image(default_img)

if __name__ == "__main__":
    root = tk.Tk()
    app = HotelManagementSystem(root)
    root.mainloop()
