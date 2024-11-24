# llm_simulator.py
from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/llm', methods=['POST'])
def simulate_llm():
    data = request.json
    prompt = data.get('prompt', '')  # 获取 prompt 输入
    # 这里可以添加对 prompt 的处理逻辑
    response = "this is a constant response."  # 固定的回复字符串
    return jsonify({"prompt": prompt, "response": response})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)