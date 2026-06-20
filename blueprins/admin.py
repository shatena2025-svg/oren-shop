from flask import Blueprint,render_template,request,redirect,session,abort,url_for,flash
import config
from models.product import Product
from models.product_image import ProductImage
from models.productcolor import ProductColor
from models.productsize import ProductSize
from models.cart import Cart
from extentions import db

app = Blueprint('admin',__name__ , url_prefix='/admin')

@app.before_request
def before_request():
    if session.get('admin_login',None) == None and request.endpoint != 'admin.login':
        abort(403)  


@app.route('/login',methods=["POST","GET"])
def login():
        if request.method == "POST":
            username = request.form.get('username',None)
            password = request.form.get('password',None)

            if username == config.ADMIN_USERNAME and password == config.ADMIN_PASSWORD :
                session['admin_login'] = username
                return redirect('/admin/dashboard')
            else :
                return redirect('/admin/login')
        else:
            return render_template('admin/login.html')

@app.route('/dashboard')
def dashboard():
    carts = Cart.query.filter(Cart.status != 'pending').all()
    return render_template('admin/dashboard.html', carts=carts) 

@app.route('/dashboard/order/<id>', methods=['GET','POST'])
def order(id):
    cart = Cart.query.filter(Cart.id == id).first_or_404()
    if request.method == 'GET':
        return render_template('admin/order.html', cart=cart) 
    else:
        status = request.form.get('status')
        cart.status = status
        db.session.commit()
        return redirect(url_for('admin.order',id=id))
        

@app.route('/dashboard/products', methods=["GET","POST"])
def products():
    if request.method == 'GET':
        products = Product.query.all()
        for p in products:
            primary = ProductImage.query.filter(
                ProductImage.product_id == p.id,
                ProductImage.is_primary == True
            ).first()
            p.primary_image = primary.image_path if primary else None
        return render_template('admin/products.html', product=products)
    
    name = request.form.get('name')
    short_description = request.form.get('short_description')
    description = request.form.get('description')
    price = request.form.get('price')
    active = request.form.get('active')
    gender = request.form.get('gender', 'unisex')
    category = request.form.get('category', 'لباس')
    
    if not name or not price:
        flash('نام و قیمت محصول الزامی است')
        return redirect(url_for('admin.products'))
    
    p = Product(
        name=name,
        short_description=short_description or '',
        description=description or '',
        price=int(price),
        gender=gender,
        category=category,
        active=1 if active else 0
    )
    db.session.add(p)
    db.session.commit()
    
    files = request.files.getlist('images')
    for counter, f in enumerate(files):
        if f and allowed_file(f.filename):
            filename = f"product_{p.id}_{counter}.jpg"
            f.save(f'static/cover/{filename}')
            img = ProductImage(
                product_id=p.id,
                image_path=filename,
                is_primary=1 if counter == 0 else 0,
                sort_order=counter
            )
            db.session.add(img)
    if files:
        db.session.commit()
    
    color_names = request.form.getlist('color_name[]')
    color_codes = request.form.getlist('color_code[]')
    stocks = request.form.getlist('stock[]')
    color_prices = request.form.getlist('color_price[]')
    
    for i, color_name in enumerate(color_names):
        if color_name.strip():
            color = ProductColor(
                product_id=p.id,
                color_name=color_name.strip(),
                color_code=color_codes[i] if i < len(color_codes) and color_codes[i] else None,
                stock=int(stocks[i]) if i < len(stocks) and stocks[i] else 0,
                price=int(color_prices[i]) if i < len(color_prices) and color_prices[i] else None,
                sort_order=i
            )
            db.session.add(color)
    if color_names:
        db.session.commit()
    
    sizes = request.form.getlist('sizes[]')
    for size_name in sizes:
        if size_name.strip():
            stock = request.form.get(f'stock_{size_name}', 0)
            price = request.form.get(f'price_{size_name}')
            product_size = ProductSize(
                product_id=p.id,
                size=size_name.strip(),
                stock=int(stock) if stock else 0,
                price=int(price) if price else None
            )
            db.session.add(product_size)
    if sizes:
        db.session.commit()
    
    flash('محصول با موفقیت اضافه شد')
    return redirect(url_for('admin.products'))


