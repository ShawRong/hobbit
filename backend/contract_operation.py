# contract_interaction.py
from web3 import Web3
import json
import os
import time
import requests

# Replace with your Ethereum node's URL and port
node_url = 'http://xayah.tpddns.cn:1039'
trans_url = 'http://183.17.226.90:1040'

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

# 前后端使用
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

# 前后端使用
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

# 前后端使用
def isProvider(address):
    """
    检查地址是否为API提供者
    """
    try:
        result = contract.functions.isProvider(address).call()
        print(f"检查地址 {address} 的提供者状态: {result}")
        return result
    except Exception as e:
        print(f"检查提供者状态时出错: {str(e)}")
        return False

# 后端使用
def addApiProvider(provider_address, sender_address, private_key):
    """
    添加API提供者
    """
    try:
        nonce = web3.eth.get_transaction_count(sender_address)
        
        print(f"Debug: 发送者地址: {sender_address}")
        print(f"Debug: 提供者地址: {provider_address}")
        print(f"Debug: Chain ID: {web3.eth.chain_id}")
        
        # 构建交易
        transaction = contract.functions.addApiProvider(provider_address).build_transaction({
            'from': sender_address,
            'gas': 2000000,
            'gasPrice': web3.eth.gas_price,
            'nonce': nonce,
            'chainId': web3.eth.chain_id
        })
        
        # 签名交易
        signed_txn = web3.eth.account.sign_transaction(transaction, private_key)
        
        # 发送交易
        tx_hash = web3.eth.send_raw_transaction(signed_txn.raw_transaction.hex())
        
        # 等待交易确认
        receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
        
        # 等待几个区块确认
        time.sleep(2)
        
        # 验证提供者状态
        is_provider = contract.functions.isProvider(provider_address).call()
        print(f"Debug: 添加后立即检查提供者状态: {is_provider}")
        
        return receipt
    except Exception as e:
        print(f"添加API提供者时出错: {str(e)}")
        return None


# 后端使用
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
            'chainId': web3.eth.chain_id
        })
        
        # 签名交易
        signed_txn = web3.eth.account.sign_transaction(transaction, private_key)
        
        # 发送交易
        tx_hash = web3.eth.send_raw_transaction(signed_txn.raw_transaction.hex())
        
        # 等待交易确认
        receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
        return receipt
    except Exception as e:
        print(f"移除API提供者时出错: {str(e)}")
        return None


# 前端使用
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
            'chainId': web3.eth.chain_id
        })
        
        # 签名交易
        signed_txn = web3.eth.account.sign_transaction(transaction, private_key)
        
        # 发送交易
        tx_hash = web3.eth.send_raw_transaction(signed_txn.raw_transaction.hex())
        
        # 等待交易确认
        receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
        return receipt
    except Exception as e:
        print(f"使用API时出错: {str(e)}")
        return None

# 前端使用
def buyTokens(amount, sender_address, private_key):
    """
    购买代币
    """
    try:
        nonce = web3.eth.get_transaction_count(sender_address)
        
        # 构建交易
        transaction = contract.functions.buyTokens().build_transaction({
            'from': sender_address,
            'value': web3.to_wei(amount, 'ether'),  # 发送的ETH数量
            'gas': 2000000,
            'gasPrice': web3.eth.gas_price,
            'nonce': nonce,
            'chainId': web3.eth.chain_id  # 添加 chainId
        })
        
        # 签名交易
        signed_txn = web3.eth.account.sign_transaction(transaction, private_key)
        
        # 发送交易 - 使用 hex() 转换
        tx_hash = web3.eth.send_raw_transaction(signed_txn.raw_transaction.hex())
        
        # 等待交易确认
        receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
        return receipt
    except Exception as e:
        print(f"购买代币时出错: {str(e)}")
        return None

#前端使用
def burnTokens(eth_amount, sender_address, private_key):
    """
    销毁代币
    """
    try:
        nonce = web3.eth.get_transaction_count(sender_address)
        
        # 构建交易
        transaction = contract.functions.burnTokens(web3.to_wei(eth_amount, 'ether')).build_transaction({
            'from': sender_address,
            'gas': 2000000,
            'gasPrice': web3.eth.gas_price,
            'nonce': nonce,
            'chainId': web3.eth.chain_id  # 添加 chainId
        })
        
        # 签名交易
        signed_txn = web3.eth.account.sign_transaction(transaction, private_key)
        
        # 发送交易 - 使用 hex() 转换
        tx_hash = web3.eth.send_raw_transaction(signed_txn.raw_transaction.hex())
        
        # 等待交易确认
        receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
        return receipt
    except Exception as e:
        print(f"销毁代币时出错: {str(e)}")
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

def get_contract_info():
    """
    获取合约的基本信息
    """
    try:
        owner = contract.functions.owner().call()
        rate = contract.functions.rate().call()
        start_time = contract.functions.startTime().call()
        end_time = contract.functions.endTime().call()
        
        print("\n=== 合约信息 ===")
        print(f"合约地址: {contract.address}")
        print(f"合约所有者: {owner}")
        print(f"代币兑换率: {rate}")
        print(f"开始时间: {start_time}")
        print(f"结束时间: {end_time}")
        print("================\n")
        
        return {
            'owner': owner,
            'rate': rate,
            'start_time': start_time,
            'end_time': end_time
        }
    except Exception as e:
        print(f"获取合约信息时出错: {str(e)}")
        return None

