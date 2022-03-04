from brownie import Lottery, accounts, VRFCoordinatorV2Mock
from brownie.network.web3 import Web3



def test_lottery_workflow():
    # Arrange
    lottery_owner_account = accounts[0]
    first_player_account = accounts[1]
    second_player_account = accounts[2]
    third_player_account = accounts[3]
    lottery_contract, vrf_coordinator = __deploy_and_get_lottery_contract_and_dependencies(lottery_owner_account)

    #Act
    tx = lottery_contract.buyCouponAnTryToWin({"from": first_player_account, "value": Web3.toWei(0.001, 'ether')})
    __fullfill_lottery_vrf_coordinator_with_given_random_result2(tx.return_value, lottery_contract, vrf_coordinator, 600)

    tx = lottery_contract.buyCouponAnTryToWin({"from": second_player_account, "value": Web3.toWei(0.001, 'ether')})
    __fullfill_lottery_vrf_coordinator_with_given_random_result2(tx.return_value, lottery_contract, vrf_coordinator, 900)

    tx = lottery_contract.buyCouponAnTryToWin({"from": third_player_account, "value": Web3.toWei(0.001, 'ether')})
    __fullfill_lottery_vrf_coordinator_with_given_random_result2(tx.return_value, lottery_contract, vrf_coordinator, 400)

    #Assert
    assert lottery_contract.balance() == 0
    assert first_player_account.balance() == Web3.toWei(99.999, 'ether')
    assert second_player_account.balance() == Web3.toWei(99.999, 'ether')
    assert third_player_account.balance() == Web3.toWei(100.002, 'ether')


def __deploy_and_get_lottery_contract_and_dependencies(deploying_account):
    keyhash = '0xd89b2bf150e3b9e13446986e571fb9cab24b13cea0a43ea20a6049a85cc807cc'

    vrf_coordinator = VRFCoordinatorV2Mock.deploy(0, 0, {"from": deploying_account})
    subscription_id = vrf_coordinator.createSubscription().return_value

    lottery_contract = Lottery.deploy(
        vrf_coordinator,
        keyhash,
        subscription_id,
        {"from": deploying_account},
    )
    return lottery_contract, vrf_coordinator


def __fullfill_lottery_vrf_coordinator_with_given_random_result2(request_id, lottery_contract, vrf_coordinator, random_result):
    vrf_coordinator.fulfillRandomWords(request_id, lottery_contract.address, random_result)


