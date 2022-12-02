import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime

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

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


# /INDEX TODO - done
@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""

    # Final list of dicts which contain all required info for HTML table
    stocks_final = []

    # Initialise grand total
    grand_total = 0

    # Search portfolio table, saving each row of stocks as a dict in stocks_raw
    stocks_raw = db.execute("SELECT symbol, shares FROM portfolio WHERE user_id=?", session["user_id"])

    # Iterate through each stock, finding its symbol, name, shares, price, total
    for stock_raw in stocks_raw:

        # Obtain required fields
        symbol = stock_raw["symbol"]
        shares = stock_raw["shares"]
        quote = lookup(symbol)
        name = quote["name"]
        price = quote["price"]
        total = shares * price

        # Append info to new dict
        stock_final = {
            "symbol": symbol,
            "name": name,
            "shares": shares,
            "price": usd(price),
            "total": usd(total)
        }

        # Add new stock dict to list
        stocks_final.append(stock_final)

        # Add each stock's value to grand_total
        grand_total += total

    # Search for user's remaining cash
    cash_raw = db.execute("SELECT cash FROM users WHERE id=?", session["user_id"])
    cash_int = cash_raw[0]["cash"]
    cash_final = usd(cash_int)

    # Add remaining cash to grand_total
    grand_total += cash_int
    grand_total = usd(grand_total)

    return render_template("index.html", stocks=stocks_final, cash=cash_final, grand_total=grand_total)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username")

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password")

        # Query users table for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password")

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


# /REGISTER TODO - done
@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    # User reached route via GET (by clicking on link)
    if request.method == "GET":
        return render_template("register.html")

    # User reached route via POST (by submitting registration form)
    else:

        # Access form data
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        # Check for valid form inputs
        # Username field empty
        if not username:
            return apology("username field is empty!")

        # Username already exists
        elif db.execute("SELECT * FROM users WHERE username=?", username):
            return apology("username is already in use")

        # Password field empty
        elif not password or not confirmation:
            return apology("password field is empty!")

        # Passwords do not match
        elif password != confirmation:
            return apology("passwords do not match!")

        # Add user to users table
        db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", username, generate_password_hash(password))

        # Query users table for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", username)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")


