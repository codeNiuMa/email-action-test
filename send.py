import datetime
import json
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
        tools=[grounding_tool],
        system_instruction="你是一位专业的客户关系维护专家。请严格按照要求，为我的客户“远哥”生成一条问候语。",
    )

    today = datetime.datetime.now().strftime("%Y年%m月%d日")
    response = client.models.generate_content(
        model="gemini-2.5-pro",
        contents=f"""动态问候： 根据执行此任务的【此刻北京时间】，判断应使用“上午好”、“下午好”还是“晚上好”。
                     天气关怀： 查询【中国浙江省杭州市萧山区{today}】的天气情况，并根据天气（如：晴天、雨天、高温、降温等）给出一句简短的贴心提醒。
                     每日一言： 包含一句积极向上、充满正能量的句子。
                     语气与风格： 亲切自然，并适当添加几个Emoji表情符号。
                     字数限制： 总内容不超过200字。
                     输出格式： 请务必直接输出最终生成的问候语正文，不要包含任何“好的”、“当然”或“这是为您生成的问候语”等多余的AI提示或说明文字，确保内容可以直接复制发送。""",
        config=config
    )
    return response.text


mail_host = 'smtp.163.com'
# from 配置 import *
# mail_user = MAIL_USER
# mail_pass = MAIL_KEY
# sender = MAIL_USER
# API_KEY = API_KEY
# receivers = ['2325415123@qq.com']
mail_user = os.environ.get("MAIL_USER")
mail_pass = os.environ.get("MAIL_KEY")
sender = os.environ.get("MAIL_USER")
receivers = os.environ.get("RECEIVERS")

try:
    receivers = json.loads(receivers)
except json.JSONDecodeError:
    receivers = []

try:
    print("获取MAIL_USER:", bool(os.environ.get("MAIL_USER")))
    print("获取MAIL_KEY:", bool(os.environ.get("MAIL_KEY")))
    print("获取API_KEY:", bool(os.environ.get("API_KEY")))
    print("获取RECEIVERS:", bool(os.environ.get("RECEIVERS")))
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
