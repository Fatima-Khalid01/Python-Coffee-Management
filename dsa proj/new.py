import tkinter as tk
from tkinter import messagebox
from datetime import datetime
from PIL import Image, ImageTk
import os

class CoffeeShop:
    def __init__(self, master):
        self.master = master
        master.title("The Daily Sip")
        master.geometry("800x600")

        # Get the base directory (the folder containing the Python script)
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.user_data_file = os.path.join(self.base_dir, "user_orders.txt")
        self.selected_toppings = []

        # Load background image for all windows (relative path to the base directory)
        bg_image_path = os.path.join(self.base_dir, "bac.png")
        self.background_image = Image.open(bg_image_path).resize((800, 600))
        self.bg_image = ImageTk.PhotoImage(self.background_image)

        # Create GUI elements to gather user information
        self.create_user_info_widgets()

    def apply_background(self, window):
        bg_label = tk.Label(window, image=self.bg_image)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        return bg_label

    def create_user_info_widgets(self):
        for widget in self.master.winfo_children():
            widget.destroy()

        # Apply background to main window
        self.bg_label = self.apply_background(self.master)

        tk.Label(self.master, text="Welcome to The Daily Sip", bg="#d2b48c", fg="#8b5a2b", font=("Arial", 24)).pack(pady=10)

        tk.Label(self.master, text="Name:", bg="#3b2f2f", fg="white").pack(pady=5)
        self.name_entry = tk.Entry(self.master)
        self.name_entry.pack(pady=5)

        tk.Label(self.master, text="Address:", bg="#3b2f2f", fg="white").pack(pady=5)
        self.address_entry = tk.Entry(self.master)
        self.address_entry.pack(pady=5)

        tk.Button(self.master, text="Proceed", command=self.proceed_to_order, bg="#8b5a2b", fg="white").pack(pady=10)

    def proceed_to_order(self):
        self.user_name = self.name_entry.get()
        self.user_address = self.address_entry.get()

        if not self.user_name or not self.user_address:
            messagebox.showwarning("Input Error, Please enter both name and address.")
            return
        
        self.master.withdraw()
        self.order_window()

    def order_window(self):
        self.order_top = tk.Toplevel(self.master)
        self.order_top.title("Coffee Order")
        self.order_top.geometry("800x600")

        # Apply background
        self.bg_label = self.apply_background(self.order_top)

        self.coffee_options = {
            "Espresso": 2.50,
            "Latte": 3.00,
            "Cappuccino": 3.50,
            "Americano": 2.00
        }

        # Use relative paths for coffee images
        self.coffee_images = {
            "Espresso": ImageTk.PhotoImage(Image.open(os.path.join(self.base_dir, "8.png")).resize((50, 50))),
            "Latte": ImageTk.PhotoImage(Image.open(os.path.join(self.base_dir, "7.png")).resize((50, 50))),
            "Cappuccino": ImageTk.PhotoImage(Image.open(os.path.join(self.base_dir, "5.png")).resize((50, 50))),
            "Americano": ImageTk.PhotoImage(Image.open(os.path.join(self.base_dir, "9.png")).resize((50, 50)))
        }

        tk.Label(self.order_top, text="Select Coffee:" , bg="#d2b48c", fg="brown", font=("Arial", 18, "bold")).pack(pady=10)
        
        self.coffee_buttons_frame = tk.Frame(self.order_top, bg="#d2b48c")
        self.coffee_buttons_frame.pack(pady=5)

        for coffee_name in self.coffee_options.keys():
            coffee_frame = tk.Frame(self.coffee_buttons_frame, bg="#d2b48c")
            coffee_frame.pack(side=tk.TOP, pady=5)

            coffee_image_label = tk.Label(coffee_frame, image=self.coffee_images[coffee_name])
            coffee_image_label.image = self.coffee_images[coffee_name]
            coffee_image_label.pack(side=tk.LEFT, padx=5)

            btn = tk.Button(coffee_frame, text=coffee_name, command=lambda name=coffee_name: self.select_coffee(name), bg="#8b5a2b", fg="white")
            btn.pack(side=tk.LEFT, padx=5)

    def select_coffee(self, coffee_name):
        self.selected_coffee = coffee_name
        messagebox.showinfo("Coffee Selected", f"You selected {coffee_name}.")
        self.select_extra_toppings()

    def select_extra_toppings(self):
        self.toppings_window = tk.Toplevel(self.order_top)
        self.toppings_window.title("Select Extra Toppings")
        self.toppings_window.geometry("400x300")

        # Apply background
        self.bg_label = self.apply_background(self.toppings_window)

        tk.Label(self.toppings_window, text="Select Extra Toppings (Optional):", bg="#d2b48c", fg="black", font=("Arial", 16)).pack(pady=10)

        toppings = ["Whipped Cream", "Chocolate Syrup", "Caramel", "Extra Shot"]
        self.topping_vars = {}

        for topping in toppings:
            var = tk.BooleanVar()
            checkbox = tk.Checkbutton(self.toppings_window, text=topping, variable=var, bg="#d2b48c", fg="black")
            checkbox.pack(anchor=tk.W)
            self.topping_vars[topping] = var

        tk.Button(self.toppings_window, text="Done", command=self.done_selecting_toppings, bg="#8b5a2b", fg="white").pack(pady=20)
        tk.Button(self.toppings_window, text="Skip Toppings", command=self.skip_toppings, bg="#8b5a2b", fg="white").pack(pady=5)

    def done_selecting_toppings(self):
        self.selected_toppings = [topping for topping, var in self.topping_vars.items() if var.get()]
        messagebox.showinfo("Toppings Selected", f"You selected: {', '.join(self.selected_toppings)}")
        self.toppings_window.destroy()
        self.process_order_window()

    def skip_toppings(self):
        self.selected_toppings = []
        messagebox.showinfo("Toppings Skipped", "No extra toppings selected.")
        self.toppings_window.destroy()
        self.process_order_window()

    def process_order_window(self):
        self.process_order_top = tk.Toplevel(self.order_top)
        self.process_order_top.title("Process Order")
        self.process_order_top.geometry("800x600")

        # Apply background
        self.bg_label = self.apply_background(self.process_order_top)

        self.order_queue = []

        tk.Label(self.process_order_top, text="Quantity:", bg="#d2b48c", fg="black").pack(pady=5)
        
        self.quantity_entry = tk.Entry(self.process_order_top, width=10)
        self.quantity_entry.pack()

        self.order_button = tk.Button(self.process_order_top, text="Add to Order", command=self.add_to_order, state=tk.NORMAL, bg="#8b5a2b", fg="white")
        self.order_button.pack(pady=5)

        tk.Label(self.process_order_top, text="Order List:", bg="#d2b48c", fg="black").pack(pady=10)
        
        self.order_list_box = tk.Listbox(self.process_order_top, width=120, height=10)  # Increased width to 120
        self.order_list_box.pack(pady=5)

        self.payment_button = tk.Button(self.process_order_top, text="Pay and Confirm", command=self.pay_and_confirm, state=tk.DISABLED, bg="#8b5a2b", fg="white")
        self.payment_button.pack(pady=10)

        self.quantity_entry.bind("<KeyRelease>", self.enable_order_button)

    def enable_order_button(self, event):
        quantity = self.quantity_entry.get()
        if quantity.isdigit() and int(quantity) > 0:
            self.order_button.config(state=tk.NORMAL)
            if self.order_queue:
                self.payment_button.config(state=tk.NORMAL)
            else:
                self.payment_button.config(state=tk.DISABLED)

    def add_to_order(self):
        quantity = int(self.quantity_entry.get())
        price_per_cup = self.coffee_options[self.selected_coffee]
        total_price = price_per_cup * quantity

        order_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        toppings = ", ".join(self.selected_toppings) if self.selected_toppings else "No extra toppings"
        order_message = f"{self.user_name} ({self.user_address}): {quantity} x {self.selected_coffee} ({toppings}) - Total: ${total_price:.2f} - Ordered at: {order_date}"

        self.order_queue.append(order_message)
        self.order_list_box.insert(tk.END, order_message)
        self.quantity_entry.delete(0, tk.END)
        self.order_button.config(state=tk.DISABLED)

        if self.order_queue:
            self.payment_button.config(state=tk.NORMAL)

    def pay_and_confirm(self):
        total_amount = sum(float(order.split(" - Total: $")[-1].split(" ")[0]) for order in self.order_queue)
        messagebox.showinfo("Payment Successful", f"Total: ${total_amount:.2f}\nThank you for your order!")
        
        # Store order data
        self.save_order_data()

        # Show Thank You window
        self.show_thank_you_window()

    def save_order_data(self):
        with open(self.user_data_file, "a") as f:
            for order in self.order_queue:
                f.write(order + "\n")

    def show_thank_you_window(self):
        # Create a new window for the "Thank You!" message
        thank_you_window = tk.Toplevel(self.master)
        thank_you_window.title("Thank You!")
        thank_you_window.geometry("600x600")

        # Load the thank you image (ensure the relative path is correct)
        thank_you_image_path = os.path.join(self.base_dir, "thank.png")
        thank_you_image = Image.open("thank.png").resize((400, 400))  # Resize the image as needed
        thank_you_image_tk = ImageTk.PhotoImage(thank_you_image)

        # Apply background image
        self.apply_background(thank_you_window)

        # Add the image and a thank you message to the window
        img_label = tk.Label(thank_you_window, image=thank_you_image_tk)
        img_label.image = thank_you_image_tk  # Keep a reference to the image
        img_label.pack(pady=20)

        tk.Label(thank_you_window, text="Thank you for your order!", font=("Arial", 24, "bold"), fg="#8b5a2b").pack(pady=10)
       

        # Optionally, you can add a button to close the window
        tk.Button(thank_you_window, text="Close", command=lambda: self.close_thank_you_window(thank_you_window), bg="#8b5a2b", fg="white").pack(pady=10)


    def close_thank_you_window(self, window):
        window.destroy()  # Close the Thank You window
        self.master.deiconify()  # Show the main window again for the next user
        self.create_user_info_widgets()  # Reset user info fields and display the user window again

# Create the main window and run the application
root = tk.Tk()
coffee_shop = CoffeeShop(root)
root.mainloop()
