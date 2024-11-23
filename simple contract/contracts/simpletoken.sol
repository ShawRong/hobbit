// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract SimpleToken {
    string public name = "SimpleToken"; // 代币名称
    string public symbol = "STK";        // 代币符号
    uint8 public decimals = 18;           // 小数位数
    uint256 public totalSupply;           // 总供应量

    // 映射以存储每个地址的余额
    mapping(address => uint256) public balanceOf;
    // 映射以存储每个地址的授权额度
    mapping(address => mapping(address => uint256)) public allowance;

    // 事件
    event Transfer(address indexed from, address indexed to, uint256 value);
    event Approval(address indexed owner, address indexed spender, uint256 value);

    constructor(uint256 _initialSupply) {
        totalSupply = _initialSupply * (10 ** uint256(decimals)); // 设置总供应量
        balanceOf[msg.sender] = totalSupply; // 将全部代币分配给合约创建者
    }

    // 转账函数
    function transfer(address _to, uint256 _value) public returns (bool success) {
        require(_to != address(0), "Invalid address");
        require(balanceOf[msg.sender] >= _value, "Insufficient balance");
        balanceOf[msg.sender] -= _value;
        balanceOf[_to] += _value;
        emit Transfer(msg.sender, _to, _value);
        return true;
    }

    // 授权函数
    function approve(address _spender, uint256 _value) public returns (bool success) {
        allowance[msg.sender][_spender] = _value;
        emit Approval(msg.sender, _spender, _value);
        return true;
    }

    // 代币转移函数
    function transferFrom(address _from, address _to, uint256 _value) public returns (bool success) {
        require(_from != address(0), "Invalid from address");
        require(_to != address(0), "Invalid to address");
        require(balanceOf[_from] >= _value, "Insufficient balance");
        require(allowance[_from][msg.sender] >= _value, "Allowance exceeded");

        balanceOf[_from] -= _value;
        balanceOf[_to] += _value;
        allowance[_from][msg.sender] -= _value;
        emit Transfer(_from, _to, _value);
        return true;
    }

    uint256 private number;

    // 设置数值
    function setNumber(uint256 _number) public {
        number = _number;
    }

    // 获取数值
    function getNumber() public view returns (uint256) {
        return number;
    }    
    
    // 获取指定地址的余额
    function getBalance(address _owner) public view returns (uint256) {
        return balanceOf[_owner];
    }
}