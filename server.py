# Corey Knapp
# CSCI 4131
# Prof D. Kluver
# 27SEP25
# HW3

from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib
import re

orders = [
    {
        "id": 0,
        "status": "delivered",
        "cost": 18.00,
        "query": "Ungrim Ironfist",
        "address": "Slayer King\nThrone Room\nKarak Kadrin, N.W.E. Mtns",
        "product": "The One Burp Stout",
        "notes": "No dry days for the Slayer King",
    },
    {
        "id": 1,
        "status": "shipped",
        "cost": 14.00,
        "query": "Gotrek Gurnnisson",
        "address": "Red Moon Inn\nUbersreik, Reiksland",
        "product": "Burping Ale",
        "notes": "Tales are always better with good beer",
    },
    {
        "id": 2,
        "status": "placed",
        "cost": 13.00,
        "query": "Thrain",
        "address": "The Lonely Mountain",
        "product": "Twilight Shores IPA",
        "notes": "The deeper you dig, the more beer you'll need",
    },
    {
        "id": 3,
        "status": "placed",
        "cost": 13.00,
        "query": "Erik von Vonvolkvan",
        "address": "Bechafen, Ostermark",
        "product": "Brilliant Earth Hefe-weizen",
        "notes": "There are no such thing as man-sized rats",
    },
]

# PUT YOUR GLOBAL VARIABLES AND HELPER FUNCTIONS HERE.


def escape_html(str):
    str = str.replace("&", "&amp;")
    str = str.replace('"', "&quot;")

    str = str.replace('>', "&gt;")
    str = str.replace('<', "&lt;")
    
    return str


def unescape_url(url_str):
    import urllib.parse

    # NOTE -- this is the only place urllib is allowed on this assignment.
    return urllib.parse.unquote_plus(url_str)


def parse_query_parameters(response):
    # Split the query string into key-value pairs
    splitparams = response.split("&")

    # Initialize a dictionary to store parsed parameters
    paramdict = dict()

    # Iterate over each key-value pair
    for param in splitparams :

    # Split the pair by '=' to separate key and value
        #print("This param getting split on = is: " +param)
        k,v = param.split("=")
        
        paramdict[unescape_url(k)] = unescape_url(v)
        #print(paramdict)

    return paramdict


def render_tracking(order):
    # Its job should be to take one order object (I.E., one of the dictionaries from your orders list) 
    # and return a page a user would see to check the tracking status for the specific order.
    result = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Burping Turtle Orders</title>
        <link rel="stylesheet" href="/static/css/main.css">
    </head>
    
    <body>

        <header>
           <a href="/">Back to Main Page</a>
        </header>
       

        <h2>Order Tracking</h2>
    """
    if order.get('status') == 'placed':
        result+= f"<h4>Your order has been confirmed by our team and is being prepared!</h4>\n"
    elif order.get('status') == 'shipped':
        result+= f"<h4>Your order has been shipped and is currently on its way!</h4>\n"
    elif order.get('status') == 'delivered':
        result+= f"<h4>Your order should have arrived. Enjoy!</h4>\n"
    result+= """

        <h3> Order Details </h3>
        <table>
            <tr>
                <th>Order ID:</th>
            """
    result+= f"<td>{order.get('id')}</td>\n"
    result+= """
            </tr>
                
            <tr>
                <th>Product:</th>
            """
    result+= f"<td>{order.get('product')}</td>\n"
    result+= """
                </tr>
                
            <tr>
                <th>Status:</th>
                """
    result+= f"<td>{order.get('status')}</td>\n"
    result+= """
            </tr>
                
            <tr>
                <th>Cost:</th>
            """
    result+= f"<td>{typeset_dollars(order.get('cost'))}</td>\n"
    result+= """
            </tr>
            """
            
    result+= """
        </table>
    </body>
