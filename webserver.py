from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem, engine

Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()
            

class WebServerHandler(BaseHTTPRequestHandler):
        
    def do_GET(self):
        #try:
        output = ""
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers() 
        
        output += ("<html><body>")
        if self.path.endswith("/restaurant"):  
            output += ("<h1> Restaurants! </h1>")
            output += "<ul>"
            for name, id in session.query(Restaurant.name, Restaurant.id).all():
                output += ("<br><li> %s <br> \
                <a href='restaurant/%s/edit'> Edit   </a>   \
                <a href='restaurant/%s/delete'>  Delete  </a>\
                </li>") % (name,id, id)
         
            output += "</ul>"
            
        if self.path.endswith("restaurant/new"):
            output += "<form method='POST' enctype='multipart/form-data' \
                action='/restaurant/new'>\
                <h2>Fill the information to create a new restaurant</h2>\
                Name: <input name='name' type='text'><input type='submit' \
                value='Save'>\
                </form>"
                
        if self.path.endswith("/edit"):
            restaurant_id = self.path.split('/')[2]
            restaurant_to_edit = (session.query(Restaurant).
                                filter(Restaurant.id==restaurant_id).one())
                                
            output += "<form method='POST' enctype='multipart/form-data' \
                action='/restaurant/%s/edit'> <h2> %s </h2>\
                New name: <input name='name' type='text'><input type='submit' \
                value='Save'> </form>" % (restaurant_to_edit.id, 
                                            restaurant_to_edit.name)
        
        if self.path.endswith("/delete"):
            restaurant_id = self.path.split('/')[2]
            restaurant_to_delete = (session.query(Restaurant).
                                filter(Restaurant.id==restaurant_id).one())
                                
            output += "<form method='POST' enctype='multipart/form-data' \
                action='/restaurant/%s/delete'> <h2>Delete</h2> \
                Are you sure you want delete the restaurant %s? <br><br>\
                <input type='submit' value='Delete'>\
                </form>" % (restaurant_to_delete.id, 
                                restaurant_to_delete.name)
                                            
        output += "</body></html>"
        self.wfile.write(output)
        return
        
        #except:
            #self.send_error(404, 'File Not Found: %s' % self.path)
        
    def do_POST(self):
        #try:
        
        self.send_response(301)
        self.send_header('Content-type', 'text/html')
        self.send_header('location', '/restaurant')
        self.end_headers()
        ctype, pdict = cgi.parse_header(self.headers.
            getheader('Content-type'))

        if ctype == 'multipart/form-data':
            fields = cgi.parse_multipart(self.rfile, pdict)
            
            if self.path.endswith("restaurant/new"):
                restaurant_name = str(fields.get('name')[0])
                new_restaurant = Restaurant(name = restaurant_name)
                session.add(new_restaurant)
            
            if self.path.endswith("/edit"):
                restaurant_name = str(fields.get('name')[0])
                restaurant_id = self.path.split('/')[2]
                restaurant_to_edit = (session.query(Restaurant).
                                        filter(restaurant_id==Restaurant.id)
                                        .one())
                restaurant_to_edit.name = restaurant_name
            
            if self.path.endswith("/delete"):
                restaurant_id = self.path.split('/')[2]
                restaurant_to_delete = (session.query(Restaurant).
                                        filter(restaurant_id==Restaurant.id)
                                        .one())
                session.delete(restaurant_to_delete)
                  
            session.commit()
        #except: 
            #pass
        
def main():    
    try:
        port = 8080
        server = HTTPServer(('', port), WebServerHandler)
        print "Web Server running on port %s" % port
        server.serve_forever()
    except KeyboardInterrupt:
        print " ^C entered, stopping web server...."
        server.socket.close()

if __name__ == '__main__':
    
    
    main()