from main import create_app, db
from models.product import get_product_model

app = create_app()
with app.app_context():
    Product = app.config['Product']
    
    # Check if products exist
    product_count = Product.query.count()
    print(f"Current product count: {product_count}")
    
    # Create a test product if none exist
    if product_count == 0:
        new_product = Product(
            name="Test Product",
            description="A test product for API testing",
            price=19.99,
            stock=100
        )
        db.session.add(new_product)
        db.session.commit()
        print(f"Created new product with ID: {new_product.id}")
    else:
        # List existing products
        products = Product.query.all()
        for product in products:
            print(f"Product ID: {product.id}, Name: {product.name}, Price: {product.price}")