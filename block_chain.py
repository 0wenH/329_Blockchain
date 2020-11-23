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


        # create a json object that contains all the fields of the block
        # https://www.geeksforgeeks.org/reading-and-writing-json-to-a-file-in-python/
        #
        json_obj = json.dumps(self.__dict__, indent=4, sort_keys=True)
        
        file_name = "block_" + str(self.index) + ".json"
        with open(file_name, "w") as outfile:
            outfile.write(json_obj)



    # returns the computed SHA256 hash of the blocks json object
    def get_hash(self):
        dump = json.dumps(self.__dict__, indent=4, sort_keys=True)
        return sha256(dump.encode()).hexdigest()
        
class Block_chain:
    # difficulty of proof of work algorithm
    diff = 4

    # on creation, create empty lists for unconfirmed transactions and chain
    # and create the genesis block
    def __init__(self):
        self.unconfirmed_transactions = []
        self.chain = []
        self.create_genesis_block()


    # property for getter of most recent block
    # https://www.geeksforgeeks.org/getter-and-setter-in-python/
    @property
    def last_block(self):
        return self.chain[-1]


    """
    creates genesis block with default and empty values
    then appends it to the chain.
    
    hash will not be computed using previous hash (since there is none)
    and will not go through the proof of work

    params: none, returns: none
    """
    def create_genesis_block(self):
        genesis_block = Block(0, [], time.time(), "0")
        genesis_block.hash = genesis_block.get_hash()
        self.chain.append(genesis_block)

    

    """
    add_block: adds a block to the chain, if it is valid
        a valid block will match the previous hash of the last block
        and have a valid proof of work
    
    Params:
        block: block object to add
        proof: hash that conforms to proof of work rules
    
    Returns:
        bool: True if the block was valid and added, false otherwise
    """
    def add_block(self, block, proof):

        # actual previous hash of the last block
        real_prev_hash = self.last_block.hash

        # if the previous hash of the input block doesn't match the actual previous hash
        # return false and don't add the block
        if real_prev_hash != block.previous_hash:
            return False

        # if the proof of work is not valid, return false and don't add it
        if not self.is_valid_proof(block, proof):
            return False

        # the proof of work is valid, add the block and return true
        block.hash = proof
        self.chain.append(block)
        return True


    """
    is_valid_proof: checks if the computed hash starts with the right amount of zeroes
        and is the same hash as the one of the block
    """
    def is_valid_proof(self, block, block_hash):
        return (block_hash.startswith('0' * Block_chain.diff) and block_hash == block.get_hash())


    """
    proof_of_work: computes a hash with difference nonce values until hash satisfies criteria
        uses brute force to increment nonce until hash is found
    
    params: block: block to compute hash of
    returns: computed_hash: string of hash that was computed
    """
    def proof_of_work(self, block):

        # begin at 0 and keep incrementing
        #block.nonce = 0

        # while the hash does not begin with difficulty number of 0's
        # increment the block's nonce and calculate the hash again
        computed_hash = block.get_hash()
        while not computed_hash.startswith('0' * Block_chain.diff):
            block.nonce += 1
            computed_hash = block.get_hash()

        return computed_hash

    """
    append a transaction to unconfirmed pool
    """
    def add_new_transaction(self, transaction):
        self.unconfirmed_transactions.append(transaction)

    """
    mine: mines a new block containing all unconfirmed transactions

    params: none
    returns: 
        false: if there are no pending transactions and thus no blocks to add
        new_block.index: index of the newly added block
    """
    def mine(self):
        
        # if no transactions / blocks to mine
        if not self.unconfirmed_transactions:
            return False

        last_block = self.last_block

        # create a new block with all pending transactions
        new_block = Block(index=last_block.index + 1, transactions=self.unconfirmed_transactions, timestamp=time.time(), previous_hash=last_block.hash)

        # perform the proof of work
        proof = self.proof_of_work(new_block)

        # attempt to add the block to the chain with the newly computed proof of work
        self.add_block(new_block, proof)

        # reset transaction pool
        self.unconfirmed_transactions = []
        return new_block.index



####################################################################################################
# end of classes code
# beginning of interface
#################################

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


# prints a big string
def show_commands():
    print("\nEnter \"buy\" to make a transaction" + \
    "\nEnter \"mine\" to mine a new block, containing your just entered transactions" + \
    "\nEnter \"show\" to show the details of the most recent block" + \
    "\nEnter \"wallet\" to access the wallet interface" + \
    "\n\nEnter \"exit\" to exit" + \
    "\nEnter \"help\" to show these commands\n")



def main():

    # delete all pre-existing json files
    # may want to change this
    rm_json()    

    # initialize a new blockchain object
    chain = Block_chain()

    show_commands()

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
            print("mining new block with difficulty of " + str(chain.diff) + " ...")
            chain.mine()
            print("Mining successful! New block added to chain")

         #if input is "show", print the last block and all of its fields
        elif (inp == "show"):
            print("Last block:" + \
            "\n Index: " + str(chain.last_block.index) + \
            "\n Transactions: " + str(chain.last_block.transactions) + \
            "\n Time: " + str(chain.last_block.timestamp) + \
            "\n Previous Hash: " + str(chain.last_block.previous_hash) + \
            "\n This Block Hash: " + str(chain.last_block.hash) + \
            "\n Nonce: " + str(chain.last_block.nonce))

        #add elif to avoid else case, can change loop to while(true) and change continue to break;
        elif (inp == "exit"):
            continue



        #elif (inp == "wallet"):
            #wallet

        elif (inp == "help"):
            show_commands()

        #if input is wrong format, continue
        else:
            print("invalid command")



if __name__ == "__main__":
    main()