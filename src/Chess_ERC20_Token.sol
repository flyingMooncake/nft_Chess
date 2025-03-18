// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract ChessToken is ERC20, Ownable {
    constructor(address initialOwner)
        ERC20("ChessToken", "CHS")
        Ownable(0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266) 
    {
        // Mint 1,000,000 CHS to the chosen owner
        _mint(0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266, 1000000 * 10**18);
    }

    function mint(address to, uint256 amount) external onlyOwner {
        _mint(to, amount);
    }
}