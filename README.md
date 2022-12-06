# **Blockchain**
## **A Simple Blockchain By Hawshemi**
### **Live Website: https://blockchain.up.railway.app**
_This project submitted at CS50 Final Project._

---
## Website Features
- Registration and Logins with password hashing.
- Password Validation Check
- Handle Errors with codes.
- Check the Blockchain intergrity.
- Make a Transaction on blockchain.
- Review the Transaction History Table.
- Ability to export to XLS.
- Ability to Reset the Blockchian.
- Logout

## The Blockchain
- Stores the block information on a JSON file.
- Read the JSON and view to blocks.
- Validate the blocks using its hash.
- Store the JSON and blocks to a Database.

## Database and Tables
The databse consist of 3 tables. first is the users containing userid, username and hashed password. second is the sequence that stores number of users and transactions. third is the transcaction table which contain all of the blocks information including number, reciver, sender, amount, timestamp, and transaction_id.

Users can see the blockchain integrity in the main page after login. but they can only see their transactions in the history tab.

## Tech Stack
The site was built using Flask(Python), SQLite3 for the database, CSS for Styling and some Javascript for button actions, exports, and background particles.

---
# How to run
## This repo is hosted on [blockchain.up.railway.app](https://blockchain.up.railway.app).

### For Local Run:
0. Clone the github project.

1. go to `main.py` and at the end of the file edit:

    ```
    if __name__ == "__main__":
        app.run(debug=True, host='0.0.0.0', port=os.getenv("PORT", default=5000))
    ```
    To:

    ```
    if __name__ == "__main__":
        app.run(debug=True)
    ```


2. Create a virtual environmnet of python and then run:

    ```
    pip install -r requirements.txt
    ```

    And then: 

    ```
    python main.py
    ```

---
