import json
import os
import hashlib
import datetime

from cs50 import SQL


db = SQL("sqlite:///tx.db")

timestamp = str(datetime.datetime.now(datetime.timezone.utc))
BLOCKCHAIN_DIR = 'blockchain/'


# Calculate the Block Hash
def get_hash(prev_block):
    with open(BLOCKCHAIN_DIR + prev_block, 'rb') as f:
        content = f.read()
    return hashlib.md5(content).hexdigest()


# Check the blockchain integrity
def check_integrity():
    files = sorted(os.listdir(BLOCKCHAIN_DIR), key=lambda x: int(x))

    results = []

    for file in files[1:]:
        with open(BLOCKCHAIN_DIR + file) as f:
            block = json.load(f)

        prev_hash = block.get('prev_block').get('hash')
        prev_filename = block.get('prev_block').get('filename')

        actual_hash = get_hash(prev_filename)

        if prev_hash == actual_hash:
            res = 'OK'
        else:
            res = 'NOTOK'

        print(f'Block {prev_filename}: {res}')
        results.append({'block': prev_filename, 'results': res})
    return results


# Make the next Block
def write_block(reciever, sender, amount):

    blocks_count = len(os.listdir(BLOCKCHAIN_DIR))
    prev_block = str(blocks_count)
    tx_id = get_hash(prev_block)
    data = {
        "reciever": reciever,
        "sender": sender,
        "amount": amount,
        "timestamp": timestamp,
        "prev_block": {
            "hash": get_hash(prev_block),
            "filename": prev_block
        }
    }

    current_block = BLOCKCHAIN_DIR + str(blocks_count + 1)

    with open(current_block, 'w') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
        f.write('\n')
        # Also export the data to a table in a database
        db.execute("""
                INSERT INTO transactions
                    (id, sender, reciever, amount, timestamp, tx_id)
                VALUES (:id, :sender, :reciever, :amount, :timestamp, :tx_id)
            """,
                    id=prev_block,
                    sender=sender,
                    reciever=reciever,
                    amount=amount,
                    timestamp=timestamp,
                    tx_id=tx_id
                    )

def main():
    check_integrity()


if __name__ == '__main__':
    main()