# contract_interaction.py
from web3 import Web3
import json

# Replace with your Ethereum node's URL and port
node_url = 'http://xayah.tpddns.cn:1039'

# Example: 'http://your-node-ip:your-port'
web3 = Web3(Web3.HTTPProvider(node_url))

# Check connection
if not web3.is_connected():
    print("Unable to connect to the Ethereum node")
    exit()



def get_abi_from_json(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            # 返回 ABI
            
            return (data.get('abi', []), data.get('networks', []))
    except FileNotFoundError:
        print(f"文件未找到: {file_path}")
    except json.JSONDecodeError:
        print(f"无法解析 JSON 文件: {file_path}")
    except Exception as e:
        print(f"发生错误: {e}")

# 使用示例
abiwithaddress = get_abi_from_json('./hobbit/backend/docs/SimpleToken.json')
contract_abi = abiwithaddress[0]
contract_address = abiwithaddress[1]['1337']['address']


# Create contract object
contract = web3.eth.contract(address=contract_address, abi=contract_abi)

def get_function_list():
    function_list = []
    for item in contract_abi:
        if item['type'] == 'function':
            function_list.append(item['name'])
    return function_list

def get_balance(address):
    balance = contract.functions.getBalance(address).call()
    return balance

def transfer_tokens(from_address, to_address, amount, private_key):
    # Build transaction
    nonce = web3.eth.getTransactionCount(from_address)
    transaction = contract.functions.transfer(to_address, amount).buildTransaction({
        'chainId': 1,  # Change this to your network's chain ID
        'gas': 2000000,
        'gasPrice': web3.toWei('50', 'gwei'),
        'nonce': nonce,
    })

    # Sign transaction
    signed_txn = web3.eth.account.signTransaction(transaction, private_key=private_key)

    # Send transaction
    txn_hash = web3.eth.sendRawTransaction(signed_txn.rawTransaction)
    return txn_hash.hex()

if __name__ == "__main__":
    # Example: Check balance
    address_to_check = "0x57BBEC496A82eC51fBFFED75Eaa91E57e6510E83"  # Replace with the address you want to check
    print(get_function_list())
    balance = get_balance(address_to_check)
    print(f"Balance: {balance}")

    # Example: Transfer tokens
    #from_address = '0xYourAddress'  # Replace with your address
    #to_address = '0xRecipientAddress'  # Replace with recipient address
    #amount = 1000000000000000000  # Amount in wei (1 ETH = 10^18 wei)
    #private_key = 'YOUR_PRIVATE_KEY'  # Replace with your private key

    #txn_hash = transfer_tokens(from_address, to_address, amount, private_key)
    #print(f"Transaction Hash: {txn_hash}")