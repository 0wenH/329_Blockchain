# 329_Blockchain
CPSC 329 repository for group project Blockchain

----------------- nov 23-------------------
created rudimentary wallet app

added comments and did some rewriting of tutorial code, still lots more to do
------------------------



--------- Nov. 2---------------------
I made it so that the block class creates a json file upon creation.
Upon starting the program, all old json files will be deleted. 
After the program is finished running, the json files will still exist.
This is so that the "wallet" app can view them.


-------------------- Nov. 1 ---------------
I used the code from this tutorial 
https://developer.ibm.com/technologies/blockchain/tutorials/develop-a-blockchain-application-from-scratch-in-python/

up to section 6, where it begins to create a web interface.

I dowloaded the source python code, and added a simple main menu for interaction.
Currently the menu can create transactions, mine a new block and add it to the chain, and show the values of the most recent block.

You guys should try it out, it is pretty easy I think.
After you add some blocks (with whatever data you want, see below), then you mine them.
After adding at least two, you can see the previous hash will have "n-leading zeroes".
Changing the difficulty field in the BlockChain class will increase number of leading zeroes,
and increases the time of the mine function by a lot. 

I think we should add functionality to change the difficulty, which should be easy, 
so that we can showcase the mining time.

As of now, most of the functionality is there, but still things to do.

############################
Things that still need to be done:
  1. We have to change all of the code that I got from the tutorial so that it is ours
  and we don't get copyrighted. Idk exactly how to do this.. maybe change some variable names, restructure etc..

  2. Currently, the "transactions" field inside a block can be pretty much anything.
  We need to ensure a standard format of "from to amount". 
  
  I looked at this tutorial for inspiration: https://medium.com/crypto-currently/lets-make-the-tiniest-blockchain-bigger-ac360a328f4d
  Currently the data is stored however we want. I have it set up to accept a list of strings: ["from", "to", "amount"]
  Then the block class puts the data into a json format to compute the sha256 hash of it.
  
  No json file is actually created right now, we need to create one for every block.
  
  3. Lastly, this part relies on part 2. We need a way for users to keep track of the amount of money they have - a 'wallet'.
  I haven't seen any tutorial code that does this. 
  My idea is:
    once we have a standard format for storing the transactions and a json file for each block..
    create a separate application (or thread) that simply keeps track of the latest block.
      This application will have an update() method that checks for new blocks,
      a check() method that checks if the newly added block has a transaction with the name
        of the owner in it. If it does, update his account balance, else ignore.
      And of course a show() method that shows the users balance.
      
  I think this is fairly simple. All we have to do is check if the chains last_block field is the same as the one
  that the wallet has saved. If not, replace. Then parse the json file containing the transactions and see if the "from" or 
  "to" fields match the users name. Then if they, update a separate variable in the app that keeps track of the user balance.
  
  We could check for going to negative balances, but this I think would be too much work. We can say this person is in debt lol.
  
  
      
      
      
      
      
      
