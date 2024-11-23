package main

import (
	"context"
	"encoding/json"
	"fmt"
	"net/http"
	"sync"
	"time"

	"go.mongodb.org/mongo-driver/mongo"
	"go.mongodb.org/mongo-driver/mongo/options"
)

// UserBalanceResponse 代表从 API 返回的用户余额结构体
type UserBalanceResponse struct {
	Address string `json:"address"`
	Balance int    `json:"balance"`
}

// KeyManager 管理用户密钥的结构体
type KeyManager struct {
	userKeys  map[string]bool
	mux       sync.RWMutex
	apiURL    string // API 地址
	collection *mongo.Collection // MongoDB 集合
}

// NewKeyManager 创建一个新的 KeyManager
func NewKeyManager(apiURL, mongoURI, dbName, collectionName string) (*KeyManager, error) {
	client, err := mongo.Connect(context.TODO(), options.Client().ApplyURI(mongoURI))
	if err != nil {
		return nil, err
	}

	collection := client.Database(dbName).Collection(collectionName)

	km := &KeyManager{
		userKeys:  make(map[string]bool),
		apiURL:    apiURL,
		collection: collection,
	}
	if err := km.LoadFromDB(); err != nil {
		return nil, err
	}
	return km, nil
}

// ActivateKey 激活用户密钥
func (km *KeyManager) ActivateKey(userAddress string) error {
	balance, err := km.getUserBalance(userAddress)
	if err != nil {
		return err
	}

	if balance <= 0 {
		return fmt.Errorf("insufficient tokens to activate key")
	}

	km.mux.Lock()
	defer km.mux.Unlock()
	km.userKeys[userAddress] = true
	return km.SaveToDB() // 保存到数据库
}

// DeactivateKey 停用用户密钥
func (km *KeyManager) DeactivateKey(userAddress string) {
	km.mux.Lock()
	defer km.mux.Unlock()
	delete(km.userKeys, userAddress)
	km.SaveToDB() // 保存到数据库
}

// IsKeyActive 检查用户密钥是否激活
func (km *KeyManager) IsKeyActive(userAddress string) bool {
	km.mux.RLock()
	defer km.mux.RUnlock()
	return km.userKeys[userAddress]
}

// getUserBalance 调用 API 获取用户余额
func (km *KeyManager) getUserBalance(userAddress string) (int, error) {
	resp, err := http.Get(fmt.Sprintf("%s/balance?address=%s", km.apiURL, userAddress))
	if err != nil {
		return 0, err
	}
	defer resp.Body.Close()

	if resp.StatusCode != http.StatusOK {
		return 0, fmt.Errorf("failed to get balance: %s", resp.Status)
	}

	var balanceResponse UserBalanceResponse
	if err := json.NewDecoder(resp.Body).Decode(&balanceResponse); err != nil {
		return 0, err
	}

	return balanceResponse.Balance, nil
}

// SaveToDB 将密钥信息保存到 MongoDB
func (km *KeyManager) SaveToDB() error {
	km.mux.RLock()
	defer km.mux.RUnlock()

	// 清空当前集合
	_, err := km.collection.DeleteMany(context.TODO(), struct{}{})
	if err != nil {
		return err
	}

	// 插入当前的 userKeys
	for address, active := range km.userKeys {
		_, err := km.collection.InsertOne(context.TODO(), map[string]interface{}{
			"address": address,
			"active":  active,
		})
		if err != nil {
			return err
		}
	}
	return nil
}

// LoadFromDB 从 MongoDB 加载密钥信息
func (km *KeyManager) LoadFromDB() error {
	km.mux.Lock()
	defer km.mux.Unlock()

	cursor, err := km.collection.Find(context.TODO(), struct{}{})
	if err != nil {
		return err
	}
	defer cursor.Close(context.TODO())

	for cursor.Next(context.TODO()) {
		var result struct {
			Address string `bson:"address"`
			Active  bool   `bson:"active"`
		}
		if err := cursor.Decode(&result); err != nil {
			return err
		}
		km.userKeys[result.Address] = result.Active
	}
	return cursor.Err()
}

func main() {
	apiURL := "http://example.com/api" // 替换为实际的 API 地址
	mongoURI := "mongodb://localhost:27017" // MongoDB 连接字符串
	dbName := "mydatabase"                   // 数据库名称
	collectionName := "user_keys"            // 集合名称

	keyManager, err := NewKeyManager(apiURL, mongoURI, dbName, collectionName)
	if err != nil {
		fmt.Println("Error initializing KeyManager:", err)
		return
	}

	userAddress := "0x1234567890abcdef" // 示例用户地址

	// 激活密钥
	if err := keyManager.ActivateKey(userAddress); err != nil {
		fmt.Println("Error activating key:", err)
	} else {
		fmt.Println("Key activated for user:", userAddress)
	}

	// 检查密钥状态
	if keyManager.IsKeyActive(userAddress) {
		fmt.Println("Key is active for user:", userAddress)
	} else {
		fmt.Println("Key is not active for user:", userAddress)
	}

	// 停用密钥
	keyManager.DeactivateKey(userAddress)
	fmt.Println("Key deactivated for user:", userAddress)
}