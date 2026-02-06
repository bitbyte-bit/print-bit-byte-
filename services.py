"""
Zion Business Manager - Business Logic Layer
Service classes for complex business operations
"""

from typing import List, Dict, Optional
from decimal import Decimal
from database import db_manager
from models import Customer, Supplier, Category, Product, Order, OrderItem, Transaction


class CustomerService:
    """Service for customer operations"""
    
    @staticmethod
    def register_customer(name: str, email: str = "", phone: str = "", 
                          address: str = "") -> int:
        """Register a new customer"""
        return Customer.create(name, email, phone, address)
    
    @staticmethod
    def get_customer_with_orders(customer_id: int) -> Dict:
        """Get customer details with their order history"""
        customer = Customer.get_by_id(customer_id)
        if customer:
            orders = Order.get_by_status('all')
            customer['orders'] = [o for o in orders if o.get('customer_id') == customer_id]
        return customer
    
    @staticmethod
    def get_all_customers() -> List[Dict]:
        """Get all customers"""
        return Customer.get_all()
    
    @staticmethod
    def update_customer(customer_id: int, **kwargs) -> bool:
        """Update customer information"""
        return Customer.update(customer_id, **kwargs)
    
    @staticmethod
    def search_customers(query: str) -> List[Dict]:
        """Search customers"""
        return Customer.search(query)


class ProductService:
    """Service for product operations"""
    
    @staticmethod
    def add_product(name: str, sku: str, price: float, 
                    description: str = "", cost_price: float = 0,
                    quantity: int = 0, min_quantity: int = 0,
                    category_id: int = None, supplier_id: int = None) -> int:
        """Add a new product"""
        return Product.create(name, sku, price, description, cost_price,
                             quantity, min_quantity, category_id, supplier_id)
    
    @staticmethod
    def update_product(product_id: int, **kwargs) -> bool:
        """Update product information"""
        return Product.update(product_id, **kwargs)
    
    @staticmethod
    def adjust_stock(product_id: int, quantity_change: int) -> bool:
        """Adjust product stock level"""
        return Product.update_quantity(product_id, quantity_change)
    
    @staticmethod
    def get_low_stock_products() -> List[Dict]:
        """Get products that need restocking"""
        return Product.get_low_stock()
    
    @staticmethod
    def get_all_products() -> List[Dict]:
        """Get all products"""
        return Product.get_all()
    
    @staticmethod
    def search_products(query: str) -> List[Dict]:
        """Search products"""
        return Product.search(query)
    
    @staticmethod
    def get_product_by_id(product_id: int) -> Dict:
        """Get product details"""
        return Product.get_by_id(product_id)


class CategoryService:
    """Service for category operations"""
    
    @staticmethod
    def create_category(name: str, description: str = "") -> int:
        """Create a new category"""
        return Category.create(name, description)
    
    @staticmethod
    def get_all_categories() -> List[Dict]:
        """Get all categories"""
        return Category.get_all()
    
    @staticmethod
    def update_category(category_id: int, **kwargs) -> bool:
        """Update category"""
        return Category.update(category_id, **kwargs)


class SupplierService:
    """Service for supplier operations"""
    
    @staticmethod
    def create_supplier(name: str, email: str = "", phone: str = "",
                        address: str = "", contact_person: str = "") -> int:
        """Create a new supplier"""
        return Supplier.create(name, email, phone, address, contact_person)
    
    @staticmethod
    def get_all_suppliers() -> List[Dict]:
        """Get all suppliers"""
        return Supplier.get_all()
    
    @staticmethod
    def update_supplier(supplier_id: int, **kwargs) -> bool:
        """Update supplier information"""
        return Supplier.update(supplier_id, **kwargs)


class OrderService:
    """Service for order operations"""
    
    @staticmethod
    def create_order(customer_id: int = None, notes: str = "") -> int:
        """Create a new order"""
        return Order.create(customer_id, notes)
    
    @staticmethod
    def add_item_to_order(order_id: int, product_id: int, quantity: int) -> bool:
        """Add item to order"""
        product = Product.get_by_id(product_id)
        if not product:
            return False
        
        if product['quantity'] < quantity:
            return False
        
        unit_price = product['price']
        OrderItem.create(order_id, product_id, quantity, unit_price)
        
        # Update order total
        OrderService._update_order_total(order_id)
        return True
    
    @staticmethod
    def _update_order_total(order_id: int):
        """Update order total after adding/removing items"""
        with db_manager.cursor() as cursor:
            cursor.execute("""
                UPDATE orders SET total_amount = (
                    SELECT SUM(quantity * unit_price) FROM order_items
                    WHERE order_id = ?
                ), updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
            """, (order_id, order_id))
    
    @staticmethod
    def get_order_details(order_id: int) -> Dict:
        """Get complete order details"""
        return Order.get_order_details(order_id)
    
    @staticmethod
    def update_order_status(order_id: int, status: str) -> bool:
        """Update order status"""
        valid_statuses = ['pending', 'confirmed', 'processing', 'shipped', 'delivered', 'cancelled']
        if status not in valid_statuses:
            return False
        return Order.update(order_id, status=status)
    
    @staticmethod
    def get_orders_by_status(status: str) -> List[Dict]:
        """Get orders by status"""
        return Order.get_by_status(status)
    
    @staticmethod
    def get_all_orders() -> List[Dict]:
        """Get all orders"""
        return Order.get_all()
    
    @staticmethod
    def cancel_order(order_id: int) -> bool:
        """Cancel order and restore product quantities"""
        order = Order.get_by_id(order_id)
        if not order or order['status'] == 'cancelled':
            return False
        
        # Restore product quantities
        with db_manager.cursor() as cursor:
            cursor.execute("""
                SELECT product_id, quantity FROM order_items WHERE order_id = ?
            """, (order_id,))
            items = cursor.fetchall()
            
            for item in items:
                cursor.execute("""
                    UPDATE products SET quantity = quantity + ?,
                    updated_at = CURRENT_TIMESTAMP WHERE id = ?
                """, (item['quantity'], item['product_id']))
        
        return Order.update(order_id, status='cancelled')


