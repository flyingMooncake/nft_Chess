// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

import "./Chess_ERC20_Token.sol";
import "./Chess_Game.sol";

contract ChessGameFactory {
    address public owner;
    ChessToken public token;
    uint256 public feePercentage = 5; // 5% goes to the owner

    event GameCreated(address gameAddress, address player1, uint256 betAmount);

    constructor(address _tokenAddress) {
        owner = msg.sender;
        token = ChessToken(_tokenAddress);
    }

    function createGame(uint256 betAmount) external returns (address) {
        require(betAmount > 0, "Bet must be greater than 0"); // Negative token manipulation check for security 

        ChessGame newGame = new ChessGame(msg.sender, betAmount, address(token), feePercentage, owner);
        token.transferFrom(msg.sender, address(newGame), betAmount); // Lock funds in game contract

        emit GameCreated(address(newGame), msg.sender, betAmount);
        return address(newGame);

        //To create key based game identifier for 
    }
}
