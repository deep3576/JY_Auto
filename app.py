from flask import Flask, render_template, request, redirect, url_for, flash, send_file
from flask_sqlalchemy import SQLAlchemy
from weasyprint import HTML
from io import BytesIO
from datetime import datetime

# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///auto_shop.db'
# app.config['SECRET_KEY'] = 'your_secret_key'
# db = SQLAlchemy(app)
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///auto_shop.db'
app.config['SECRET_KEY'] = 'Gmsshn!43'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

with app.app_context():
    db.create_all()  # This creates the tables if they don't exist


# Define your Customer model
class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=False, nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    CarMake = db.Column(db.String(20), nullable=False)
    CarModel = db.Column(db.String(20), nullable=False)
    Vin = db.Column(db.String(120), nullable=False)
    Job = db.Column(db.String(240), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    Price = db.Column(db.Integer, nullable=False)
    Price1 = db.Column(db.Integer, nullable=True)
    Price2 = db.Column(db.Integer, nullable=True)
    Price3 = db.Column(db.Integer, nullable=True)
    Subtotal = db.Column(db.Integer, nullable=True)
    gst = db.Column(db.Integer, nullable=True)
    Total_Amount = db.Column(db.Integer, nullable=True)

    # Add other fields as needed

@app.route('/')
def home():
    return render_template('home.html')


@app.route('/customers', methods=['GET'])
def view_all_customers():
    customers = Customer.query.all()
    return render_template('view_customers.html', customers=customers)

@app.route('/add_customer', methods=['GET', 'POST'])
def add_customer():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        CarMake = request.form['CarMake']
        CarModel = request.form['CarModel']
        Vin = request.form['Vin']
        Job = request.form['Job']
        Price = request.form['Price']
        new_customer = Customer(name=name, email=email, phone=phone , CarMake=CarMake ,CarModel=CarModel,Vin=Vin ,Job=Job,Price=Price)
        
        try:
            db.session.add(new_customer)
            db.session.commit()
            flash('Customer added successfully!', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Error adding customer: {e}', 'error')
        
        return redirect(url_for('view_all_customers'))
    
    return render_template('add_customer.html')


@app.route('/customer/<int:id>', methods=['GET', 'POST'])
def update_customer(id):
    if id == 0:  # Adding a new customer
        customer = Customer()
    else:
        customer = Customer.query.get_or_404(id)
    
    if request.method == 'POST':
        customer.name = request.form['name']
        customer.email = request.form['email']
        customer.phone = request.form['phone']
        
        if id == 0:  # If adding a new customer
            db.session.add(customer)
        
        db.session.commit()
        flash('Customer saved successfully!', 'success')
        return redirect(url_for('view_all_customers'))
    

    return render_template('update_customer.html', customer=customer)

@app.route('/customer/delete/<int:id>', methods=['POST'])
def delete_customer(id):
    customer = Customer.query.get_or_404(id)
    db.session.delete(customer)
    db.session.commit()
    flash('Customer deleted successfully!', 'success')
    return redirect(url_for('view_all_customers'))

@app.route('/invoice/<int:id>')
def invoice(id):
    customer = Customer.query.get_or_404(id)
    customer.Subtotal = Calculate_Subtotal(customer.Price,customer.Price1,customer.Price2,customer.Price3)
    customer.gst=Calculate_gst(customer.Total_Amount)
    customer.Total_Amount = customer.Subtotal + customer.gst
    
    html = render_template('invoice.html', customer=customer)
    pdf = BytesIO()
    HTML(string=html).write_pdf(pdf)
    pdf.seek(0)
    return send_file(pdf, download_name='invoice.pdf', as_attachment=True)


def Calculate_gst(Total_Amount) :
    return Total_Amount * 13 / 100

def Calculate_Subtotal (Price,Price1,Price2,Price3):
    if (Price1 == null ):
        return Price
    if (Price2 == null ):
        return Price + Price1
    if (Price3 == null ):
        return Price + Price1 + Price2
    return Price + Price1 + Price2 + Price3


if __name__ == '__main__':
    db.create_all() 
    app.run(debug=False)

