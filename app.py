# إيقاف إجباري لأي خادم قديم يعمل على نفس المنفذ لضمان عدم التداخل
import os
import signal
import subprocess

PORT = 9000

try:
    command = f"lsof -t -i:{PORT}"
    pid = subprocess.check_output(command, shell=True).decode().strip()
    if pid:
        os.kill(int(pid), signal.SIGKILL)
        print(f"تم إيقاف الخادم القديم على المنفذ {PORT} بنجاح.")
except Exception:
    pass

from flask import Flask, render_template_string, request, jsonify

app = Flask(__name__)

# واجهة تطبيق C ROBOT AI المتكاملة في شاشة واحدة مطابقة للتصميم
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>C ROBOT AI - الروبوت الذكي المتكلم</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
        body {
            background-color: #030712;
            color: #ffffff;
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            background-image: radial-gradient(circle at center, #0f172a 0%, #030712 100%);
            padding: 15px;
        }
        .container {
            width: 100%;
            max-width: 450px;
            display: flex;
            flex-direction: column;
            align-items: center;
            text-align: center;
        }
        .header h1 {
            font-size: 24px;
            color: #38bdf8;
            margin-bottom: 4px;
            text-shadow: 0 0 10px rgba(56, 189, 248, 0.5);
        }
        .header p {
            font-size: 13px;
            color: #94a3b8;
            margin-bottom: 15px;
        }
        .robot-face-box {
            position: relative;
            width: 240px;
            height: 240px;
            border-radius: 50%;
            background: linear-gradient(145deg, #0f172a, #1e293b);
            border: 3px solid #38bdf8;
            box-shadow: 0 0 30px rgba(56, 189, 248, 0.4), inset 0 0 20px rgba(56, 189, 248, 0.2);
            display: flex;
            align-items: center;
            justify-content: center;
            margin-bottom: 15px;
            overflow: hidden;
        }
        .robot-face-box img {
            width: 100%;
            height: 100%;
            object-fit: cover;
            border-radius: 50%;
        }
        .status-badge {
            background: rgba(15, 23, 42, 0.9);
            border: 1px solid #38bdf8;
            padding: 6px 14px;
            border-radius: 20px;
            font-size: 12px;
            color: #38bdf8;
            margin-bottom: 15px;
            display: flex;
            align-items: center;
            gap: 6px;
        }
        .status-dot {
            width: 7px;
            height: 7px;
            background-color: #22c55e;
            border-radius: 50%;
            box-shadow: 0 0 6px #22c55e;
        }
        .chat-box {
            width: 100%;
            background: rgba(15, 23, 42, 0.8);
            border: 1px solid rgba(56, 189, 248, 0.3);
            border-radius: 14px;
            padding: 12px;
            min-height: 100px;
            max-height: 150px;
            overflow-y: auto;
            margin-bottom: 15px;
            text-align: right;
            font-size: 13px;
            line-height: 1.5;
        }
        .chat-message {
            margin-bottom: 8px;
            color: #e2e8f0;
        }
        .chat-message.bot {
            color: #38bdf8;
        }
        .talk-btn {
            width: 100%;
            background: linear-gradient(135deg, #0284c7, #0369a1);
            color: white;
            border: none;
            padding: 14px;
            border-radius: 25px;
            font-size: 15px;
            font-weight: bold;
            cursor: pointer;
            box-shadow: 0 4px 15px rgba(2, 132, 199, 0.4);
            transition: 0.3s;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 8px;
        }
        .talk-btn:hover {
            background: linear-gradient(135deg, #0369a1, #075985);
        }
        .footer-note {
            margin-top: 12px;
            font-size: 11px;
            color: #64748b;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>C ROBOT AI</h1>
            <p>الروبوت الذكي المتكلم</p>
        </div>

        <div class="robot-face-box">
            <img src="https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?q=80&w=500&auto=format&fit=crop" alt="C Robot AI">
        </div>

        <div class="status-badge">
            <div class="status-dot"></div>
            <span>Online & Ready - متصل وجاهز (Port 9000)</span>
        </div>

        <div class="chat-box" id="chatBox">
            <div class="chat-message bot">🤖 مرحباً، أنا C ROBOT AI روبوت ذكي متكلم حقيقي، كيف يمكنني مساعدتك اليوم؟</div>
        </div>

        <button class="talk-btn" onclick="startTalking()">
            🎙️ تحدث مع C ROBOT AI
        </button>

        <div class="footer-note">
            C ROBOT AI - الذكاء الاصطناعي في خدمتك
        </div>
    </div>

    <script>
        function startTalking() {
            const chatBox = document.getElementById('chatBox');
            chatBox.innerHTML += `<div class="chat-message">👤 مستخدم: ما هو الطقس اليوم في الجزائر؟</div>`;
            setTimeout(() => {
                chatBox.innerHTML += `<div class="chat-message bot">🤖 C ROBOT AI: اليوم في الجزائر مشمس، درجة الحرارة 25°C. أتمنى لك يوماً رائعاً!</div>`;
                chatBox.scrollTop = chatBox.scrollHeight;
            }, 1000);
            chatBox.scrollTop = chatBox.scrollHeight;
        }
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get('message', '')
    return jsonify({"response": f"تم استلام رسالتك: {user_message}"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=PORT, debug=True)
