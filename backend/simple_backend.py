# backend_service.py
from flask import Flask, jsonify, request
from db.llm_manager import LLMAPIManager
import contract_operation as co

app = Flask(__name__)

# 固定的余额值
owner_address= "0x57BBEC496A82eC51fBFFED75Eaa91E57e6510E83"
owner_private_key = "faf683280f42e11e130d57797f67e00d19d1ad1e3463b4f29340d21e83f8c61f"
llm_api_manager = LLMAPIManager("mongodb://localhost:27017", "hobbit", "llm_apis")

#simple balance  
@app.route('/balance', methods=['GET'])
def get_balance():
    user_address = request.args.get('address')  # 获取请求中的地址参数
    balance = co.balanceOf(user_address)
    return jsonify({"balance": balance})


@app.route('/add_api', methods=['POST'])
def add_api():
    data = request.json
    llm_api = data.get('llm_api')
    wallet_address = data.get('wallet_address')
    other_info = data.get('other_info', 0)  # Default to 0 if not provided
    llm_api_manager.add_api(llm_api, wallet_address, other_info)
    co.addApiProvider(wallet_address, owner_address, owner_private_key)
    return jsonify({"message": "API added successfully"}), 201

@app.route('/remove_api', methods=['POST'])
def remove_api():
    data = request.json
    llm_api = data.get('llm_api')
    wallet_address = data.get('wallet_address')
    
    # 从数据库中移除 API
    if llm_api_manager.remove_api(llm_api):
        # 调用智能合约移除 API provider
        co.removeApiProvider(wallet_address, owner_address, owner_private_key)
        return jsonify({"message": "API removed successfully"}), 200
    else:
        return jsonify({"error": "API not found"}), 404


@app.route('/apis', methods=['GET'])
def get_apis():
    try:
        apis = llm_api_manager.get_api_info()
        # 使用列表推导式过滤提供者，添加错误处理
        apis = [api for api in apis if (lambda addr: co.isProvider(addr) if addr else False)(api["wallet_address"])]
        llm_api_manager.apis = apis
        return jsonify(apis), 200
    except Exception as e:
        print(f"获取API信息时出错: {str(e)}")
        return jsonify({"error": str(e)}), 500  # 返回详细的错误信息


#Not used.
@app.route('/a', methods=['POST'])
def pay():
    data = request.json
    wallet_address = data.get('wallet_address')
    amount = data.get('amount', 0)  # Default to 0 if not provided
    sender_address = data.get('sender_address', )
    tx = co.useApi(wallet_address, amount, sender_address)
      
    return jsonify({"message": f"Paid {amount} to {wallet_address}"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
