// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract ChessToken is ERC20, Ownable {
    constructor() ERC20("ChessToken", "CHS") {
        _mint(msg.sender, 1000000 * 10**18); // 1M Tokens to deployer
    }

    function mint(address to, uint256 amount) external onlyOwner {
        _mint(to, amount);
    }
}
