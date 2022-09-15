from locust import HttpLocust, TaskSet, task
from random import randrange

import ujson
import json


class UserBehaviour(TaskSet):

    @task()
    def random_estimategas(self):
        body = {"jsonrpc": "2.0", "method": "eth_estimateGas",
                "id": 1, "params": [{}]}
        self.client.post("/", name="eth_estimateGas", json=body)

    @task()
    def gasprice(self):
        body = {"jsonrpc": "2.0", "method": "eth_gasPrice", "params": [], "id": 1}
        self.client.post("/", name="eth_gasPrice", json=body)

    @task()
    def random_unclecount(self):
        block_nr = str(hex(randrange(1, self.locust.max_block)))
        body = {"jsonrpc": "2.0", "method": "eth_getUncleCountByBlockNumber",
                "params": [block_nr], "id": 1}
        self.client.post("/", name="eth_getUncleCountByBlockNumber", json=body)

    @task()
    def random_txsum(self):
        block_nr = str(hex(randrange(1, self.locust.max_block)))
        body = {"jsonrpc": "2.0", "method": "eth_getBlockTransactionCountByNumber",
                "params": [block_nr], "id": 1}
        self.client.post(
            "/", name="eth_getBlcokTransactionCountByNumber", json=body)

    @task()
    def random_txcount(self):
        block_nr = str(hex(randrange(1, self.locust.max_block)))
        body = {"jsonrpc": "2.0", "method": "eth_getTransactionCount",
                "params": [self.locust.token['address'], block_nr], "id": 1}
        self.client.post("/", name="eth_getTransactionCount", json=body)

    @task()
    def random_code(self):
        block_nr = str(hex(randrange(1, self.locust.max_block)))
        body = {"jsonrpc": "2.0", "method": "eth_getCode",
                "params": [self.locust.token['address'], block_nr], "id": 1}
        self.client.post("/", name="eth_getCode", json=body)

    @task()
    def random_storage(self):
        block_nr = str(hex(randrange(1, self.locust.max_block)))
        body = {"jsonrpc": "2.0", "method": "eth_getStorageAt",
                "params": [self.locust.token['address'], "0x0", block_nr], "id": 1}
        self.client.post("/", name="eth_getStorageAt", json=body)

    @task()
    def random_balance(self):
        block_nr = str(hex(randrange(1, self.locust.max_block)))
        rndnum = randrange(0, len(self.locust.wallets))
        address = str(self.locust.wallets[rndnum]["address"])
        body = {"jsonrpc": "2.0", "method": "eth_getBalance", "params": [address, block_nr], "id": 1}
        self.client.post("/", name="eth_getBalance", json=body)

    @task()
    def random_blockbynumber(self):
        block_nr = str(hex(randrange(1, self.locust.max_block)))

        body = {"jsonrpc": "2.0", "method": "eth_getBlockByNumber",
                "params": [block_nr, True], "id": 1}
        self.client.post("/", name="eth_getBlockByNumber", json=body)

    # @task(1)
    # def get_all_eos_logs(self):
    #     startblock = "0x494681"  # 4802177
    #     endblock = "0x4D90D1"  # 5083345
    #     eosaddr = "0xd0a6E6C54DbC68Db5db3A091B171A77407Ff7ccf"  # eos crowfunding contract
    #     body = {"jsonrpc": "2.0",
    #             "method": "eth_getLogs",
    #             "id": 1,
    #             "params": [{"fromBlock": startblock,
    #                         "toBlock": endblock,
    #                         "address": eosaddr}]}
    #     self.client.post(
    #         "/", name="eth_getLogs (EOS Crowdfunding all 280k blocks", json=body)

    # @task(1)
    # def get_some_eos_logs(self):
    #     startblock = "0x4D230D"  # 5055245
    #     endblock = "0x4D90D1"  # 5083345
    #     eosaddr = "0xd0a6E6C54DbC68Db5db3A091B171A77407Ff7ccf"
    #     body = {"jsonrpc": "2.0",
    #             "method": "eth_getLogs",
    #             "id": 1,
    #             "params": [{"fromBlock": startblock,
    #                         "toBlock": endblock,
    #                         "address": eosaddr}]}
    #     self.client.post(
    #         "/", name="eth_getLogs (EOS Crowdfunding 28k blocks", json=body)

    # @task(1)
    # def get_last_eos_logs(self):
    #     eosaddr = "0xd0a6E6C54DbC68Db5db3A091B171A77407Ff7ccf"
    #     body = {"jsonrpc": "2.0",
    #             "method": "eth_getLogs",
    #             "id": 1,
    #             "params": [{"address": eosaddr}]}
    #     self.client.post(
    #         "/", name="eth_getLogs (EOS Crowdfunding last block", json=body)

    @task()
    def get_random_tx_by_hash(self):
        rndnum = randrange(0, len(self.locust.txs))
        tx = str(self.locust.txs[rndnum]["tx"])
        body = {"jsonrpc": "2.0", "method": "eth_getTransactionByHash", "id": 1,
                "params": [tx]}
        self.client.post("/", name="eth_getTransactionByHash", json=body)

    # @task()
    # def random_eth_call(self):
    #     block_nr = str(hex(randrange(1, 5083345)))

    #     body = {"jsonrpc": "2.0", "method": "eth_call",
    #             "params": [{"to": self.locust.token['address'], "data": "0x18160ddd"}, block_nr],
    #             "id": 1}
    #     self.client.post(
    #         "/", name="eth_call (balanceOf for token on an address for random block)", json=body)

    # eth_sendRawTransaction
    # skipping this for now
    

class APIUser(HttpLocust):
    task_set = UserBehaviour
    def wait_time(stuff):
        return 10000

    # Requires that we have populated a json file with tx hashes.
    with open("tx_out.json", "r") as jsonfile:
        txs = json.load(jsonfile)
    with open("token.json", "r") as jsonfile:
        token = json.load(jsonfile)
    with open("wallets.json", "r") as jsonfile:
        wallets = json.load(jsonfile)
    max_block = 1000