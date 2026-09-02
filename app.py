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

# كود HTML و CSS الشامل والمطابق لتصميم C ROBOT AI بنسبة 100%
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
            justify-content: flex-start;
            background-image: radial-gradient(circle at center, #0f172a 0%, #030712 100%);
            padding: 15px;
        }
        .main-container {
            width: 100%;
            max-width: 440px;
            display: flex;
            flex-direction: column;
            align-items: center;
        }
        /* الهيدر العلوي */
        .app-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            width: 100%;
            margin-bottom: 15px;
            padding: 0 5px;
        }
        .logo-area {
            display: flex;
            align-items: center;
            gap: 10px;
        }
        .logo-badge {
            background: linear-gradient(135deg, #0284c7, #0369a1);
            width: 40px;
            height: 40px;
            border-radius: 12px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 22px;
            font-weight: bold;
            color: white;
            box-shadow: 0 0 10px rgba(56, 189, 248, 0.5);
        }
        .title-text h1 {
            font-size: 18px;
            color: #ffffff;
            font-weight: bold;
        }
        .title-text p {
            font-size: 11px;
            color: #38bdf8;
        }
        .lang-switcher {
            display: flex;
            background: #0f172a;
            border: 1px solid #0284c7;
            border-radius: 20px;
            padding: 3px;
        }
        .lang-btn {
            background: transparent;
            border: none;
            color: #94a3b8;
            padding: 4px 10px;
            font-size: 11px;
            border-radius: 15px;
            cursor: pointer;
        }
        .lang-btn.active {
            background: #0284c7;
            color: white;
        }

        /* حاوية الروبوت الرئيسية */
        .robot-showcase {
            position: relative;
            width: 100%;
            background: linear-gradient(180deg, rgba(15, 23, 42, 0.8) 0%, rgba(3, 7, 18, 0.9) 100%);
            border: 1px solid rgba(56, 189, 248, 0.3);
            border-radius: 20px;
            padding: 20px;
            display: flex;
            flex-direction: column;
            align-items: center;
            box-shadow: 0 0 25px rgba(2, 132, 199, 0.2);
            margin-bottom: 15px;
        }

        .robot-circle-img {
            width: 180px;
            height: 180px;
            border-radius: 50%;
            border: 3px solid #38bdf8;
            box-shadow: 0 0 25px rgba(56, 189, 248, 0.6);
            object-fit: cover;
            margin-bottom: 12px;
        }

        .status-pill {
            background: rgba(15, 23, 42, 0.9);
            border: 1px solid #22c55e;
            padding: 5px 15px;
            border-radius: 20px;
            font-size: 12px;
            color: #22c55e;
            display: flex;
            align-items: center;
            gap: 6px;
            margin-bottom: 15px;
        }
        .status-dot-green {
            width: 7px;
            height: 7px;
            background-color: #22c55e;
            border-radius: 50%;
            box-shadow: 0 0 8px #22c55e;
        }

        /* صندوق المحادثة داخل الشاشة */
        .chat-display {
            width: 100%;
            background: rgba(3, 7, 18, 0.7);
            border: 1px solid rgba(56, 189, 248, 0.3);
            border-radius: 14px;
            padding: 12px;
            min-height: 90px;
            max-height: 130px;
            overflow-y: auto;
            text-align: right;
            font-size: 13px;
            margin-bottom: 12px;
        }
        .msg-user { color: #e2e8f0; margin-bottom: 6px; }
        .msg-bot { color: #38bdf8; font-weight: 500; }

        /* زر التحدث الرئيسي البارز */
        .main-action-btn {
            width: 100%;
            background: linear-gradient(135deg, #0284c7, #0369a1);
            color: white;
            border: none;
            padding: 14px;
            border-radius: 25px;
            font-size: 15px;
            font-weight: bold;
            cursor: pointer;
            box-shadow: 0 4px 15px rgba(2, 132, 199, 0.5);
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 8px;
            transition: 0.3s;
        }
        .main-action-btn:hover {
            background: linear-gradient(135deg, #0369a1, #075985);
        }

        /* شبكة الأزرار الستة السفلية المطابقة للصورة */
        .features-grid {
            width: 100%;
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 10px;
            margin-top: 5px;
        }
        .feature-card {
            background: rgba(15, 23, 42, 0.7);
            border: 1px solid rgba(56, 189, 248, 0.2);
            border-radius: 14px;
            padding: 12px 8px;
            display: flex;
            flex-direction: column;
            align-items: center;
            text-align: center;
            cursor: pointer;
            transition: 0.2s;
        }
        .feature-card:hover {
            border-color: #38bdf8;
            background: rgba(15, 23, 42, 0.9);
        }
        .feature-icon {
            font-size: 20px;
            margin-bottom: 6px;
        }
        .feature-title {
            font-size: 11px;
            color: #cbd5e1;
        }
        .footer-credit {
            margin-top: 12px;
            font-size: 11px;
            color: #64748b;
            text-align: center;
        }
    </style>
</head>
<body>
    <div class="main-container">
        <!-- الهيدر العلوي -->
        <div class="app-header">
            <div class="logo-area">
                <div class="logo-badge">C</div>
                <div class="title-text">
                    <h1>C ROBOT AI</h1>
                    <p>الروبوت الذكي المتكلم</p>
                </div>
            </div>
            <div class="lang-switcher">
                <button class="lang-btn active">العربية</button>
                <button class="lang-btn">English</button>
            </div>
        </div>

        <!-- واجهة عرض الروبوت -->
        <div class="robot-showcase">
            <!-- صورة وجه الروبوت الحقيقية المتطابقة -->
            <img src="https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?q=80&w=500&auto=format&fit=crop" alt="C Robot AI Face" class="robot-circle-img">
            
            <div class="status-pill">
                <div class="status-dot-green"></div>
                <span>Online & Ready - متصل وجاهز (Port 9000)</span>
            </div>

            <div class="chat-display" id="chatDisplay">
                <div class="msg-bot">🤖 مرحباً، أنا C ROBOT AI روبوت ذكي متكلم حقيقي، كيف يمكنني مساعدتك اليوم؟</div>
            </div>

            <button class="main-action-btn" onclick="triggerRobotTalk()">
                🎙️ تحدث مع C ROBOT AI
            </button>
        </div>

        <!-- الأزرار الستة الرئيسية في الأسفل -->
        <div class="features-grid">
            <div class="feature-card" onclick="runFeature('محادثة ذكية')">
                <div class="feature-icon">💬</div>
                <div class="feature-title">محادثة ذكية</div>
            </div>
            <div class="feature-card" onclick="runFeature('ترجمة فورية')">
                <div class="feature-icon">🌐</div>
                <div class="feature-title">ترجمة فورية</div>
            </div>
            <div class="feature-card" onclick="runFeature('مساعد شخصي')">
                <div class="feature-icon">👤</div>
                <div class="feature-title">مساعد شخصي</div>
            </div>
            <div class="feature-card" onclick="runFeature('بحث ذكي')">
                <div class="feature-icon">🔍</div>
                <div class="feature-title">بحث ذكي</div>
            </div>
            <div class="feature-card" onclick="runFeature('معلومات عامة')">
                <div class="feature-icon">📖</div>
                <div class="feature-title">معلومات عامة</div>
            </div>
            <div class="feature-card" onclick="runFeature('إعدادات')">
                <div class="feature-icon">⚙️</div>
                <div class="feature-title">إعدادات</div>
            </div>
        </div>

        <div class="footer-credit">
            C ROBOT AI – الذكاء الاصطناعي في خدمتك
        </div>
    </div>

    <script>
        function triggerRobotTalk() {
            const display = document.getElementById('chatDisplay');
            display.innerHTML += `<div class="msg-user">👤 مستخدم: ما هو الطقس اليوم في الجزائر؟</div>`;
            setTimeout(() => {
                display.innerHTML += `<div class="msg-bot">🤖 C ROBOT AI: الطقس اليوم في الجزائر مشمس وجميل، درجة الحرارة 25°C. أتمنى لك يوماً رائعاً! ☀️</div>`;
                display.scrollTop = display.scrollHeight;
            }, 800);
            display.scrollTop = display.scrollHeight;
        }

        function runFeature(featureName) {
            const display = document.getElementById('chatDisplay');
            display.innerHTML += `<div class="msg-bot">⚙️ تم تفعيل ميزة: ${featureName}. كيف أساعدك فيها؟</div>`;
            display.scrollTop = display.scrollHeight;
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
    return jsonify({"response": f"تم استقبال طلبك: {user_message}"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=PORT, debug=True)
