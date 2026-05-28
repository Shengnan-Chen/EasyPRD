import streamlit as st
import requests

# 请替换为你从 Render 获取的真实 URL
API_URL = "https://easyprd.onrender.com/generate_prd"

st.title("PRD 生成器 (网页版)")
user_input = st.text_area("请输入你的需求", height=150)

if st.button("生成 PRD"):
    if not user_input:
        st.warning("请先输入需求！")
    else:
        with st.spinner("AI 正在思考中..."):
            try:
                response = requests.post(API_URL, json={"prompt": user_input})
                
                if response.status_code == 200:
                    result = response.json()
                    if result.get("status") == "success":
                        st.markdown("### 生成结果：")
                        st.write(result.get("prd_content"))
                    else:
                        st.error(f"后端报错: {result.get('message')}")
                else:
                    st.error(f"无法连接到服务器 (错误码: {response.status_code})")
            except Exception as e:
                st.error(f"发生异常: {str(e)}")