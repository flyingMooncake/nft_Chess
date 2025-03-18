// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

import "./Chess_ERC20_Token.sol";
import "./Chess_Game.sol";

contract ChessGameFactory {
    address public owner;
    ChessToken public token;
    uint256 public feePercentage = 5; // 5% to the factory owner

    address[] public activeGames;

    event GameCreated(address gameAddress, address player1, uint256 betAmount);

    // Constructor that accepts a deployed ChessToken address
    constructor(address _tokenAddress) {
        owner = msg.sender;
        token = ChessToken(_tokenAddress);
    }

    // Create a new ChessGame, transferring bet from user to the new game
    function createGame(uint256 betAmount) external returns (address) {
        require(betAmount > 0, "Bet must be > 0");

        ChessGame newGame = new ChessGame(
            msg.sender,
            betAmount,
            address(token),
            feePercentage,
            owner
        );

        // The user must have approved the factory for `betAmount` tokens
        token.transferFrom(msg.sender, address(newGame), betAmount);

        activeGames.push(address(newGame));
        emit GameCreated(address(newGame), msg.sender, betAmount);

        return address(newGame);
    }

    // Retrieve all active ChessGame addresses
    function getActiveGames() external view returns (address[] memory) {
        return activeGames;
    }

    // Return the token address
    function showTokenAddress() external view returns (address) {
        return address(token);
    }

    // For debugging/UX: confirm this is a factory
    function isFactory() external pure returns (bool) {
        return true;
    }
}
