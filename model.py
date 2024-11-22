class ProductModel:
    def __init__(self, db_instance):
        """Khởi tạo với một instance của cơ sở dữ liệu."""
        self.db = db_instance

    def get_all_products(self):
        """Lấy tất cả sản phẩm từ bảng 'products'."""
        return self.db.load_data('products')
