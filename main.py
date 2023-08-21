from os import chdir, listdir, remove, getcwd
from flask import Flask, render_template, request, flash, session, redirect
from flask_session import Session
import re
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from block import *
from helpers import *


app = Flask(__name__)


# A nice Secret Key for flash messages
app.config['SECRET_KEY'] = '69'


# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True


# Ensure responses aren't cached
@app.after_request
def after_request(response):

    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


# A function for resetting blockchain (Deleting all blocks in folder except the genesis) 
def delete_from(directory: str, keep: list) -> None:

    cwd = getcwd()
    try:
        chdir(directory)
        for file in listdir():
            if not file in keep:
                remove(file)
    finally:
        chdir(cwd)


# Evoid redondemcy by using is_provided function
def is_provided(field):

    if not request.form.get(field):
        return error(f"MUST PROVIDE {field}", 400)


# Main index - Blockchain Validity Status
@app.route('/')
@login_required
def check():
    username0 = db.execute("""
        SELECT username FROM users
        WHERE id=:user_id""", user_id=session["user_id"])
    username = (str(username0)).strip().replace("username","").replace(":","").replace("[{","").replace("'}]","").replace("''","").replace("'","") # Yea, I know... (-_-)
    
    results = check_integrity()
    return render_template('index.html', checking_results=results, username=username)


# Make a Transaction
@app.route('/send', methods=['GET', 'POST'])
@login_required
def send():

    if request.method == 'POST':
        reciever = request.form.get('reciever')
        sender = request.form.get('sender')
        amount = request.form.get('amount')

        # Check if all fields are correct and filled.
        result_check = is_provided("reciever") or is_provided("sender") or is_provided("amount")

        if result_check != None:
            return result_check

        write_block(reciever=reciever, sender=sender, amount=amount)
        
        flash(f"Transaction Created: {sender} sent {'$'+ amount} to {reciever}")

    return render_template('send.html')


# Shows all transactions history table
@app.route('/history', methods=['GET', 'POST'])
@login_required
def history():

    transactions = db.execute("""
        SELECT id, reciever, sender, amount, timestamp, tx_id
        FROM transactions WHERE user_id=:user_id
        """, user_id=session["user_id"])

    return render_template("history.html", transactions=transactions)


#Reset the Blockchian - Delete All blocks except genesis block and clear the Database.
@app.route('/delete', methods=['GET', 'POST'])
@login_required
def delete():

    # Delete the transactions & sequence in database file
    db.execute("DELETE FROM transactions")
    db.execute("DELETE FROM sqlite_sequence WHERE name = 'transactions'")

    # Delete all files in blockchain directory except first one (Genesis Block)
    delete_from('blockchain', ['1'])

    flash('Blockchain Resetted.')

    return render_template("history.html")


#Log user in
@app.route("/login", methods=["GET", "POST"])
def login():

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username and password was submitted
        result_check = is_provided("username") or is_provided("password")
        if result_check is not None:
            return result_check

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username").lower())

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return error("INVALID USERNAME AND/OR PASSWORD", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


# Log user out
@app.route("/logout")
def logout():

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


# Password Validation Function
def validate(password):

    if len(password) < 8:
        return error("Password should be at least 8 characters.")
    # elif not re.search("[0-9]", password):
        # return error("PASSWORD MUST CONTAIN AT LEAST ONE DIGIT.")
    # elif not re.search("[A-Z]", password):
        # return error("PASSWORD MUST CONTAIN AT LEAST ONE UPPERCASE LETTER.")
    # elif not re.search("[@_!#$%&^*()<>?~+-/\{}:]", password):
        # return error("PASSWORD MUST CONTAIN AT LEAST ONE SPECIAL CHARACTER.")


# Register a new user
@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":
        # Ensure username password and confirmation was provided
        result_check = is_provided("username") or is_provided("password") or is_provided("confirmation")

        if result_check != None:
            return result_check

        # Validate the user password
        validation_errors = validate(request.form.get("password"))
        if validation_errors:
            return validation_errors

        # Ensure password and confirmation match
        if request.form.get("password") != request.form.get("confirmation"):
            return error("PASSWORDS DOES NOT MATCH.")

        # Query database for username
        try:
            prim_key = db.execute("INSERT INTO users (username, hash) VALUES (:username, :hash)",
                                  username=request.form.get("username").lower(),
                                  hash=generate_password_hash(request.form.get("password")))
        except:
            return error("USERNAME ALREADY EXISTS.", 400)

        if prim_key is None:
            return error("REGISTRATION ERROR.", 403)

        # Remember which user has logged in
        session["user_id"] = prim_key

        flash("Registered!")
        return redirect("/")

    else:
        return render_template("register.html")

# Handle Error
def errorhandler(e):

    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return error(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=os.getenv("PORT", default=5000))