</html>
"""
    return result


def render_table_row(order):
    # render a single row of the admin orders table.
    # This is recommended, but not required
    pass


def render_orders(order_filters: dict[str, str]):
    
    result = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Burping Turtle Orders</title>
        <link rel="stylesheet" href="/static/css/main.css">
    </head>
    
    <body>

        <header>
                <a href="/">Back to Main Page</a>
        </header>
       
        <h2>Orders</h2> """

    # Default if there are no params.
    if len(order_filters) == 0 or (order_filters["status"] == 'all' and order_filters["query"] == ''):
        result+= """
        <form action="/admin/orders" method="GET">
        <p>
            <label for="query">query:</label>
            <input type="text" name="query" id="query">
        </p>
        <p>
        <select name="status">
            <option value="placed">placed</option>
            <option value="shipped">shipped</option>
            <option value="delivered">delivered</option>
            <option value="all">All statuses</option>
        </select>
        </p>
            <input type="submit">
        </form>

        <table>
            <tr>
                <th>#</th>
                <th>Status</th>
                <th>Cost</th>
                <th>From</th>
                <th>Address</th>
                <th>Product</th>
                <th>Notes</th>
                <th>Link</th>
            </tr>"""
        for order in orders:
            result+= f"<tr>\n"
            result+= f"<td>{order.get('id')}</td>\n"
            result+= f"<td>{order.get('status')}</td>\n"
            result+= f"<td>{typeset_dollars(order.get('cost'))}</td>\n"
            result+= f"<td>{order.get('query')}</td>\n"
            result+= f"<td>{order.get('address')}</td>\n"
            result+= f"<td>{order.get('product')}</td>\n"
            result+= f"<td>{order.get('notes')}</td>\n"
            result+= f"<td><a href='/tracking/{order.get('id')}'>tracking</a></td>\n"
            result+= f"</tr>\n"

        
        result+= """
        </table>
        """

    # Match parameters and return filtered results.    
    else :

        result+= """
        <form action="/admin/orders" method="GET">
        <p>
            <label for="query">query:</label>
            <input type="text" name="query" id="query">
        </p>
        <p>
        <select name="status">
            <option value="placed">Placed</option>
            <option value="shipped">Shipped</option>
            <option value="delivered">Delivered</option>
            <option value="all">All Statuses</option>
        </select>
        </p>
            <input type="submit">
        </form>


        """
            
        if order_filters["status"] == 'all' or order_filters["status"] == 'delivered' or order_filters["status"] == 'shipped' or order_filters["status"] == 'placed':
            result+= f"<h4>Searched for: {order_filters["status"]}</h4>\n"
        
        if order_filters["query"] != '':
            result+= f"<h4>Searched for: {order_filters["query"]}</h4>\n"
            
        result+= """




        <table>
            <tr>
                <th>#</th>
                <th>Status</th>
                <th>Cost</th>
                <th>From</th>
                <th>Address</th>
                <th>Product</th>
                <th>Notes</th>
                <th>Link</th>
            </tr>"""
        

        # I'm sure there is a better way to filter results. But this is what we got.
        found = False    
        for order in orders:
             
            if order_filters["status"] == 'all' and order_filters["query"] in order.get("query") and order_filters["query"] != '':
                
                result+= f"<tr>\n"
                result+= f"<td>{order.get('id')}</td>\n"
                result+= f"<td>{order.get('status')}</td>\n"
                result+= f"<td>{typeset_dollars(order.get('cost'))}</td>\n"
                result+= f"<td>{order.get('query')}</td>\n"
                result+= f"<td>{order.get('address')}</td>\n"
                result+= f"<td>{order.get('product')}</td>\n"
                result+= f"<td>{order.get('notes')}</td>\n"
                result+= f"<td><a href='/tracking/{order.get('id')}'>tracking</a></td>\n"
                result+= f"</tr>\n"
                found = True

            if order_filters["status"] == 'placed' and order_filters["status"] == order.get('status') and (order_filters["query"] in order.get("query") or order_filters["query"] == '') :
              
                
                result+= f"<tr>\n"
                result+= f"<td>{order.get('id')}</td>\n"
                result+= f"<td>{order.get('status')}</td>\n"
                result+= f"<td>{typeset_dollars(order.get('cost'))}</td>\n"
                result+= f"<td>{order.get('query')}</td>\n"
                result+= f"<td>{order.get('address')}</td>\n"
                result+= f"<td>{order.get('product')}</td>\n"
                result+= f"<td>{order.get('notes')}</td>\n"
                result+= f"<td><a href='/tracking/{order.get('id')}'>tracking</a></td>\n"
                result+= f"</tr>\n"
                found = True
            
            if order_filters["status"] == 'shipped' and order_filters["status"] == order.get('status') and (order_filters["query"] in order.get("query") or order_filters["query"] == '') :
              
                
                result+= f"<tr>\n"
                result+= f"<td>{order.get('id')}</td>\n"
                result+= f"<td>{order.get('status')}</td>\n"
                result+= f"<td>{typeset_dollars(order.get('cost'))}</td>\n"
                result+= f"<td>{order.get('query')}</td>\n"
                result+= f"<td>{order.get('address')}</td>\n"
                result+= f"<td>{order.get('product')}</td>\n"
                result+= f"<td>{order.get('notes')}</td>\n"
                result+= f"<td><a href='/tracking/{order.get('id')}'>tracking</a></td>\n"
                result+= f"</tr>\n"
                found = True

            if order_filters["status"] == 'delivered' and order_filters["status"] == order.get('status') and (order_filters["query"] in order.get("query") or order_filters["query"] == '') :
              
                
                result+= f"<tr>\n"
                result+= f"<td>{order.get('id')}</td>\n"
                result+= f"<td>{order.get('status')}</td>\n"
                result+= f"<td>{typeset_dollars(order.get('cost'))}</td>\n"
                result+= f"<td>{order.get('query')}</td>\n"
                result+= f"<td>{order.get('address')}</td>\n"
                result+= f"<td>{order.get('product')}</td>\n"
                result+= f"<td>{order.get('notes')}</td>\n"
                result+= f"<td><a href='/tracking/{order.get('id')}'>tracking</a></td>\n"
                result+= f"</tr>\n"
                found = True


        result+= """
        </table>
        """
        if found == False :
            result+= """
            <h4>We couldn't find any orders matching those specifications.</h4>

            """

    result+= """
    </body>
</html>
"""
    return result


