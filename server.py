# Corey Knapp
# CSCI 4131
# Prof D. Kluver
# 27SEP25
# HW3

from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib
import re
import time
import datetime
from datetime import *


orders = [
    {
        "id": 0,
        "status": "delivered",
        "cost": 18.00,
        "query": "Ungrim Ironfist",
        "address": "Slayer King\nThrone Room\nKarak Kadrin, N.W.E. Mtns",
        "product": "The One Burp Stout",
        "notes": "No dry days for the Slayer King",
        "time": datetime.now(None),
    },
    {
        "id": 1,
        "status": "shipped",
        "cost": 14.00,
        "query": "Gotrek Gurnnisson",
        "address": "Red Moon Inn\nUbersreik, Reiksland",
        "product": "Burping Ale",
        "notes": "Tales are always better with good beer",
        "time": datetime.now(None),
    },
    {
        "id": 2,
        "status": "placed",
        "cost": 13.00,
        "query": "Thrain",
        "address": "The Lonely Mountain",
        "product": "Twilight Shores IPA",
        "notes": "The deeper you dig, the more beer you'll need",
        "time": datetime.now(None),
    },
    {
        "id": 3,
        "status": "placed",
        "cost": 13.00,
        "query": "Erik von Vonvolkvan",
        "address": "Bechafen, Ostermark",
        "product": "Brilliant Earth Hefe-weizen",
        "notes": "There are no such thing as man-sized rats",
        "time": datetime.now(None),
    },
]

# PUT YOUR GLOBAL VARIABLES AND HELPER FUNCTIONS HERE.


# I dont know how to account for freed up id enties after deletion.
# Therefore, we will simply find the largest id currently in the list
# and increment new order id by 1.
def idAssignment(): 

    newid = max(order["id"] for order in orders) + 1
    return newid
     

def render_order_failure():
    
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
       

        <h2>Sorry!</h2>

        <h4>We were unable to process your order</h4>
   
        </table>
    </body>
</html>
"""
    return result


# A simple page to express a successful order cancellation. We pass in the order id simply for display.
def cancel_order_success(params):

    # UPDATE: I guess this needs to account for empty body. My bad.
    if params != '':
        if "=" in params:
            k,v = params.split("=")


    

    result = f"""
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
       

        <h2>Success</h2>

        <h4>You have successfully cancelled order #{v}.</h4>
   
        </table>
    </body>
</html>
"""
    return result



def cancel_order_failure():
    
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
       

        <h2>Sorry!</h2>

        <h4>Something wrong happened when attempting to cancel your order.
            Please verify your orders and contact our Customer Support team
            if the issue persists</h4>
   
        </table>
    </body>
</html>
"""
    return result



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
    #print("We just entered PQP ")
    
    # Split the query string into key-value pairs
    if response != '':
        if "&" in response:
            splitparams = response.split("&")
        
        # Forgot to handle this.
        elif "=" in response:
            k,v = response.split("=")
            paramdict = dict()
            paramdict[unescape_url(k)] = unescape_url(v)
            return paramdict

        
    print("PQP SP: "+ str(splitparams))
    # Initialize a dictionary to store parsed parameters
    paramdict = dict()

   
    # Iterate over each key-value pair
    for param in splitparams :

    # Split the pair by '=' to separate key and value
        #print("This param getting split on = is: " +param)
        if response != '':
            if "=" in response:
                k,v = param.split("=")
        
                paramdict[unescape_url(k)] = unescape_url(v)
                #print(paramdict)
    
    return paramdict


# ASSUMPTION: The time-to-shipment is triggered by the tracking page. This is probably
# bad practice in the long run.
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
        <script src="/static/js/update.js" defer></script>
    </head>
    
    <body>

        <header>
           <a href="/">Back to Main Page</a>
        </header>
       

        <h2>Order Tracking</h2>
    """

    # Change order status before displaying the details using datetime.
    diff = datetime.now(None) - order["time"]

    if diff > timedelta(minutes=1):
        order["status"] = "shipped"

    if diff > timedelta(minutes=2):
        order["status"] = "delivered"
    
    
    if order.get('status') == 'placed':
        result+= f"<h4>Your order has been confirmed by our team and is being prepared!</h4>\n"
    elif order.get('status') == 'shipped':
        result+= f"<h4>Your order has been shipped and is currently on its way!</h4>\n"
    elif order.get('status') == 'delivered':
        result+= f"<h4>Your order should have arrived. Enjoy!</h4>\n"
    elif order.get('status') == 'cancelled':
        result+= f"<h4>This order has been cancelled.</h4>\n"
    result+= """

    <div class = "main">

    <div class = "left">
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
    </div>

    <div class = "right">
    """

    if order.get('status') == 'placed':
        result+= f"""
                <form action="cancel_order" method="POST" id="cancel">
                    <input type="hidden" name="cancel" value="{order.get('id')}"> 
                    <button type="submit" form="cancel" value="Submit" id="cancelButton">Cancel Order</button>
                </form>
                

                <form action="update_shipping" method="POST" id="update">
                </form>
                <button type="submit" form="update" value="Submit" id="updateButton">Update Order</button>\n

                <p id="countdown">Time until shipment.</p>\n

                """
    elif order.get('status') == 'cancelled':
        result+= f"<h4> Order number {order.get('id')} was recently cancelled.</h4>\n"


    result+= """
    </div>

    </body>
