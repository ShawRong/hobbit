# llm_simulator.py
from flask import Flask, jsonify, request
import asyncio
import poe

app = Flask(__name__)

@app.route('/gpt', methods=['POST'])
async def gpt():
    data = request.json
    prompt = data.get('prompt')  # 获取 prompt 输入
    key = data.get('key')  # 获取 key 输入

    # Check for missing prompt or key
    if not prompt or not key:
        return jsonify({"error": "Missing prompt or key"}), 400

    # 这里可以添加对 prompt 的处理逻辑
    try:
        response = await poe.gpt3_5(prompt, key)
        return jsonify({"prompt": prompt, "response": response})
    except Exception as e:
        return jsonify({"error": str(e)}), 500  # Handle errors from the poe function

@app.route('/capybara', methods=['POST'])
async def capybara():
    data = request.json
    prompt = data.get('prompt')  # 获取 prompt 输入
    key = data.get('key')  # 获取 key 输入

    # Check for missing prompt or key
    if not prompt or not key:
        return jsonify({"error": "Missing prompt or key"}), 400

    # 这里可以添加对 prompt 的处理逻辑
    try:
        response = await poe.capybara(prompt, key)
        return jsonify({"prompt": prompt, "response": response})
    except Exception as e:
        return jsonify({"error": str(e)}), 500  # Handle errors from the poe function

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)