def transferOwnership(new_owner, sender_address):
    """
    转移合约所有权
    """
    try:
        # 首先检查当前所有者
        current_owner = contract.functions.owner().call()
        if current_owner.lower() != sender_address.lower():
            raise Exception(f"只有当前所有者才能转移所有权。当前所有者: {current_owner}")
            
        nonce = web3.eth.get_transaction_count(sender_address)
        
        print(f"Debug: 当前所有者: {sender_address}")
        print(f"Debug: 新所有者: {new_owner}")
        print(f"Debug: Chain ID: {web3.eth.chain_id}")
        
        # 构建交易
        transaction = contract.functions.transferOwnership(new_owner).build_transaction({
            'from': sender_address,
            'gas': 2000000,
            'gasPrice': web3.eth.gas_price,
            'nonce': nonce,
            'chainId': web3.eth.chain_id,
        })
        
        # 准备签名请求
        sign_request = {
            "id": 2,
            "jsonrpc": "2.0",
            "method": "account_signTransaction",
            "params": [{
                "from": transaction['from'],
                "gas": hex(transaction['gas']),
                "gasPrice": hex(transaction['gasPrice']),
                "input": transaction['data'],
                "nonce": hex(transaction['nonce']),
                "to": transaction['to'],
                "value": "0x0",
                "chainId": hex(1337)  # 使用正确的 chainId
            }]
        }
        
        print("Debug: 签名请求:", json.dumps(sign_request, indent=2))
        
        # 发送签名请求
        headers = {'Content-Type': 'application/json'}
        response = requests.post(
            trans_url,  # 使用签名服务的 URL
            data=json.dumps(sign_request),
            headers=headers
        )
        
        if response.status_code != 200:
            raise Exception(f"签名请求失败: {response.text}")
            
        # 解析响应
        sign_result = response.json()
        if 'error' in sign_result:
            raise Exception(f"签名错误: {sign_result['error']}")
            
        print("Debug: 签名响应:", json.dumps(sign_result, indent=2))
        
        # 发送已签名的交易
        tx_hash = web3.eth.send_raw_transaction(sign_result['result']['raw'])
        
        # 等待交易确认
        receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
        
        # 验证所有权转移
        new_owner_check = contract.functions.owner().call()
        print(f"所有权转移后的新所有者: {new_owner_check}")
        
        if new_owner_check.lower() == new_owner.lower():
            print("所有权转移成功！")
        else:
            print("警告：所有权可能未成功转移")
            
        return receipt
    except Exception as e:
        print(f"转移所有权时出错: {str(e)}")
        return None

# 使用示例
if __name__ == "__main__":
    #contract_info = get_contract_info()
    owner_address= "0x57BBEC496A82eC51fBFFED75Eaa91E57e6510E83"
    owner_private_key = "faf683280f42e11e130d57797f67e00d19d1ad1e3463b4f29340d21e83f8c61f"
    _address = "0x57BBEC496A82eC51fBFFED75Eaa91E57e6510E83"
    _private_key = "faf683280f42e11e130d57797f67e00d19d1ad1e3463b4f29340d21e83f8c61f"
    
    # 获取合约函数列表
    print("合约函数列表:")
    print(get_function_list())
    
    # 检查余额
    balance = balanceOf(_address)
    print(f"账户余额: {balance}")

    # 检查是否为提供者
    try:
        print(f"尝试添加API提供者: {_address}")
        
        # 检查初始状态
        initial_status = contract.functions.isProvider(_address).call()
        print(f"初始提供者状态: {initial_status}")
        
        # 添加提供者
        result = addApiProvider(_address, owner_address, owner_private_key)
        if result:
            # 等待交易确认
            web3.eth.wait_for_transaction_receipt(result['transactionHash'])
            print(f"成功添加API提供者，交易哈希: {result['transactionHash'].hex()}")
            
            # 多等待几秒确保状态更新
            time.sleep(5)
            
            # 检查状态
            is_provider = contract.functions.isProvider(_address).call()
            print(f"添加后提供者状态: {is_provider}")
            
            # 获取提供者详细信息
            provider_info = contract.functions.apiProviders(_address).call()
            print(f"提供者详细信息: {provider_info}")
            
        else:
            print("添加API提供者失败")
            
    except Exception as e:
        print(f"测试过程中发生错误: {str(e)}")

    try:
        print(f"尝试移除API提供者: {_address}")
        result = removeApiProvider(_address, owner_address, owner_private_key)
        if result:
            print(f"成功移除API提供者，交易哈希: {result['transactionHash'].hex()}")
        else:
            print("移除API提供者失败")
            
        is_provider = isProvider(_address)
        print(f"是否为提供者: {is_provider}")
    except Exception as e:
        print(f"移除API提供者过程中发生错误: {str(e)}")
    
    # 获取提供者信息
    provider_info = apiProviders(_address)
    print(f"提供者信息: {provider_info}")

    #amount = 1000
    #buyTokens(amount, _address, _private_key)
    #print(f"buy tokens: {amount}{_address}")
    #burnTokens(amount, _address, _private_key)
    #print(f"burn tokens: {amount}{_address}")

    # 获取合约信息