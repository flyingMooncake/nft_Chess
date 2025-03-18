# Chess_RPC Python Virtual Environment

This project contains a Python virtual environment for interacting with the Chess_RPC smart contracts. The `main.py` script provides command-line utilities to interact with deployed Ethereum smart contracts.

## Project Structure

```
Chess_RPC
├── README.md    # Documentation file
├── abi          # ABI files for deployed smart contracts
├── bin          # Python virtual environment binaries
├── include      # Python virtual environment includes
├── lib          # Virtual environment dependencies
├── lib64 -> lib # Symlink to lib
├── main.py      # Python script for contract interaction
└── pyvenv.cfg   # Python virtual environment configuration file
```

## Setting Up the Environment

### 1. Activating the Virtual Environment

To activate the Python virtual environment, run:

```bash
source bin/activate
```

### 2. : 
Run the local anvil blockchain. 

```bash
    anvil
```

### 3. :
Ensure that you deploy your contract before you use the demo app.
See: ../readMe.md

### 4. :
    configure line 11 & 12 with the addresses you got after the deployment of the contract. 
```
    CHESS_TOKEN_ADDRESS = w3.to_checksum_address("0xe1Aa25618fA0c7A1CFDab5d6B456af611873b629") 
    CHESS_FACTORY_ADDRESS = w3.to_checksum_address("0xe1DA8919f262Ee86f9BE05059C9280142CF23f48")
    
```

## Running the Python Script

Once the virtual environment is activated, you can run the `main.py` script to interact with the deployed contracts.

### Available Commands:

- **Check CHS Token Balance**
  ```bash
  python main.py showChess <PUBLIC_ADDRESS>
  ```

- **Approve Tokens for Contract**
  ```bash
  python main.py approveTokens <PRIVATE_KEY> <AMOUNT>
  ```

- **Create a New Chess Game**
  ```bash
  python main.py createGame <PRIVATE_KEY> <BET_AMOUNT>
  ```

- **List Active Games**
  ```bash
  python main.py activeGames
  ```

- **Transfer Tokens**
  ```bash
  python main.py transferTokens <PRIVATE_KEY> <DESTINATION_PUBLIC_ADDRESS> <AMOUNT>
  ```

- **Join an Existing Game**
  ```bash
  python main.py joinGame <PRIVATE_KEY> <GAME_CONTRACT_ADDRESS>
  ```

## Deactivating the Virtual Environment

Once you're done, deactivate the virtual environment by running:

```bash
deactivate
```



## License

This project is licensed under the GNU General Public License.

## Contributor

- **Bogdan Togoé**
