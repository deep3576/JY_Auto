from flask import Flask, render_template, request, redirect, url_for, send_file
from flask_sqlalchemy import SQLAlchemy
import os
from weasyprint import HTML
from io import BytesIO
from urllib.parse import quote

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///auto_shop.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    vehicle = db.Column(db.String(100), nullable=False)
    service = db.Column(db.String(200), nullable=False)
    cost = db.Column(db.Float, nullable=False)

db.create_all()

@app.route('/')
def home():
    return render_template('form.html')

@app.route('/submit', methods=['POST'])
def submit():
    name = request.form['name']
    email = request.form['email']
    vehicle = request.form['vehicle']
    service = request.form['service']
    cost = request.form['cost']
    customer = Customer(name=name, email=email, vehicle=vehicle, service=service, cost=cost)
    db.session.add(customer)
    db.session.commit()
    return redirect(url_for('home'))

@app.route('/search')
def search():
    return render_template('search.html')

@app.route('/results', methods=['POST'])
def results():
    search_query = request.form['query']
    results = Customer.query.filter(Customer.name.contains(search_query)).all()
    return render_template('results.html', results=results)

@app.route('/invoice/<int:id>')
def invoice(id):
    customer = Customer.query.get_or_404(id)
    html = render_template('invoice.html', customer=customer)
    pdf = BytesIO()
    HTML(string=html).write_pdf(pdf)
    pdf.seek(0)
    return send_file(pdf, attachment_filename='invoice.pdf', as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
