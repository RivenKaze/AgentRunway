import requests
import json
 
# API URL
url = 'https://api.coze.cn/v1/workflow/run'
 
# Headers
headers = {
    'Authorization': 'Bearer pat_bdVgMIeib37gvbyxHzlKzloZj4ooqWZL9Z62SFy0JMZJziWVpweXsy1A4OeEM5kM',  # 替换为真实的token
    'Content-Type': 'application/json'
}
 
# 请求数据
data = {
    "workflow_id": "7537982459381350400",  # 替换为实际的workflow_id
    "parameters": {   # 你的工作流的输入
        "input": "金发女模特"
    }
}
 
response = requests.post(url, headers=headers, data=json.dumps(data))
print(response.status_code)
print(response.json())  # 如果返回的是 JSON 数据