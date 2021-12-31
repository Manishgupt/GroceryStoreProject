"""from flask import Flask, request, jsonify,render_template
from sql_connection import get_sql_connection
import mysql.connector
import json
import products_dao
import orders_dao
import uom_dao

app = Flask(__name__)

connection = get_sql_connection()


@app.route('/getUOM', methods=['GET'])
def get_uom():
    response = uom_dao.get_uoms(connection)
    response = jsonify(response)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


@app.route('/getProducts', methods=['GET'])
def get_products():
    response = products_dao.get_all_products(connection)
    response = jsonify(response)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


@app.route('/insertProduct', methods=['POST'])
def insert_product():
    request_payload = json.loads(request.form['data'])
    product_id = products_dao.insert_new_product(connection, request_payload)
    response = jsonify({
        'product_id': product_id
    })
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


@app.route('/getAllOrders', methods=['GET'])
def get_all_orders():
    response = orders_dao.get_all_orders(connection)
    response = jsonify(response)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


@app.route('/insertOrder', methods=['POST'])
def insert_order():
    request_payload = json.loads(request.form['data'])
    order_id = orders_dao.insert_order(connection, request_payload)
    response = jsonify({
        'order_id': order_id
    })
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


@app.route('/deleteProduct', methods=['POST'])
def delete_product():
    return_id = products_dao.delete_product(connection, request.form['product_id'])
    response = jsonify({
        'product_id': return_id
    })
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


@app.route('/')
def home():
    return render_template('home.html')


if __name__ == "__main__":
    print("Starting Python Flask Server For Grocery Store Management System")
    app.run(debug=True)
"""

from flask import Flask, request, jsonify,render_template,url_for,request,redirect,session
from sql_connection import get_sql_connection
import mysql.connector
import json
import products_dao
import orders_dao
import uom_dao
from enum import EnumMeta
import re
#from flask import Flask,render_template,url_for,request,redirect,session
from flask.wrappers import Request
import os 


app = Flask(__name__)


app.secret_key=os.urandom(24) 

conn=mysql.connector.connect(host="remotemysql.com",user="91yKbjoVQb",password="hu2iwKd7wK",database="91yKbjoVQb")
cursor=conn.cursor()

connection = get_sql_connection()


@app.route('/getUOM', methods=['GET'])
def get_uom():
    response = uom_dao.get_uoms(connection)
    response = jsonify(response)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


@app.route('/getProducts', methods=['GET'])
def get_products():
    response = products_dao.get_all_products(connection)
    response = jsonify(response)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


@app.route('/insertProduct', methods=['POST'])
def insert_product():
    request_payload = json.loads(request.form['data'])
    product_id = products_dao.insert_new_product(connection, request_payload)
    response = jsonify({
        'product_id': product_id
    })
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


@app.route('/getAllOrders', methods=['GET'])
def get_all_orders():
    response = orders_dao.get_all_orders(connection)
    response = jsonify(response)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


@app.route('/insertOrder', methods=['POST'])
def insert_order():
    request_payload = json.loads(request.form['data'])
    order_id = orders_dao.insert_order(connection, request_payload)
    response = jsonify({
        'order_id': order_id
    })
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


@app.route('/deleteProduct', methods=['POST'])
def delete_product():
    return_id = products_dao.delete_product(connection, request.form['product_id'])
    response = jsonify({
        'product_id': return_id
    })
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


@app.route('/')
def login():
    return render_template("login.html")

@app.route('/register')
def about():
    return render_template("register.html")


@app.route('/home')
def home():
    if 'user_id' in session:
        return render_template('home.html')
    else:
        return redirect('/')


@app.route('/showproducts')
def showproducts():
    return render_template('manage-product.html')

@app.route('/orders')
def orders():
    return render_template('order.html')

@app.route('/about')
def about1():
    return render_template('blogdescription.html')

@app.route('/allorders')
def allorders():
    return render_template('index1.html')

@app.route('/custo')
def custo():
    return render_template('index1.html')

@app.route('/contact')
def contact():
    return render_template('contactus.html')    
    
@app.route("/login_validation",methods=['POST'])
def login_validation():
    email=request.form.get('email')
    password=request.form.get('password')
    query="""select * from `users` where `email` like '{}' And `password` like '{}'""".format(email,password)
    cursor.execute(query)
    user=cursor.fetchall()
    if(len(user)>0):
        session['user_id']=user[0][0]
        return redirect('/home')
    else:
        return redirect('/')
    
@app.route('/add_user',methods=['POST'])
def add_user():
    name=request.form.get('uname')
    email=request.form.get('uemail')
    password=request.form.get('upassword')
    query="""insert into `users` (`name`,`email`,`password`) values('{}','{}','{}')""".format(name,email,password)
    cursor.execute(query)
    conn.commit()

    cursor.execute("""select * from `users` where `email` like '{}' """.format(email))
    myuser=cursor.fetchall()
    session['user_id']=myuser[0][0]
    return redirect('/home') 

@app.route('/logout')
def logout():
    session.pop('user_id')
    return redirect('/')

@app.route('/forget')
def forget():
    return render_template("forgetpassword.html")


@app.route('/forgetpassword',methods=['POST'])
def forgetpassword():
    email=request.form.get('femail')
    password=request.form.get('fpassword')
    conform_pass=request.form.get('fconformpassword')

    if(password==conform_pass):
        query="""update `users` set `password`='{}' where `email`='{}'""".format(password,email)
        cursor.execute(query)
        conn.commit()
        return redirect('/')
    else:
        return render_template("forget.html")


#payment route
@app.route('/info',methods=['POST','GET'])
def info():
    return("hello")

if __name__ == '__main__':
    app.run(debug=True)
 


