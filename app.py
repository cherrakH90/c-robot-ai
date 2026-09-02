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

from flask import Flask, render_template_string

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="ar" dir="rtl" id="htmlRoot">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>C ROBOT AI - الروبوت الذكي المتكلم V3</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
        body {
            background-color: #030712;
            color: #ffffff;
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            align-items: center;
            background: radial-gradient(circle at center, #0b1329 0%, #030712 100%);
            padding: 12px;
        }
        .app-container {
            width: 100%;
            max-width: 460px;
            display: flex;
            flex-direction: column;
            gap: 12px;
        }
        /* الهيدر العلوي */
        .top-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            background: rgba(15, 23, 42, 0.85);
            border: 1px solid rgba(56, 189, 248, 0.4);
            border-radius: 16px;
            padding: 10px 14px;
            box-shadow: 0 0 15px rgba(56, 189, 248, 0.2);
        }
        .brand-box { display: flex; align-items: center; gap: 10px; }
        .brand-logo {
            background: linear-gradient(135deg, #0284c7, #38bdf8);
            width: 38px; height: 38px; border-radius: 10px;
            display: flex; align-items: center; justify-content: center;
            font-size: 20px; font-weight: bold; color: white;
            box-shadow: 0 0 12px rgba(56, 189, 248, 0.8);
        }
        .brand-titles h1 { font-size: 16px; color: #ffffff; font-weight: bold; }
        .brand-titles p { font-size: 10px; color: #38bdf8; }
        .lang-switch {
            display: flex; background: #090d16;
            border: 1px solid #0284c7; border-radius: 20px; padding: 2px;
        }
        .l-btn {
            background: transparent; border: none; color: #94a3b8;
            padding: 4px 10px; font-size: 11px; border-radius: 15px; cursor: pointer;
        }
        .l-btn.active { background: #0284c7; color: white; font-weight: bold; box-shadow: 0 0 8px #0284c7; }

        /* منطقة عرض الروبوت الأساسية */
        .robot-main-card {
            position: relative;
            background: rgba(10, 15, 30, 0.9);
            border: 1px solid rgba(56, 189, 248, 0.5);
            border-radius: 22px; padding: 15px;
            display: flex; flex-direction: column; align-items: center;
            box-shadow: 0 0 35px rgba(2, 132, 199, 0.35);
        }
        .robot-avatar-wrapper {
            position: relative; width: 170px; height: 170px; border-radius: 50%;
            border: 3px solid #38bdf8;
            box-shadow: 0 0 30px rgba(56, 189, 248, 0.8), inset 0 0 20px rgba(56, 189, 248, 0.5);
            overflow: hidden; margin-bottom: 10px; background: #000;
        }
        /* صورة وجه الروبوت الحقيقي المطابقة للصورة الإعلانية */
        .robot-avatar-wrapper img { width: 100%; height: 100%; object-fit: cover; }

        .status-badge {
            background: rgba(15, 23, 42, 0.95);
            border: 1px solid #22c55e; padding: 4px 14px; border-radius: 20px;
            font-size: 11px; color: #22c55e; display: flex; align-items: center; gap: 6px; margin-bottom: 10px;
        }
        .dot { width: 6px; height: 6px; background-color: #22c55e; border-radius: 50%; box-shadow: 0 0 8px #22c55e; }

        .chat-panel {
            width: 100%; background: rgba(3, 7, 18, 0.85);
            border: 1px solid rgba(56, 189, 248, 0.35); border-radius: 12px; padding: 10px;
            min-height: 80px; max-height: 110px; overflow-y: auto; text-align: right; font-size: 12px; margin-bottom: 10px;
        }
        .msg-u { color: #cbd5e1; margin-bottom: 4px; }
        .msg-b { color: #38bdf8; font-weight: 500; }

        .sound-wave { display: flex; align-items: center; gap: 3px; height: 20px; margin-bottom: 10px; }
        .bar { width: 3px; background: #38bdf8; border-radius: 3px; animation: pulseWave 1.2s infinite ease-in-out; }
        .bar:nth-child(2) { animation-delay: 0.1s; }
        .bar:nth-child(3) { animation-delay: 0.2s; }
        .bar:nth-child(4) { animation-delay: 0.3s; }
        .bar:nth-child(5) { animation-delay: 0.4s; }
        .bar:nth-child(6) { animation-delay: 0.5s; }
        @keyframes pulseWave {
            0%, 100% { height: 6px; opacity: 0.5; }
            50% { height: 18px; opacity: 1; }
        }

        .talk-action-btn {
            width: 100%;
            background: linear-gradient(135deg, #0284c7, #0369a1);
            color: white; border: none; padding: 12px; border-radius: 25px;
            font-size: 14px; font-weight: bold; cursor: pointer;
            box-shadow: 0 4px 18px rgba(2, 132, 199, 0.6);
            display: flex; align-items: center; justify-content: center; gap: 8px; transition: 0.2s;
        }
        .talk-action-btn:hover { background: linear-gradient(135deg, #0369a1, #075985); }

        .features-row { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; }
        .feature-box-v3 {
            background: rgba(15, 23, 42, 0.85);
            border: 1px solid rgba(56, 189, 248, 0.3); border-radius: 14px; padding: 10px; display: flex; flex-direction: column; gap: 6px;
        }
        .box-title { font-size: 11px; color: #94a3b8; display: flex; justify-content: space-between; }
        .sub-preview { width: 100%; height: 45px; border-radius: 8px; object-fit: cover; border: 1px solid rgba(56, 189, 248, 0.4); }
        .active-status-text { font-size: 10px; color: #22c55e; display: flex; align-items: center; gap: 4px; }

        .capabilities-list {
            background: rgba(15, 23, 42, 0.7);
            border: 1px solid rgba(56, 189, 248, 0.3); border-radius: 14px; padding: 10px 14px; display: flex; flex-direction: column; gap: 6px;
        }
        .capability-item { font-size: 11px; color: #cbd5e1; display: flex; align-items: center; gap: 8px; border-bottom: 1px solid rgba(255,255,255,0.05); padding-bottom: 4px; }

        .bottom-nav-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 8px; }
        .nav-card {
            background: rgba(15, 23, 42, 0.85);
            border: 1px solid rgba(56, 189, 248, 0.35); border-radius: 12px; padding: 10px 6px;
            display: flex; flex-direction: column; align-items: center; text-align: center; cursor: pointer; transition: 0.2s;
        }
        .nav-card:hover { border-color: #38bdf8; background: rgba(15, 23, 42, 1); box-shadow: 0 0 10px rgba(56, 189, 248, 0.3); }
        .nav-icon { font-size: 18px; margin-bottom: 4px; }
        .nav-text { font-size: 10px; color: #e2e8f0; }

        .footer-note { text-align: center; font-size: 10px; color: #64748b; margin-top: 4px; }
    </style>
</head>
<body>
    <div class="app-container">
        <!-- الهيدر -->
        <div class="top-header">
            <div class="brand-box">
                <div class="brand-logo">C</div>
                <div class="brand-titles">
                    <h1 id="txtTitle">C ROBOT AI</h1>
                    <p id="txtSub">الروبوت الذكي المتكلم</p>
                </div>
            </div>
            <div class="lang-switch">
                <button class="l-btn active" id="btnAr" onclick="changeLanguage('ar')">العربية</button>
                <button class="l-btn" id="btnEn" onclick="changeLanguage('en')">English</button>
            </div>
        </div>

        <!-- قسم التفاعل الرئيسي مع وجه الروبوت الحقيقي -->
        <div class="robot-main-card">
            <div class="robot-avatar-wrapper">
                <!-- صورة وجه الروبوت الذكي المتكلم بدقة عالية وتصميم مطابق -->
                <img src="https://images.unsplash.com/photo-1614680376593-902f749f7ffc?q=80&w=500&auto=format&fit=crop" alt="C Robot Real Talking Face">
            </div>

            <div class="status-badge">
                <div class="dot"></div>
                <span id="txtStatus">Online & Ready - متصل وجاهز</span>
            </div>

            <div class="chat-panel" id="chatBox">
                <div class="msg-b" id="welcomeMsg">🤖 مرحباً، أنا C ROBOT AI روبوت ذكي متكلم حقيقي، كيف يمكنني مساعدتك اليوم؟</div>
            </div>

            <!-- موجات الصوت -->
            <div class="sound-wave">
                <div class="bar" style="height: 10px;"></div>
                <div class="bar" style="height: 16px;"></div>
                <div class="bar" style="height: 8px;"></div>
                <div class="bar" style="height: 18px;"></div>
                <div class="bar" style="height: 12px;"></div>
                <div class="bar" style="height: 15px;"></div>
            </div>

            <button class="talk-action-btn" id="talkBtn" onclick="triggerTalk()">
                🎙️ تحدث مع C ROBOT AI
            </button>
        </div>

        <!-- مؤشرات العين والفم -->
        <div class="features-row">
            <div class="feature-box-v3">
                <div class="box-title"><span id="lblEye">تتبع العين</span><span>Eye</span></div>
                <img src="https://images.unsplash.com/photo-1534447677768-be436bb09401?q=80&w=300&auto=format&fit=crop" class="sub-preview" alt="Eye Tracking">
                <div class="active-status-text" id="lblEyeActive"><span class="dot"></span> نشط Active</div>
            </div>
            <div class="feature-box-v3">
                <div class="box-title"><span id="lblMouth">تحريك الفم</span><span>Mouth</span></div>
                <img src="https://images.unsplash.com/photo-1509967419530-da38b4704bc6?q=80&w=300&auto=format&fit=crop" class="sub-preview" alt="Mouth Animation">
                <div class="active-status-text" id="lblMouthActive"><span class="dot"></span> نشط Active</div>
            </div>
        </div>

        <!-- قائمة الخصائص الذكية الجانبية -->
        <div class="capabilities-list" id="capList">
            <div class="capability-item">🌐 يتحدث العربية والإنجليزية بطلاقة</div>
            <div class="capability-item">🧠 فهم الأسئلة المعقدة بدقة متناهية</div>
            <div class="capability-item">⚡ إجابات فورية وتفاعل بصوت وصورة</div>
        </div>

        <!-- شبكة الأزرار السفلية الستة -->
        <div class="bottom-nav-grid">
            <div class="nav-card" onclick="runAction('chat')">
                <div class="nav-icon">💬</div>
                <div class="nav-text" id="nav1">محادثة ذكية</div>
            </div>
            <div class="nav-card" onclick="runAction('translate')">
                <div class="nav-icon">🌐</div>
                <div class="nav-text" id="nav2">ترجمة فورية</div>
            </div>
            <div class="nav-card" onclick="runAction('assistant')">
                <div class="nav-icon">👤</div>
                <div class="nav-text" id="nav3">مساعد شخصي</div>
            </div>
            <div class="nav-card" onclick="runAction('search')">
                <div class="nav-icon">🔍</div>
                <div class="nav-text" id="nav4">بحث ذكي</div>
            </div>
            <div class="nav-card" onclick="runAction('knowledge')">
                <div class="nav-icon">📖</div>
                <div class="nav-text" id="nav5">معلومات عامة</div>
            </div>
            <div class="nav-card" onclick="runAction('settings')">
                <div class="nav-icon">⚙️</div>
                <div class="nav-text" id="nav6">إعدادات</div>
            </div>
        </div>

        <div class="footer-note" id="footerText">
            C ROBOT AI V3 – الذكاء الاصطناعي في خدمتك
        </div>
    </div>

    <script>
        let currentLang = 'ar';

        const translations = {
            ar: {
                sub: "الروبوت الذكي المتكلم",
                status: "Online & Ready - متصل وجاهز",
                welcome: "🤖 مرحباً، أنا C ROBOT AI روبوت ذكي متكلم حقيقي، كيف يمكنني مساعدتك اليوم؟",
                talkBtn: "🎙️ تحدث مع C ROBOT AI",
                eye: "تتبع العين",
                mouth: "تحريك الفم",
                active: "نشط Active",
                caps: [
                    "🌐 يتحدث العربية والإنجليزية بطلاقة",
                    "🧠 فهم الأسئلة المعقدة بدقة متناهية",
                    "⚡ إجابات فورية وتفاعل بصوت وصورة"
                ],
                navs: ["محادثة ذكية", "ترجمة فورية", "مساعد شخصي", "بحث ذكي", "معلومات عامة", "إعدادات"],
                footer: "C ROBOT AI V3 – الذكاء الاصطناعي في خدمتك",
                speechWelcome: "مرحباً بك، أنا C ROBOT AI جاهز للتحدث معك الآن."
            },
            en: {
                sub: "The Real Talking AI Robot",
                status: "Online & Ready - Connected",
                welcome: "🤖 Hello, I'm C ROBOT AI a real talking AI robot. How can I help you today?",
                talkBtn: "🎙️ Talk with C ROBOT AI",
                eye: "Eye Tracking",
                mouth: "Mouth Animation",
                active: "Active",
                caps: [
                    "🌐 Speaks Arabic and English fluently",
                    "🧠 Understands complex questions precisely",
                    "⚡ Instant responses with voice & vision"
                ],
                navs: ["Smart Chat", "Translate", "Assistant", "Smart Search", "Knowledge", "Settings"],
                footer: "C ROBOT AI V3 – AI at your service",
                speechWelcome: "Hello, I am C ROBOT AI, ready to talk with you now."
            }
        };

        function changeLanguage(lang) {
            currentLang = lang;
            const root = document.getElementById('htmlRoot');
            root.setAttribute('lang', lang);
            root.setAttribute('dir', lang === 'ar' ? 'rtl' : 'ltr');

            document.getElementById('btnAr').classList.toggle('active', lang === 'ar');
            document.getElementById('btnEn').classList.toggle('active', lang === 'en');

            const t = translations[lang];
            document.getElementById('txtSub').innerText = t.sub;
            document.getElementById('txtStatus').innerText = t.status;
            document.getElementById('welcomeMsg').innerText = t.welcome;
            document.getElementById('talkBtn').innerText = t.talkBtn;
            document.getElementById('lblEye').innerText = t.eye;
            document.getElementById('lblMouth').innerText = t.mouth;
            
            document.getElementById('lblEyeActive').innerHTML = `<span class="dot"></span> ${t.active}`;
            document.getElementById('lblMouthActive').innerHTML = `<span class="dot"></span> ${t.active}`;

            const capItems = document.querySelectorAll('.capability-item');
            capItems.forEach((item, idx) => { item.innerText = t.caps[idx]; });

            for(let i = 1; i <= 6; i++) {
                document.getElementById('nav' + i).innerText = t.navs[i-1];
            }
            document.getElementById('footerText').innerText = t.footer;

            speak(t.speechWelcome);
        }

        function speak(text) {
            const chatBox = document.getElementById('chatBox');
            chatBox.innerHTML += `<div class="msg-b">🤖 ${text}</div>`;
            chatBox.scrollTop = chatBox.scrollHeight;

            if ('speechSynthesis' in window) {
                window.speechSynthesis.cancel();
                const utterance = new SpeechSynthesisUtterance(text);
                utterance.lang = currentLang === 'ar' ? 'ar-SA' : 'en-US';
                utterance.rate = 1.0;
                window.speechSynthesis.speak(utterance);
            }
        }

        function triggerTalk() {
            const msg = currentLang === 'ar' ? "أنا أستمع إليك الآن، تفضل بطرح سؤالك." : "I am listening to you now, please ask your question.";
            speak(msg);
        }

        function runAction(action) {
            const responses = {
                ar: { chat: "تم تفعيل محادثة ذكية.", translate: "ترجمة فورية نشطة.", assistant: "مساعدك الشخصي جاهز.", search: "بحث ذكي نشط.", knowledge: "قسم المعلومات العامة مفتوح.", settings: "لوحة الإعدادات نشطة." },
                en: { chat: "Smart chat activated.", translate: "Instant translation active.", assistant: "Personal assistant ready.", search: "Smart search active.", knowledge: "Knowledge base open.", settings: "Settings panel active." }
            };
            speak(responses[currentLang][action]);
        }
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=PORT, debug=True)
