import time
import hashlib

class Block:
    def __init__(self, index, timestamp, transactions, proof, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.transactions = transactions
        self.proof = proof
        self.previous_hash = previous_hash

    def __str__(self):
        return "B{index: %d time: %f transactions: %s proof: %s previous_hash: %s}" % (self.index, self.timestamp, str([str(s) for s in self.transactions]), self.proof, self.previous_hash)

class Transaction:
    def __init__(self, sender, recipient, amount):
        self.sender = sender
        self.recipient = recipient
        self.amount = amount

    def __str__(self):
        return "T{s: %s, r: %s, a: %d}" % (self.sender, self.recipient, self.amount)

def hash_block(block):
    return hashlib.sha256(str(block).encode()).hexdigest()

def valid_proof(previous_hash, previous_proof, proof):
    s = "{%s %s %s}" % (previous_hash, previous_proof, proof)
    h = hashlib.sha256(s.encode()).hexdigest()
    if h[:3] == '000':
        #print("proof block was:", h)
        return True

def proof_of_work(previous_hash, previous_proof):
    proof = 1
    while not valid_proof(previous_hash, previous_proof, proof):
        proof += 1
    return proof

def new_block(previous_block, transactions):
    index = previous_block.index + 1
    timestamp = time.time()
    previous_proof = previous_block.proof
    previous_hash = hash_block(previous_block)
    proof = proof_of_work(previous_hash, previous_proof)
    return Block(index, timestamp, transactions, proof, previous_hash)

def main():
    b0 = Block(0, time.time(), [Transaction("me", "me", 1)], "", "")
    chain = [b0]
    t0 = Transaction("a", "b", 10)
    t1 = Transaction("me", "me", 1)
    b1 = new_block(b0, [t0, t1])
    chain.append(b1)
    print([str(b) for b in chain])

if __name__ == '__main__':
    main()

