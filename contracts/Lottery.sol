// SPDX-License-Identifier: MIT

pragma solidity ^0.8.7;


import "@chainlink/contracts/src/v0.8/interfaces/VRFCoordinatorV2Interface.sol";
import "@chainlink/contracts/src/v0.8/VRFConsumerBaseV2.sol";

contract Lottery is VRFConsumerBaseV2 {
    VRFCoordinatorV2Interface COORDINATOR;
    bytes32 keyHash;
    uint64 subscriptionId;
    uint64 winningProbabilityInPromiles;

    enum LOTTERY_STATE {
        OPEN,
        IN_PROGRESS
    }
    LOTTERY_STATE public lottery_state = LOTTERY_STATE.OPEN;

    mapping(uint256 => address) public requestId2address;

    address payable public winner;
    uint256 public randomNumber;
    bool public isItWinningCoupon;

    constructor(address _vrfCoordinator, bytes32 _keyHash, uint64 _subscriptionId, uint64 _winningProbabilityInPromiles) VRFConsumerBaseV2(_vrfCoordinator) {
        COORDINATOR = VRFCoordinatorV2Interface(_vrfCoordinator);
        keyHash = _keyHash;
        subscriptionId = _subscriptionId;
        winningProbabilityInPromiles = _winningProbabilityInPromiles;
    }

    modifier isCouponPrice() {
        //Coupon price = 0.001ETH
        uint256 couponPriceInWei = 1000000000000000;
        require(
        couponPriceInWei == msg.value,
        "You need to pay exactly 0.001ETH for coupon"
        );
        _;
    }

    function buyCouponAndTryToWin() public payable isCouponPrice returns(uint256) {
        require(lottery_state == LOTTERY_STATE.OPEN);
        lottery_state = LOTTERY_STATE.IN_PROGRESS;
        return tryToWin();
    }

    function tryToWin() internal returns(uint256) {
        uint16 requestConfirmations = 3;
        uint32 callbackGasLimit = 100000;
        uint32 numWords = 1;
        uint256 requestId = COORDINATOR.requestRandomWords(
            keyHash,
            subscriptionId,
            requestConfirmations,
            callbackGasLimit,
            numWords
        );
        requestId2address[requestId] = msg.sender;
        return requestId;
    }

    function fulfillRandomWords(uint256 requestId, uint256[] memory randomWords) internal override {
        randomNumber = randomWords[0];
        isItWinningCoupon = ((randomNumber % 1000) < winningProbabilityInPromiles);
        if(isItWinningCoupon){
            winner = payable(requestId2address[requestId]);
            winner.transfer(address(this).balance);
        }
        lottery_state = LOTTERY_STATE.OPEN;
    }

}
