# **Blockchain**

## **A Simple Blockchain By Hawshemi**
### **Live Website: https://blockchain.up.railway.app**
#### Video Demo: https://youtu.be/iEPosDOyiPg
_This project submitted at CS50 Final Project._


---
## Website Features
- Registration and Logins with password hashing.
- Password Validation Check
- Handle Errors with codes.
- Check the Blockchain integrity.
- Make a Transaction on the blockchain.
- Review the Transaction History Table.
- Ability to export to XLS.
- Ability to Reset the blockchain.
- Logout

## The Blockchain
- Stores the block information on a JSON file.
- Read the JSON and view to blocks.
- Validate the blocks using their hash.
- Store the JSON and blocks in a Database.

## Database and Tables
The database consists of 3 tables:
- The _users_ containing userid, username and hashed password.
- The _sequence_ that stores the number of users and transactions.
- The _transcaction_ table contains all block information, including number, receiver, sender, amount, timestamp, and transaction_id.

Users can see the blockchain integrity on the main page after login. But they can only see their transactions in the history tab.

## Tech Stack
The site was built using Flask(Python), SQLite3 for the database, CSS for Styling and some Javascript for button actions, exports, and background particles.

---
# How to run
## This repo is hosted on [blockchain.up.railway.app](https://blockchain.up.railway.app).

### For Local Run:
0. Clone the GitHub project.

1. go to `main.py` and at the end of the file, edit:

    ```
    if __name__ == "__main__":
        app.run(debug=True, host='0.0.0.0', port=os.getenv("PORT", default=5000))
    ```
    To:

    ```
    if __name__ == "__main__":
        app.run(debug=True)
    ```


2. Create a virtual environment of python and then run:

    ```
    pip install -r requirements.txt
    ```

    And then: 

    ```
    python main.py
    ```

---
# How this works?
First, we have a `blockchain` folder which contains the blocks JSON.

The blocks are created in the `block.py` file (`def write_block`). The Genesis block is file number `1` in the folder(DO NOT DELETE THIS FILE). For hashing, it uses the `hashlib` library. 

`hashlib.md5(content).hexdigest()`

When a new block is created, it generates a hash, and then the old hash is compared to the new one for an integrity check.

In `main.py`, the flask app would run, and all the routing for HTML.

---
For more information of how blockchians work:
https://www.investopedia.com/terms/b/blockchain.asp