class InventoryService:
    """Service for inventory management"""
    
    @staticmethod
    def get_stock_level(product_id: int) -> int:
        """Get current stock level for a product"""
        product = Product.get_by_id(product_id)
        return product['quantity'] if product else 0
    
    @staticmethod
    def restock_product(product_id: int, quantity: int) -> bool:
        """Restock a product"""
        return Product.update_quantity(product_id, quantity)
    
    @staticmethod
    def get_inventory_report() -> Dict:
        """Generate inventory report"""
        products = Product.get_all()
        
        total_items = sum(p['quantity'] for p in products)
        total_value = sum(p['quantity'] * p['price'] for p in products)
        low_stock = Product.get_low_stock()
        
        return {
            'total_products': len(products),
            'total_items': total_items,
            'total_inventory_value': total_value,
            'low_stock_count': len(low_stock),
            'low_stock_products': low_stock
        }
    
    @staticmethod
    def get_products_by_category(category_id: int) -> List[Dict]:
        """Get all products in a category"""
        with db_manager.cursor() as cursor:
            cursor.execute("""
                SELECT p.*, c.name as category_name
                FROM products p
                JOIN categories c ON p.category_id = c.id
                WHERE p.category_id = ?
            """, (category_id,))
            return [dict(row) for row in cursor.fetchall()]


class FinancialService:
    """Service for financial operations"""
    
    @staticmethod
    def record_transaction(transaction_type: str, order_id: int = None, 
                           amount: float = 0, payment_method: str = "", 
                           notes: str = "") -> int:
        """Record a financial transaction"""
        return Transaction.create(transaction_type, order_id, amount, 
                                  payment_method, notes)
    
    @staticmethod
    def get_financial_summary(start_date: str = None, end_date: str = None) -> Dict:
        """Get financial summary"""
        summary = Transaction.get_summary(start_date, end_date)
        
        # Calculate profit (if cost data available)
        with db_manager.cursor() as cursor:
            cursor.execute("""
                SELECT SUM(oi.quantity * p.cost_price) as total_cost
                FROM order_items oi
                JOIN products p ON oi.product_id = p.id
                JOIN orders o ON oi.order_id = o.id
                WHERE o.status != 'cancelled'
            """)
            result = cursor.fetchone()
            total_cost = result['total_cost'] if result else 0
        
        revenue = summary.get('payment', 0) + summary.get('sale', 0)
        profit = revenue - total_cost
        
        return {
            'revenue': revenue,
            'total_cost': total_cost,
            'profit': profit,
            'by_type': summary
        }
    
    @staticmethod
    def record_payment(order_id: int, amount: float, payment_method: str) -> int:
        """Record payment for an order"""
        return Transaction.create('payment', order_id, amount, payment_method, 
                                  f"Payment for order #{order_id}")


class DashboardService:
    """Service for dashboard statistics"""
    
    @staticmethod
    def get_dashboard_stats() -> Dict:
        """Get dashboard statistics"""
        customers = Customer.get_all()
        products = Product.get_all()
        orders = Order.get_all()
        low_stock = Product.get_low_stock()
        
        # Calculate metrics
        total_revenue = sum(o['total_amount'] for o in orders 
                          if o['status'] not in ['cancelled', 'pending'])
        pending_orders = sum(1 for o in orders if o['status'] == 'pending')
        
        # Orders by status
        orders_by_status = {}
        for o in orders:
            status = o['status']
            orders_by_status[status] = orders_by_status.get(status, 0) + 1
        
        return {
            'total_customers': len(customers),
            'total_products': len(products),
            'total_orders': len(orders),
            'total_revenue': total_revenue,
            'pending_orders': pending_orders,
            'low_stock_alerts': len(low_stock),
            'orders_by_status': orders_by_status,
            'recent_orders': orders[-5:] if orders else []
        }
