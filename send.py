import datetime
import os
import smtplib
from email.mime.text import MIMEText


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
        contents=f"给我写一个发给客户远哥的清晨问候语，概括中国浙江省杭州市萧山区{today}的天气，包含正能量的每日一言等等，200字以内。要求直接输出正文内容，删除掉多余的AI输出提示，可以直接用于发送给他人的邮件正文中。",
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
    smtpObj = smtplib.SMTP_SSL(mail_host, 465)
    smtpObj.login(mail_user, mail_pass)
    for receiver in receivers:
        print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] 生成中。。。\n")
        try:
            content2 = content()
            print("生成完毕\n", content2, "\n[{datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')}] EOF\n")
        except Exception as e:
            print(f"[{datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')}] 生成内容时发生错误: {e}\n")
            content2 = f"[{datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')}] 生成内容时发生错误，请稍后再试。"

        message = MIMEText(content2, 'plain', 'utf-8')

        # 邮件主题
        message['Subject'] = f'{datetime.datetime.now().strftime("%Y年%m月%d日")}——早上好！'

        # 发送方信息
        message['From'] = sender

        # 接受方信息
        message['To'] = receiver

        smtpObj.sendmail(sender, [receiver], message.as_string())

    smtpObj.quit()
    print('success')
except smtplib.SMTPException as e:
    print('error', e)
