from brownie import Lottery, accounts, network, config

from scripts.helper import get_config


def deploy_lottery():
    working_network, account, vrf_coordinator, keyhash, subscription_id = get_config()

    print(f"Deploying lottery contract to {working_network} network")
    contract = Lottery.deploy(vrf_coordinator, keyhash, subscription_id, {"from": account}, publish_source=True)
    print(f"Lottery Contract deployed. Contract address: {contract.address}")
    print(
        f"You can find it on {working_network} network etherscan: https://{working_network}.etherscan.io/address/{contract.address}"
    )


def main():
    deploy_lottery()