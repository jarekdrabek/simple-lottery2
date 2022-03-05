from brownie import Contract, network, config

from scripts.helper import get_deployed_lottery_address


def get_the_recent_winner_address():
    lottery_contract = Contract(get_deployed_lottery_address())

    winner_address = lottery_contract.winner()
    print(f"The winner is {winner_address}")


def main():
    get_the_recent_winner_address()
