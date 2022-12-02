import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///birthdays.db")

@app.route("/", methods=["GET", "POST"])
def index():
    # Page is accessed via POST (user submitted form)
    if request.method == "POST":

        # TODO: Add the user's entry into the database
        # Access form entries
        name = request.form.get("name")
        month = request.form.get("month")
        day = request.form.get("day")

        # If name already exists in database, modify the birthday
        if db.execute("SELECT * FROM birthdays WHERE name=?", name):
            db.execute("UPDATE birthdays SET month=?, day=? WHERE name=?", month, day, name)

        # If name does not exist in database, create a new entry
        else:
            db.execute("INSERT INTO birthdays (name, month, day) VALUES (?, ?, ?)", name, month, day)

        # Refreshes page via GET
        return redirect("/")

    # Page is accessed via GET
    else:

        # TODO: Display the entries in the database on index.html
        people = db.execute("SELECT * FROM birthdays")
        return render_template("index.html", people=people)

@app.route("/delete", methods=["POST"])
def delete():

    # Access form entries
    name = request.form.get("name")

    # Only delete entry if name is in database
    if db.execute("SELECT name FROM birthdays WHERE name=?", name):
        db.execute("DELETE FROM birthdays WHERE name=?", name)

    return redirect("/")