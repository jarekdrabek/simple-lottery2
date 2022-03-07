# Simple Lottery
Simple lottery blockchain application. This project is working with the Rinkeby Ethereum testnet. 
You can interact with the lottery executing commands in console (see below). 

## How it works
You can buy a lottery coupon for 0.001ETH and try to win. 

if you are not lucky, your money will be added to the winning pool.

If you are lucky you will get the whole collected winning pool.
After that the lottery start over.
 

## How it works technically

After a player bought the lottery coupon the random number is draw using [chainlink VRF v2](https://docs.chain.link/docs/get-a-random-number/). 
Then this random number is [mod](https://en.wikipedia.org/wiki/Modulo_operation) by 1000. Then, if the result is lower then **_winning_probability_in_promiles_** property in `brownie-config.yaml` file, the player is the winner and is given the whole winning pool. Otherwise he is a looser and his money is added to the winning pool.   


## Installation and running

### Requirements:
you need to have `Python 3.9` and [brownie](https://eth-brownie.readthedocs.io/en/stable/install.html) installed


### Prerequisuites

Installing project dependencies:
```
pip install -r requirements.txt
```


Use my Infura project id to interact with Rinkeby network
```
export WEB3_INFURA_PROJECT_ID=3b60db32abff40358b27faee00f6cc83
```
In order to interact with Rinkeby Ethereum testnet you need to create Rinkeby account 
(you need to provide private key to your Metamask account - PLEASE DON'T USE THE ONE WITH REAL MONEY ON IT!)

```
brownie accounts new rinkeby-account1 
```

### How to take part in the current Lottery:
In order to be able to test the whole functionality of the lottery. The winning probability in the deployed contract is set to 30%.

```
brownie run scripts/buy_coupon_and_try_to_win.py --network rinkeby
```


### How to run contract tests

Executing tests
```
brownie test
```

### How to deploy you own version of Lottery and take part in it:
1. In order to use [chainlink VRF v2](https://docs.chain.link/docs/get-a-random-number/)  first [create and fund a chainlink subscription](https://docs.chain.link/docs/get-a-random-number/#create-and-fund-a-subscription).
After that you need to change **_subscription_id_** with your value.  

    ```
    contract:
      rinkeby:
        dependencies:
          randomness:
            subscription_id: 638
    ```
2. Set the **_winning_probability_in_promiles_** property in `brownie-config.yaml` file with value between 1 and 999. 


3. Deploying to Rinkeby Ethereum network.
    ```
    brownie run scripts/deploy.py --network rinkeby
    ```

    you should see message similar to following:
    
    > Lottery Contract deployed. Contract address: 0xA7fEe2a153C32e28914226D1CC9CDa27FA9194a9
    > 
    > You can find it on rinkeby network etherscan: https://rinkeby.etherscan.io/address/0xA7fEe2a153C32e28914226D1CC9CDa27FA9194a9


4. Copy the contract address and paste in `brownie-config.yaml` file similarly like below
    ```
    contract:
      rinkeby:
        address: '0xA7fEe2a153C32e28914226D1CC9CDa27FA9194a9' 
    ```
5. Add the newly created contract address to the chainlink subscriptions consumers [here](https://vrf.chain.link/?_ga=2.152986495.7328963.1646313202-37205130.1644920393)


CONGRATULATIONS! THE LOTTERY IS NOW LIVE on Rinkeby Test Network!

You can now take part in your own Lottery executing:

```
brownie run scripts/buy_coupon_and_try_to_win.py --network rinkeby
```

### How to figure out who won:


You can check what was the recent winner address using this command:
```
brownie run scripts/get_the_recent_winner_address.py --network rinkeby
```
