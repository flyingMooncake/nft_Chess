import os
import json
import argparse
from web3 import Web3

# Set your RPC URL (e.g., "http://localhost:8545" or an Infura URL)
RPC_URL = os.getenv("WEB3_PROVIDER_URI", "http://localhost:8545")
w3 = Web3(Web3.HTTPProvider(RPC_URL))

# Replace these with your deployed contract addresses \this are placeholders.
CHESS_TOKEN_ADDRESS = w3.to_checksum_address("0xe1Aa25618fA0c7A1CFDab5d6B456af611873b629")
CHESS_FACTORY_ADDRESS = w3.to_checksum_address("0xe1DA8919f262Ee86f9BE05059C9280142CF23f48")

def load_abi(filename):
    """Load ABI from a file in the abi/ directory."""
    path = os.path.join("abi", filename)
    with open(path, "r") as f:
        return json.load(f)

# Load ABIs from files
CHESS_TOKEN_ABI = load_abi("ChessToken_abi.json")
CHESS_FACTORY_ABI = load_abi("ChessGameFactory_abi.json")
CHESS_GAME_ABI    = load_abi("ChessGame_abi.json")  # ABI for ChessGame contract

def show_chess_balance(pub_address):
    """Show the CHS token balance for a public address."""
    token_contract = w3.eth.contract(address=CHESS_TOKEN_ADDRESS, abi=CHESS_TOKEN_ABI)
    balance = token_contract.functions.balanceOf(pub_address).call()
    print(f"CHS token balance for {pub_address}: {balance}")

def approve_tokens(private_key, amount):
    """Approve the factory contract to spend tokens on your behalf."""
    account = w3.eth.account.from_key(private_key)
    token_contract = w3.eth.contract(address=CHESS_TOKEN_ADDRESS, abi=CHESS_TOKEN_ABI)
    nonce = w3.eth.get_transaction_count(account.address)
    
    txn = token_contract.functions.approve(CHESS_FACTORY_ADDRESS, amount).build_transaction({
        "chainId": w3.eth.chain_id,
        "from": account.address,
        "nonce": nonce,
        "gasPrice": w3.eth.gas_price,
    })
    
    gas_estimate = w3.eth.estimate_gas({
        "from": account.address,
        "to": CHESS_TOKEN_ADDRESS,
        "data": txn["data"],
    })
    txn["gas"] = gas_estimate

    print("Sending approval transaction...")
    signed_txn = w3.eth.account.sign_transaction(txn, private_key)
    tx_hash = w3.eth.send_raw_transaction(signed_txn.raw_transaction)
    receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    print(f"Approval transaction mined in block {receipt.blockNumber}")
    print("Receipt:", receipt)

def create_game(private_key, bet_amount):
    """
    Create a new game using the ChessGameFactory contract.
    This function calls approve_tokens first before creating the game.
    """
    try:
        approve_tokens(private_key, bet_amount)
    finally:
        account = w3.eth.account.from_key(private_key)
        factory_contract = w3.eth.contract(address=CHESS_FACTORY_ADDRESS, abi=CHESS_FACTORY_ABI)
        nonce = w3.eth.get_transaction_count(account.address)
    
        txn = factory_contract.functions.createGame(bet_amount).build_transaction({
            "chainId": w3.eth.chain_id,
            "from": account.address,
            "nonce": nonce,
            "gasPrice": w3.eth.gas_price,
        })
    
        gas_estimate = w3.eth.estimate_gas({
            "from": account.address,
            "to": CHESS_FACTORY_ADDRESS,
            "data": txn["data"],
        })
        txn["gas"] = gas_estimate
    
        print("Sending transaction to create a game...")
        signed_txn = w3.eth.account.sign_transaction(txn, private_key)
        tx_hash = w3.eth.send_raw_transaction(signed_txn.raw_transaction)
        print(f"Transaction sent, tx hash: {tx_hash.hex()}")
        receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        print(f"Transaction mined in block {receipt.blockNumber}")
        print("Receipt:", receipt)

def show_active_games():
    """Show the list of active game addresses from the ChessGameFactory contract."""
    factory_contract = w3.eth.contract(address=CHESS_FACTORY_ADDRESS, abi=CHESS_FACTORY_ABI)
    active_games = factory_contract.functions.getActiveGames().call()
    print("Active games:")
    for game in active_games:
        print(game)

def send_tokens(private_key, to_address, amount):
    """
    Send a specified amount of tokens from the sender (identified by the private key)
    to the recipient public address.
    """
    account = w3.eth.account.from_key(private_key)
    token_contract = w3.eth.contract(address=CHESS_TOKEN_ADDRESS, abi=CHESS_TOKEN_ABI)
    nonce = w3.eth.get_transaction_count(account.address)
    
    txn = token_contract.functions.transfer(w3.to_checksum_address(to_address), amount).build_transaction({
        "chainId": w3.eth.chain_id,
        "from": account.address,
        "nonce": nonce,
        "gasPrice": w3.eth.gas_price,
    })
    
    gas_estimate = w3.eth.estimate_gas({
        "from": account.address,
        "to": CHESS_TOKEN_ADDRESS,
        "data": txn["data"],
    })
    txn["gas"] = gas_estimate

    print("Sending token transfer transaction...")
    signed_txn = w3.eth.account.sign_transaction(txn, private_key)
    tx_hash = w3.eth.send_raw_transaction(signed_txn.raw_transaction)
    receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    print(f"Token transfer transaction mined in block {receipt.blockNumber}")
    print("Receipt:", receipt)

