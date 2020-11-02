from hashlib import sha256
import json
import time
import os
import glob

class Block:
    def __init__(self, index, transactions, timestamp, previous_hash):
        self.index = index
        self.transactions = transactions
        self.timestamp = timestamp
        self.previous_hash = previous_hash
        self.nonce = 0

        #Logans code
        # https://www.geeksforgeeks.org/reading-and-writing-json-to-a-file-in-python/

        self.json_obj = json.dumps(self.__dict__, indent=4, sort_keys=True)
        
        file_name = "block_" + str(self.index) + ".json"
        with open(file_name, "w") as outfile:
            outfile.write(self.json_obj)


    # I edited this, no need to change
    def compute_hash(self):
        """
        A function that return the hash of the block contents.
        """
        dump = json.dumps(self.__dict__, indent=4, sort_keys=True)
        return sha256(dump.encode()).hexdigest()


class Blockchain:
    # difficulty of our PoW algorithm
    difficulty = 3

    def __init__(self):
        self.unconfirmed_transactions = []
        self.chain = []
        self.create_genesis_block()

    def create_genesis_block(self):
        """
        A function to generate genesis block and appends it to
        the chain. The block has index 0, previous_hash as 0, and
        a valid hash.
        """
        genesis_block = Block(0, [], time.time(), "0")
        genesis_block.hash = genesis_block.compute_hash()
        self.chain.append(genesis_block)

    @property
    def last_block(self):
        return self.chain[-1]

    def add_block(self, block, proof):
        """
        A function that adds the block to the chain after verification.
        Verification includes:
        * Checking if the proof is valid.
        * The previous_hash referred in the block and the hash of latest block
          in the chain match.
        """
        previous_hash = self.last_block.hash

        if previous_hash != block.previous_hash:
            return False

        if not self.is_valid_proof(block, proof):
            return False

        block.hash = proof
        self.chain.append(block)
        return True

    def is_valid_proof(self, block, block_hash):
        """
        Check if block_hash is valid hash of block and satisfies
        the difficulty criteria.
        """
        return (block_hash.startswith('0' * Blockchain.difficulty) and
                block_hash == block.compute_hash())

    def proof_of_work(self, block):
        """
        Function that tries different values of nonce to get a hash
        that satisfies our difficulty criteria.
        """
        block.nonce = 0

        computed_hash = block.compute_hash()
        while not computed_hash.startswith('0' * Blockchain.difficulty):
            block.nonce += 1
            computed_hash = block.compute_hash()

        return computed_hash

    def add_new_transaction(self, transaction):
        self.unconfirmed_transactions.append(transaction)

    def mine(self):
        """
        This function serves as an interface to add the pending
        transactions to the blockchain by adding them to the block
        and figuring out Proof Of Work.
        """
        if not self.unconfirmed_transactions:
            return False

        last_block = self.last_block

        new_block = Block(index=last_block.index + 1,
                          transactions=self.unconfirmed_transactions,
                          timestamp=time.time(),
                          previous_hash=last_block.hash)

        proof = self.proof_of_work(new_block)
        self.add_block(new_block, proof)

        self.unconfirmed_transactions = []
        return new_block.index



###########################################################################
# everything above here is straight from 
# https://developer.ibm.com/technologies/blockchain/tutorials/develop-a-blockchain-application-from-scratch-in-python/
# 
# we need to edit this code to make it our's and not get copyrighted.
############
# everything below, I wrote as a simple user menu. 


"""
 delete all pre-existing json files
 done at setup to initialize a new chain
 https://stackoverflow.com/questions/185936/how-to-delete-the-contents-of-a-folder
"""
def rm_json():

    cwd = os.getcwd()
    dir_json = cwd + "/*.json"

    files = glob.glob(dir_json)
    for f in files:
        os.remove(f)

def main():

    # delete all pre-existing json files
    # json files will exist after executing the python program
    # so that the wallet program can access them
    rm_json()    

    # initialize a new blockchain object
    chain = Blockchain()

    print("\nEnter \"buy\" to make a transaction")
    print("Enter \"mine\" to mine a new block, containing your just entered transactions")
    print("Enter \"show\" to show the details of the most recent block\n")

    inp = ""
    while (inp != "exit"):
        inp = raw_input("\nenter command: ")


        # if input is "buy", enter transaction menu
        if (inp == "buy"):
            print("\nFormat for Transactions, separated with spaces: from(str), to(str), amount(int)")
            print("eg: enter transaction: John Bob 5\n")
            
            # process transaction as string with three values, separated by spaces
            trans_inp = raw_input("enter your transaction: ")
            trans = trans_inp.split()
            if (len(trans) != 3):
                print("invalid transaction")
            else:    
                print("Your transaction: " + \
                "   \nfrom: " + trans[0] + ", to: " + trans[1] + ", amount: " + trans[2])
                
                # confirm or cancel transaction
                conf = raw_input("\nConfirm transaction (y/n): ")
                if(conf == "y"):
                    chain.add_new_transaction(trans)
                else:
                    print("transaction discarded.. returning to main menu")


        # if input is "mine", call mine function
        # program will mine a new block and user will have to wait
        elif (inp == "mine"):
            print("mining new block with difficulty of " + str(chain.difficulty) + " ...")
            chain.mine()
            print("Mining successful! New block added to chain")

         #if input is "show", print the last block and all of its fields
        elif (inp == "show"):
            print("Last block:" + \
            "\n Index: " + str(chain.last_block.index) + \
            "\n Transactions: " + str(chain.last_block.transactions) + \
            "\n Time: " + str(chain.last_block.timestamp) + \
            "\n Previous Hash: " + str(chain.last_block.previous_hash) + \
            "\n Nonce: " + str(chain.last_block.nonce))

        #add elif to avoid else case, can change loop to while(true) and change continue to break;
        elif (inp == "exit"):
            continue;
        #if input is wrong format, continue
        else:
            print("invalid command")

if __name__ == "__main__":
    main()