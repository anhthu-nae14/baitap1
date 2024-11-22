import tkinter as tk
from tkinter import ttk, messagebox
import csv
from database import DatabaseApp

class AppGUI:
    def __init__(self, root):
        """Khởi tạo giao diện và liên kết với cơ sở dữ liệu."""
        self.root = root
        self.root.title("Quản lý sản phẩm")

        # Khởi tạo đối tượng DatabaseApp
        self.db_app = DatabaseApp()
        self.table_name = "products"
        self.current_page = 1  # Trang hiện tại
        self.page_size = 10    # Số sản phẩm mỗi trang

        # Tạo các thành phần giao diện
        self.create_widgets()

    def create_widgets(self):
        """Tạo giao diện chính."""
        # Khu vực kết nối cơ sở dữ liệu
        connection_frame = tk.Frame(self.root)
        connection_frame.pack(pady=10)

        tk.Button(connection_frame, text="Kết nối cơ sở dữ liệu", command=self.connect_to_db).grid(row=0, column=0, padx=5, pady=5)

        # Khu vực tìm kiếm nâng cao
        search_frame = tk.Frame(self.root)
        search_frame.pack(pady=10)

        # Tìm kiếm theo từ khóa
        tk.Label(search_frame, text="Tìm kiếm:").grid(row=0, column=0, padx=5)
        self.search_text = tk.StringVar()
        tk.Entry(search_frame, textvariable=self.search_text).grid(row=0, column=1, padx=5)

        # Tìm kiếm theo khoảng giá
        tk.Label(search_frame, text="Giá từ:").grid(row=1, column=0, padx=5)
        self.price_min = tk.StringVar()
        tk.Entry(search_frame, textvariable=self.price_min, width=10).grid(row=1, column=1, padx=5)

        tk.Label(search_frame, text="đến:").grid(row=1, column=2, padx=5)
        self.price_max = tk.StringVar()
        tk.Entry(search_frame, textvariable=self.price_max, width=10).grid(row=1, column=3, padx=5)

        # Tìm kiếm theo thời gian
        tk.Label(search_frame, text="Ngày tạo từ:").grid(row=2, column=0, padx=5)
        self.date_start = tk.StringVar()
        tk.Entry(search_frame, textvariable=self.date_start, width=15).grid(row=2, column=1, padx=5)

        tk.Label(search_frame, text="đến:").grid(row=2, column=2, padx=5)
        self.date_end = tk.StringVar()
        tk.Entry(search_frame, textvariable=self.date_end, width=15).grid(row=2, column=3, padx=5)

        # Nút tìm kiếm
        tk.Button(search_frame, text="Tìm", command=self.search_products).grid(row=3, column=1, pady=5)
        tk.Button(search_frame, text="Tải lại", command=self.load_data).grid(row=3, column=2, pady=5)

        # Khu vực hiển thị dữ liệu
        data_frame = tk.Frame(self.root)
        data_frame.pack(pady=10)

        columns = ("id", "name", "description", "price", "stock_quantity", "created_at")
        self.tree = ttk.Treeview(data_frame, columns=columns, show="headings")
        for col in columns:
            self.tree.heading(col, text=col.capitalize())
            self.tree.column(col, width=150 if col == "description" else 100)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = tk.Scrollbar(data_frame, orient="vertical", command=self.tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill="y")
        self.tree.configure(yscroll=scrollbar.set)

        # Khu vực hành động
        action_frame = tk.Frame(self.root)
        action_frame.pack(pady=10)

        tk.Button(action_frame, text="Thêm sản phẩm", command=self.insert_product).grid(row=0, column=0, padx=5)
        tk.Button(action_frame, text="Chỉnh sửa sản phẩm", command=self.edit_product).grid(row=0, column=1, padx=5)
        tk.Button(action_frame, text="Xóa sản phẩm", command=self.delete_product).grid(row=0, column=2, padx=5)
        tk.Button(action_frame, text="Xuất CSV", command=self.export_to_csv).grid(row=0, column=3, padx=5)
        tk.Button(action_frame, text="Xem Log", command=self.view_logs).grid(row=0, column=4, padx=5)

        # Khu vực phân trang
        pagination_frame = tk.Frame(self.root)
        pagination_frame.pack(pady=5)

        tk.Button(pagination_frame, text="Trang trước", command=self.previous_page).pack(side=tk.LEFT, padx=5)
        tk.Button(pagination_frame, text="Trang sau", command=self.next_page).pack(side=tk.LEFT, padx=5)
        
        connection_frame = tk.Frame(self.root)
        connection_frame.pack(pady=10)

        tk.Button(connection_frame, text="Kết nối cơ sở dữ liệu", command=self.connect_to_db).grid(row=0, column=0, padx=5, pady=5)

        

    def connect_to_db(self):
        """Kết nối cơ sở dữ liệu và tải dữ liệu."""
        try:
            self.db_app.connect_db()
            messagebox.showinfo("Thành công", "Kết nối cơ sở dữ liệu thành công!")
            self.load_data()
        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi kết nối cơ sở dữ liệu: {e}")

    def load_data(self):
        """Tải dữ liệu từ cơ sở dữ liệu theo phân trang."""
        try:
            self.tree.delete(*self.tree.get_children())
            offset = (self.current_page - 1) * self.page_size
            query = f"""
            SELECT id, name, description, price, stock_quantity, created_at
            FROM {self.table_name}
            LIMIT {self.page_size} OFFSET {offset}
            """
            self.db_app.cur.execute(query)
            rows = self.db_app.cur.fetchall()
            for row in rows:
                self.tree.insert("", "end", values=row)
        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi khi tải dữ liệu: {e}")

    def search_products(self):
        """Tìm kiếm sản phẩm theo từ khóa, giá, và ngày tạo."""
        search_text = self.search_text.get().lower()
        price_min = self.price_min.get()
        price_max = self.price_max.get()
        date_start = self.date_start.get()
        date_end = self.date_end.get()

        # Xây dựng câu truy vấn động
        conditions = []
        params = []

        if search_text:
            conditions.append("(LOWER(name) LIKE %s OR LOWER(description) LIKE %s)")
            params.extend([f"%{search_text}%", f"%{search_text}%"])
        if price_min:
            conditions.append("price >= %s")
            params.append(price_min)
        if price_max:
            conditions.append("price <= %s")
            params.append(price_max)
        if date_start:
            conditions.append("created_at >= %s")
            params.append(date_start)
        if date_end:
            conditions.append("created_at <= %s")
            params.append(date_end)

        where_clause = " AND ".join(conditions)
        query = f"""
        SELECT id, name, description, price, stock_quantity, created_at
        FROM {self.table_name}
        """
        if where_clause:
            query += f" WHERE {where_clause}"

        try:
            self.tree.delete(*self.tree.get_children())
            self.db_app.cur.execute(query, params)
            rows = self.db_app.cur.fetchall()
            for row in rows:
                self.tree.insert("", "end", values=row)
        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi khi tìm kiếm sản phẩm: {e}")
            
        

    def insert_product(self):
        """Thêm sản phẩm mới."""
        def save_product():
            name = name_var.get()
            description = desc_var.get()
            try:
                price = float(price_var.get())
                quantity = int(quantity_var.get())
            except ValueError:
                messagebox.showerror("Lỗi", "Giá và số lượng phải là số hợp lệ!")
                return

            if not name or not description:
                messagebox.showerror("Lỗi", "Tên và mô tả không được để trống!")
                return

            try:
                self.db_app.insert_product(self.table_name, (name, description, price, quantity))
                messagebox.showinfo("Thành công", "Thêm sản phẩm thành công!")
                popup.destroy()
                self.load_data()
            except Exception as e:
                messagebox.showerror("Lỗi", f"Lỗi khi thêm sản phẩm: {e}")

        popup = tk.Toplevel(self.root)
        popup.title("Thêm sản phẩm mới")

        name_var = tk.StringVar()
        desc_var = tk.StringVar()
        price_var = tk.StringVar()
        quantity_var = tk.StringVar()

        tk.Label(popup, text="Tên sản phẩm:").grid(row=0, column=0, padx=5, pady=5)
        tk.Entry(popup, textvariable=name_var).grid(row=0, column=1, padx=5, pady=5)

        tk.Label(popup, text="Mô tả:").grid(row=1, column=0, padx=5, pady=5)
        tk.Entry(popup, textvariable=desc_var).grid(row=1, column=1, padx=5, pady=5)

        tk.Label(popup, text="Giá:").grid(row=2, column=0, padx=5, pady=5)
        tk.Entry(popup, textvariable=price_var).grid(row=2, column=1, padx=5, pady=5)

        tk.Label(popup, text="Số lượng:").grid(row=3, column=0, padx=5, pady=5)
        tk.Entry(popup, textvariable=quantity_var).grid(row=3, column=1, padx=5, pady=5)

        tk.Button(popup, text="Lưu", command=save_product).grid(row=4, columnspan=2, pady=10)

    def edit_product(self):
        """Chỉnh sửa sản phẩm được chọn."""
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn sản phẩm để chỉnh sửa!")
            return

        values = self.tree.item(selected_item)["values"]
        product_id = values[0]
        name, description, price, stock_quantity = values[1:5]

        def save_changes():
            new_name = name_var.get()
            new_desc = desc_var.get()
            try:
                new_price = float(price_var.get())
                new_quantity = int(quantity_var.get())
            except ValueError:
                messagebox.showerror("Lỗi", "Giá và số lượng phải là số hợp lệ!")
                return

            if not new_name or not new_desc:
                messagebox.showerror("Lỗi", "Tên và mô tả không được để trống!")
                return

            try:
                self.db_app.update_product(self.table_name, (new_name, new_desc, new_price, new_quantity), product_id)
                messagebox.showinfo("Thành công", "Chỉnh sửa sản phẩm thành công!")
                popup.destroy()
                self.load_data()
            except Exception as e:
                                messagebox.showerror("Lỗi", f"Lỗi khi chỉnh sửa sản phẩm: {e}")

        popup = tk.Toplevel(self.root)
        popup.title("Chỉnh sửa sản phẩm")

        name_var = tk.StringVar(value=name)
        desc_var = tk.StringVar(value=description)
        price_var = tk.StringVar(value=price)
        quantity_var = tk.StringVar(value=stock_quantity)

        tk.Label(popup, text="Tên sản phẩm:").grid(row=0, column=0, padx=5, pady=5)
        tk.Entry(popup, textvariable=name_var).grid(row=0, column=1, padx=5, pady=5)

        tk.Label(popup, text="Mô tả:").grid(row=1, column=0, padx=5, pady=5)
        tk.Entry(popup, textvariable=desc_var).grid(row=1, column=1, padx=5, pady=5)

        tk.Label(popup, text="Giá:").grid(row=2, column=0, padx=5, pady=5)
        tk.Entry(popup, textvariable=price_var).grid(row=2, column=1, padx=5, pady=5)

        tk.Label(popup, text="Số lượng:").grid(row=3, column=0, padx=5, pady=5)
        tk.Entry(popup, textvariable=quantity_var).grid(row=3, column=1, padx=5, pady=5)

        tk.Button(popup, text="Lưu", command=save_changes).grid(row=4, columnspan=2, pady=10)

    def delete_product(self):
        """Xóa sản phẩm được chọn."""
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn sản phẩm để xóa!")
            return

        confirm = messagebox.askyesno("Xác nhận", "Bạn có chắc chắn muốn xóa sản phẩm này?")
        if not confirm:
            return

        values = self.tree.item(selected_item)["values"]
        product_id = values[0]
        try:
            self.db_app.delete_product(self.table_name, product_id)
            messagebox.showinfo("Thành công", "Xóa sản phẩm thành công!")
            self.load_data()
        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi khi xóa sản phẩm: {e}")

    def export_to_csv(self):
        """Xuất dữ liệu ra file CSV."""
        try:
            with open("products_export.csv", "w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(["ID", "Name", "Description", "Price", "Stock Quantity", "Created At"])
                for row in self.tree.get_children():
                    writer.writerow(self.tree.item(row)["values"])
            messagebox.showinfo("Thành công", "Dữ liệu đã được xuất ra file 'products_export.csv'!")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi khi xuất dữ liệu: {e}")

    def view_logs(self):
        """Hiển thị log hành động."""
        try:
            # Xóa dữ liệu cũ
            self.tree.delete(*self.tree.get_children())
        
            # Cập nhật cột hiển thị log
            self.tree["columns"] = ("id", "action_type", "product_id", "product_name", "timestamp", "details")
            for col in self.tree["columns"]:
                self.tree.heading(col, text=col.replace("_", " ").capitalize())
                self.tree.column(col, width=150 if col == "details" else 100)

            # Truy vấn log
            query = "SELECT id, action_type, product_id, product_name, timestamp, details FROM audit_log ORDER BY timestamp DESC"
            self.db_app.cur.execute(query)
            logs = self.db_app.cur.fetchall()

            # Hiển thị log trong Treeview
            for log in logs:
                self.tree.insert("", "end", values=log)
        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi khi tải log: {e}")


    def next_page(self):
        """Chuyển đến trang tiếp theo."""
        self.current_page += 1
        self.load_data()

    def previous_page(self):
        """Quay lại trang trước."""
        if self.current_page > 1:
            self.current_page -= 1
            self.load_data()

    def on_closing(self):
        """Đóng ứng dụng và kết nối cơ sở dữ liệu."""
        if self.db_app:
            self.db_app.close_db()
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = AppGUI(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()