def join_game(private_key, game_address):
    """
    Join an active game by first approving the game contract to spend the bet tokens,
    then calling joinGame() on the ChessGame contract.
    """
    account = w3.eth.account.from_key(private_key)
    game_addr = w3.to_checksum_address(game_address)
    game_contract = w3.eth.contract(address=game_addr, abi=CHESS_GAME_ABI)

    # Retrieve the bet amount required from the game contract
    bet_amount = game_contract.functions.betAmount().call()
    print(f"Bet amount required to join game: {bet_amount}")

    # Approve the game contract to transfer the bet tokens from the joining account
    token_contract = w3.eth.contract(address=CHESS_TOKEN_ADDRESS, abi=CHESS_TOKEN_ABI)
    nonce = w3.eth.get_transaction_count(account.address)
    approval_txn = token_contract.functions.approve(game_addr, bet_amount).build_transaction({
        "chainId": w3.eth.chain_id,
        "from": account.address,
        "nonce": nonce,
        "gasPrice": w3.eth.gas_price,
    })
    gas_estimate = w3.eth.estimate_gas({
        "from": account.address,
        "to": CHESS_TOKEN_ADDRESS,
        "data": approval_txn["data"],
    })
    approval_txn["gas"] = gas_estimate

    print("Sending token approval transaction for joining the game...")
    signed_approval = w3.eth.account.sign_transaction(approval_txn, private_key)
    approval_tx_hash = w3.eth.send_raw_transaction(signed_approval.raw_transaction)
    approval_receipt = w3.eth.wait_for_transaction_receipt(approval_tx_hash)
    print(f"Approval transaction mined in block {approval_receipt.blockNumber}")

    # Now, call joinGame() on the ChessGame contract
    nonce = w3.eth.get_transaction_count(account.address)
    txn = game_contract.functions.joinGame().build_transaction({
        "chainId": w3.eth.chain_id,
        "from": account.address,
        "nonce": nonce,
        "gasPrice": w3.eth.gas_price,
    })
    gas_estimate = w3.eth.estimate_gas({
        "from": account.address,
        "to": game_addr,
        "data": txn["data"],
    })
    txn["gas"] = gas_estimate

    print("Sending transaction to join game...")
    signed_txn = w3.eth.account.sign_transaction(txn, private_key)
    tx_hash = w3.eth.send_raw_transaction(signed_txn.raw_transaction)
    receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    print(f"Join game transaction mined in block {receipt.blockNumber}")
    print("Receipt:", receipt)

def main():
    parser = argparse.ArgumentParser(description="Chess Utility Script")
    subparsers = parser.add_subparsers(dest="command", help="Commands")

    # Command to show CHS token balance
    parser_show = subparsers.add_parser("showChess", help="Show the CHS token balance for a public address")
    parser_show.add_argument("pub_address", type=str, help="Public address to check balance")

    # Command to approve tokens for the factory
    parser_approve = subparsers.add_parser("approveTokens", help="Approve the factory to spend tokens")
    parser_approve.add_argument("private_key", type=str, help="Private key for signing the approval transaction")
    parser_approve.add_argument("amount", type=int, help="Amount of tokens to approve (in token units)")

    # Command to create a game
    parser_create = subparsers.add_parser("createGame", help="Create a game using a private key and bet amount")
    parser_create.add_argument("private_key", type=str, help="Private key to send the transaction from")
    parser_create.add_argument("amount", type=int, help="Bet amount (in token units)")

    # Command to show active games
    parser_active = subparsers.add_parser("activeGames", help="Show active games")

    # Command to transfer tokens
    parser_transfer = subparsers.add_parser("transferTokens", help="Transfer tokens from a private key to a public address")
    parser_transfer.add_argument("private_key", type=str, help="Private key to send the tokens from")
    parser_transfer.add_argument("to_address", type=str, help="Destination public address")
    parser_transfer.add_argument("amount", type=int, help="Amount of tokens to transfer (in token units)")

    # Command to join a game
    parser_join = subparsers.add_parser("joinGame", help="Join a game using a private key and the game contract address")
    parser_join.add_argument("private_key", type=str, help="Private key to send the transaction from")
    parser_join.add_argument("game_address", type=str, help="Game contract address to join")

    args = parser.parse_args()

    if args.command == "showChess":
        pub_address = w3.to_checksum_address(args.pub_address)
        show_chess_balance(pub_address)
    elif args.command == "approveTokens":
        approve_tokens(args.private_key, args.amount)
    elif args.command == "createGame":
        create_game(args.private_key, args.amount)
    elif args.command == "activeGames":
        show_active_games()
    elif args.command == "transferTokens":
        send_tokens(args.private_key, args.to_address, args.amount)
    elif args.command == "joinGame":
        join_game(args.private_key, args.game_address)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
