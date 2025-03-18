// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

import "forge-std/Script.sol";
import "../src/Chess_ERC20_Token.sol";
import "../src/Chess_Game_Factory.sol";

contract DeployLocal is Script {
    function run() external {
        vm.startBroadcast();

        address deployer = tx.origin; 
        // or msg.sender, depending on your usage
        
        // Deploy ChessToken, owned by `deployer`
        ChessToken token = new ChessToken(deployer);
        console.log("ChessToken deployed at:", address(token));

        // Deploy factory, pass the token address
        ChessGameFactory factory = new ChessGameFactory(address(token));
        console.log("ChessGameFactory deployed at:", address(factory));

        vm.stopBroadcast();
    }
}