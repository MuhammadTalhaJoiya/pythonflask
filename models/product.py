def get_product_model(db):
    class Product(db.Model):
        __tablename__ = 'products'
        id = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.String(100), nullable=False)
        description = db.Column(db.Text)
        price = db.Column(db.Float, nullable=False)
        stock = db.Column(db.Integer, default=0)

    return Product

Product = None