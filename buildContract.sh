#!/usr/bin/env bash

# 1) Compile your contracts to ensure we have fresh artifacts
forge build

# 2) Deploy using your DeployLocal script & the local RPC node
forge script script/DeployLocal.s.sol:DeployLocal \
  --rpc-url http://127.0.0.1:8545 \
  --private-key 0x2a871d0798f97d79848a013d4936a73bf4cc922c825d33c1cf7073dff6d409c6 \
  --broadcast

# 3) Clear the old ABI files
rm abi/*

# 4) Generate ABIs for each contract & place them into chess-app/public/abi
forge inspect src/Chess_Game_Factory.sol:ChessGameFactory abi --json > abi/ChessGameFactory_abi.json
forge inspect src/Chess_ERC20_Token.sol:ChessToken abi --json        > abi/ChessToken_abi.json
forge inspect src/Chess_Game.sol:ChessGame abi --json               > abi/ChessGame_abi.json

echo "Build, deployment, and ABI generation complete!"
