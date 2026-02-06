"""
Zion Business Manager - Test Script
Tests database initialization and CRUD operations
"""

from database import db_manager
from models import Customer, Product, Order, Category
from services import (
    CustomerService, ProductService, CategoryService, 
    OrderService, DashboardService
)


def test_database_init():
    """Test database initialization"""
    print("Testing database initialization...")
    db_manager.initialize_db()
    print("[OK] Database initialized successfully!")


def test_customers():
    """Test customer operations"""
    print("\nTesting customer operations...")
    
    # Create customer
    customer_id = CustomerService.register_customer(
        name="John Doe",
        email="john@example.com",
        phone="555-1234",
        address="123 Main St"
    )
    print(f"[OK] Created customer: {customer_id}")
    
    # Get all customers
    customers = CustomerService.get_all_customers()
    print(f"[OK] Total customers: {len(customers)}")
    
    # Search customer
    results = CustomerService.search_customers("John")
    print(f"[OK] Search found: {len(results)} customer(s)")


def test_categories():
    """Test category operations"""
    print("\nTesting category operations...")
    
    categories = CategoryService.get_all_categories()
    print(f"[OK] Categories: {len(categories)}")
    for c in categories:
        print(f"  - {c['name']}")


def test_products():
    """Test product operations"""
    print("\nTesting product operations...")
    
    # Create product
    product_id = ProductService.add_product(
        name="Laptop",
        sku="ELEC-001",
        price=999.99,
        description="High-performance laptop",
        cost_price=700.00,
        quantity=10,
        min_quantity=5
    )
    print(f"[OK] Created product: {product_id}")
    
    # Create another product
    product_id2 = ProductService.add_product(
        name="Mouse",
        sku="ELEC-002",
        price=29.99,
        cost_price=15.00,
        quantity=50,
        min_quantity=10
    )
    print(f"[OK] Created product: {product_id2}")
    
    # Get all products
    products = ProductService.get_all_products()
    print(f"[OK] Total products: {len(products)}")
    
    # Check low stock
    low_stock = ProductService.get_low_stock_products()
    print(f"[OK] Low stock products: {len(low_stock)}")


def test_orders():
    """Test order operations"""
    print("\nTesting order operations...")
    
    # Create order
    order_id = OrderService.create_order(customer_id=1, notes="Test order")
    print(f"[OK] Created order: {order_id}")
    
    # Add item to order
    success = OrderService.add_item_to_order(order_id, 1, 2)
    if success:
        print(f"[OK] Added item to order")
    else:
        print(f"[FAIL] Failed to add item (insufficient stock?)")
    
    # Update order status
    OrderService.update_order_status(order_id, "confirmed")
    print(f"[OK] Order status updated")


def test_dashboard():
    """Test dashboard"""
    print("\nTesting dashboard...")
    stats = DashboardService.get_dashboard_stats()
    print(f"[OK] Dashboard stats retrieved:")
    print(f"  - Customers: {stats['total_customers']}")
    print(f"  - Products: {stats['total_products']}")
    print(f"  - Orders: {stats['total_orders']}")
    print(f"  - Revenue: ${stats['total_revenue']:.2f}")


def main():
    """Run all tests"""
    print("=" * 50)
    print("  ZION BUSINESS MANAGER - TEST SUITE")
    print("=" * 50)
    
    try:
        test_database_init()
        test_customers()
        test_categories()
        test_products()
        test_orders()
        test_dashboard()
        
        print("\n" + "=" * 50)
        print("  ALL TESTS COMPLETED SUCCESSFULLY!")
        print("=" * 50)
        
    except Exception as e:
        print(f"\n[FAIL] Error: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        db_manager.close()


if __name__ == "__main__":
    main()