</html>
"""
    return result


def render_table_row(order):
    # render a single row of the admin orders table.
    # This is recommended, but not required
    pass



# UPDATE 1 HW3: There is some serious spaghetti going on in here.
# UPDATE 2 HW3: Was using order_filters["X"] instead of order_filters.get("X") in some placed causing instant crash instead of returning None.
def render_orders(order_filters: dict[str, str]):
   
    #print("these are the order filters" + str(order_filters))

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
    if len(order_filters) == 0 or (order_filters.get("status") == 'all' and order_filters.get("query") == ''):
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
        </p>\n
        <p>
        <select name="status">
            <option value="placed">Placed</option>
            <option value="shipped">Shipped</option>
            <option value="delivered">Delivered</option>
            <option value="all">All Statuses</option>
        </select>
        </p>\n
            <input type="submit">
        </form>


        """
            
        if order_filters.get("status") == 'all' or order_filters.get("status") != '':
            result+= f"<h4>Searched for status: {order_filters.get("status")}</h4>\n"
        
        if order_filters.get("query") != '':
            result+= f"<h4>Searched for query: {order_filters.get("query")}</h4>\n"
            
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



            if "query" in order_filters and "status" in order_filters :
            
                if order_filters.get("status") == 'all' and  order_filters.get("query") in order.get("query") and order_filters.get("query") != '':
                    
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

                if order_filters.get("status") == 'placed' and order_filters.get("status") == order.get('status') and ( order_filters.get("query") in order.get("query") or  order_filters.get("query") == '') :
                
                    
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
                
                if order_filters.get("status") == 'shipped' and order_filters.get("status") == order.get('status') and ( order_filters.get("query") in order.get("query") or  order_filters.get("query") == '') :
                
                    
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

                if order_filters.get("status") == 'delivered' and order_filters.get("status") == order.get('status') and ( order_filters.get("query") in order.get("query") or  order_filters.get("query") == '') :
                
                    
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
            
            elif "query" in order_filters and "status" not in order_filters :
                print("FOUND QUERY ONLY")
                if  order_filters.get("query") in order.get("query"):
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
            
            elif "query" not in order_filters and "status" in order_filters :
                print("FOUND STATUS ONLY")
                if order_filters.get("status") == order.get('status'):
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
            #print("WE MADE IT THROUGH A LOOP")


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
       

        <h2>Success!</h2>
   
        </table>
    </body>
</html>
"""
    return result


def add_new_order(params):
    
    scrutinize = parse_query_parameters(params)

    # If anything goes wrong, the order will fail. Hopefully that will includes any 
    # detection of XSS?
    flag = False

    for k, v in scrutinize.items():
        
        # Client must fill in all fields
        if not v:
            flag = True

    # Client must provide integers for quantity field.
    if not scrutinize.get("quantity").isdigit() :
        flag = True
        
    # TODO: Sift through the address. Do not allow anything strange through
    # %0D%0A is \r\n .
    # NOTE 1: Worst case, cant we just escape the address portion since quantity is already
    # picky?

    # HW3 NOTE: This is where the order is created, so time will be setup here.
    if flag:
        return None
    else:
        assign = idAssignment()
        orders.append(
            {
            "id": assign,
            "status": "placed",
            "cost": 0.00,
            "query": scrutinize.get("query"),
            "address": scrutinize.get("address"),
            "product": scrutinize.get("product"),
            "notes": "",
            "time": datetime.now(None),
            }
        )

        return assign
        



def cancel_order(params):
    
    # NOTE: I really only care about the right-hand side. I hope this doesnt backfire.
    if params != '':
        if "=" in params:
            k,v = params.split("=")
    else:
        return False
    
    for order in orders:
        if order.get('id') == int(v) :
            if order.get('status') == "placed":
                #print("We found a match to cancel")
                order['status'] = "cancelled"

                return True
    
    return False




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
                #print(url[14:])
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
            return open("static/html/order.html","r").read(), "text/html", 200

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
        

        # IMAGES CALL
        if "/images/main" in url:
            return open("static/images/main.png","rb").read(), "image/", 200
        if "staff.png" in url:
            return open("static/images/staff.png","rb").read(), "image/", 200



        if "/static/js/update" in url:
            return open("static/js/update.js","r").read(), "application/javascript", 200
        


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

    # Placeholder for POST sent by /order.
    if "new_order_attempt" in url :
        
        try:

            print("Post URL: " + url + " POST content: " + body)
            toVerify = add_new_order(body)
            if toVerify != None:
                return render_order_success(toVerify), "text/html", 201
            else:
                return render_order_failure(), "text/html", 400
            

        except Exception as e:

            return open("static/html/404.html","r").read(), "text/html", 500
        
    if "cancel_order" in url :
        
        try:

            #print("Post URL: " + url + " POST content: " + body)
            # Yet another bandaid to get around empty POST?
            if body == None or body == '' :
                return cancel_order_failure(), "text/html", 400
                
            else:
                if cancel_order(body):
                    return cancel_order_success(body), "text/html", 200
                else:
                    return cancel_order_failure(), "text/html", 400
                
            
        except Exception as e:
            print(e)
            return open("static/html/404.html","r").read(), "text/html", 500
        

    return open("static/html/404.html","r").read(), "text/html", 404
    

     

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
