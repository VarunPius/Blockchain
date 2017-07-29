import hashlib
import datetime as date


class Block:
    def __init__(self, idx, ts, data, prev_hash):
        self.idx = idx
        self.ts = ts
        self.data = data
        self.prev_hash = prev_hash
        self.curr_hash = self.hash_generator()

    def hash_generator(self):
        sha = hashlib.sha256()
        sha.update(str(self.idx) + str(self.ts) + str(self.data) + str(self.prev_hash))
        return sha.hexdigest()


def create_genesis_block():
    # Genesis block is the first block of a blockchain. We manually create it with an idx 0 and random hash
    print "Generating Genesis block"
    genesis_block = Block(0, date.datetime.now(), "First Block", "0")
    print "Genesis Block idx: {}".format(genesis_block.idx)
    print "Genesis Block Hash: {}".format(genesis_block.curr_hash)
    return genesis_block


def create_next_block(last_block):
    idx = last_block.idx + 1
    ts = date.datetime.now()
    data = "Block number: " + str(idx)
    prev_hash = last_block.curr_hash
    return Block(idx, ts, data, prev_hash)


blockchain_list = [create_genesis_block()]
prev_block = blockchain_list[0]

nos_of_blocks = 5

for i in range(0, nos_of_blocks):
    new_block = create_next_block(prev_block)
    blockchain_list.append(new_block)

    print "Block number: {} added to chain".format(new_block.idx)
    print "Hash of the block: {}".format(new_block.curr_hash)

    prev_block = new_block
