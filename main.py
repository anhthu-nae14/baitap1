import tkinter as tk
from tkinter import messagebox

# Hàm thực hiện các phép toán cơ bản
def basic_operations():
    try:
        num1 = float(entry_num1.get())
        num2 = float(entry_num2.get())
        operation = operation_var.get()

        if operation == 'add':
            result = num1 + num2
        elif operation == 'subtract':
            result = num1 - num2
        elif operation == 'multiply':
            result = num1 * num2
        elif operation == 'divide':
            if num2 != 0:
                result = num1 / num2
            else:
                messagebox.showerror("Error", "Không thể chia cho số 0")
                return

        messagebox.showinfo("Result", f"The result is: {result}")
    except ValueError:
        messagebox.showerror("Error", "Vui lòng nhập số hợp lệ")

# Hàm tính toán hằng đẳng thức đáng nhớ
def identity_operations():
    try:
        a = float(entry_a.get())
        b = float(entry_b.get())
        choice = identity_var.get()

        if choice == '1':
            result = a**2 + 2*a*b + b**2
            messagebox.showinfo("Result", f"({a} + {b})^2 = {result}")
        elif choice == '2':
            result = a**2 - 2*a*b + b**2
            messagebox.showinfo("Result", f"({a} - {b})^2 = {result}")
        elif choice == '3':
            result = (a - b) * (a + b)
            messagebox.showinfo("Result", f"{a}^2 - {b}^2 = {result}")
    except ValueError:
        messagebox.showerror("Error", "Vui lòng nhập số hợp lệ")

# Tạo cửa sổ chính
root = tk.Tk()
root.title("Máy Tính")

# Giao diện cho các phép toán cơ bản
tk.Label(root, text="Number 1:").grid(row=0, column=0, padx=10, pady=5)
entry_num1 = tk.Entry(root)
entry_num1.grid(row=0, column=1, padx=10, pady=5)

tk.Label(root, text="Number 2:").grid(row=1, column=0, padx=10, pady=5)
entry_num2 = tk.Entry(root)
entry_num2.grid(row=1, column=1, padx=10, pady=5)

operation_var = tk.StringVar(value='add')
tk.Label(root, text="Operation:").grid(row=2, column=0, padx=10, pady=5)

tk.Radiobutton(root, text="Add", variable=operation_var, value='add').grid(row=2, column=1, sticky='w')
tk.Radiobutton(root, text="Subtract", variable=operation_var, value='subtract').grid(row=3, column=1, sticky='w')
tk.Radiobutton(root, text="Multiply", variable=operation_var, value='multiply').grid(row=4, column=1, sticky='w')
tk.Radiobutton(root, text="Divide", variable=operation_var, value='divide').grid(row=5, column=1, sticky='w')

basic_button = tk.Button(root, text="Calculate Basic Operation", command=basic_operations)
basic_button.grid(row=6, column=0, columnspan=2, pady=10)

# Giao diện cho các hằng đẳng thức đáng nhớ
tk.Label(root, text="a:").grid(row=7, column=0, padx=10, pady=5)
entry_a = tk.Entry(root)
entry_a.grid(row=7, column=1, padx=10, pady=5)

tk.Label(root, text="b:").grid(row=8, column=0, padx=10, pady=5)
entry_b = tk.Entry(root)
entry_b.grid(row=8, column=1, padx=10, pady=5)

identity_var = tk.StringVar(value='1')
tk.Label(root, text="Identity:").grid(row=9, column=0, padx=10, pady=5)

tk.Radiobutton(root, text="(a + b)^2", variable=identity_var, value='1').grid(row=9, column=1, sticky='w')
tk.Radiobutton(root, text="(a - b)^2", variable=identity_var, value='2').grid(row=10, column=1, sticky='w')
tk.Radiobutton(root, text="a^2 - b^2", variable=identity_var, value='3').grid(row=11, column=1, sticky='w')

identity_button = tk.Button(root, text="Calculate Identity Operation", command=identity_operations)
identity_button.grid(row=12, column=0, columnspan=2, pady=10)

# Bắt đầu vòng lặp giao diện
root.mainloop()
