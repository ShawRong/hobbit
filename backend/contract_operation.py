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
abiwithaddress = get_abi_from_json('./hobbit/backend/docs/IntegratedTokenPlatform.json')
contract_abi = abiwithaddress[0]
contract_address = abiwithaddress[1]['1337']['address']


# Create contract object
contract = web3.eth.contract(address=contract_address, abi=contract_abi)

def apiProviders(provider_address):
    """
    获取API提供者的信息
    """
    try:
        provider = contract.functions.apiProviders(provider_address).call()
        return {
            'providerAddress': provider[0],
            'earnings': provider[1]
        }
    except Exception as e:
        print(f"获取API提供者信息时出错: {e}")
        return None

def balanceOf(address):
    """
    获取指定地址的代币余额
    """
    try:
        balance = contract.functions.balanceOf(address).call()
        return balance
    except Exception as e:
        print(f"获取余额时出错: {e}")
        return None

def isProvider(address):
    """
    检查地址是否为API提供者
    """
    try:
        return contract.functions.isProvider(address).call()
    except Exception as e:
        print(f"检查提供者状态时出错: {e}")
        return False

def addApiProvider(provider_address, sender_address, private_key):
    """
    添加API提供者
    """
    try:
        nonce = web3.eth.get_transaction_count(sender_address)
        
        # 构建交易
        transaction = contract.functions.addApiProvider(provider_address).build_transaction({
            'from': sender_address,
            'gas': 2000000,
            'gasPrice': web3.eth.gas_price,
            'nonce': nonce,
        })
        
        # 签名交易
        signed_txn = web3.eth.account.sign_transaction(transaction, private_key)
        
        # 发送交易
        tx_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
        
        # 等待交易确认
        receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
        return receipt
    except Exception as e:
        print(f"添加API提供者时出错: {e}")
        return None

def removeApiProvider(provider_address, sender_address, private_key):
    """
    移除API提供者
    """
    try:
        nonce = web3.eth.get_transaction_count(sender_address)
        
        # 构建交易
        transaction = contract.functions.removeApiProvider(provider_address).build_transaction({
            'from': sender_address,
            'gas': 2000000,
            'gasPrice': web3.eth.gas_price,
            'nonce': nonce,
        })
        
        # 签名交易
        signed_txn = web3.eth.account.sign_transaction(transaction, private_key)
        
        # 发送交易
        tx_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
        
        # 等待交易确认
        receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
        return receipt
    except Exception as e:
        print(f"移除API提供者时出错: {e}")
        return None

def useApi(provider_address, amount, sender_address, private_key):
    """
    使用API服务
    """
    try:
        nonce = web3.eth.get_transaction_count(sender_address)
        
        # 构建交易
        transaction = contract.functions.useApi(provider_address, amount).build_transaction({
            'from': sender_address,
            'gas': 2000000,
            'gasPrice': web3.eth.gas_price,
            'nonce': nonce,
        })
        
        # 签名交易
        signed_txn = web3.eth.account.sign_transaction(transaction, private_key)
        
        # 发送交易
        tx_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
        
        # 等待交易确认
        receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
        return receipt
    except Exception as e:
        print(f"使用API时出错: {e}")
        return None

# 添加一些辅助函数

def get_function_list():
    """
    获取合约的所有函数列表
    """
    try:
        function_list = []
        for item in contract_abi:
            if item['type'] == 'function':
                function_list.append(item['name'])
        return function_list
    except Exception as e:
        print(f"获取函数列表时出错: {e}")
        return []

def get_contract_address():
    """
    获取合约地址
    """
    return contract_address

# 使用示例
if __name__ == "__main__":
    # 示例地址和私钥（请替换为实际值）
    owner_address = "0x3d47335fd2b7330d90c6b6f674cf0735de094549"
    owner_address = web3.to_checksum_address(owner_address)
    owner_private_key = "0ad1df7638c948fd3181361d9436e901d0540fde045d02fdc05c208d605277e5"
    provider_address = "0x57BBEC496A82eC51fBFFED75Eaa91E57e6510E83"
    
    # 获取合约函数列表
    print("合约函数列表:")
    print(get_function_list())
    
    # 检查余额
    balance = balanceOf(owner_address)
    print(f"账户余额: {balance}")
    
    # 检查是否为提供者
    is_provider = isProvider(provider_address)
    print(f"是否为提供者: {is_provider}")
    
    # 获取提供者信息
    provider_info = apiProviders(provider_address)
    print(f"提供者信息: {provider_info}")