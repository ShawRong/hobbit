package main

import (
	"context"
	"fmt"
	"log"
	"time"
	"db"

	"go.mongodb.org/mongo-driver/mongo"
	"go.mongodb.org/mongo-driver/mongo/options"
)

type ApiRecord struct {
	URL           string    `bson:"url"`
	Key           string    `bson:"key"`
	WalletAddress string    `bson:"wallet_address"`
	Timestamp     time.Time `bson:"timestamp"`
}

func getCollection(client *mongo.Client) (*mongo.Collection) {
	return collection := client.Database("url_tracker").Collection("api_records")
}

type Collection struct{
	content *mongo.Collection
}

func (collection Collection) saveRecord(url, key, walletAddress string) {
	record := ApiRecord{
		URL:           url,
		Key:           key,
		WalletAddress: walletAddress,
		Timestamp:     time.Now(),
	}

	_, err := collection.InsertOne(context.TODO(), record)
	if err != nil {
		log.Fatal(err)
	}
	fmt.Println("Record saved successfully!")
}

func (collection Collection) getRecords() []ApiRecord {
	cursor, err := collection.Find(context.TODO(), nil)
	if err != nil {
		log.Fatal(err)
	}
	defer cursor.Close(context.TODO())

	var records []ApiRecord
	if err = cursor.All(context.TODO(), &records); err != nil {
		log.Fatal(err)
	}

	if len(records) == 0 {
		fmt.Println("没有找到任何记录。")
	}
	return records
}

func main() {
	connection := db.connectToMongo()
	defer client.Disconnect(context.TODO())
	collection := getCollection(connection)

	for {
		var action int
		fmt.Println("请选择操作：1-添加记录，2-获取记录，3-退出：")
		fmt.Scan(&action)

		switch action {
		case 1:
			var url, key, walletAddress string
			fmt.Print("请输入 API URL：")
			fmt.Scan(&url)
			fmt.Print("请输入密钥：")
			fmt.Scan(&key)
			fmt.Print("请输入钱包地址：")
			fmt.Scan(&walletAddress)
			collection.saveRecord(url, key, walletAddress)
		case 2:
			fmt.Println("当前记录：")
			collection.getRecords()
		case 3:
			return
		default:
			fmt.Println("无效的选择，请重试。")
		}
	}
}