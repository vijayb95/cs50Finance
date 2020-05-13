import os, hashlib

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from datetime import datetime
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")
#adding api key to os.environ
os.environ["API_KEY"] = "pk_300a5d641905415c94653a221ef39f2d"

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    id = session["user_id"]
    cash = db.execute("select cash from users where id = ?", id)
    cash = float(cash[0]["cash"])
    # total = usd(total)
    try:
        total = cash
        rows = db.execute("select symbol,name,shares from holdings where userId = ?", id)
        i = 0
        for row in rows[0:]:
            shares = row["shares"]
            curCost = lookup(row["symbol"])
            curCost = curCost["price"]
            value = curCost * shares
            rows[i]["curCost"] = curCost
            rows[i]["value"] = value
            i += 1
            total = value + total
        return render_template("index.html",cash = usd(cash), total = usd(total), rows = rows)

    except:
        total = cash
        return render_template("index.html",cash = cash, total = total)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "POST":
        if not request.form.get("symbol"):
            return apology("Please enter a Symbol")

        # Ensure password was submitted
        elif not request.form.get("shares"):
            return apology("Enter the number of shares you want to buy")
        
        symbol = request.form.get("symbol")
        quote = lookup(symbol)

        if not quote:
            return apology("Invalid Symbol")
        company = quote["name"]
        price = quote["price"]
        symbol = request.form.get("symbol")
        qty = float(request.form.get("shares"))
        id = session["user_id"]
        cash = db.execute("select cash from users where id = ?", id)
        q=qty
        qty = (price * qty)
        c = cash[0]["cash"]
        price = float(c)
        amt = price - qty
        # UPDATE employees SET lastname = 'Smith' WHERE employeeid = 3;
        # updating the amount in users table
        db.execute("UPDATE users SET cash = ? where id = ?", amt, id)
        # determining current Date
        curDate = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        # creating history by adding the transaction to history table
        db.execute("INSERT INTO history (userId,symbol,actionType,shares,price,transDate) VALUES (?,?,?,?,?,?)",id,symbol,'BUY',q,qty,curDate)

        try:
            row = db.execute("SELECT * FROM holdings WHERE userId = :userId AND symbol = :symb",userId=id, symb = symbol)
            if row:
                share = q + row[0]["shares"]
                share = int(share)
                db.execute("UPDATE holdings SET shares = ? where userId =? AND symbol = ?", share, id, symbol)
            else:
                db.execute("INSERT INTO holdings (userId,symbol,name,shares) VALUES (?,?,?,?)",id, symbol,company,q)
            pass
        except:
            db.execute("INSERT INTO holdings (userId,symbol,name,shares) VALUES (?,?,?,?)",id, symbol,company,q)
            pass
        return redirect("/")
    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    return apology("TODO")

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))
        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "POST":
        if not request.form.get("symbol"):
            return apology("Symbol is blank")
        symbol = request.form.get("symbol")
        quote = lookup(symbol)
        if not quote:
            return apology("Symbol is not valid")
        company = quote["name"]
        price = usd(quote["price"])
        # price = str(quote["price"])
        
        # content = "A share of " + company + " " + symbol + " costs $:" + price
        # return render_template("quote.html", company = company, price = price, symbol = symbol)
        # Having this variable called number in both post and get
        #  methods to determine which part to executed in html file
        return render_template("quote.html", company = company, symbol = symbol, price = price, number = 1)

    else:
        return render_template("quote.html", number = 0)


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":

        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Make sure password and confirm password are same
        elif request.form.get("password") != request.form.get("confirmation"):
            return apology("password and confirm password must be same", 403)

        user = request.form.get("username")
        passw = request.form.get("password")
        h = generate_password_hash(passw)
        # return redirect("/")
        # Inserting the values into db
        # db.execute("insert into users (?, ?)", (*request.form.get("username"),*request.form.get("password"))
        db.execute("INSERT INTO users (id,username,hash) VALUES (NULL,?,?)",user,h)

        # Returning to login page
        return redirect("/")
    else:
        return render_template("/register.html")



@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    return apology("TODO")


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
