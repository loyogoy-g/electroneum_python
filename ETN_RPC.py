#json rpc for electroneum coin written in python
#you can find the rpc wallet documenatation here "https://community.electroneum.com/t/wallet-rpc-documentation/6138
#i just compiled all the common commands
#you should have a node synchronize to the whole blockchain of electroneum
#you can use the remote node of hashvault

import requests
import json

class ETN:
    def __init__(self, port): # Port for mainnet is 26969 and for testnet is 26968
        self.port = port
        self.url = "http://127.0.0.1:{}/json_rpc".format(self.port)
        self.header = "Content-Type: application/json"

    def get_address(self): # return the address of your opened wallet
        data = requests.post(self.url, '{"jsonrpc":"2.0","id":"0","method":"getaddress"}', self.header)
        result = data.json()["result"]["address"]
        return result

    def balance(self): # return the list of balance of the opened wallet [balance, unlocked_balance]
        data = requests.post(self.url, '{"jsonrpc":"2.0","id":"0","method":"getbalance"}', self.header)
        result = data.json()["result"]
        balance = round(float(result["balance"])/100, 2) # 1 etn = 100 atomic units and they are using two decimal
        unlocked_balance = round(float(result["unlocked_balance"]) / 100, 2)
        return [balance, unlocked_balance]

    def query_key_view(self): # return the view key of wallet
        data = requests.post(self.url,'{"jsonrpc":"2.0","id":"0","method":"query_key","params":{"key_type":"view_key"}}', self.header)
        return data.json()["result"]["key"]

    def query_key_spend(self): # return the spend key of wallet
        data = requests.post(self.url,'{"jsonrpc":"2.0","id":"0","method":"query_key","params":{"key_type":"spend_key"}}', self.header)
        return data.json()["result"]["key"]

    def transfer(self, amount, address): # return the tx hash if the transfer is success and the error message if there's an error
        param = {"destinations":[{"amount":amount ,"address":address}],"priority":1,"unlock_time":0,"get_tx_keys":True,"get_tx_hex":True,"mixin":0}
        data_json = {"jsonrpc":"2.0","id":"0","method":"transfer","params":param}
        data = requests.post(self.url,json.dumps(data_json), self.header)
        if "error" in data.json():
            return [False, data.json()['error']['message']]
        else:
            return data.json()["result"]["tx_hash"]

    def transfer_split(self,list_of_payment): #same as transfer but can split into more than one tx , return True if success and the error message if there's an error
        param = {"destinations": list_of_payment, "priority": 1, "unlock_time": 0,
                 "get_tx_keys": True, "get_tx_hex": True, "mixin": 0}
        data_json = {"jsonrpc": "2.0", "id": "0", "method": "transfer", "params": param}
        data = requests.post(self.url, json.dumps(data_json), self.header)
        if "error" in data.json():
            return data.json()['error']['message']
        else:
            return True

    def create_wallet(self, name, password): # return True if success, and False if there's an error
        param = {"filename":name,"password":password,"language":"English"}
        data_json = {"jsonrpc": "2.0", "id": "0", "method": "create_wallet", "params": param}
        data = requests.post(self.url, json.dumps(data_json), self.header)
        if "error" in data.json():
            return False
        else:
            return True

    def open_wallet(self, name, password): #open your wallet
        param = {"filename": name, "password": password, "language": "English"}
        data_json = {"jsonrpc": "2.0", "id": "0", "method": "open_wallet", "params": param}
        data = requests.post(self.url, json.dumps(data_json), self.header)
        return data.json()

    def height(self): #return the current block height of electroneum blockchain
        data = requests.post(self.url, '{"jsonrpc":"2.0","id":"0","method":"getheight"}', self.header)
        result = data.json()
        if "error" in result:
            return False
        else:
            return result["result"]["height"]