# Provided function -- converts numbers like 42 or 7.347 to "$42.00" or "$7.35"
def typeset_dollars(number):
    return f"${number:.2f}"


def render_order_success(order):
    pass


def add_new_order(params):
    pass


def cancel_order(params):
    pass


def update_shipping_info(params):
    pass


def server_GET(url: str) -> tuple[str | bytes, str, int]:
    """
    url is a *PARTIAL* URL. If the browser requests `http://localhost:4131/contact?name=joe`
    then the `url` parameter will have the value "/contact?name=joe". (so the schema and
    authority will not be included, but the full path, any query, and any anchor will be included)

    This function is called each time another program/computer makes a request to this website.
    The URL represents the requested file.

    This function should return three values (string or bytes, string, int) in a list or tuple. The first is the content to return
    The second is the content-type. The third is the HTTP Status Code for the response
    """
    # YOUR CODE GOES HERE!
    # step 1: process URL
    try:
        
        # LANDING
        if "/about" in url:
            return open("static/html/about.html","r").read(), "text/html", 200


        # ORDERS BLOCK
        if "/orders" in url:

            # The following will be called if there are any parameters from the search, or 
            # manually placed into the URL.
            # NOTE TO TA: I'm guessing this is where we are supposed to escape to prevent
            # naughty behavior.
            if "?" in url:
                try:
                    return render_orders(parse_query_parameters(url[14:])) , "text/html", 200

                except Exception as e: 
                    print(e)
                    return open("static/html/404.html","r").read(), "text/html", 404
            
            # The following will be called without any parameters. Due to they way I have chosen to
            # write the code, I am simply going to pass in an empty dictionary for order_filters.
            # I AM ASSUMING that we want to see all orders if there are no filters!
            else:
                try:
                    return render_orders({}) , "text/html", 200

                except Exception as e: 
                    print(e)
                    return open("static/html/404.html","r").read(), "text/html", 404
        

        # NEW ORDER BLOCK. This condition seems a bit risky.
        if "/order" in url:
            return open("static/html/temp.html","r").read(), "text/html", 200

        # TRACKING PAGE
        if "/tracking" in url:

            try:
                ordernum = int(url[10:])
                print(ordernum)
                for order in orders:
                    if order.get('id') == ordernum :
                        return render_tracking(order) , "text/html", 200
                
                return open("static/html/404.html","r").read(), "text/html", 404

            except Exception as e:
                print(e) 
                return open("static/html/404.html","r").read(), "text/html", 404



        # CSS CALL
        if url.startswith("/static/css/") or "main.css" in url:  
            return open("static/css/main.css","r").read(), "text/css", 200
        


        if "/images/main" in url:
            return open("static/images/main.png","rb").read(), "image/", 200
        if "staff.png" in url:
            return open("static/images/staff.png","rb").read(), "image/", 200



        # EDGE CASES, HANDLING
        if "/orders" not in url and "/about" not in url:
          
            # NOTE: The following line is to short circuit if it happens to see "/". 
            # Don't get too angry yet.
            if url == "/":
                return open("static/html/about.html","r").read(), "text/html", 200
            
            # Now we handle the other cases of 'complicated' "/" variants since the short
            # wasn't successful. This should be fine due to thwwwwwwwwwwwwwwwa requirements of 
            # the parent if statement. 
            # Development 1: I thought about adding: or "/?" in url: but
            # I'm pretty sure that would cause bugs with opening main instead of 404 page.
            if url.startswith("/?"):
                return open("static/html/about.html","r").read(), "text/html", 200
            
            else:
                return open("static/html/404.html","r").read(), "text/html", 404

           
            

    except Exception as e:
        print(e)
        return open("static/html/404.html","r").read(), "text/html", 404
    
    return open("static/html/404.html","r").read(), "text/html", 500
    


