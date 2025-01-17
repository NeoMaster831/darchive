"""
dnet.py - A network interface (SDK) for the Web3 
"""

from web3 import Web3
from configparser import ConfigParser
from dcontract import DeContract
import logging

class DeNetwork:

    def __init__(self, cfg_file: str = 'network.cfg'):
        self.config = ConfigParser()
        self.config.read(cfg_file)

        # 중요 정보
        self.web3 = Web3(Web3.HTTPProvider(self.config["network"]["rpc"]))
        self.account = self.web3.eth.account.from_key(self.config["account"]["private_key"])
        self.contract = DeContract()

        # 기타 정보
        self.web3_name = self.config["network"]["name"]
        self.data_size = 0

        logging.info(f"Initialized {self.web3_name} network.")

    def get_owner_address(self):
        return self.account.address

    def initialize_contract(self, address: str = None):
        self.contract.set_rpc(str(self.config["network"]["rpc"]))
        self.contract.set_owner(self.account.address)
        self.contract.set_deployer(self.account.key)
        if address:
            self.contract.load_contract(address)
            logging.info(f"Contract loaded on {self.web3_name}.")
        else:
            gas_used = self.contract.create_contract()
            logging.info(f"Contract created on {self.web3_name} with gas used: {gas_used}")
        
        ctx = self.contract.get_contract()
        logging.info(f"Contract address: {ctx.address}")

        self.data_size = ctx.functions.size().call()
        logging.info(f"Initial data size: {self.data_size}")

    def get(self, idx: int):
        ctx = self.contract.get_contract()
        logging.info(f"Getting data from {self.web3_name}. - Index: {idx}")
        return ctx.functions.get(idx).call()
    
    def save(self, data: bytes, tx_dict: dict):
        ctx = self.contract.get_contract()
        tx_hash = ctx.functions.save(data).transact(tx_dict)
        tx_receipt = self.web3.eth.wait_for_transaction_receipt(tx_hash)
        tx_hash_hex = "0x" + tx_hash.hex()

        self.data_size += 1
        logging.info(f"Data saved on {self.web3_name}. - Network size: {self.data_size}")
        logging.info(f"Transaction hash: {tx_hash.hex()}, Gas used: {tx_receipt.gasUsed}")
        return tx_hash.hex(), tx_receipt.gasUsed

    def size(self):
        return self.data_size

    def __repr__(self):
        return f"DeNetwork({self.web3_name})"

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    network = DeNetwork()
    #network.initialize_contract()
    network.initialize_contract("0x8A791620dd6260079BF849Dc5567aDC3F2FdC318")
    account = network.account # we test as an owner

    tx = {
        'from': account.address,
        'gas': 2000000,
    }

    _, _ = network.save(b"naga", tx) # cuz we enabled logging..
    print(network.get(1))