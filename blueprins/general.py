from flask import Blueprint, render_template, session
from models.product import Product
from models.product_image import ProductImage 
from models.productcolor import ProductColor
from models.productsize import ProductSize
from extentions import db

app = Blueprint('general', __name__)

@app.route('/')
def main(): 
    products = Product.query.filter(Product.active == 1).all()
    popular_products = Product.query.filter(Product.active == 1).order_by(Product.view_count.desc()).limit(10).all()
    
    for p in products:
        primary = ProductImage.query.filter(
            ProductImage.product_id == p.id,
            ProductImage.is_primary == True
        ).first()
        if not primary:
            primary = ProductImage.query.filter(
                ProductImage.product_id == p.id
            ).order_by(ProductImage.sort_order).first()
        p.primary_image = primary.image_path if primary else None
    
    for p in popular_products:
        primary = ProductImage.query.filter(
            ProductImage.product_id == p.id,
            ProductImage.is_primary == True
        ).first()
        if not primary:
            primary = ProductImage.query.filter(
                ProductImage.product_id == p.id
            ).order_by(ProductImage.sort_order).first()
        p.primary_image = primary.image_path if primary else None
        
    return render_template('main.html', products=products, popular_products=popular_products)

@app.route('/product/<id>/<name>')
def product_detail(id, name):
    product = Product.query.get(id)
    if not product:
        return "محصول یافت نشد", 404
    
    viewed_products = session.get('viewed_products', [])
    if str(id) not in viewed_products:
        product.view_count += 1
        db.session.commit()
        viewed_products.append(str(id))
        session['viewed_products'] = viewed_products
    
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