from brownie import Contract, Lottery
from brownie.network.web3 import Web3

from scripts.helper import get_config, get_deployed_lottery_address


def buy_coupon_and_try_to_win():
    working_network, account, _, _, _ = get_config()

    lottery_contract = Contract.from_abi('Lottery', get_deployed_lottery_address(), Lottery.abi)
    if lottery_contract.lottery_state() == 1:
        print("The lottery processing is IN PROGRESS. You need to wait until the previous request will be finished.")
        return
    transaction_receipt = lottery_contract.buyCouponAndTryToWin({"from": account, "value": Web3.toWei(0.001, 'ether')})
    print(f"You took part in Lottery.")
    print(f"You can find your transaction on {working_network} network etherscan: https://{working_network}.etherscan.io/tx/{transaction_receipt.txid}")


def main():
    buy_coupon_and_try_to_win()
