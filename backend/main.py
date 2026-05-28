from fastapi import FastAPI, Request
import os
import requests

app = FastAPI()

# 确保在 Render 中配置了环境变量 API_KEY
API_KEY = os.environ.get("API_KEY")

@app.post("/generate_prd")
async def generate_prd(request: Request):
    if not API_KEY:
        return {"status": "error", "message": "API Key 未在服务器配置"}

    try:
        data = await request.json()
        user_prompt = data.get("prompt", "")
        
        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": "openai/gpt-3.5-turbo", 
            "messages": [
                {"role": "system", "content": "你是一位专业的产品经理，请根据用户需求生成结构化、清晰的 PRD 文档。"},
                {"role": "user", "content": user_prompt}
            ]
        }
        
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=payload
        )
        
        if response.status_code != 200:
            return {"status": "error", "message": f"OpenRouter 错误: {response.text}"}
            
        result = response.json()
        # 提取 AI 的回答内容
        prd_content = result.get("choices", [{}])[0].get("message", {}).get("content", "未能生成 PRD")
        
        return {"status": "success", "prd_content": prd_content}

    except Exception as e:
        return {"status": "error", "message": str(e)}