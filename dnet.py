"""
dnet.py - A network interface (SDK) for the Web3 
"""

from web3 import Web3
from configparser import ConfigParser

class DeNetwork:

    def __init__(self, cfg_file: str = 'network.cfg'):
        self.config = ConfigParser()
        self.config.read(cfg_file)

        # 중요 정보
        self.web3 = Web3(Web3.HTTPProvider(self.config["network"]["rpc"]))
        self.account = self.web3.eth.account.from_key(self.config["account"]["private_key"])

        # 기타 정보
        self.web3_name = self.config["network"]["name"]

    def get_owner_address(self):
        return self.account.address

    def __repr__(self):
        return f"DeNetwork({self.web3_name})"

if __name__ == "__main__":
    network = DeNetwork()
    print(network)
    print(network.get_owner_address())