package main

import (
	"bytes"
	"encoding/json"
	"fmt"
	"io/ioutil"
	"log"
	"net/http"
)

// 请求体结构体
type RequestBody struct {
	Input string `json:"input"`
}

// 响应体结构体
type ResponseBody struct {
	Output string `json:"output"`
}

// 发送请求并获取 LLM 回复
func getLLMResponse(url string, input string) (string, error) {
	body := RequestBody{Input: input}
	jsonData, err := json.Marshal(body)
	if err != nil {
		return "", err
	}

	resp, err := http.Post(url, "application/json", bytes.NewBuffer(jsonData))
	if err != nil {
		return "", err
	}
	defer resp.Body.Close()

	if resp.StatusCode != http.StatusOK {
		return "", fmt.Errorf("failed to get response: %s", resp.Status)
	}

	var responseBody ResponseBody
	if err := json.NewDecoder(resp.Body).Decode(&responseBody); err != nil {
		return "", err
	}

	return responseBody.Output, nil
}

func main() {
	// 保存 URL 列表
	urls := []string{
		"http://example.com/llm1", // 替换为实际的 LLM API URL
		"http://example.com/llm2", // 替换为实际的 LLM API URL
	}

	input := "Hello, how can I use LLM for my application?"

	for _, url := range urls {
		response, err := getLLMResponse(url, input)
		if err != nil {
			log.Printf("Error calling %s: %v", url, err)
			continue
		}
		fmt.Printf("Response from %s: %s\n", url, response)
	}
}