def server_POST(url: str, body: str) -> tuple[str | bytes, str, int]:
    """
    url is a *PARTIAL* URL. If the browser requests `http://localhost:4131/contact?name=joe`
    then the `url` parameter will have the value "/contact?name=joe". (so the schema and
    authority will not be included, but the full path, any query, and any anchor will be included)

    This function is called each time another program/computer makes a POST request to this website.

    This function should return three values (string or bytes, string, int) in a list or tuple. The first is the content to return
    The second is the content-type. The third is the HTTP Status Code for the response
    """
    print("Post URL: " + url + " POST Body: " + body)
    return open("static/html/temp.html","r").read(), "text/html", 200


# You shouldn't need to change content below this. It would be best if you just left it alone.


class RequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        # Read the content-length header sent by the BROWSER
        content_length = int(self.headers.get("Content-Length", 0))
        # read the data being uploaded by the BROWSER
        body = self.rfile.read(content_length)
        # we're making some assumptions here -- but decode to a string.
        body = str(body, encoding="utf-8")

        message, content_type, response_code = server_POST(self.path, body)

        # Convert the return value into a byte string for network transmission
        if type(message) == str:
            message = bytes(message, "utf8")

        # prepare the response object with minimal viable headers.
        self.protocol_version = "HTTP/1.1"
        # Send response code
        self.send_response(response_code)
        # Send headers
        # Note -- this would be binary length, not string length
        self.send_header("Content-Length", len(message))
        self.send_header("Content-Type", content_type)
        self.send_header("X-Content-Type-Options", "nosniff")
        self.end_headers()

        # Send the file.
        self.wfile.write(message)
        return

    def do_GET(self):
        # Call the student-edited server code.
        message, content_type, response_code = server_GET(self.path)

        # Convert the return value into a byte string for network transmission
        if type(message) == str:
            message = bytes(message, "utf8")

        # prepare the response object with minimal viable headers.
        self.protocol_version = "HTTP/1.1"
        # Send response code
        self.send_response(response_code)
        # Send headers
        # Note -- this would be binary length, not string length
        self.send_header("Content-Length", len(message))
        self.send_header("Content-Type", content_type)
        self.send_header("X-Content-Type-Options", "nosniff")
        self.end_headers()

        # Send the file.
        self.wfile.write(message)
        return


def run():
    PORT = 4131
    print(f"Starting server http://localhost:{PORT}/")
    server = ("", PORT)
    httpd = HTTPServer(server, RequestHandler)
    httpd.serve_forever()


run()
