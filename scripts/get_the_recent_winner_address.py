from brownie import Contract, Lottery

from scripts.helper import get_deployed_lottery_address


def get_the_recent_winner_address():
    lottery_contract = Contract.from_abi('Lottery', get_deployed_lottery_address(), Lottery.abi)

    winner_address = lottery_contract.winner()
    print(f"The winner is {winner_address}")


def main():
    get_the_recent_winner_address()
