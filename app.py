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
    last_updated = db.Column(db.DateTime , nullable= True )
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
        Price1 = request.form['Price1']
        new_customer = Customer(name=name, email=email, phone=phone , CarMake=CarMake ,CarModel=CarModel,Vin=Vin ,Job=Job,Price=Price,Price1=Price1)
        
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
    print ('Total Amount ::',customer.Total_Amount)
    customer.Subtotal = Calculate_Subtotal(customer.Price,customer.Price1,customer.Price2,customer.Price3)
    customer.gst=Calculate_gst(customer.Subtotal)
    customer.Total_Amount = customer.Subtotal + customer.gst
    
    html = render_template('invoice.html', customer=customer)
    pdf = BytesIO()
    HTML(string=html).write_pdf(pdf)
    pdf.seek(0)
    return send_file(pdf, download_name='invoice.pdf', as_attachment=True)



@app.route('/search_customers', methods=['GET'])
def search_customers():
    # Get search parameters from the query string
    search_by = request.args.get('search_by', 'name')
    search_term = request.args.get('search_term', '').strip()
    start_date = request.args.get('start_date', '')
    end_date = request.args.get('end_date', '')

    # Start with a base query
    query = Customer.query

    # Apply filters based on search criteria
    if search_term:
        if search_by == 'name':
            query = query.filter(Customer.name.ilike(f"%{search_term}%"))
        elif search_by == 'email':
            query = query.filter(Customer.email.ilike(f"%{search_term}%"))
        elif search_by == 'phone':
            query = query.filter(Customer.phone.ilike(f"%{search_term}%"))

    if start_date:
        try:
            start_date = datetime.strptime(start_date, '%Y-%m-%d')
            query = query.filter(Customer.created_at >= start_date)
        except ValueError:
            pass  # handle date parsing errors or inform the user
    if end_date:
        try:
            end_date = datetime.strptime(end_date, '%Y-%m-%d')
            query = query.filter(Customer.created_at <= end_date)
        except ValueError:
            pass  # handle date parsing errors or inform the user

    # Execute the query and fetch the results
    customers = query.limit(10).all()

    # Render the template with the filtered results
    return render_template('view_customers.html', customers=customers)


def Calculate_gst(Subtotal) :
    return Subtotal * 13 / 100

def Calculate_Subtotal (Price,Price1,Price2,Price3):
    if (Price1 == None ):
        return Price
    if (Price2 == None ):
        return Price + Price1
    if (Price3 == None ):
        return Price + Price1 + Price2
    return Price + Price1 + Price2 + Price3


if __name__ == '__main__':
    db.create_all() 
    app.run(debug=True)

