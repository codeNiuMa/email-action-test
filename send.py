import datetime
import os
import smtplib
from email.mime.text import MIMEText
import ssl


# 设置服务器所需信息
def content():
    import datetime
    from google import genai
    from google.genai import types

    # from 配置 import API_KEY
    # API_KEY = API_KEY
    API_KEY = os.environ.get("API_KEY")
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
        model="gemini-2.5-pro",
        contents=f"根据此刻的时间，给我写一个发给客户远哥的上午或下午或晚间的问候语，根据中国浙江省杭州市萧山区{today}的天气给出必要的提示，包含正能量的每日一言，适当添加emoji表情，200字以内。要求直接输出正文内容，删除掉多余的AI输出提示，可以直接用于发送给他人的邮件正文中。",
        config=config
    )
    return response.text


mail_host = 'smtp.163.com'
# from 配置 import *
# mail_user = MAIL_USER
# mail_pass = MAIL_KEY
# sender = MAIL_USER
# API_KEY = API_KEY
mail_user = os.environ.get("MAIL_USER")
mail_pass = os.environ.get("MAIL_KEY")
sender = os.environ.get("MAIL_USER")

receivers = ['2325415123@qq.com']
# 与收件人列表对应的姓名列表
names = ["远哥"]

# 确保名字和接收者列表长度相同
assert len(names) == len(receivers), "Names and receivers lists must have the same length."

try:
    print("获取MAIL_USER:", bool(os.environ.get("MAIL_USER")))
    print("获取MAIL_KEY:", bool(os.environ.get("MAIL_KEY")))
    print("获取API_KEY:", bool(os.environ.get("API_KEY")))
    for receiver in receivers:
        print("1️⃣ 创建 SMTP 对象…")
        smtpObj = smtplib.SMTP_SSL(mail_host, 465, context=ssl.create_default_context(), timeout=30)
        print("2️⃣ 登录…")
        smtpObj.login(mail_user, mail_pass)
        print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] 生成中。。。")
        try:
            # content = "测试内容"
            content2 = content()
            print("生成完毕\n", content2, f"\n[{datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')}] EOF")
        except Exception as e:
            print(f"[{datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')}] 生成内容时发生错误: {e}\n")
            content2 = f"[{datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')}] 生成内容时发生错误，请稍后再试。"
            content = content2

        message = MIMEText(content2, 'plain', 'utf-8')

        # 根据UTC时间判断北京时间上下午晚上
        if (datetime.datetime.utcnow().hour + 8) % 24 < 12:
            message['Subject'] = f'{datetime.datetime.now().strftime("%Y年%m月%d日")}——上午好！'
        elif (datetime.datetime.utcnow().hour + 8) % 24 < 18:
            message['Subject'] = f'{datetime.datetime.now().strftime("%Y年%m月%d日")}——下午好！'
        else:
            message['Subject'] = f'{datetime.datetime.now().strftime("%Y年%m月%d日")}——晚上好！'

        # 发送方信息
        message['From'] = sender

        # 接受方信息
        message['To'] = receiver

        smtpObj.sendmail(sender, [receiver], message.as_string())

        smtpObj.quit()
    print(f'{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")} success')
except Exception as e:
    print(f'{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")} 发送失败error', e)
