import cgi
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem, engine
from flask import Flask, render_template, url_for, request, redirect, flash
app = Flask(__name__)

Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()
            
@app.route('/', methods = ['GET','POST'])
@app.route('/restaurants/', methods = ['GET','POST'])
def index():

    items = session.query(MenuItem).all()
    if request.method == 'GET':
        return render_template('menuItems.html', items=items)
    elif request.method == 'POST':
        item_to_delete = (session.query(MenuItem).
                            filter(MenuItem.id==request.form['id']).one())
        session.delete(item_to_delete)
        session.commit()
        return redirect(url_for('index'))
    
@app.route('/restaurants/<int:restaurant_id>/')
def restaurantMenu(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id=restaurant.id)
    return render_template('menu.html', restaurant=restaurant, items=items)

# Task 1: Create route for newMenuItem function here
@app.route('/restaurants/newMenuItem/', methods=['GET','POST'])
def AddMenuItem():
    restaurants = session.query(Restaurant).all()
    new_item = MenuItem()
    if request.method == 'GET':
        return render_template('newMenuItem.html', restaurants=restaurants)
        
    elif request.method == 'POST':
        if request.form['name']:
            new_item.name = request.form['name']
        if request.form['course']:
            new_item.course = request.form['course']
        if request.form['description']:
            new_item.description = request.form['description']
        if request.form['price']:
            new_item.price = request.form['price']
        if request.form['restaurant_id']:
            new_item.restaurant_id = request.form['restaurant_id']    
        
        session.add(new_item)
        session.commit()
        flash('New Item created!')
        return redirect(url_for('index'))

@app.route('/restaurants/<int:restaurant_id>/<int:menuitem_id>/', 
            methods = ['GET','POST'])    
def editMenuItem(restaurant_id, menuitem_id):
    print "edit"
    restaurant = (session.query(Restaurant).
        filter(Restaurant.id==restaurant_id).one())
    item = (session.query(MenuItem).
        filter(MenuItem.id==menuitem_id).one())
    if request.method == 'GET':
        return render_template('editMenuItem.html', 
                                restaurant=restaurant, item=item)
                                
    elif request.method == 'POST':
        if request.form['name'] != item.name:
            item.name = request.form['name']
        if request.form['course'] != item.course:
            item.course = request.form['course']
        if request.form['desc'] != item.description:
            item.description = request.form['desc']
        if request.form['price'] != item.price:
            item.price = request.form['price']
        item.restaurant_id = restaurant_id  
        session.commit()
        return  redirect(url_for('restaurantMenu',restaurant_id=restaurant_id))
      
@app.route('/restaurants/delete/<int:menuitem_id>/', methods = ['GET','POST'])    
def deleteMenuItem(menuitem_id):
    item = (session.query(MenuItem).
                filter(MenuItem.id==menuitem_id).one())
    if request.method == 'GET':
        return render_template('deleteMenuItem.html', item=item)
        
    elif request.method == 'POST':
        flash("Item deleted!")
        session.delete(item)
        session.commit()
        return redirect(url_for('index'))
        
if __name__ == '__main__':
    app.secret_key = 'Secret_key    '
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
    