from flask import Flask, render_template, request, redirect, url_for, flash, send_file
from flask_sqlalchemy import SQLAlchemy
from weasyprint import HTML
from io import BytesIO
from datetime import datetime
from sqlalchemy import desc
import pandas as pd
import io



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
    email = db.Column(db.String(120), unique=False, nullable=True)
    phone = db.Column(db.String(20), nullable=False)
    CarMake = db.Column(db.String(20), nullable=False)
    CarModel = db.Column(db.String(20), nullable=False)
    Vin = db.Column(db.String(120), nullable=False)
    Odometer= db.Column(db.String(120), nullable=True)
    Job = db.Column(db.String(240), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    last_updated = db.Column(db.DateTime , nullable= True )
    Price = db.Column(db.Integer, nullable=False)
    Job1 = db.Column(db.String(240), nullable=True)
    Price1 = db.Column(db.Integer, nullable=True)

    Job2 = db.Column(db.String(240), nullable=True)
    Price2 = db.Column(db.Integer, nullable=True)

    Job3 = db.Column(db.String(240), nullable=True)
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
    customers = Customer.query.order_by(desc(Customer.id)).limit(20).all()
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

        Caryear = request.form['Caryear']
        CarColor = request.form['CarColor']


        Odometer = request.form['Odometer']

        Job = request.form['Job']
        Price = request.form['Price']

        Job1 = request.form['Job1']
        Price1 = request.form['Price1']

        Job2 = request.form['Job2']
        Price2 = request.form['Price2']

        Job3 = request.form['Job3']
        Price3 = request.form['Price3']

        new_customer = Customer(name=name, email=email, phone=phone , CarMake=CarMake ,CarModel=CarModel,Vin=Vin ,Odometer=Odometer,Job=Job,Price=Price,Job1=Job1,Price1=Price1,Job2=Job2,Price2=Price2,Job3=Job3,Price3=Price3)
        
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
        customer.CarMake = request.form['CarMake']
        customer.CarModel = request.form['CarModel']
        customer.Odometer = request.form['Odometer']

        customer.Vin = request.form['Vin']
        customer.CarColor = request.form['CarColor']
        customer.Caryear = request.form['Caryear']



        customer.Price = request.form['Price']
        customer.Price2 = request.form['Price2']
        customer.Price3 = request.form['Price3']
        customer.Price1 = request.form['Price1']

        customer.Job = request.form['Job']
        customer.Job1 = request.form['Job1']
        customer.Job2 = request.form['Job2']
        customer.Job3 = request.form['Job3']


    
        
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
    customers = query.order_by(desc(Customer.id)).limit(20).all()

    # Render the template with the filtered results
    return render_template('view_customers.html', customers=customers)



@app.route('/export')
def export_data():
    users = Customer.query.order_by(desc(Customer.id)).all()
    data = [
        {"id": user.id, "username": user.username, "email": user.email, "created_at": user.created_at}
        for user in users
    ]
    df = pd.DataFrame(data)
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Users')
    output.seek(0)
    return send_file(output, as_attachment=True, download_name="users.xlsx", mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

@app.route('/import', methods=['POST'])
def import_users():
    if 'file' not in request.files:
        return redirect(url_for('users'))
    file = request.files['file']
    if file.filename == '':
        return redirect(url_for('users'))
    if file and file.filename.endswith('.xlsx'):
        df = pd.read_excel(file)
        for index, row in df.iterrows():
            user = Customer(username=row['username'], email=row['email'])
            db.session.add(user)
        db.session.commit()
    return redirect(url_for('users'))




def Calculate_gst(Subtotal) :
    return Subtotal * 13 / 100

def Calculate_Subtotal (Price,Price1,Price2,Price3):
    Price1=check_and_set_none(Price1)
    Price2=check_and_set_none(Price2)
    Price3=check_and_set_none(Price3)
    Price=check_and_set_none(Price)

    if (Price1 == None ) :
        return Price
    if (Price2 == None  ):
        return Price + Price1
    if (Price3 == None ):
        return Price + Price1 + Price2
    return Price + Price1 + Price2 + Price3

def check_and_set_none(value):
    if isinstance(value, str):
        return None
    return value


if __name__ == '__main__':
    db.create_all() 
    app.run(debug=True)