@app.route('/dashboard/edit-product/<id>', methods=["GET","POST"])
def edit_product(id):
    product = Product.query.filter(Product.id == id).first_or_404()
    
    if request.method == 'GET':
        images = ProductImage.query.filter(ProductImage.product_id == id).order_by(ProductImage.sort_order).all()
        return render_template('admin/edit-product.html', product=product, images=images)
    
    product.name = request.form.get('name')
    product.short_description = request.form.get('short_description')
    product.description = request.form.get('description')
    product.price = int(request.form.get('price'))
    product.gender = request.form.get('gender')
    product.category = request.form.get('category')
    product.active = 1 if request.form.get('active') else 0
    db.session.commit()

    color_ids = request.form.getlist('color_id[]')
    for color_id in color_ids:
        color = ProductColor.query.get(color_id)
        if color:
            color.color_name = request.form.get(f'color_name_{color_id}')
            color.color_code = request.form.get(f'color_code_{color_id}')
            color.stock = int(request.form.get(f'stock_{color_id}') or 0)
            color.price = int(request.form.get(f'color_price_{color_id}')) if request.form.get(f'color_price_{color_id}') else None
    db.session.commit()

    selected_sizes = request.form.getlist('sizes[]')
    size_list = ['S', 'M', 'L', 'XL', 'XXL', 'XXXL']
    
    for size in product.sizes:
        if size.size not in selected_sizes:
            db.session.delete(size)
    
    for size_name in size_list:
        if size_name in selected_sizes:
            existing = ProductSize.query.filter(
                ProductSize.product_id == product.id,
                ProductSize.size == size_name
            ).first()
            
            stock = request.form.get(f'stock_{size_name}', 0)
            price = request.form.get(f'price_{size_name}')
            
            if existing:
                existing.stock = int(stock) if stock else 0
                existing.price = int(price) if price else None
            else:
                product_size = ProductSize(
                    product_id=product.id,
                    size=size_name,
                    stock=int(stock) if stock else 0,
                    price=int(price) if price else None
                )
                db.session.add(product_size)
    
    db.session.commit()

    new_color_names = request.form.getlist('new_color_name[]')
    new_color_codes = request.form.getlist('new_color_code[]')
    new_stocks = request.form.getlist('new_stock[]')
    new_color_prices = request.form.getlist('new_color_price[]')

    for i, name in enumerate(new_color_names):
        if name.strip():
            color = ProductColor(
                product_id=product.id,
                color_name=name.strip(),
                color_code=new_color_codes[i] if i < len(new_color_codes) else None,
                stock=int(new_stocks[i]) if i < len(new_stocks) and new_stocks[i] else 0,
                price=int(new_color_prices[i]) if i < len(new_color_prices) and new_color_prices[i] else None
            )
            db.session.add(color)
    db.session.commit()

    files = request.files.getlist('images')
    for counter, f in enumerate(files):
        if f:
            last_image = ProductImage.query.filter(ProductImage.product_id == product.id).order_by(ProductImage.sort_order.desc()).first()
            next_order = (last_image.sort_order + 1) if last_image else 0
            filename = f"product_{product.id}_{next_order}.jpg"
            f.save(f'static/cover/{filename}')
            img = ProductImage(
                product_id=product.id,
                image_path=filename,
                is_primary=0,
                sort_order=next_order
            )
            db.session.add(img)
    db.session.commit()

    flash('تغییرات با موفقیت ذخیره شد')
    return redirect(url_for('admin.edit_product', id=id))
    
@app.route('/dashboard/delete-image/<id>', methods=['POST'])
def delete_image(id):
    image = ProductImage.query.get(id)
    if image:
        import os
        os.remove(f'static/cover/{image.image_path}')
        db.session.delete(image)
        db.session.commit()
    return redirect(request.referrer)


@app.route('/dashboard/set-primary/<id>', methods=['POST'])
def set_primary(id):
    image = ProductImage.query.get(id)
    if image:
        ProductImage.query.filter(ProductImage.product_id == image.product_id).update({ProductImage.is_primary: False})
        image.is_primary = True
        db.session.commit()
    return redirect(request.referrer)
        
    
