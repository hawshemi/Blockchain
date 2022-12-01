from flask import Flask
from flask import render_template
from flask import request

from block import write_block, check_integrity


app = Flask(__name__)


@app.route('/send', methods=['GET', 'POST'])
def send():
    if request.method == 'POST':
        reciever = request.form.get('reciever')
        sender = request.form.get('sender')
        amount = request.form.get('amount')

        write_block(reciever=reciever, sender=sender, amount=amount)

    return render_template('send.html')


@app.route('/')
def check():
    results = check_integrity()
    return render_template('index.html', checking_results=results)


if __name__ == '__main__':
    app.run(debug=True)