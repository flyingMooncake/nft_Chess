// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

import "./Chess_ERC20_Token.sol";

contract ChessGame {
    address public player1;
    address public player2;
    uint256 public betAmount;
    uint256 public startBlock;
    uint256 public timeLimitBlocks = 500000000; // Time limit in blocks , for testing no limit
    bool public gameOver = false;
    address public winner;
    ChessToken public token;
    uint256 public feePercentage;
    address public factoryOwner;

    struct Move {
        address player;
        string move;
    }

    Move[] public moveHistory;

    event PlayerJoined(address player);
    event MoveMade(address player, string move);
    event GameOver(address winner);
    event Draw();

    constructor(address _player1, uint256 _betAmount, address _tokenAddress, uint256 _feePercentage, address _factoryOwner) {
        player1 = _player1;
        betAmount = _betAmount;
        token = ChessToken(_tokenAddress);
        feePercentage = _feePercentage;
        factoryOwner = _factoryOwner;
        startBlock = block.number;
    }

    function joinGame() external {
        require(player2 == address(0), "Game already started");
        require(msg.sender != player1, "Player1 cannot join their own game");

        player2 = msg.sender;
        token.transferFrom(msg.sender, address(this), betAmount); // Lock second player's funds

        emit PlayerJoined(msg.sender);
    }

    function makeMove(string memory move) external {
        require(msg.sender == player1 || msg.sender == player2, "Not a player");
        require(!gameOver, "Game over");

        // Add move to history
        moveHistory.push(Move(msg.sender, move));

        emit MoveMade(msg.sender, move);
    }

    function endGame(address _winner) external {
        require(msg.sender == player1 || msg.sender == player2, "Not a player");
        require(!gameOver, "Game over");

        // Set winner & distribute funds
        winner = _winner;
        gameOver = true;

        uint256 totalPrize = betAmount * 2;
        uint256 fee = (totalPrize * feePercentage) / 100;
        uint256 winnerPrize = totalPrize - fee;

        token.transfer(winner, winnerPrize);
        token.transfer(factoryOwner, fee);

        emit GameOver(winner);
    }

    function declareDraw() external {
        require(!gameOver, "Game over");

        gameOver = true;
        token.transfer(player1, betAmount);
        token.transfer(player2, betAmount);

        emit Draw();
    }

    function checkTimeout() external {
        require(!gameOver, "Game over");
        require(block.number > startBlock + timeLimitBlocks, "Game still within time limit");

        if (moveHistory.length % 2 == 0) {
            winner = player2;
        } else {
            winner = player1;
        }

        gameOver = true;
        uint256 totalPrize = betAmount * 2;
        uint256 fee = (totalPrize * feePercentage) / 100;
        uint256 winnerPrize = totalPrize - fee;

        token.transfer(winner, winnerPrize);
        token.transfer(factoryOwner, fee);

        emit GameOver(winner);
    }
}
