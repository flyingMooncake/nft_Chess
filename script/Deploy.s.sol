// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;
import "forge-std/Script.sol";
import "../contracts/Chess_ERC20_Token.sol";
import "../contracts/Chess_Game_Factory.sol";

contract Deploy is Script {
    function run() external {
        vm.startBroadcast();
        ChessToken token = new ChessToken();
        ChessGameFactory factory = new ChessGameFactory(address(token));
        vm.stopBroadcast();
    }
}
