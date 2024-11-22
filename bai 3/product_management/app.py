from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config
from models import db, Product, Category, User, Order, OrderItem, ProductReview, Cart, CartItem
from werkzeug.security import generate_password_hash, check_password_hash
from flask import session
from functools import wraps

app = Flask(__name__)
app.config.from_object(Config)

# Khởi tạo database và migrate
db.init_app(app)
migrate = Migrate(app, db)

@app.route('/')
def index():
    products = Product.query.all()
    return render_template('index.html', products=products)

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Kiểm tra nếu người dùng không phải admin
        if session.get('role') != 'admin':  # Session lưu thông tin `role`
            flash('You do not have permission to access this page.', 'danger')
            return redirect(url_for('index'))  # Chuyển hướng về trang chủ
        return f(*args, **kwargs)
    return decorated_function

@app.route('/admin/products', methods=['GET', 'POST'])
@admin_required
def admin_products():
    if request.method == 'POST':
        # Xử lý thêm sản phẩm
        name = request.form['name']
        description = request.form['description']
        price = request.form['price']
        stock = request.form['stock']
        category_id = request.form['category_id']

        # Tạo sản phẩm mới
        new_product = Product(name=name, description=description, price=price, stock=stock, category_id=category_id)
        db.session.add(new_product)
        db.session.commit()
        flash('Product added successfully!', 'success')
        return redirect(url_for('admin_products'))

    # Lấy danh sách sản phẩm và danh mục
    products = Product.query.all()
    categories = Category.query.all()  # Đảm bảo query này trả về danh mục
    return render_template('admin_products.html', products=products, categories=categories)


@app.route('/products/create', methods=['GET', 'POST'])
def create_product():
    categories = Category.query.all()
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        price = request.form['price']
        stock = request.form['stock']
        category_id = request.form['category_id']
        image_url = request.form['image_url']  # Lấy URL hình ảnh từ form

        # Tạo đối tượng sản phẩm mới với URL hình ảnh
        product = Product(name=name, description=description, price=price, stock=stock, category_id=category_id, image_url=image_url)
        db.session.add(product)
        db.session.commit()
        flash('Product created successfully!', 'success')
        return redirect(url_for('index'))
    return render_template('create_product.html', categories=categories)


# Hiển thị danh mục sản phẩm
@app.route('/categories/<int:category_id>')
def category_products(category_id):
    category = Category.query.get_or_404(category_id)
    products = Product.query.filter_by(category_id=category_id).all()
    return render_template('category_products.html', category=category, products=products)

# Chi tiết sản phẩm
@app.route('/product/<int:product_id>')
def product_detail(product_id):
    product = Product.query.get_or_404(product_id)
    return render_template('product_detail.html', product=product)


# Xử lý giỏ hàng
@app.route('/cart')
def cart():
    user_id = session.get('user_id')
    if not user_id:
        flash('Please log in to view your cart.', 'warning')
        return redirect(url_for('login'))

    cart = Cart.query.filter_by(user_id=user_id).first()
    if not cart:
        cart_items = []
        total_price = 0
    else:
        cart_items = cart.items
        total_price = sum(item.quantity * item.product.price for item in cart_items)

    return render_template('cart.html', cart_items=cart_items, total_price=total_price)

@app.route('/cart/add/<int:product_id>', methods=['POST'])
def add_to_cart(product_id):
    user_id = session.get('user_id')
    if not user_id:
        flash('Please log in to add items to your cart.', 'warning')
        return redirect(url_for('login'))

    cart = Cart.query.filter_by(user_id=user_id).first()
    if not cart:
        cart = Cart(user_id=user_id)
        db.session.add(cart)
        db.session.commit()

    cart_item = CartItem.query.filter_by(cart_id=cart.id, product_id=product_id).first()
    if cart_item:
        cart_item.quantity += 1
    else:
        cart_item = CartItem(cart_id=cart.id, product_id=product_id, quantity=1)
        db.session.add(cart_item)

    db.session.commit()
    flash('Added to cart!', 'success')
    return redirect(url_for('cart'))


@app.route('/cart/remove/<int:cart_item_id>', methods=['POST'])
def remove_from_cart(cart_item_id):
    cart_item = CartItem.query.get_or_404(cart_item_id)
    db.session.delete(cart_item)
    db.session.commit()
    flash('Removed from cart!', 'success')
    return redirect(url_for('cart'))

@app.route('/cart/update/<int:cart_item_id>', methods=['POST'])
def update_cart(cart_item_id):
    quantity = int(request.form.get('quantity'))
    if quantity < 0:
        quantity = 0
    elif quantity > 10:
        quantity = 10
    
    cart_item = CartItem.query.get_or_404(cart_item_id)
    cart_item.quantity = quantity
    db.session.commit()
    flash('Cart updated!', 'success')
    return redirect(url_for('cart'))



@app.route('/checkout')
def checkout():
    # Xử lý thanh toán (có thể thêm logic thanh toán tại đây)
    session['cart'] = []  # Làm trống giỏ hàng sau khi thanh toán
    flash('Thanh toán thành công!', 'success')
    return redirect(url_for('index'))

@app.route('/admin/products/edit/<int:id>', methods=['GET', 'POST'])
@admin_required
def edit_product(id):
    product = Product.query.get_or_404(id)
    categories = Category.query.all()
    if request.method == 'POST':
        product.name = request.form['name']
        product.description = request.form['description']
        product.price = request.form['price']
        product.stock = request.form['stock']
        product.category_id = request.form['category_id']
        product.image_url = request.form['image_url']  # Cập nhật URL hình ảnh
        db.session.commit()
        flash('Product updated successfully!', 'success')
        return redirect(url_for('admin_products'))
    return render_template('edit_product.html', product=product, categories=categories)


@app.route('/categories', methods=['GET', 'POST'])
def categories():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        category = Category(name=name, description=description)
        db.session.add(category)
        db.session.commit()
        flash('Category added successfully!', 'success')
        return redirect(url_for('categories'))
    categories = Category.query.all()
    return render_template('categories.html', categories=categories)

@app.context_processor
def inject_categories():
    categories = Category.query.all()  # Lấy tất cả danh mục từ database
    return {'categories': categories}  # Truyền vào context


@app.route('/admin/products/delete/<int:id>', methods=['POST'])
@admin_required
def delete_product(id):
    product = Product.query.get_or_404(id)
    db.session.delete(product)
    db.session.commit()
    flash('Product deleted successfully!', 'danger')
    return redirect(url_for('admin_products'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        # Mặc định role là "customer"
        role = "customer"

        # Mã hóa mật khẩu
        hashed_password = generate_password_hash(password)
        # Tạo người dùng mới
        new_user = User(username=username, email=email, password=hashed_password, role=role)
        db.session.add(new_user)
        db.session.commit()

        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        # Kiểm tra người dùng
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            session['role'] = user.role
            session['username'] = user.username
            flash('Login successful!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid email or password', 'danger')
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out!', 'success')
    return redirect(url_for('login'))

# Trang khuyến mãi
@app.route('/promotions')
def promotions():
    return render_template('promotions.html')

# Trang giới thiệu
@app.route('/about')
def about():
    return render_template('about.html')

# Tìm kiếm sản phẩm
@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query', '')
    products = Product.query.filter(Product.name.ilike(f'%{query}%')).all()
    return render_template('search_results.html', products=products, query=query)

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('role') != 'admin':
            flash('You do not have permission to access this page.', 'danger')
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function

if __name__ == '__main__':
    app.run(debug=True)