# /BUY TODO - done
@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""

    # User reached route via GET (by clicking on link)
    if request.method == "GET":
        return render_template("buy.html")

    # User reached route via POST (by submitting shares)
    else:

        # Access form data
        symbol_raw = request.form.get("symbol")
        shares_bought_raw = request.form.get("shares")

        # Ensure symbol and shares are filled in
        if not symbol_raw or not shares_bought_raw:
            return apology("must provide stock symbol and number of shares")

        # Ensure shares is an integer - non-negative, non-decimal
        try:
            shares_bought = int(shares_bought_raw)
        except ValueError:
            return apology("number of shares must be an integer")
        if shares_bought <= 0:
            return apology("must provide a valid number of shares")

        # Obtain quote - quote is a dict with 3 keys
        quote = lookup(symbol_raw)

        # Invalid symbol
        if quote == None:
            return apology("invalid symbol")

        # Initialise variables
        symbol = quote["symbol"]  # ensures symbol is all caps
        name = quote["name"]
        price = quote["price"]
        cost = shares_bought * price

        # Lookup balance in user's account
        cash_raw = db.execute("SELECT cash FROM users WHERE id=?", session["user_id"])
        cash = cash_raw[0]["cash"]

        # User cannot afford shares
        if cost > cash:
            return apology("you do not have enough cash to complete this transaction")

        # Update users table
        db.execute("UPDATE users SET cash = cash - ? WHERE id=?", cost, session["user_id"])

        # Update transactions table
        db.execute("INSERT INTO transactions VALUES (?, ?, ?, ?, ?)",
                   session["user_id"], symbol, shares_bought, price, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

        # Update portfolio table
        # If no entry for current symbol, insert new row
        current = db.execute("SELECT shares FROM portfolio WHERE user_id=? AND symbol=?", session["user_id"], symbol)
        if not current:
            db.execute("INSERT INTO portfolio (user_id, symbol, shares) VALUES (?, ?, ?)",
                       session["user_id"], symbol, shares_bought)

        # Entry already exists, update entry
        else:
            db.execute("UPDATE portfolio SET shares = shares + ? WHERE user_id=? AND symbol=?",
                       shares_bought, session["user_id"], symbol)

        # Update companies table
        company = db.execute("SELECT name FROM companies WHERE symbol=?", symbol)
        if not company:
            db.execute("INSERT INTO companies (symbol, name) VALUES (?, ?)", symbol, name)

        return redirect("/")


# /SELL TODO - done
@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""

    # User reached route via GET (by clicking on link)
    if request.method == "GET":

        # Retrieve user's owned stocks as a list of dicts
        stocks = db.execute("SELECT symbol FROM portfolio WHERE user_id=?", session["user_id"])

        return render_template("sell.html", stocks=stocks)

    # User reached route via POST (by submitting sell form)
    else:

        # Access form data
        symbol = request.form.get("symbol")
        shares_sold_raw = request.form.get("shares")

        # Check for valid form inputs
        # Ensure symbol and shares are filled in
        if not symbol or not shares_sold_raw:
            return apology("must provide stock symbol and number of shares")

        # Query portfolio table for number of owned shares
        shares_owned_raw = db.execute("SELECT shares FROM portfolio WHERE user_id=? AND symbol=?",
                                      session["user_id"], symbol)

        # Ensure user owns at least 1 stock
        if not shares_owned_raw:
            return apology("no stocks owned for this company!")

        # Initialise variables
        shares_owned = shares_owned_raw[0]["shares"]
        shares_sold = int(shares_sold_raw)
        price = lookup(symbol)["price"]
        revenue = shares_sold * price

        # Ensure user does not sell more stocks than owned
        if shares_owned < shares_sold:
            return apology("you do not own sufficient stocks!")

        # Update users table
        db.execute("UPDATE users SET cash = cash + ? WHERE id=?", revenue, session["user_id"])

        # Update transactions table
        db.execute("INSERT INTO transactions VALUES (?, ?, ?, ?, ?)",
                   session["user_id"], symbol, shares_sold * -1, price, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

        # Update portfolio table
        # If there are leftover stocks, update row
        if shares_owned > shares_sold:
            db.execute("UPDATE portfolio SET shares = shares - ? WHERE user_id=? AND symbol=?",
                       shares_sold, session["user_id"], symbol)

        # If all owned shares are sold, delete row
        elif shares_owned == shares_sold:
            db.execute("DELETE FROM portfolio WHERE user_id=? AND symbol=?", session["user_id"], symbol)

            # Remove company from companies table
            db.execute("DELETE FROM companies WHERE symbol=?", symbol)

        return redirect("/")


# /QUOTE TODO - done
@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""

    # User reached route via GET (by clicking on link)
    if request.method == "GET":
        return render_template("quote.html")

    # User reached route via POST (by submitting quote)
    else:

        # Lookup symbol and store as quoted (dict with 3 keys - name, price, symbol)
        symbol = request.form.get("symbol")
        quote = lookup(symbol)

        # Ensure symbol is filled in
        if not symbol:
            return apology("must provide stock symbol")

        # Ensure symbol is valid
        if quote == None:
            return apology("must provide valid stock symbol")

        # Access individual fields of quoted dict
        name = quote["name"]
        symbol = quote["symbol"]
        price = usd(quote["price"])

        return render_template("quoted.html", name=name, symbol=symbol, price=price)


# /HISTORY TODO - done
@app.route("/history")
@login_required
def history():
    """Show history of transactions"""

    # Query transactions from transactions table
    transactions = db.execute('''SELECT transactions.symbol, transactions.shares, transactions.price, transactions.transacted, companies.name
        FROM transactions INNER JOIN companies ON companies.symbol=transactions.symbol WHERE user_id=?''', session["user_id"])

    # Reverse order of transactions list so latest transaction appears at top of table
    transactions.reverse()

    return render_template("history.html", transactions=transactions)


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
