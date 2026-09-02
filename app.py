# إيقاف إجباري لأي خادم قديم يعمل على نفس المنفذ لضمان عدم التداخل
import os
import signal
import subprocess

PORT = 7000

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

# واجهة المستخدم الموحدة (شاشة واحدة: وجه الروبوتية المتكلمة الحقيقية فقط بتصميم مطابق 100%)
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
            overflow-x: hidden;
            background-image: radial-gradient(circle at center, #0f172a 0%, #030712 100%);
        }
        .container {
            width: 100%;
            max-width: 480px;
            padding: 20px;
            display: flex;
            flex-direction: column;
            align-items: center;
            text-align: center;
        }
        .header {
            margin-bottom: 20px;
        }
        .header h1 {
            font-size: 26px;
            color: #38bdf8;
            margin-bottom: 5px;
            text-shadow: 0 0 15px rgba(56, 189, 248, 0.6);
            letter-spacing: 1px;
        }
        .header p {
            font-size: 14px;
            color: #94a3b8;
        }
        /* إطار وجه الروبوت المتكلم الساطع */
        .robot-face-box {
            position: relative;
            width: 280px;
            height: 280px;
            border-radius: 50%;
            background: linear-gradient(145deg, #0f172a, #1e293b);
            border: 3px solid #38bdf8;
            box-shadow: 0 0 40px rgba(56, 189, 248, 0.5), inset 0 0 25px rgba(56, 189, 248, 0.3);
            display: flex;
            align-items: center;
            justify-content: center;
            margin-bottom: 20px;
            overflow: hidden;
        }
        .robot-face-box img {
            width: 100%;
            height: 100%;
            object-fit: cover;
            border-radius: 50%;
            animation: pulseGlow 3s infinite alternate;
        }
        @keyframes pulseGlow {
            0% { transform: scale(1); filter: drop-shadow(0 0 8px #38bdf8); }
            100% { transform: scale(1.02); filter: drop-shadow(0 0 20px #38bdf8); }
        }
        .status-badge {
            background: rgba(15, 23, 42, 0.85);
            border: 1px solid #38bdf8;
            padding: 8px 18px;
            border-radius: 20px;
            font-size: 13px;
            color: #38bdf8;
            margin-bottom: 20px;
            display: flex;
            align-items: center;
            gap: 8px;
            box-shadow: 0 0 12px rgba(56, 189, 248, 0.3);
        }
        .status-dot {
            width: 8px;
            height: 8px;
            background-color: #22c55e;
            border-radius: 50%;
            box-shadow: 0 0 10px #22c55e;
        }
        /* نافذة المحادثة التفاعلية */
        .chat-box {
            width: 100%;
            background: rgba(15, 23, 42, 0.7);
            border: 1px solid rgba(56, 189, 248, 0.4);
            border-radius: 16px;
            padding: 15px;
            min-height: 110px;
            max-height: 170px;
            overflow-y: auto;
            margin-bottom: 20px;
            text-align: right;
            font-size: 14px;
            line-height: 1.6;
            box-shadow: inset 0 2px 5px rgba(0,0,0,0.5);
        }
        .chat-message {
            margin-bottom: 10px;
            color: #e2e8f0;
        }
        .chat-message.bot {
            color: #38bdf8;
            font-weight: 500;
        }
        /* زر التحدث الرئيسي */
        .talk-btn {
            width: 100%;
            background: linear-gradient(135deg, #0284c7, #0369a1);
            color: white;
            border: none;
            padding: 16px;
            border-radius: 30px;
            font-size: 16px;
            font-weight: bold;
            cursor: pointer;
            box-shadow: 0 4px 20px rgba(2, 132, 199, 0.5);
            transition: 0.3s;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 10px;
        }
        .talk-btn:hover {
            background: linear-gradient(135deg, #0369a1, #075985);
            box-shadow: 0 6px 25px rgba(2, 132, 199, 0.7);
            transform: translateY(-2px);
        }
        .footer-note {
            margin-top: 15px;
            font-size: 12px;
            color: #64748b;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>C ROBOT AI</h1>
            <p>الروبوت الذكي المتكلم - The Real Talking AI Robot</p>
        </div>

        <div class="robot-face-box">
            <!-- وجه الروبوتية المتكلمة الحقيقية (قم برفع صورة وجه الروبوت إلى مستودعك واستبدل الرابط أدناه باسم الصورة مثل /robot-face.jpg) -->
            <img src="https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?q=80&w=500&auto=format&fit=crop" alt="C Robot AI Face">
        </div>

        <div class="status-badge">
            <div class="status-dot"></div>
            <span>Online & Ready - متصل وجاهز</span>
        </div>

        <div class="chat-box" id="chatBox">
            <div class="chat-message bot">🤖 مرحباً، أنا C ROBOT AI روبوت ذكي متكلم حقيقي، كيف يمكنني مساعدتك اليوم؟</div>
        </div>

        <button class="talk-btn" onclick="startTalking()">
            🎙️ تحدث مع C ROBOT AI
        </button>

        <div class="footer-note">
            الذكاء الاصطناعي في خدمتك - C ROBOT AI
        </div>
    </div>

    <script>
        function startInitializing() {
            console.log("C ROBOT AI Interface Initialized on Port 7000.");
        }
        window.onload = startInitializing;

        function startTalking() {
            const chatBox = document.getElementById('chatBox');
            chatBox.innerHTML += `<div class="chat-message">👤 مستخدم: ما هو الطقس اليوم؟</div>`;
            setTimeout(() => {
                chatBox.innerHTML += `<div class="chat-message bot">🤖 C ROBOT AI: الطقس مشمس وجميل، درجة الحرارة 25°C. أتمنى لك يوماً رائعاً!</div>`;
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
    response_text = f"مرحباً! لقد تلقيت رسالتك: '{user_message}'. أنا جاهز للرد بالصوت والصورة الحية."
    return jsonify({"response": response_text})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=PORT, debug=True)
