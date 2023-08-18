from datetime import datetime

from flask_sqlalchemy import SQLAlchemy
import json

database = SQLAlchemy()


product_category = database.Table('product_category',
                                  database.Column('pid', database.Integer, database.ForeignKey('product.id'),
                                                  primary_key=True),
                                  database.Column('cid', database.Integer, database.ForeignKey('category.id'),
                                                  primary_key=True)
                                  )


class Product(database.Model):
    __tablename__ = "product"
    id = database.Column(database.Integer, primary_key=True)
    name = database.Column(database.String(256), nullable=False, unique=True)
    price = database.Column(database.Float(), nullable=False)
    categories = database.relationship('Category', secondary=product_category, backref=database.backref('products'))
    orders = database.relationship("ProductOrder", back_populates="product")


class Category(database.Model):
    __tablename__ = "category"
    id = database.Column(database.Integer, primary_key=True)
    name = database.Column(database.String(256), nullable=False, unique=True)


    def __repr__(self):
        return self.name


class ProductOrder(database.Model):
    __tablename__ = "product_order"
    id = database.Column(database.Integer, primary_key=True)
    pid = database.Column(database.Integer, database.ForeignKey('product.id'), nullable=False)
    oid = database.Column(database.Integer, database.ForeignKey('order_stat.id'), nullable=False)
    quantity = database.Column(database.Integer, nullable=False)
    order = database.relationship("OrderStat", back_populates="products")
    product = database.relationship("Product", back_populates="orders")
    def to_dict(self):
        return {
                "categories": [cat.name for cat in self.product.categories],
                "name": self.product.name,
                "price": self.product.price,
                "quantity": self.quantity
            }

class OrderStat(database.Model):
    __tablename__ = "order_stat"
    id = database.Column(database.Integer, primary_key=True)
    price = database.Column(database.Float, nullable=False)
    status = database.Column(database.String(20), nullable=False)
    created = database.Column(database.DateTime, nullable=False)
    bemail = database.Column(database.String(256), nullable=False)
    products = database.relationship("ProductOrder", back_populates="order")
    address = database.Column(database.String(256))
    def to_dict(self):
        return {
            "products": [prod.to_dict() for prod in self.products],
            "price": self.price,
            "status": self.status,
            "timestamp": self.created.isoformat()+"Z"
        }


