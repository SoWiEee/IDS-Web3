# IDS-WEB3
This is a application for blockchain course project, it implements:
    * Specific event type listener
    * Contract recorder
    * Web view render

# Requirement
* Foundry (forge, cast, anvil, chisel) [doc](!https://book.getfoundry.sh/)
* Python Flask
* Sysmon


## Foundry

**Foundry is a blazing fast, portable and modular toolkit for Ethereum application development written in Rust.**

Foundry consists of:

-   **Forge**: Ethereum testing framework (like Truffle, Hardhat and DappTools).
-   **Cast**: Swiss army knife for interacting with EVM smart contracts, sending transactions and getting chain data.
-   **Anvil**: Local Ethereum node, akin to Ganache, Hardhat Network.
-   **Chisel**: Fast, utilitarian, and verbose solidity REPL.



# Quick Start
1. Initialize project @IDS-Web3/
```shell
$ forge init --force
```


2. Install all required package with this command:
```shell
$ uv pip install -r requirements.txt
```

3. Compile contract
```shell
$ forge build
```

4. Deploy contract
```shell
$ forge script script/Deploy.s.sol:DeployScript --rpc-url http://localhost:7545 --pricate_key 0x?? --broadcast
```

5. Run sysmon
```shell
$ sudo ./sysmon64.exe -c
```

6. Launch flask server
```shell
$ python app.py
```

