"""
dcontract.py - A smart contract interface (SDK) for the Web3
"""

from web3 import Web3
from subpapi import run_cmd
import os
import json

WEB3_CONTRACT_NAME = "DeArchive"
WEB3_CONTRACT_FILE = f"w3/{WEB3_CONTRACT_NAME}.sol"
FORGE_CLI_BUILD_CMD = f"forge build -C {WEB3_CONTRACT_FILE}"
OUT_DEARCHIVE_ABI = f"out/{WEB3_CONTRACT_NAME}.sol/{WEB3_CONTRACT_NAME}.json"

class DeContract:

    def __init__(self, contract_address: str = None):

        if contract_address is not None:
            self.contract = self.web3.eth.contract(address=contract_address)
        else:
            self.contract = None
        
        self.web3 = None
        self.deployer = None
        self.owner_address = None
    
    def set_rpc(self, rpc: str):
        self.web3 = Web3(Web3.HTTPProvider(rpc))
        assert self.web3.is_connected(), "Web3 connection failed."
    
    def get_rpc(self):
        return self.web3.providers[0].endpoint_uri
    
    def set_owner(self, owner_address: str):
        self.owner_address = owner_address

    def get_owner(self):
        return self.owner_address
    
    def set_deployer(self, deployer_key: str):
        self.deployer = self.web3.eth.account.from_key(deployer_key)
    
    def get_deployer(self):
        return self.deployer.address

    """
    Create a contract on the blockchain. (Build & Deploy)
    Returns the gas used for the transaction.
    """
    def create_contract(self):
        
        assert self.deployer is not None, "Deployer account not set."
        assert self.owner_address is not None, "Owner address not set."
        assert self.web3 is not None, "RPC connection not set."
        
        out, err = run_cmd(FORGE_CLI_BUILD_CMD)
        assert os.path.exists(OUT_DEARCHIVE_ABI), f"\nContract build failed:\nstdout: {out}\nstderr: {err}"
        with open(OUT_DEARCHIVE_ABI, 'r') as f:
            contract_json = json.loads(f.read())
        
        tx_hash = self.web3.eth.contract(
            abi=contract_json['abi'],
            bytecode=contract_json['bytecode']['object']
        ).constructor(self.owner_address).transact({'from': self.deployer.address})
        
        tx_receipt = self.web3.eth.wait_for_transaction_receipt(tx_hash)
        contract_address = tx_receipt.contractAddress
        
        self.contract = self.web3.eth.contract(address=contract_address, abi=contract_json['abi'])

        gas_used = tx_receipt.gasUsed
        return gas_used
    
    def get_contract(self):
        return self.contract

    def __repr__(self):
        if self.contract is None:
            return "DeContract(None)"
        return f"DeContract({self.contract.address})"

if __name__ == "__main__":
    contract = DeContract()
    print(contract)
    contract.set_rpc("http://localhost:8545")
    contract.set_owner("0x23618e81E3f5cdF7f54C3d65f7FBc0aBf5B21E8f")
    contract.set_deployer("0xac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80")
    gas_used = contract.create_contract()
    ctx = contract.get_contract()
    print(ctx)
    print(contract)
    print(f"Contract performance: {gas_used}")
    # 480128, not bad.
    # == 0.000000000000480128 ETH + alpha, less than 1$