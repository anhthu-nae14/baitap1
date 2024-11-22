import psycopg2
from psycopg2 import sql
from dotenv import load_dotenv
import os

# Load các biến môi trường từ file .env
load_dotenv()

class DatabaseApp:
    def __init__(self):
        """Khởi tạo kết nối cơ sở dữ liệu từ biến môi trường."""
        self.conn = None
        self.cur = None
        self.db_name = os.getenv('DB_NAME')  # Lấy từ file .env
        self.user = os.getenv('DB_USER')
        self.password = os.getenv('DB_PASSWORD')
        self.host = os.getenv('DB_HOST', 'localhost')  
        self.port = os.getenv('DB_PORT', '5432') 

    def connect_db(self):
        """Kết nối cơ sở dữ liệu."""
        try:
            self.conn = psycopg2.connect(
                dbname=self.db_name,
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port
            )
            self.cur = self.conn.cursor()
            print("Connected to the database successfully!")
        except Exception as e:
            print(f"Error connecting to the database: {e}")

    def load_data(self, table_name):
        """Tải dữ liệu từ bảng chỉ định."""
        try:
            query = sql.SQL(
                "SELECT id, name, description, price, stock_quantity, created_at FROM {}"
            ).format(sql.Identifier(table_name))
            self.cur.execute(query)
            rows = self.cur.fetchall()
            return rows
        except Exception as e:
            print(f"Error loading data: {e}")
            return None

    def insert_product(self, table_name, product_data):
        """Thêm sản phẩm vào cơ sở dữ liệu."""
        try:
            insert_query = sql.SQL(
                "INSERT INTO {} (name, description, price, stock_quantity) VALUES (%s, %s, %s, %s)"
            ).format(sql.Identifier(table_name))
            self.cur.execute(insert_query, product_data)
            self.conn.commit()

            # Ghi log
            product_name = product_data[0]
            self.log_action(
                "ADD",
                product_name=product_name,
                details=f"Added product: {product_name}"
            )
            print("Product inserted successfully!")
        except Exception as e:
            print(f"Error inserting product: {e}")

    def update_product(self, table_name, product_data, product_id):
        """Cập nhật thông tin sản phẩm."""
        try:
            # Lấy dữ liệu cũ trước khi cập nhật
            query = sql.SQL("SELECT name, description, price, stock_quantity FROM {} WHERE id = %s").format(sql.Identifier(table_name))
            self.cur.execute(query, (product_id,))
            old_data = self.cur.fetchone()

            # Thực hiện cập nhật
            update_query = sql.SQL(
                "UPDATE {} SET name = %s, description = %s, price = %s, stock_quantity = %s WHERE id = %s"
            ).format(sql.Identifier(table_name))
            self.cur.execute(update_query, product_data + (product_id,))
            self.conn.commit()

            # So sánh dữ liệu mới và cũ để ghi log
            changes = []
            fields = ["name", "description", "price", "stock_quantity"]
            for i, field in enumerate(fields):
                if old_data[i] != product_data[i]:
                    changes.append(f"{field}: '{old_data[i]}' -> '{product_data[i]}'")

            # Ghi log với chi tiết các thay đổi
            product_name = product_data[0]
            details = "; ".join(changes) if changes else "No changes detected"
            self.log_action(
                "EDIT",
                product_id=product_id,
                product_name=product_name,
                details=f"Updated product: {product_name}; Changes: {details}"
            )
            print("Product updated successfully!")
        except Exception as e:
            print(f"Error updating product: {e}")

    def delete_product(self, table_name, product_id):
        """Xóa sản phẩm từ cơ sở dữ liệu."""
        try:
            # Lấy thông tin sản phẩm trước khi xóa để log
            query = sql.SQL("SELECT name FROM {} WHERE id = %s").format(sql.Identifier(table_name))
            self.cur.execute(query, (product_id,))
            product_name = self.cur.fetchone()[0]

            delete_query = sql.SQL(
                "DELETE FROM {} WHERE id = %s"
            ).format(sql.Identifier(table_name))
            self.cur.execute(delete_query, (product_id,))
            self.conn.commit()

            # Ghi log
            self.log_action(
                "DELETE",
                product_id=product_id,
                product_name=product_name,
                details=f"Deleted product: {product_name}"
            )
            print("Product deleted successfully!")
        except Exception as e:
            print(f"Error deleting product: {e}")

    def log_action(self, action_type, product_id=None, product_name=None, details=None):
        """Ghi lại hành động vào bảng audit_log."""
        try:
            log_query = """
            INSERT INTO audit_log (action_type, product_id, product_name, details)
            VALUES (%s, %s, %s, %s)
            """
            self.cur.execute(log_query, (action_type, product_id, product_name, details))
            self.conn.commit()
            print(f"Logged action: {action_type} for product_id={product_id} with details: {details}")
        except Exception as e:
            print(f"Error logging action: {e}")

    def close_db(self):
        """Đóng kết nối cơ sở dữ liệu."""
        if self.cur:
            self.cur.close()
        if self.conn:
            self.conn.close()
            print("Database connection closed.")

if __name__ == "__main__":
    db_app = DatabaseApp()
    db_app.connect_db()
    data = db_app.load_data("products")
    print(data)
    db_app.close_db()
