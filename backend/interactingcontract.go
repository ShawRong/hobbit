package main

import (
	"context"
	"fmt"
	"log"
	"math/big"

	"github.com/ethereum/go-ethereum"
	"github.com/ethereum/go-ethereum/accounts/abi"
	"github.com/ethereum/go-ethereum/common"
	"github.com/ethereum/go-ethereum/ethclient"
)

// ERC20 ABI (只包含 balanceOf 方法)
const erc20ABI = `[{"constant":true,"inputs":[{"name":"_owner","type":"address"}],"name":"balanceOf","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"}]`

func main() {
	// 以太坊节点的 URL
	nodeURL := "https://your.ethereum.node.url" // 替换为你的以太坊节点 URL
	// 用户地址
	userAddress := "0x1234567890abcdef1234567890abcdef12345678" // 替换为实际用户地址
	// 合约地址
	contractAddress := "0xabcdefabcdefabcdefabcdefabcdefabcdefabcd" // 替换为实际合约地址

	// 创建以太坊客户端
	client, err := ethclient.Dial(nodeURL)
	if err != nil {
		log.Fatalf("Failed to connect to the Ethereum client: %v", err)
	}

	// 解析合约的 ABI
	parsedABI, err := abi.JSON(strings.NewReader(erc20ABI))
	if err != nil {
		log.Fatalf("Failed to parse ABI: %v", err)
	}

	// 创建调用数据
	data, err := parsedABI.Pack("balanceOf", common.HexToAddress(userAddress))
	if err != nil {
		log.Fatalf("Failed to pack data: %v", err)
	}

	// 创建调用参数
	msg := ethereum.CallMsg{
		To:   &common.HexToAddress(contractAddress),
		Data: data,
	}

	// 调用合约方法
	result, err := client.CallContract(context.Background(), msg, nil)
	if err != nil {
		log.Fatalf("Failed to call contract: %v", err)
	}

	// 解码返回值
	var balance *big.Int
	err = parsedABI.UnpackIntoInterface(&balance, "balanceOf", result)
	if err != nil {
		log.Fatalf("Failed to unpack result: %v", err)
	}

	// 输出余额
	fmt.Printf("Balance of %s: %s\n", userAddress, balance.String())
}