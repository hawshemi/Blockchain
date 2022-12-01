from os import chdir, listdir, remove, getcwd
from flask import Flask, render_template, request, flash
import datetime

from block import *


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


# Main index - Blockchain Validity Check
@app.route('/')
def check():
    results = check_integrity()
    return render_template('index.html', checking_results=results)


# Make a Transaction
@app.route('/send', methods=['GET', 'POST'])
def send():
    if request.method == 'POST':
        reciever = request.form.get('reciever')
        sender = request.form.get('sender')
        amount = request.form.get('amount')

        write_block(reciever=reciever, sender=sender, amount=amount)

    return render_template('send.html')


# Shows all transactions history table
@app.route('/history', methods=['GET', 'POST'])
def history():
    """Show history of transactions"""
    # Query database for displying everything
    transactions = db.execute("""
        SELECT id, reciever, sender, amount, timestamp, tx_id
        FROM transactions
        """)
    return render_template("history.html", transactions=transactions)


#Reset the Blockchian - Delete All blocks except genesis block and clear the Database.
@app.route('/delete', methods=['GET', 'POST'])
def delete():
    db.execute("DELETE FROM transactions")
    delete_from('blockchain', ['1'])
    return render_template("history.html")


if __name__ == '__main__':
        app.run(debug=True)