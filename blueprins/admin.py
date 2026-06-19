from flask import Blueprint,render_template,request,redirect,session,abort,url_for
import config
from models.product import Product
from models.product_image import ProductImage
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
    product = Product.query.all()
    
    if request.method == 'GET':
        for p in product:
            primary = ProductImage.query.filter(
                ProductImage.product_id == p.id,
                ProductImage.is_primary == True
            ).first()
            p.primary_image = primary.image_path if primary else None
            
        return render_template('admin/products.html', product=product)
    else:
        name = request.form.get('name', None)
        description = request.form.get('description', None)  
        price = request.form.get('price', None)
        active = request.form.get('active', None)

        p = Product(name=name, description=description, price=price)  
        if active == None:
            p.active = 0
        else:
            p.active = 1
            
        db.session.add(p)
        db.session.commit()
        
        files = request.files.getlist('images')
        counter = 0
        for f in files:
            if f:
                filename = f"product_{p.id}_{counter}.jpg"
                f.save(f'static/cover/{filename}')
                
                img = ProductImage(
                    product_id=p.id,
                    image_path=filename,
                    is_primary=1 if counter == 0 else 0, 
                    sort_order=counter
                )
                db.session.add(img)
                counter = counter + 1
        
        if counter > 0:
            db.session.commit()        
        return redirect(url_for('admin.products'))

    
@app.route('/dashboard/edit-product/<id>', methods=["GET","POST"])
def edit_product(id):
    product = Product.query.filter(Product.id == id).first_or_404()
    if request.method == 'GET':
        images = ProductImage.query.filter(ProductImage.product_id == id).order_by(ProductImage.sort_order).all()
        return render_template('admin/edit-product.html', product=product, images=images)
    else:
        name = request.form.get('name', None)
        description = request.form.get('description', None)  
        price = request.form.get('price', None)
        active = request.form.get('active', None)
        file = request.files.get('cover', None)
        
        product.name = name
        product.description = description
        product.price = price
        if active == None:
            product.active = 0
        else:
            product.active = 1
            
        db.session.commit()
        
        files = request.files.getlist('images')
        counter = 0
        for f in files:
            if f:
                last_image = ProductImage.query.filter(ProductImage.product_id == product.id).order_by(ProductImage.sort_order.desc()).first()
                if last_image:
                    next_order = last_image.sort_order + 1
                else:
                    next_order = 0
                
                filename = f"product_{product.id}_{next_order}.jpg"
                f.save(f'static/cover/{filename}')
                
                img = ProductImage(
                    product_id=product.id,
                    image_path=filename,
                    is_primary=0,  
                    sort_order=next_order
                )
                db.session.add(img)
                counter = counter + 1
        
        if counter > 0:
            db.session.commit()
        
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
        
    
