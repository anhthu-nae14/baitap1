import tkinter as tk
from tkinter import messagebox


def basic_operations():
    try:
        expression = entry_expression.get()
        result = eval(expression)
        add_to_history(f"{expression} = {result}")
        messagebox.showinfo("Kết Quả", f"Kết quả là: {result}")
    except ZeroDivisionError:
        messagebox.showerror("Lỗi", "Không thể chia cho số 0!")
    except Exception:
        messagebox.showerror("Lỗi", "Có lỗi xảy ra trong chuỗi nhập!")


def identity_operations():
    try:
        a = float(entry_a.get())
        b = float(entry_b.get())
        choice = identity_var.get()

        if choice == '1':
            result = a**2 + 2*a*b + b**2
            add_to_history(f"({a} + {b})^2 = {result}")
            messagebox.showinfo("Kết Quả", f"({a} + {b})^2 = {result}")
        elif choice == '2':
            result = a**2 - 2*a*b + b**2
            add_to_history(f"({a} - {b})^2 = {result}")
            messagebox.showinfo("Kết Quả", f"({a} - {b})^2 = {result}")
        elif choice == '3':
            result = (a - b) * (a + b)
            add_to_history(f"{a}^2 - {b}^2 = {result}")
            messagebox.showinfo("Kết Quả", f"{a}^2 - {b}^2 = {result}")
    except ValueError:
        messagebox.showerror("Lỗi", "Vui lòng nhập số hợp lệ!")


def add_to_history(calculation):
    history_text.configure(state=tk.NORMAL)
    history_text.insert(tk.END, calculation + "\n")
    history_text.configure(state=tk.DISABLED)


def toggle_virtual_keyboard():
    if hasattr(root, "virtual_keyboard"):
        if root.virtual_keyboard.state() == "withdrawn":
            root.virtual_keyboard.deiconify()  # Hiển thị lại bàn phím ảo nếu bị ẩn
        else:
            root.virtual_keyboard.withdraw()  
    else:
        create_virtual_keyboard() 


def create_virtual_keyboard():
    # Tạo bàn phím ảo (được sử dụng khi bàn phím số bị hỏng thì sẽ dùng phím ảo)
    root.virtual_keyboard = tk.Toplevel(root)
    root.virtual_keyboard.title("Bàn Phím Ảo")
    root.virtual_keyboard.geometry("300x400")
    root.virtual_keyboard.resizable(False, False)

    keys = [
        '7', '8', '9', '+',
        '4', '5', '6', '-',
        '1', '2', '3', '*',
        '0', '.', '/', '=',
        'DEL', 'C', '(', ')'
    ]

    for i, key in enumerate(keys):
        if key == 'C':
            action = clear_entry
        elif key == 'DEL':
            action = delete_last_char
        elif key == '=':
            action = calculate_expression
        else:
            action = lambda x=key: insert_char(x)

        tk.Button(
            root.virtual_keyboard,
            text=key,
            command=action,
            width=5,
            height=2
        ).grid(row=i // 4, column=i % 4, pady=5, padx=5)


def insert_char(char):
    if focused_entry:
        focused_entry.insert(tk.END, char)


def clear_entry():
    if focused_entry:
        focused_entry.delete(0, tk.END)


def delete_last_char():
    if focused_entry:
        current_text = focused_entry.get()
        focused_entry.delete(0, tk.END)
        focused_entry.insert(0, current_text[:-1])


def calculate_expression():
    if focused_entry:
        expression = focused_entry.get()
        try:
            result = eval(expression)
            focused_entry.delete(0, tk.END)
            focused_entry.insert(0, str(result))
            add_to_history(f"{expression} = {result}")
        except Exception:
            messagebox.showerror("Lỗi", "Biểu thức không hợp lệ!")


def set_focused_entry(entry):
    global focused_entry
    focused_entry = entry


# Tạo cửa sổ chính
root = tk.Tk()
root.title("Máy Tính Nâng Cao")
root.configure(bg="#F0F8FF")

large_font = ("Comic Sans MS", 14)
button_font = ("Comic Sans MS", 12, "bold")

focused_entry = None  # Lưu ô nhập liệu hiện tại

# Giao diện phép toán cơ bản
frame_basic = tk.Frame(root, bg="#FFEB99", padx=10, pady=10)
frame_basic.pack(pady=10, fill=tk.X)

tk.Label(frame_basic, text="🔢 Phép Toán Cơ Bản", font=large_font, bg="#FFEB99").pack()

tk.Label(frame_basic, text="Nhập chuỗi phép tính (ví dụ: 3 + 3 + 3 - 2):", font=large_font, bg="#FFEB99").pack()
entry_expression = tk.Entry(frame_basic, font=large_font)
entry_expression.pack(pady=5)
entry_expression.bind("<FocusIn>", lambda e: set_focused_entry(entry_expression))

tk.Button(frame_basic, text="🎉 Tính Ngay", command=basic_operations, font=button_font, bg="#FFD700").pack(pady=10)

# Giao diện hằng đẳng thức
frame_identity = tk.Frame(root, bg="#FFCCCB", padx=10, pady=10)
frame_identity.pack(pady=10, fill=tk.X)

tk.Label(frame_identity, text="🔢 Hằng Đẳng Thức Đáng Nhớ", font=large_font, bg="#FFCCCB").pack()

tk.Label(frame_identity, text="Nhập giá trị a:", font=large_font, bg="#FFCCCB").pack()
entry_a = tk.Entry(frame_identity, font=large_font)
entry_a.pack(pady=5)
entry_a.bind("<FocusIn>", lambda e: set_focused_entry(entry_a))

tk.Label(frame_identity, text="Nhập giá trị b:", font=large_font, bg="#FFCCCB").pack()
entry_b = tk.Entry(frame_identity, font=large_font)
entry_b.pack(pady=5)
entry_b.bind("<FocusIn>", lambda e: set_focused_entry(entry_b))

identity_var = tk.StringVar(value='1')
frame_identity_operations = tk.Frame(frame_identity, bg="#FFCCCB")
frame_identity_operations.pack()

tk.Radiobutton(frame_identity_operations, text="(a + b)^2", variable=identity_var, value='1', font=large_font, bg="#FFCCCB").pack(side=tk.LEFT)
tk.Radiobutton(frame_identity_operations, text="(a - b)^2", variable=identity_var, value='2', font=large_font, bg="#FFCCCB").pack(side=tk.LEFT)
tk.Radiobutton(frame_identity_operations, text="a^2 - b^2", variable=identity_var, value='3', font=large_font, bg="#FFCCCB").pack(side=tk.LEFT)

tk.Button(frame_identity, text="✨ Tính Ngay", command=identity_operations, font=button_font, bg="#FF6F61").pack(pady=10)

# Lịch sử tính toán
frame_history = tk.Frame(root, bg="#E0FFFF", padx=10, pady=10)
frame_history.pack(pady=10, fill=tk.X)

tk.Label(frame_history, text="🕒 Lịch Sử Tính Toán", font=large_font, bg="#E0FFFF").pack()
history_text = tk.Text(frame_history, font=large_font, height=6, state=tk.DISABLED, wrap=tk.WORD, bg="#F0FFFF")
history_text.pack(pady=5)

# Nút bật/tắt bàn phím ảo
tk.Button(root, text="🖥️ Bật Bàn Phím Ảo", command=toggle_virtual_keyboard, font=button_font, bg="#90EE90").pack(pady=10)

root.mainloop()
