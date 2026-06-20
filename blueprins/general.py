from flask import Blueprint, render_template
from models.product import Product
from models.product_image import ProductImage 
from models.productcolor import ProductColor
from models.productsize import ProductSize

app = Blueprint('general', __name__)

@app.route('/')
def main(): 
    products = Product.query.filter(Product.active == 1).all()
    return render_template('main.html', products=products)

@app.route('/product/<id>/<name>')
def product_detail(id, name):
    product = Product.query.get(id)
    if not product:
        return "محصول یافت نشد", 404
    
    primary_image = ProductImage.query.filter(
        ProductImage.product_id == id,
        ProductImage.is_primary == True
    ).first()
    
    if not primary_image:
        primary_image = ProductImage.query.filter(
            ProductImage.product_id == id
        ).order_by(ProductImage.sort_order).first()
    
    product.primary_image = primary_image.image_path if primary_image else None
    
    return render_template('product.html', product=product)

@app.route('/about')
def about():
    return render_template('about.html')