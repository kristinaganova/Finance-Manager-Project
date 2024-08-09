import tkinter as tk
from tkinter import ttk, messagebox
from decimal import Decimal

class PaymentMethodsWindow:
    def __init__(self, root, finance_manager, refresh_ui_callback):
        self.root = root
        self.root.title("Manage Payment Methods")
        self.account_manager = finance_manager.account_manager
        self.refresh_ui_callback = refresh_ui_callback

        self.create_widgets()

    def create_widgets(self):
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Frame for adding payment methods
        frame_payment_methods = ttk.LabelFrame(main_frame, text="Add Payment Method")
        frame_payment_methods.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        ttk.Label(frame_payment_methods, text="Method Name:").grid(row=0, column=0, padx=5, pady=5)
        self.method_name_entry = ttk.Entry(frame_payment_methods, width=12)
        self.method_name_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(frame_payment_methods, text="Method Type:").grid(row=1, column=0, padx=5, pady=5)
        self.method_type_combobox = ttk.Combobox(frame_payment_methods, values=["cash", "card"], width=10)
        self.method_type_combobox.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(frame_payment_methods, text="Initial Balance:").grid(row=2, column=0, padx=5, pady=5)
        self.initial_balance_entry = ttk.Entry(frame_payment_methods, width=12)
        self.initial_balance_entry.grid(row=2, column=1, padx=5, pady=5)

        ttk.Button(frame_payment_methods, text="Add Payment Method", command=self.add_payment_method).grid(row=3, column=0, columnspan=2, padx=5, pady=5)

        # Frame for displaying payment methods
        frame_display = ttk.LabelFrame(main_frame, text="Payment Methods")
        frame_display.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

        self.methods_tree = ttk.Treeview(frame_display, columns=("Name", "Type", "Balance"), show="headings", height=5)
        self.methods_tree.heading("Name", text="Name")
        self.methods_tree.heading("Type", text="Type")
        self.methods_tree.heading("Balance", text="Balance")
        self.methods_tree.grid(row=0, column=0, padx=5, pady=5)
        self.methods_tree.column("Name", width=100)
        self.methods_tree.column("Type", width=100)
        self.methods_tree.column("Balance", width=100)

        self.update_methods_tree()

        ttk.Button(frame_display, text="Delete Payment Method", command=self.delete_payment_method).grid(row=1, column=0, padx=5, pady=5)

    def add_payment_method(self):
        method_name = self.method_name_entry.get()
        method_type = self.method_type_combobox.get()
        initial_balance = self.initial_balance_entry.get()

        if method_name and method_type in ["cash", "card"]:
            try:
                initial_balance_decimal = Decimal(initial_balance)
                self.account_manager.add_payment_method(method_name, method_type, initial_balance=initial_balance_decimal)
                messagebox.showinfo("Success", f"Payment method '{method_name}' added successfully.")
                self.method_name_entry.delete(0, tk.END)
                self.method_type_combobox.set("")
                self.initial_balance_entry.delete(0, tk.END)
                self.update_methods_tree()  
                self.refresh_ui_callback()  
            except Exception as e:
                messagebox.showerror("Error", str(e))
        else:
            messagebox.showerror("Error", "Please enter valid payment method details.")

    def delete_payment_method(self):
        try:
            selected_item = self.methods_tree.selection()[0]
            method_name = self.methods_tree.item(selected_item, 'values')[0]
            self.account_manager.remove_payment_method(method_name)
            self.update_methods_tree() 
            self.refresh_ui_callback()  
        except IndexError:
            messagebox.showerror("Error", "No payment method selected")

    def update_methods_tree(self):
        for item in self.methods_tree.get_children():
            self.methods_tree.delete(item)
        for row in self.account_manager.get_payment_methods_with_balance():
            rounded_balance = round(row[2], 2)
            self.methods_tree.insert("", "end", values=(row[0], row[1], rounded_balance))