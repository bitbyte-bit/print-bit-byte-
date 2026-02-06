"""
Zion Business Manager - Flask Web Application
"""

from flask import Flask, render_template, request, redirect, url_for, flash
from database import db_manager
from services import (
    CustomerService, ProductService, CategoryService,
    SupplierService, OrderService, InventoryService,
    FinancialService, DashboardService
)

app = Flask(__name__)
app.secret_key = 'zion_business_manager_secret_key'


@app.route('/')
def index():
    """Dashboard/Home page"""
    stats = DashboardService.get_dashboard_stats()
    return render_template('dashboard.html', stats=stats)


# ==================== CUSTOMERS ====================

@app.route('/customers')
def customers():
    """List all customers"""
    customers = CustomerService.get_all_customers()
    return render_template('customers.html', customers=customers)


@app.route('/customers/add', methods=['GET', 'POST'])
def add_customer():
    """Add new customer"""
    if request.method == 'POST':
        name = request.form['name']
        email = request.form.get('email', '')
        phone = request.form.get('phone', '')
        address = request.form.get('address', '')
        
        CustomerService.register_customer(name, email, phone, address)
        flash('Customer added successfully!', 'success')
        return redirect(url_for('customers'))
    
    return render_template('add_customer.html')


@app.route('/customers/search')
def search_customers():
    """Search customers"""
    query = request.args.get('q', '')
    customers = CustomerService.search_customers(query) if query else []
    return render_template('customers.html', customers=customers, search_query=query)


# ==================== PRODUCTS ====================

@app.route('/products')
def products():
    """List all products"""
    products = ProductService.get_all_products()
    return render_template('products.html', products=products)


@app.route('/products/add', methods=['GET', 'POST'])
def add_product():
    """Add new product"""
    categories = CategoryService.get_all_categories()
    suppliers = SupplierService.get_all_suppliers()
    
    if request.method == 'POST':
        name = request.form['name']
        sku = request.form['sku']
        price = float(request.form['price'])
        description = request.form.get('description', '')
        cost_price = float(request.form.get('cost_price', 0))
        quantity = int(request.form.get('quantity', 0))
        min_quantity = int(request.form.get('min_quantity', 0))
        category_id = request.form.get('category_id')
        supplier_id = request.form.get('supplier_id')
        
        ProductService.add_product(
            name, sku, price, description, cost_price,
            quantity, min_quantity,
            int(category_id) if category_id else None,
            int(supplier_id) if supplier_id else None
        )
        flash('Product added successfully!', 'success')
        return redirect(url_for('products'))
    
    return render_template('add_product.html', categories=categories, suppliers=suppliers)


@app.route('/products/low-stock')
def low_stock():
    """View low stock products"""
    products = ProductService.get_low_stock_products()
    return render_template('low_stock.html', products=products)


@app.route('/products/<int:product_id>/adjust-stock', methods=['GET', 'POST'])
def adjust_stock(product_id):
    """Adjust product stock"""
    product = ProductService.get_product_by_id(product_id)
    
    if request.method == 'POST':
        quantity_change = int(request.form['quantity_change'])
        ProductService.adjust_stock(product_id, quantity_change)
        flash('Stock adjusted successfully!', 'success')
        return redirect(url_for('products'))
    
    return render_template('adjust_stock.html', product=product)


# ==================== ORDERS ====================

@app.route('/orders')
def orders():
    """List all orders"""
    orders = OrderService.get_all_orders()
    return render_template('orders.html', orders=orders)


@app.route('/orders/create', methods=['GET', 'POST'])
def create_order():
    """Create new order"""
    customers = CustomerService.get_all_customers()
    
    if request.method == 'POST':
        customer_id = request.form.get('customer_id')
        notes = request.form.get('notes', '')
        
        order_id = OrderService.create_order(
            int(customer_id) if customer_id else None,
            notes
        )
        flash(f'Order #{order_id} created!', 'success')
        return redirect(url_for('add_order_item', order_id=order_id))
    
    return render_template('create_order.html', customers=customers)


@app.route('/orders/<int:order_id>')
def view_order(order_id):
    """View order details"""
    order = OrderService.get_order_details(order_id)
    return render_template('view_order.html', order=order)


@app.route('/orders/<int:order_id>/add-item', methods=['GET', 'POST'])
def add_order_item(order_id):
    """Add item to order"""
    products = ProductService.get_all_products()
    
    if request.method == 'POST':
        product_id = int(request.form['product_id'])
        quantity = int(request.form['quantity'])
        
        if OrderService.add_item_to_order(order_id, product_id, quantity):
            flash('Item added to order!', 'success')
        else:
            flash('Error: Insufficient stock!', 'error')
        
        return redirect(url_for('view_order', order_id=order_id))
    
    return render_template('add_order_item.html', order_id=order_id, products=products)


@app.route('/orders/<int:order_id>/update-status', methods=['POST'])
def update_order_status(order_id):
    """Update order status"""
    status = request.form['status']
    OrderService.update_order_status(order_id, status)
    flash('Order status updated!', 'success')
    return redirect(url_for('view_order', order_id=order_id))


@app.route('/orders/<int:order_id>/cancel')
def cancel_order(order_id):
    """Cancel order"""
    OrderService.cancel_order(order_id)
    flash('Order cancelled!', 'success')
    return redirect(url_for('orders'))


# ==================== CATEGORIES ====================

@app.route('/categories')
def categories():
    """List all categories"""
    categories = CategoryService.get_all_categories()
    return render_template('categories.html', categories=categories)


@app.route('/categories/add', methods=['GET', 'POST'])
def add_category():
    """Add new category"""
    if request.method == 'POST':
        name = request.form['name']
        description = request.form.get('description', '')
        CategoryService.create_category(name, description)
        flash('Category added!', 'success')
        return redirect(url_for('categories'))
    
    return render_template('add_category.html')


# ==================== SUPPLIERS ====================

@app.route('/suppliers')
def suppliers():
    """List all suppliers"""
    suppliers = SupplierService.get_all_suppliers()
    return render_template('suppliers.html', suppliers=suppliers)


@app.route('/suppliers/add', methods=['GET', 'POST'])
def add_supplier():
    """Add new supplier"""
    if request.method == 'POST':
        name = request.form['name']
        email = request.form.get('email', '')
        phone = request.form.get('phone', '')
        address = request.form.get('address', '')
        contact_person = request.form.get('contact_person', '')
        
        SupplierService.create_supplier(name, email, phone, address, contact_person)
        flash('Supplier added!', 'success')
        return redirect(url_for('suppliers'))
    
    return render_template('add_supplier.html')


# ==================== REPORTS ====================

@app.route('/inventory-report')
def inventory_report():
    """Inventory report"""
    report = InventoryService.get_inventory_report()
    return render_template('inventory_report.html', report=report)


@app.route('/financial-report')
def financial_report():
    """Financial report"""
    summary = FinancialService.get_financial_summary()
    return render_template('financial_report.html', summary=summary)


# ==================== INIT ====================

def init_db():
    """Initialize database on startup"""
    db_manager.initialize_db()


if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='0.0.0.0', port=5000)
