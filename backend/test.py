import requests
import json

def main():
    url = "https://qianfan.baidubce.com/v2/chat/completions"
    
    payload = json.dumps({
        "model": "deepseek-v3.1-250821",
        "messages": [
            {
                "role": "system",
                "content": "You are a helpful assistant."
            },
            {
                "role": "user",
                "content": "你用的是什么大模型呢？"
            }
        ]
    })
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer bce-v3/ALTAK-CY40GtnpaRqV7Q5Q6eJTz/6f8f0b57ba68382fa8e48a530562bb2576ecfdef'
    }
    
    response = requests.request("POST", url, headers=headers, data=payload)
    
    print(response.text)
    

if __name__ == '__main__':
    main()