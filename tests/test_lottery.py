import pytest
from brownie import Lottery, accounts, VRFCoordinatorV2Mock
from brownie.exceptions import VirtualMachineError
from brownie.network.web3 import Web3


def test_lottery_workflow():
    # Arrange
    first_player_account = accounts[0]
    second_player_account = accounts[1]
    third_player_account = accounts[2]
    lottery_contract, vrf_coordinator = __deploy_and_get_lottery_contract_and_dependencies(first_player_account)

    #Act
    tx = lottery_contract.buyCouponAnTryToWin({"from": first_player_account, "value": Web3.toWei(0.001, 'ether')})
    __fullfill_lottery_vrf_coordinator_with_given_random_result2(tx.return_value, lottery_contract, vrf_coordinator, 14)

    tx = lottery_contract.buyCouponAnTryToWin({"from": second_player_account, "value": Web3.toWei(0.001, 'ether')})
    __fullfill_lottery_vrf_coordinator_with_given_random_result2(tx.return_value, lottery_contract, vrf_coordinator, 90)

    tx = lottery_contract.buyCouponAnTryToWin({"from": third_player_account, "value": Web3.toWei(0.001, 'ether')})
    __fullfill_lottery_vrf_coordinator_with_given_random_result2(tx.return_value, lottery_contract, vrf_coordinator, 4)

    #Assert
    assert lottery_contract.balance() == 0
    assert first_player_account.balance() == Web3.toWei(99.999, 'ether')
    assert second_player_account.balance() == Web3.toWei(99.999, 'ether')
    assert third_player_account.balance() == Web3.toWei(100.002, 'ether')


def test_cannot_buy_another_coupon_whe_the_previous_one_was_not_resolved():
    # Arrange
    first_player_account = accounts[0]
    second_player_account = accounts[1]
    lottery_contract, vrf_coordinator = __deploy_and_get_lottery_contract_and_dependencies(first_player_account)

    # Act and Assert
    lottery_contract.buyCouponAnTryToWin({"from": first_player_account, "value": Web3.toWei(0.001, 'ether')})
    with pytest.raises(VirtualMachineError):
        lottery_contract.buyCouponAnTryToWin({"from": second_player_account, "value": Web3.toWei(0.001, 'ether')})


def test_you_can_start_new_lottery_when_the_previous_one_was_finished():
    # Arrange
    first_player_account = accounts[0]
    second_player_account = accounts[1]
    lottery_contract, vrf_coordinator = __deploy_and_get_lottery_contract_and_dependencies(first_player_account)

    # Act
    tx = lottery_contract.buyCouponAnTryToWin({"from": first_player_account, "value": Web3.toWei(0.001, 'ether')})
    __fullfill_lottery_vrf_coordinator_with_given_random_result2(tx.return_value, lottery_contract, vrf_coordinator, 4)

    tx = lottery_contract.buyCouponAnTryToWin({"from": second_player_account, "value": Web3.toWei(0.001, 'ether')})
    __fullfill_lottery_vrf_coordinator_with_given_random_result2(tx.return_value, lottery_contract, vrf_coordinator, 90)

    #Assert
    assert lottery_contract.balance() == Web3.toWei(0.001, 'ether')


def test_coupon_for_more_then_one_million_gwei():
    # Arrange
    first_player_account = accounts[0]
    testing_contract,_ = __deploy_and_get_lottery_contract_and_dependencies(first_player_account)


    # Act and Assert
    with pytest.raises(VirtualMachineError):
        testing_contract.buyCouponAnTryToWin(
            {"from": first_player_account, "value": Web3.toWei(0.001, 'ether') + 1}
        )


def test_coupon_for_less_then_one_million_gwei():
    # Arrange
    first_player_account = accounts[0]
    testing_contract,_ = __deploy_and_get_lottery_contract_and_dependencies(first_player_account)

    # Act and Assert
    with pytest.raises(VirtualMachineError):
        testing_contract.buyCouponAnTryToWin({"from": first_player_account, "value": Web3.toWei(0.001, 'ether') - 1})


def __deploy_and_get_lottery_contract_and_dependencies(deploying_account):
    keyhash = '0xd89b2bf150e3b9e13446986e571fb9cab24b13cea0a43ea20a6049a85cc807cc'

    vrf_coordinator = VRFCoordinatorV2Mock.deploy(0, 0, {"from": deploying_account})
    subscription_id = vrf_coordinator.createSubscription().return_value
    winning_probability_in_promiles = 10

    lottery_contract = Lottery.deploy(
        vrf_coordinator,
        keyhash,
        subscription_id,
        winning_probability_in_promiles,
        {"from": deploying_account},
    )
    return lottery_contract, vrf_coordinator


def __fullfill_lottery_vrf_coordinator_with_given_random_result2(request_id, lottery_contract, vrf_coordinator, random_result):
    vrf_coordinator.fulfillRandomWords(request_id, lottery_contract.address, random_result)


