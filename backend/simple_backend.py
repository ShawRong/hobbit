# backend_service.py
from flask import Flask, jsonify, request
from db.llm_manager import LLMAPIManager

app = Flask(__name__)

# 固定的余额值
FIXED_BALANCE = 100
llm_api_manager = LLMAPIManager("mongodb://localhost:27017", "hobbit", "llm_apis")

#simple balance  
@app.route('/balance', methods=['GET'])
def get_balance():
    user_address = request.args.get('address')  # 获取请求中的地址参数
    return jsonify({"balance": FIXED_BALANCE})


@app.route('/add_api', methods=['POST'])
def add_api():
    data = request.json
    llm_api = data.get('llm_api')
    wallet_address = data.get('wallet_address')
    other_info = data.get('other_info', 0)  # Default to 0 if not provided
    llm_api_manager.add_api(llm_api, wallet_address, other_info)
    return jsonify({"message": "API added successfully"}), 201

@app.route('/apis', methods=['GET'])
def get_apis():
    return jsonify(llm_api_manager.get_api_info()), 200

@app.route('/pay', methods=['POST'])
def pay():
    data = request.json
    wallet_address = data.get('wallet_address')
    amount = data.get('amount', 0)  # Default to 0 if not provided
    # 这里可以添加实际的支付逻辑
    # TODO
    return jsonify({"message": f"Paid {amount} to {wallet_address}"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
