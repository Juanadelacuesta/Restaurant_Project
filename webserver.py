from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem, engine


class WebServerHandler(BaseHTTPRequestHandler):
        
    def do_GET(self):
        #try:
        Base.metadata.bind = engine
        DBSession = sessionmaker(bind = engine)
        session = DBSession()
        
        output = ""
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers() 
        if self.path.endswith("/restaurant"):  
            output += ("<html><body>Restaurants!")
            output += "<ul>"
            for each in restaurants_list = session.query(Restaurant.name).all():
                output += "<li> %s </li>" % each
            
            output += "</ul>"
        output += "</body></html>"
        self.wfile.write(output)
        return
            
        #except:
            #self.send_error(404, 'File Not Found: %s' % self.path)
        
    def do_POST(self):
        try:
            self.send_response(301)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            
            ctype, pdict = cgi.parse_header(self.headers.
                getheader('Content-type'))
            print ctype
           
            
            if ctype == 'multipart/form-data':
                fields = cgi.parse_multipart(self.rfile, pdict)
                messagecontent = fields.get('message')
   
            output = ""
            output += "<html><body>"
            output += "<h2>Okay, how about this: </h2>"
            output += "<h1> %s </h1>" % messagecontent[0]
            output += "<form method='POST' enctype='multipart/form-data' \
                action='/hello'><h2>What would you like me to say?</h2>\
                <input name='message' type='text'><input type='submit' \
                value='submit'></form>"
            output += "</body></html>"
            self.wfile.write(output)
            #print output

        except: 
            pass
        
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