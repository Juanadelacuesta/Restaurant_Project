import cgi
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem, engine
from flask import Flask, render_template, url_for
app = Flask(__name__)

Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()
            
@app.route('/')
@app.route('/restaurants/')
def index():
    items = session.query(MenuItem).all()
    return render_template('menuItems.html', items=items)
    
@app.route('/restaurants/<int:restaurant_id>/')
def restaurantMenu(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id=restaurant.id)
    return render_template('menu.html', restaurant=restaurant, items=items)

# Task 1: Create route for newMenuItem function here
@app.route('/restaurants/newMenuItem/')
def AddMenuItem():
    output = ''
    output += '<h1> New Menu Item</h2> '
    output += "<form method='POST' enctype='multipart/form-data' \
        action='/restaurant/newMenuItem'>\
        <h2>Enter information to create a new menu item</h2>\
        <p>\
        Name: <input name='name' type='text'></br>\
        Course: <input name='course' type='text'> </br>\
        Description: <input name='description' type='text'></br>\
        Price: <input name ='price' type='text'> </br>\
        Restaurant: <select name='restaurant_id'>"
    for restaurant in session.query(Restaurant).all():
        output += ("<option value='%s'> %s </option>"  
            % (restaurant.id, restaurant.name))
    output += "</br></select>"
    output += "</br></br><input type='submit' value='Save'> </p>\
        </form>"
    return output


@app.route('/restaurants/<int:restaurant_id>/<int:menuitem_id>/')    
def editMenuItem(restaurant_id, menuitem_id):
    print restaurant_id, menuitem_id
    output = ''
    restaurant = (session.query(Restaurant).
        filter(Restaurant.id==restaurant_id).one())
    item = (session.query(MenuItem).
        filter(MenuItem.id==menuitem_id).one())
      
    output = ''
    output += ("<form method='POST' enctype='multipart/form-data' \
        action='/restaurant/'>\
        <h2>Edit the item %s and add it to restaurant %s</h2>" 
        % (item.name, restaurant.name))
    output +=  ("Name: <input name='name' placeholder='%s' type='text'></br>\
        Course: <input name='course' placeholder='%s' type='text'> </br>\
        Description: <input name='desc' placeholder='%s' type='text'></br>\
        Price: <input price='price' placeholder='%s' type='text'> </br>" %
        (item.name, item.course, item.description, item.price))
    output += "</br><input type='submit' value='Save and Add'>"
    output += "</form>"   
    return output


@app.route('/restaurants/delete/<int:restaurant_id>/<int:menuitem_id>/')    
def deleteMenuItem(restaurant_id, menuitem_id):
    output = ''
    output += "listo parce"
    return output
    
if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)