import datetime

from google import genai
from google.genai import types

from 服务器.邮件新.配置 import API_KEY

client = genai.Client(api_key=API_KEY)

# Define the grounding tool
grounding_tool = types.Tool(
    google_search=types.GoogleSearch()
)

# Configure generation settings
config = types.GenerateContentConfig(
    tools=[grounding_tool]
)

today = datetime.datetime.now().strftime("%Y年%m月%d日")
response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=f"根据中国浙江省杭州市萧山区{today}的天气，给我一个发给客户远哥的清晨问候语。要求直接输出正文内容，删除掉多余的AI输出提示，可以直接用于发送给他人的邮件正文中。",
    config=config
)

if __name__ == '__main__':
    print(response.text)
