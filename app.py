import os
import signal
import subprocess
import sys
import time

PORT = 9000

# ============================================================
# 🔪 قتل الخادم القديم — يعمل على Linux + macOS + Windows
# ============================================================
def kill_existing_server(port):
    """محاولة إيقاف أي عملية تستخدم المنفذ — عبر 4 طرق"""
    killed = False

    # الطريقة 1: lsof (Linux / macOS)
    try:
        cmd = f"lsof -t -i:{port}"
        pids = subprocess.check_output(cmd, shell=True, stderr=subprocess.DEVNULL).decode().strip().split('\n')
        for pid in pids:
            if pid.strip():
                try:
                    os.kill(int(pid), signal.SIGKILL)
                    print(f"✅ [lsof] تم إيقاف العملية {pid}")
                    killed = True
                except Exception:
                    pass
    except Exception:
        pass

    # الطريقة 2: fuser (Linux)
    if not killed and sys.platform.startswith('linux'):
        try:
            subprocess.run(f"fuser -k {port}/tcp", shell=True,
                           stderr=subprocess.DEVNULL, timeout=3)
            print(f"✅ [fuser] تم إيقاف العملية على المنفذ {port}")
            killed = True
        except Exception:
            pass

    # الطريقة 3: netstat + taskkill (Windows)
    if not killed and sys.platform.startswith('win'):
        try:
            output = subprocess.check_output(f'netstat -ano | findstr :{port}',
                                             shell=True).decode()
            pids = set()
            for line in output.splitlines():
                parts = line.split()
                if len(parts) >= 5 and parts[1].endswith(f":{port}"):
                    pids.add(parts[-1])
            for pid in pids:
                subprocess.run(f"taskkill /F /PID {pid}", shell=True,
                               stderr=subprocess.DEVNULL)
                print(f"✅ [taskkill] تم إيقاف العملية {pid}")
                killed = True
        except Exception:
            pass

    # الطريقة 4: psutil (يعمل على كل الأنظمة إذا كان مثبتاً)
    if not killed:
        try:
            import psutil
            for conn in psutil.net_connections(kind='inet'):
                if conn.laddr.port == port and conn.pid:
                    try:
                        p = psutil.Process(conn.pid)
                        p.kill()
                        print(f"✅ [psutil] تم إيقاف العملية {conn.pid}")
                        killed = True
                    except Exception:
                        pass
        except ImportError:
            pass
        except Exception:
            pass

    if not killed:
        print(f"ℹ️  لا توجد عملية تستخدم المنفذ {port} (أو لا توجد صلاحيات).")

    # انتظار قصير لتحرير المنفذ
    time.sleep(0.5)
    return killed


kill_existing_server(PORT)

from flask import Flask, render_template_string, send_from_directory, jsonify, request

app = Flask(__name__)


# ============================================================
# مسار خدمة خلفيات Bg_XX.jpg
# ============================================================
@app.route('/Bg_<int:num>.jpg')
def serve_bg(num):
    if 1 <= num <= 55:
        return send_from_directory('.', f'Bg_{num:02d}.jpg')
    return "Image not found", 404


# ============================================================
# مسار خدمة صورة وجه الروبوت
# ============================================================
@app.route('/robot_face.png')
def serve_robot_face():
    return send_from_directory('.', 'robot_face.png')


# ============================================================
# 📱 PWA — manifest
# ============================================================
@app.route('/manifest.json')
def manifest():
    return jsonify({
        "name": "C ROBOT AI V6",
        "short_name": "C ROBOT",
        "description": "الروبوت الذكي المتكلم الحقيقي",
        "start_url": "/",
        "display": "standalone",
        "background_color": "#05070f",
        "theme_color": "#0ea5e9",
        "orientation": "portrait",
        "icons": [
            {"src": "/robot_face.png", "sizes": "192x192", "type": "image/png"},
            {"src": "/robot_face.png", "sizes": "512x512", "type": "image/png"}
        ]
    })


# ============================================================
# 📱 PWA — service worker
# ============================================================
@app.route('/sw.js')
def service_worker():
    sw = """
    const CACHE = 'crobot-v6';
    self.addEventListener('install', e => {
        e.waitUntil(caches.open(CACHE).then(c => c.addAll(['/', '/robot_face.png'])));
        self.skipWaiting();
    });
    self.addEventListener('activate', e => {
        e.waitUntil(caches.keys().then(keys =>
            Promise.all(keys.filter(k => k !== CACHE).map(k => caches.delete(k)))
        ));
        self.clients.claim();
    });
    self.addEventListener('fetch', e => {
        e.respondWith(
            caches.match(e.request).then(r => r || fetch(e.request).catch(() => caches.match('/')))
        );
    });
    """
    return sw, 200, {'Content-Type': 'application/javascript'}


# ============================================================
# 🧠 محرك حل المشكلات العملية (Problem Solving Engine)
# ============================================================
PROBLEM_KNOWLEDGE_BASE = {
    "marketing": {
        "keywords": ["زبائن", "زبون", "عملاء", "عميل", "محل", "متجر", "تسويق", "مبيعات", "بيزنس", "مشروع",
                     "customers", "clients", "shop", "store", "marketing", "sales", "business"],
        "cause_ar": "ضعف الوصول للعملاء المحتملين + غياب هوية تجارية واضحة + عدم وجود قنوات تواصل فعّالة.",
        "cause_en": "Weak reach to potential customers + missing brand identity + no active communication channels.",
        "solutions_ar": [
            "تحديد الجمهور المستهدف بدقة (العمر، المنطقة، الاهتمام، القدرة الشرائية).",
            "بناء عرض قيمة واضح (Offer) يميزك عن المنافسين.",
            "إنشاء هوية بصرية موحّدة (شعار، ألوان، نبرة صوت).",
            "فتح قنوات تواصل: واتساب بزنس + إنستغرام + خرائط جوجل (Google My Business).",
            "حملة إعلانية محلية صغيرة الميزانية (Meta Ads أو Google Ads).",
            "برنامج إحالة: عميل يجلب عميل بمكافأة."
        ],
        "solutions_en": [
            "Precisely define target audience (age, area, interest, purchasing power).",
            "Build a clear unique value offer.",
            "Create a unified visual identity (logo, colors, tone).",
            "Open channels: WhatsApp Business + Instagram + Google My Business.",
            "Small budget local ads campaign (Meta Ads or Google Ads).",
            "Referral program: customer brings customer with reward."
        ],
        "plan_ar": [
            {"step": "اليوم 1-2", "task": "تحديد الجمهور المستهدف وكتابة بروفايل العميل المثالي."},
            {"step": "اليوم 3-4", "task": "تصميم عرض قيمة + شعار مؤقت + صفحة واتساب بزنس."},
            {"step": "اليوم 5-6", "task": "إنشاء حساب إنستغرام + Google My Business ونشر أول 3 منشورات."},
            {"step": "اليوم 7",   "task": "إطلاق أول حملة إعلانية بميزانية صغيرة (5$ يومياً)."},
            {"step": "أسبوع 2",   "task": "نشر 5 منشورات أسبوعياً + الرد على كل رسالة خلال ساعة."},
            {"step": "أسبوع 3-4", "task": "قياس النتائج: عدد الرسائل، التحويلات، والتكلفة لكل عميل."}
        ],
        "plan_en": [
            {"step": "Day 1-2", "task": "Define target audience and write ideal customer profile."},
            {"step": "Day 3-4", "task": "Design value offer + temporary logo + WhatsApp Business page."},
            {"step": "Day 5-6", "task": "Create Instagram + Google My Business, publish first 3 posts."},
            {"step": "Day 7",   "task": "Launch first small ad campaign ($5/day)."},
            {"step": "Week 2",  "task": "Post 5 times weekly + reply to every message within 1 hour."},
            {"step": "Week 3-4","task": "Measure results: messages, conversions, cost per customer."}
        ],
        "kpis_ar": ["عدد الرسائل الجديدة أسبوعياً", "نسبة التحويل من رسالة إلى شراء", "تكلفة اكتساب العميل (CAC)", "متوسط قيمة الطلب"],
        "kpis_en": ["New messages per week", "Message-to-purchase conversion rate", "Customer acquisition cost (CAC)", "Average order value"],
        "fallback_ar": "إذا لم تنجح الحملة الإعلانية خلال أسبوعين، جرّب: (1) إعلانات على TikTok، (2) التعاون مع مؤثر محلي، (3) عروض حصرية عبر واتساب للعملاء الحاليين.",
        "fallback_en": "If the ad campaign fails in 2 weeks, try: (1) TikTok ads, (2) local influencer collab, (3) exclusive WhatsApp offers to existing customers."
    },
    "productivity": {
        "keywords": ["وقت", "إنتاجية", "تنظيم", "تأجيل", "تسويف", "مهام", "مشغول", "إدارة",
                     "time", "productivity", "organize", "procrastination", "tasks", "busy", "management"],
        "cause_ar": "غياب نظام أولويات + تشتت رقمي + عدم وجود مراجعة أسبوعية.",
        "cause_en": "Missing priority system + digital distraction + no weekly review.",
        "solutions_ar": [
            "تطبيق قاعدة 1-3-5 (مهمة كبيرة + 3 متوسطة + 5 صغيرة).",
            "استخدام تقنية بومودورو (25 دقيقة عمل + 5 راحة).",
            "حجب الإشعارات أثناء جلسات التركيز.",
            "مراجعة أسبوعية كل جمعة لتصفية المهام.",
            "تخصيص صباح بلا هاتف لأول 30 دقيقة."
        ],
        "solutions_en": [
            "Apply 1-3-5 rule (1 big + 3 medium + 5 small tasks).",
            "Use Pomodoro (25 min work + 5 min break).",
            "Block notifications during focus sessions.",
            "Weekly review every Friday to clean tasks.",
            "Phone-free mornings for first 30 minutes."
        ],
        "plan_ar": [
            {"step": "اليوم 1", "task": "كتابة كل المهام الحالية وتصنيفها حسب الأهمية."},
            {"step": "اليوم 2", "task": "تطبيق قاعدة 1-3-5 ليوم واحد فقط كتجربة."},
            {"step": "اليوم 3-5", "task": "تفعيل 4 جلسات بومودورو يومياً."},
            {"step": "اليوم 6-7", "task": "مراجعة أسبوعية وحذف ما لم يُنفذ بدون سبب."}
        ],
        "plan_en": [
            {"step": "Day 1", "task": "List all tasks and rank by importance."},
            {"step": "Day 2", "task": "Apply 1-3-5 rule for one day only as test."},
            {"step": "Day 3-5", "task": "Run 4 Pomodoro sessions daily."},
            {"step": "Day 6-7", "task": "Weekly review and delete what wasn't done without reason."}
        ],
        "kpis_ar": ["عدد المهام المنجزة يومياً", "ساعات التركيز الفعلي", "نسبة الالتزام بالخطة"],
        "kpis_en": ["Tasks completed daily", "Actual focus hours", "Plan adherence rate"],
        "fallback_ar": "إذا لم تتحسن الإنتاجية، قلل المهام إلى 3 يومياً فقط وركّز على الأهم.",
        "fallback_en": "If productivity doesn't improve, reduce tasks to 3 per day and focus on the most important."
    },
    "learning": {
        "keywords": ["تعلم", "دراسة", "مذاكرة", "امتحان", "دورة", "لغة", "مهارة",
                     "learn", "study", "exam", "course", "language", "skill"],
        "cause_ar": "غياب منهجية تعلم فعّالة + عدم تطبيق المعلومة + تشتت بين مصادر كثيرة.",
        "cause_en": "Missing effective learning method + no information application + distraction across many sources.",
        "solutions_ar": [
            "استخدام تقنية فاينمان: اشرح ما تعلمته بصوت عالٍ كأنك تدرّس طفلاً.",
            "التعلم بالمشروع: طبق كل درس بمشروع صغير فوراً.",
            "اختيار مصدر واحد رئيسي وإتمامه قبل الانتقال لغيره.",
            "جلسات تعلم 50 دقيقة + راحة 10 دقائق.",
            "اختبار ذاتي أسبوعي."
        ],
        "solutions_en": [
            "Use Feynman technique: explain out loud as if teaching a child.",
            "Project-based learning: apply each lesson immediately.",
            "Pick one main source and finish it before switching.",
            "50-min sessions + 10-min breaks.",
            "Weekly self-testing."
        ],
        "plan_ar": [
            {"step": "اليوم 1", "task": "اختيار مصدر واحد فقط والتخلص من الباقي مؤقتاً."},
            {"step": "اليوم 2-7", "task": "جلسة يومية 50 دقيقة + تلخيص بصوت عالٍ."},
            {"step": "الأسبوع 2", "task": "بناء مشروع صغير يطبق ما تعلمته."},
            {"step": "الأسبوع 3-4", "task": "اختبار أسبوعي ذاتي وتعديل الخطة."}
        ],
        "plan_en": [
            {"step": "Day 1", "task": "Choose one source only, pause everything else."},
            {"step": "Day 2-7", "task": "Daily 50-min session + out-loud summary."},
            {"step": "Week 2", "task": "Build a small project applying what you learned."},
            {"step": "Week 3-4", "task": "Weekly self-test and adjust plan."}
        ],
        "kpis_ar": ["ساعات التعلم الفعلية", "عدد المشاريع المنجزة", "نتائج الاختبار الذاتي"],
        "kpis_en": ["Actual learning hours", "Projects completed", "Self-test results"],
        "fallback_ar": "إذا لم تستوعب، غيّر أسلوب الشرح (فيديو بدل نص) وخذ استراحة يوم كامل.",
        "fallback_en": "If you're not absorbing, switch explanation style (video over text) and take a full-day break."
    }
}


def analyze_problem(message):
    """تحليل المشكلة وتحديد المجال"""
    text = (message or "").lower()
    scores = {}
    for domain, data in PROBLEM_KNOWLEDGE_BASE.items():
        scores[domain] = sum(1 for kw in data["keywords"] if kw.lower() in text)
    best_domain = max(scores, key=scores.get)
    if scores[best_domain] == 0:
        best_domain = "marketing"  # default عملي
    return best_domain, PROBLEM_KNOWLEDGE_BASE[best_domain]


def build_solution_plan(message, lang='ar'):
    """بناء خطة حل كاملة خطوة بخطوة"""
    domain, data = analyze_problem(message)
    is_ar = (lang == 'ar')
    return {
        "domain": domain,
        "problem": message,
        "cause": data["cause_ar"] if is_ar else data["cause_en"],
        "solutions": data["solutions_ar"] if is_ar else data["solutions_en"],
        "plan": data["plan_ar"] if is_ar else data["plan_en"],
        "kpis": data["kpis_ar"] if is_ar else data["kpis_en"],
        "fallback": data["fallback_ar"] if is_ar else data["fallback_en"]
    }


# ============================================================
# 🧩 نقطة نهاية حل المشكلات العملية
# ============================================================
@app.route('/api/solve', methods=['POST'])
def api_solve():
    data = request.get_json(silent=True) or {}
    problem = (data.get('problem') or '').strip()
    lang = data.get('lang', 'ar')

    if not problem:
        return jsonify({
            "error": "Please provide a problem.",
            "error_ar": "الرجاء إرسال مشكلة لحلها."
        }), 400

    plan = build_solution_plan(problem, lang)

    if lang == 'ar':
        summary = (
            f"حللت مشكلتك: «{problem}»\n"
            f"🔍 السبب الجذري: {plan['cause']}\n"
            f"🧠 تم اقتراح {len(plan['solutions'])} حلول، "
            f"وتحويلها إلى خطة من {len(plan['plan'])} خطوات "
            f"مع {len(plan['kpis'])} مؤشرات قياس."
        )
    else:
        summary = (
            f"I analyzed your problem: \"{problem}\"\n"
            f"🔍 Root cause: {plan['cause']}\n"
            f"🧠 Suggested {len(plan['solutions'])} solutions, "
            f"converted to a {len(plan['plan'])}-step plan "
            f"with {len(plan['kpis'])} KPIs."
        )

    plan["summary"] = summary
    return jsonify(plan)


# ============================================================
# 🤖 نقطة نهاية API جاهزة للربط بـ OpenAI / Gemini
# ============================================================
@app.route('/api/chat', methods=['POST'])
def api_chat():
    """
    نقطة نهاية للربط بالذكاء الاصطناعي.
    حالياً تعيد رد تجريبي — استبدلها بـ OpenAI/Gemini لاحقاً.
    مثال:
        from openai import OpenAI
        client = OpenAI(api_key=os.environ['OPENAI_API_KEY'])
        r = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": user_msg}]
        )
        reply = r.choices[0].message.content
    """
    data = request.get_json(silent=True) or {}
    user_msg = (data.get('message') or '').strip()
    lang = data.get('lang', 'en')

    if not user_msg:
        return jsonify({"reply": "Please provide a message."}), 400

    # 🔁 رد تجريبي — استبدله بـ AI حقيقي
    if lang == 'ar':
        reply = f"لقد سمعت سؤالك: {user_msg}. جاري معالجته."
    else:
        reply = f"I heard your question: {user_msg}. Processing now."

    return jsonify({"reply": reply, "lang": lang})


# ============================================================
# 🏥 Health check
# ============================================================
@app.route('/health')
def health():
    return jsonify({
        "status": "online",
        "version": "6.0.0",
        "name": "C ROBOT AI",
        "port": PORT
    })


HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="ar" dir="rtl" id="htmlRoot">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover, user-scalable=no">
    <meta name="theme-color" content="#0ea5e9">
    <meta name="description" content="C ROBOT AI V6 - روبوت ذكي متكلم حقيقي">
    <meta name="apple-mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
    <link rel="manifest" href="/manifest.json">
    <link rel="apple-touch-icon" href="/robot_face.png">
    <title>C ROBOT AI V6 - Modern Tech Edition</title>
    <link href="https://fonts.googleapis.com/css2?family=Tajawal:wght@400;500;700;900&family=Orbitron:wght@400;600;800;900&display=swap" rel="stylesheet">
    <style>
        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
            font-family: 'Tajawal', 'Orbitron', -apple-system, BlinkMacSystemFont, sans-serif;
            -webkit-tap-highlight-color: transparent;
        }

        html, body {
            min-height: 100vh;
            background: #05070f;
            overflow-x: hidden;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 30px 15px;
            position: relative;
        }

        body::before,
        body::after {
            content: "";
            position: fixed;
            border-radius: 50%;
            filter: blur(120px);
            z-index: -1;
            pointer-events: none;
        }
        body::before {
            width: 500px; height: 500px;
            background: radial-gradient(circle, rgba(56, 189, 248, 0.35), transparent 70%);
            top: -150px; right: -150px;
            animation: floatGlow 12s ease-in-out infinite alternate;
        }
        body::after {
            width: 600px; height: 600px;
            background: radial-gradient(circle, rgba(168, 85, 247, 0.28), transparent 70%);
            bottom: -200px; left: -200px;
            animation: floatGlow 15s ease-in-out infinite alternate-reverse;
        }
        @keyframes floatGlow {
            0%   { transform: translate(0, 0) scale(1); }
            100% { transform: translate(40px, 30px) scale(1.15); }
        }

        /* ============================================================
           إطار iPhone
        ============================================================ */
        .iphone-frame {
            position: relative;
            width: 400px;
            height: 830px;
            background: linear-gradient(145deg, #2a2a2e 0%, #1a1a1d 50%, #0f0f11 100%);
            border-radius: 55px;
            padding: 12px;
            box-shadow:
                0 0 0 2px #3a3a3f,
                0 0 0 3px #0a0a0a,
                0 30px 80px rgba(0, 0, 0, 0.8),
                0 0 120px rgba(56, 189, 248, 0.25),
                inset 0 1px 2px rgba(255, 255, 255, 0.15);
            animation: phoneFloat 6s ease-in-out infinite;
        }
        @keyframes phoneFloat {
            0%, 100% { transform: translateY(0); }
            50%      { transform: translateY(-12px); }
        }

        .iphone-frame::before {
            content: "";
            position: absolute;
            left: -3px; top: 130px;
            width: 3px; height: 32px;
            background: linear-gradient(180deg, #3a3a3f, #1a1a1d);
            border-radius: 3px 0 0 3px;
            box-shadow: 0 60px 0 #1a1a1d, 0 120px 0 #1a1a1d;
        }
        .iphone-frame::after {
            content: "";
            position: absolute;
            right: -3px; top: 180px;
            width: 3px; height: 80px;
            background: linear-gradient(180deg, #3a3a3f, #1a1a1d);
            border-radius: 0 3px 3px 0;
        }

        /* ============================================================
           شاشة iPhone
        ============================================================ */
        .iphone-screen {
            position: relative;
            width: 100%;
            height: 100%;
            border-radius: 44px;
            overflow: hidden;
            display: flex;
            flex-direction: column;
            isolation: isolate;
            background: url('/Bg_01.jpg') no-repeat center center / cover;
        }

        .iphone-screen::before {
            content: "";
            position: absolute;
            inset: 0;
            background:
                linear-gradient(180deg,
                    rgba(5, 7, 15, 0.75) 0%,
                    rgba(5, 7, 15, 0.55) 40%,
                    rgba(5, 7, 15, 0.75) 100%),
                radial-gradient(circle at 20% 10%, rgba(56, 189, 248, 0.18), transparent 45%),
                radial-gradient(circle at 80% 90%, rgba(168, 85, 247, 0.16), transparent 45%);
            z-index: 0;
            pointer-events: none;
        }

        .dynamic-island {
            position: absolute;
            top: 12px;
            left: 50%;
            transform: translateX(-50%);
            width: 120px; height: 34px;
            background: #000;
            border-radius: 20px;
            z-index: 100;
            box-shadow: inset 0 0 8px rgba(255, 255, 255, 0.05);
            display: flex;
            align-items: center;
            justify-content: flex-end;
            padding-right: 14px;
        }
        .dynamic-island::after {
            content: "";
            width: 10px; height: 10px;
            border-radius: 50%;
            background: radial-gradient(circle at 30% 30%, #1a3a5c, #060812);
            box-shadow: 0 0 6px rgba(56, 189, 248, 0.4);
        }

        .status-bar {
            position: relative;
            z-index: 50;
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 14px 30px 8px;
            color: #fff;
            font-size: 13px;
            font-weight: 600;
            font-family: 'Orbitron', sans-serif;
            text-shadow: 0 1px 4px rgba(0, 0, 0, 0.8);
        }
        .status-bar .time { letter-spacing: 0.5px; }
        .status-bar .icons {
            display: flex;
            gap: 6px;
            align-items: center;
            font-size: 12px;
        }

        .screen-content {
            position: relative;
            z-index: 10;
            flex: 1;
            overflow-y: auto;
            padding: 8px 16px 20px;
            display: flex;
            flex-direction: column;
            gap: 12px;
            scrollbar-width: none;
        }
        .screen-content::-webkit-scrollbar { display: none; }

        .glass {
            background: rgba(255, 255, 255, 0.07);
            backdrop-filter: blur(22px) saturate(180%);
            -webkit-backdrop-filter: blur(22px) saturate(180%);
            border: 1px solid rgba(255, 255, 255, 0.14);
            border-radius: 22px;
            box-shadow:
                0 8px 32px rgba(0, 0, 0, 0.4),
                inset 0 1px 0 rgba(255, 255, 255, 0.18),
                inset 0 -1px 0 rgba(255, 255, 255, 0.04);
            position: relative;
            overflow: hidden;
        }
        .glass::before {
            content: "";
            position: absolute;
            top: 0; left: 0; right: 0;
            height: 1px;
            background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.5), transparent);
            pointer-events: none;
        }

        .top-header {
            padding: 12px 14px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            gap: 10px;
        }
        .brand-box { display: flex; align-items: center; gap: 10px; }
        .brand-logo {
            width: 40px; height: 40px;
            border-radius: 12px;
            background: linear-gradient(135deg, #0ea5e9, #38bdf8);
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 20px;
            font-weight: 900;
            color: white;
            box-shadow: 0 0 20px rgba(56, 189, 248, 0.7), inset 0 1px 0 rgba(255, 255, 255, 0.3);
            font-family: 'Orbitron', sans-serif;
        }
        .brand-titles h1 {
            font-size: 15px;
            font-weight: 800;
            color: #fff;
            letter-spacing: 0.3px;
        }
        .brand-titles p {
            font-size: 10px;
            color: #38bdf8;
            margin-top: 1px;
        }
        .lang-switch {
            display: flex;
            background: rgba(0, 0, 0, 0.4);
            border: 1px solid rgba(56, 189, 248, 0.4);
            border-radius: 20px;
            padding: 3px;
        }
        .l-btn {
            background: transparent;
            border: none;
            color: #94a3b8;
            padding: 5px 10px;
            font-size: 10px;
            border-radius: 15px;
            cursor: pointer;
            transition: 0.3s;
            font-weight: 600;
        }
        .l-btn.active {
            background: linear-gradient(135deg, #0ea5e9, #38bdf8);
            color: white;
            box-shadow: 0 0 12px rgba(56, 189, 248, 0.8);
        }

        .robot-main-card {
            padding: 18px 14px;
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 12px;
        }

        /* ============================================================
           🤖 رأس روبوت 3D
        ============================================================ */
        .robot-3d-stage {
            width: 100%;
            display: flex;
            justify-content: center;
            align-items: center;
            perspective: 900px;
            perspective-origin: 50% 40%;
            padding: 4px 0 8px;
        }

        .robot-head-3d {
            position: relative;
            width: 160px;
            height: 170px;
            transform-style: preserve-3d;
            animation: headIdle 6s ease-in-out infinite;
            transform-origin: 50% 80%;
        }

        @keyframes headIdle {
            0%   { transform: rotateY(0deg)   rotateX(0deg)   translateY(0); }
            15%  { transform: rotateY(-12deg) rotateX(3deg)   translateY(-2px); }
            30%  { transform: rotateY(0deg)   rotateX(-2deg)  translateY(1px); }
            50%  { transform: rotateY(12deg)  rotateX(4deg)   translateY(-3px); }
            70%  { transform: rotateY(0deg)   rotateX(-1deg)  translateY(2px); }
            85%  { transform: rotateY(-6deg)  rotateX(2deg)   translateY(-1px); }
            100% { transform: rotateY(0deg)   rotateX(0deg)   translateY(0); }
        }

        .robot-head-3d.talking-head {
            animation: headTalking 1.2s ease-in-out infinite;
        }
        @keyframes headTalking {
            0%   { transform: rotateY(0deg)   rotateX(0deg)  translateY(0)    translateZ(0); }
            20%  { transform: rotateY(-8deg)  rotateX(4deg)  translateY(-3px) translateZ(4px); }
            40%  { transform: rotateY(6deg)   rotateX(-3deg) translateY(2px)  translateZ(0); }
            60%  { transform: rotateY(-5deg)  rotateX(2deg)  translateY(-2px) translateZ(3px); }
            80%  { transform: rotateY(4deg)   rotateX(-2deg) translateY(1px)  translateZ(0); }
            100% { transform: rotateY(0deg)   rotateX(0deg)  translateY(0)    translateZ(0); }
        }

        .robot-head-3d.listening-head {
            animation: headListening 2s ease-in-out infinite;
        }
        @keyframes headListening {
            0%, 100% { transform: rotateY(0deg) rotateX(8deg); }
            50%      { transform: rotateY(0deg) rotateX(12deg); }
        }

        .robot-neck {
            position: absolute;
            bottom: -20px;
            left: 50%;
            transform: translateX(-50%);
            width: 80px;
            height: 30px;
            border-radius: 12px;
            background: linear-gradient(180deg, #1e293b, #0b1220);
            border: 1px solid rgba(56, 189, 248, 0.35);
            box-shadow: inset 0 0 12px rgba(56, 189, 248, 0.25);
            z-index: -1;
        }

        .robot-head-cube {
            position: relative;
            width: 100%;
            height: 100%;
            transform-style: preserve-3d;
            border-radius: 50% 50% 45% 45%;
            background: url('/robot_face.png') no-repeat center center / cover;
            border: 2px solid rgba(56, 189, 248, 0.55);
            box-shadow:
                0 0 40px rgba(56, 189, 248, 0.45),
                0 20px 40px rgba(0, 0, 0, 0.5),
                inset 0 0 30px rgba(56, 189, 248, 0.2);
            overflow: hidden;
        }

        .robot-head-cube::before {
            content: "";
            position: absolute;
            top: 0; left: 0; right: 0;
            height: 40%;
            background: linear-gradient(180deg, rgba(255, 255, 255, 0.18), transparent);
            border-radius: 50% 50% 50% 50%;
            pointer-events: none;
            z-index: 5;
        }

        .robot-face-3d {
            position: absolute;
            inset: 0;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            gap: 14px;
            padding: 20px 12px 12px;
            transform: translateZ(24px);
            transform-style: preserve-3d;
            z-index: 10;
        }

        .robot-eyes-3d {
            display: flex;
            gap: 30px;
            position: absolute;
            top: 42%;
            left: 50%;
            transform: translate(-50%, -50%) translateZ(10px);
            width: 100px;
            justify-content: space-between;
        }
        .eye-3d {
            position: relative;
            width: 28px;
            height: 28px;
            border-radius: 50%;
            background: transparent;
            overflow: hidden;
        }
        .eye-3d::before {
            content: "";
            position: absolute;
            top: 0; left: 0; right: 0;
            height: 100%;
            background: #dcdcdc;
            border-radius: 50% 50% 0 0;
            transform-origin: top;
            animation: eyeBlink 4.5s infinite;
            z-index: 2;
        }
        .eye-3d::after {
            content: "";
            position: absolute;
            top: 50%; left: 50%;
            width: 14px; height: 14px;
            border-radius: 50%;
            background: radial-gradient(circle, #ffffff 0%, #a5f3fc 60%, transparent 100%);
            transform: translate(-50%, -50%);
            box-shadow: 0 0 12px #ffffff;
            z-index: 1;
        }

        @keyframes eyeBlink {
            0%, 90%, 100% { transform: scaleY(0); }
            93%           { transform: scaleY(1); }
            96%           { transform: scaleY(0); }
        }

        .robot-mouth-3d {
            position: absolute;
            top: 68%;
            left: 50%;
            transform: translate(-50%, -50%) translateZ(10px);
            width: 30px;
            height: 10px;
            border-radius: 50%;
            background: #1a1a1a;
            overflow: hidden;
            transition: height 0.1s ease;
        }
        .robot-mouth-3d.talking {
            animation: mouthTalk3D 0.15s ease-in-out infinite alternate;
        }
        @keyframes mouthTalk3D {
            0%   { height: 4px;  width: 20px; }
            50%  { height: 16px; width: 34px; }
            100% { height: 6px;  width: 24px; }
        }

        .robot-avatar-wrapper {
            position: relative;
            width: 100%;
            display: flex;
            justify-content: center;
            align-items: center;
            padding-top: 14px;
        }
        .robot-avatar-wrapper::before {
            content: "";
            position: absolute;
            width: 220px; height: 220px;
            border-radius: 50%;
            border: 1px solid rgba(56, 189, 248, 0.35);
            border-top-color: transparent;
            border-right-color: transparent;
            animation: rotateRing 6s linear infinite;
            pointer-events: none;
        }
        .robot-avatar-wrapper::after {
            content: "";
            position: absolute;
            width: 250px; height: 250px;
            border-radius: 50%;
            border: 1px dashed rgba(168, 85, 247, 0.3);
            animation: rotateRing 12s linear infinite reverse;
            pointer-events: none;
        }
        @keyframes rotateRing {
            from { transform: rotate(0deg); }
            to   { transform: rotate(360deg); }
        }

        .robot-status-ring {
            position: absolute;
            inset: 0;
            pointer-events: none;
        }
        .robot-status-dot {
            position: absolute;
            width: 6px; height: 6px;
            border-radius: 50%;
            background: #22c55e;
            box-shadow: 0 0 10px #22c55e;
            animation: dotPulse 1.5s infinite;
        }
        .robot-status-dot.d1 { top: 12%; left: 10%; animation-delay: 0s; }
        .robot-status-dot.d2 { top: 12%; right: 10%; animation-delay: 0.5s; }
        .robot-status-dot.d3 { bottom: 12%; left: 10%; animation-delay: 1s; }
        .robot-status-dot.d4 { bottom: 12%; right: 10%; animation-delay: 1.5s; }

        .status-badge {
            display: flex;
            align-items: center;
            gap: 6px;
            padding: 5px 14px;
            background: rgba(0, 0, 0, 0.4);
            border: 1px solid rgba(34, 197, 94, 0.5);
            border-radius: 20px;
            font-size: 10px;
            color: #22c55e;
            font-weight: 600;
        }
        .dot {
            width: 6px; height: 6px;
            border-radius: 50%;
            background: #22c55e;
            box-shadow: 0 0 8px #22c55e;
            animation: dotPulse 1.5s infinite;
        }
        @keyframes dotPulse {
            0%, 100% { opacity: 1; transform: scale(1); }
            50%      { opacity: 0.5; transform: scale(1.3); }
        }

        .chat-panel {
            width: 100%;
            background: rgba(0, 0, 0, 0.45);
            border: 1px solid rgba(56, 189, 248, 0.25);
            border-radius: 16px;
            padding: 10px 12px;
            min-height: 70px;
            max-height: 100px;
            overflow-y: auto;
            text-align: right;
            font-size: 11.5px;
            line-height: 1.6;
            backdrop-filter: blur(10px);
        }
        .chat-panel::-webkit-scrollbar { width: 3px; }
        .chat-panel::-webkit-scrollbar-thumb {
            background: rgba(56, 189, 248, 0.5);
            border-radius: 3px;
        }
        .msg-u { color: #cbd5e1; margin-bottom: 4px; }
        .msg-b { color: #38bdf8; font-weight: 500; }

        .sound-wave {
            display: flex;
            align-items: center;
            gap: 4px;
            height: 20px;
        }
        .bar {
            width: 3px;
            background: linear-gradient(180deg, #38bdf8, #a855f7);
            border-radius: 3px;
            box-shadow: 0 0 6px rgba(56, 189, 248, 0.7);
            animation: pulseWave 1.2s infinite ease-in-out;
        }
        .bar:nth-child(1) { animation-delay: 0s; }
        .bar:nth-child(2) { animation-delay: 0.15s; }
        .bar:nth-child(3) { animation-delay: 0.3s; }
        .bar:nth-child(4) { animation-delay: 0.45s; }
        .bar:nth-child(5) { animation-delay: 0.6s; }
        .bar:nth-child(6) { animation-delay: 0.75s; }
        @keyframes pulseWave {
            0%, 100% { height: 6px; opacity: 0.5; }
            50%      { height: 18px; opacity: 1; }
        }

        .talk-action-btn {
            width: 100%;
            padding: 14px;
            border-radius: 18px;
            background: linear-gradient(135deg,
                rgba(14, 165, 233, 0.85),
                rgba(59, 130, 246, 0.85),
                rgba(168, 85, 247, 0.75));
            backdrop-filter: blur(20px);
            border: 1px solid rgba(255, 255, 255, 0.2);
            color: white;
            font-size: 13px;
            font-weight: 800;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 8px;
            box-shadow:
                0 8px 25px rgba(14, 165, 233, 0.5),
                inset 0 1px 0 rgba(255, 255, 255, 0.3);
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
        }
        .talk-action-btn::before {
            content: "";
            position: absolute;
            top: 0; left: -100%;
            width: 100%; height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.3), transparent);
            transition: left 0.5s;
        }
        .talk-action-btn:hover::before { left: 100%; }
        .talk-action-btn:active {
            transform: scale(0.97);
        }
        .talk-action-btn.listening {
            background: linear-gradient(135deg, #dc2626, #ef4444, #f97316);
            animation: listenPulse 1s ease-in-out infinite;
        }
        @keyframes listenPulse {
            0%, 100% { box-shadow: 0 8px 25px rgba(239, 68, 68, 0.6); }
            50%      { box-shadow: 0 8px 45px rgba(239, 68, 68, 0.9); }
        }

        .quick-actions {
            display: grid;
            grid-template-columns: 1fr 1fr 1fr;
            gap: 8px;
        }
        .quick-btn {
            padding: 12px 6px;
            border-radius: 16px;
            background: rgba(255, 255, 255, 0.06);
            backdrop-filter: blur(15px);
            border: 1px solid rgba(255, 255, 255, 0.12);
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 5px;
            cursor: pointer;
            transition: all 0.3s ease;
        }
        .quick-btn:active {
            background: rgba(56, 189, 248, 0.2);
            border-color: rgba(56, 189, 248, 0.5);
            transform: scale(0.96);
        }
        .quick-icon {
            font-size: 22px;
            filter: drop-shadow(0 0 6px rgba(56, 189, 248, 0.6));
        }
        .quick-text {
            font-size: 9.5px;
            color: #e2e8f0;
            font-weight: 600;
        }

        .stats-row {
            display: grid;
            grid-template-columns: 1fr 1fr 1fr;
            gap: 8px;
        }
        .stat-card {
            padding: 12px 8px;
            border-radius: 16px;
            background: rgba(255, 255, 255, 0.06);
            backdrop-filter: blur(15px);
            border: 1px solid rgba(255, 255, 255, 0.12);
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 4px;
            text-align: center;
        }
        .stat-value {
            font-family: 'Orbitron', sans-serif;
            font-size: 16px;
            font-weight: 900;
            background: linear-gradient(135deg, #38bdf8, #a855f7);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        .stat-label {
            font-size: 8.5px;
            color: #94a3b8;
            font-weight: 600;
            letter-spacing: 0.3px;
        }

        .features-row {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 10px;
        }
        .feature-box-v3 {
            padding: 10px;
            display: flex;
            flex-direction: column;
            gap: 6px;
        }
        .box-title {
            font-size: 10px;
            color: #94a3b8;
            display: flex;
            justify-content: space-between;
            font-weight: 600;
        }
        .sub-preview {
            width: 100%;
            height: 42px;
            border-radius: 10px;
            object-fit: cover;
            border: 1px solid rgba(56, 189, 248, 0.3);
            opacity: 0.85;
        }
        .active-status-text {
            font-size: 9px;
            color: #22c55e;
            display: flex;
            align-items: center;
            gap: 4px;
            font-weight: 600;
        }

        .capabilities-list {
            padding: 12px 14px;
            display: flex;
            flex-direction: column;
            gap: 8px;
        }
        .capability-item {
            font-size: 10.5px;
            color: #cbd5e1;
            display: flex;
            align-items: center;
            gap: 8px;
            padding-bottom: 6px;
            border-bottom: 1px solid rgba(255, 255, 255, 0.06);
            font-weight: 500;
        }
        .capability-item:last-child {
            border-bottom: none;
            padding-bottom: 0;
        }

        .bottom-nav-grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 8px;
        }
        .nav-card {
            padding: 12px 6px;
            display: flex;
            flex-direction: column;
            align-items: center;
            text-align: center;
            cursor: pointer;
            transition: all 0.3s ease;
            background: rgba(255, 255, 255, 0.06);
            backdrop-filter: blur(15px);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 16px;
            box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.1);
        }
        .nav-card:hover,
        .nav-card:active {
            background: rgba(56, 189, 248, 0.15);
            border-color: rgba(56, 189, 248, 0.5);
            box-shadow: 0 0 20px rgba(56, 189, 248, 0.4), inset 0 1px 0 rgba(255, 255, 255, 0.2);
            transform: translateY(-2px);
        }
        .nav-icon {
            font-size: 20px;
            margin-bottom: 4px;
            filter: drop-shadow(0 0 6px rgba(56, 189, 248, 0.5));
        }
        .nav-text {
            font-size: 9.5px;
            color: #e2e8f0;
            font-weight: 600;
        }

        .footer-note {
            text-align: center;
            font-size: 9.5px;
            color: #94a3b8;
            margin-top: 6px;
            padding-bottom: 10px;
            font-weight: 500;
            text-shadow: 0 1px 3px rgba(0, 0, 0, 0.8);
        }

        /* ============================================================
           📊 شريط معلومات النظام الجديد
        ============================================================ */
        .sys-info-strip {
            display: flex;
            justify-content: space-around;
            padding: 6px 10px;
            background: rgba(0, 0, 0, 0.35);
            border-radius: 12px;
            font-size: 8.5px;
            color: #94a3b8;
            font-family: 'Orbitron', monospace;
            gap: 8px;
        }
        .sys-info-strip span {
            display: flex;
            align-items: center;
            gap: 3px;
        }
        .sys-info-strip .ok { color: #22c55e; }
        .sys-info-strip .warn { color: #f59e0b; }

        /* ============================================================
           🧠 لوحة حل المشكلات الجديدة
        ============================================================ */
        .solver-panel {
            padding: 14px 12px;
            display: flex;
            flex-direction: column;
            gap: 10px;
        }
        .solver-head {
            display: flex;
            justify-content: space-between;
            align-items: center;
            gap: 6px;
        }
        .solver-title {
            font-size: 12px;
            font-weight: 800;
            color: #fff;
            display: flex;
            align-items: center;
            gap: 6px;
        }
        .solver-title::before {
            content: "🧠";
            filter: drop-shadow(0 0 6px rgba(168, 85, 247, 0.7));
        }
        .solver-badge {
            font-size: 8.5px;
            color: #a855f7;
            background: rgba(168, 85, 247, 0.15);
            border: 1px solid rgba(168, 85, 247, 0.4);
            padding: 3px 8px;
            border-radius: 10px;
            font-weight: 700;
        }
        .problem-input {
            width: 100%;
            min-height: 52px;
            max-height: 90px;
            padding: 10px 12px;
            border-radius: 14px;
            background: rgba(0, 0, 0, 0.45);
            border: 1px solid rgba(56, 189, 248, 0.35);
            color: #e2e8f0;
            font-size: 11px;
            line-height: 1.5;
            resize: none;
            outline: none;
            font-family: 'Tajawal', sans-serif;
            transition: border 0.3s ease;
        }
        .problem-input:focus {
            border-color: rgba(56, 189, 248, 0.8);
            box-shadow: 0 0 12px rgba(56, 189, 248, 0.25);
        }
        .problem-input::placeholder {
            color: #64748b;
            font-size: 10.5px;
        }
        .solve-btn {
            width: 100%;
            padding: 12px;
            border-radius: 14px;
            background: linear-gradient(135deg,
                rgba(168, 85, 247, 0.9),
                rgba(236, 72, 153, 0.85),
                rgba(14, 165, 233, 0.85));
            border: 1px solid rgba(255, 255, 255, 0.2);
            color: white;
            font-size: 12px;
            font-weight: 800;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 6px;
            box-shadow: 0 6px 22px rgba(168, 85, 247, 0.45),
                        inset 0 1px 0 rgba(255, 255, 255, 0.25);
            transition: all 0.3s ease;
        }
        .solve-btn:active { transform: scale(0.97); }
        .solve-btn.loading {
            opacity: 0.7;
            pointer-events: none;
        }
        .solve-result {
            display: none;
            flex-direction: column;
            gap: 8px;
            margin-top: 4px;
            animation: slideUp 0.4s ease;
        }
        .solve-result.visible { display: flex; }
        @keyframes slideUp {
            from { opacity: 0; transform: translateY(10px); }
            to   { opacity: 1; transform: translateY(0); }
        }
        .solve-block {
            background: rgba(0, 0, 0, 0.4);
            border: 1px solid rgba(56, 189, 248, 0.2);
            border-radius: 12px;
            padding: 10px 12px;
        }
        .solve-block-title {
            font-size: 10px;
            color: #38bdf8;
            font-weight: 800;
            margin-bottom: 6px;
            letter-spacing: 0.3px;
            display: flex;
            align-items: center;
            gap: 5px;
        }
        .solve-block.cause .solve-block-title { color: #f59e0b; }
        .solve-block.solutions .solve-block-title { color: #a855f7; }
        .solve-block.plan .solve-block-title { color: #22c55e; }
        .solve-block.kpis .solve-block-title { color: #ec4899; }
        .solve-block.fallback .solve-block-title { color: #ef4444; }

        .solve-block ul {
            list-style: none;
            padding: 0;
            margin: 0;
            display: flex;
            flex-direction: column;
            gap: 4px;
        }
        .solve-block li {
            font-size: 10.5px;
            color: #cbd5e1;
            line-height: 1.55;
            padding-right: 14px;
            position: relative;
        }
        .solve-block li::before {
            content: "▸";
            position: absolute;
            right: 0;
            color: #38bdf8;
            font-weight: 900;
        }
        .solve-block.plan li::before { content: "✓"; color: #22c55e; }
        .solve-block.kpis li::before { content: "📊"; font-size: 8px; }
        .solve-block.fallback li::before { content: "⚠"; color: #ef4444; }

        .plan-step {
            display: flex;
            gap: 8px;
            align-items: flex-start;
            padding: 6px 0;
            border-bottom: 1px dashed rgba(255, 255, 255, 0.08);
        }
        .plan-step:last-child { border-bottom: none; }
        .plan-step-label {
            font-size: 9px;
            color: #22c55e;
            font-weight: 800;
            background: rgba(34, 197, 94, 0.15);
            padding: 2px 6px;
            border-radius: 6px;
            white-space: nowrap;
            min-width: 55px;
            text-align: center;
        }
        .plan-step-task {
            font-size: 10.5px;
            color: #e2e8f0;
            line-height: 1.5;
            flex: 1;
        }

        .solve-status {
            font-size: 9.5px;
            color: #94a3b8;
            text-align: center;
            padding: 4px;
            font-style: italic;
        }
        .solve-status.done { color: #22c55e; }
        .solve-status.error { color: #ef4444; }

        @media (max-width: 480px) {
            body { padding: 0; background: #05070f; }
            .iphone-frame {
                width: 100vw;
                height: 100vh;
                border-radius: 0;
                padding: 0;
                box-shadow: none;
                animation: none;
            }
            .iphone-frame::before,
            .iphone-frame::after { display: none; }
            .iphone-screen { border-radius: 0; }
            .dynamic-island { top: 8px; height: 28px; width: 100px; }
        }
    </style>
</head>
<body>

<div class="iphone-frame">
    <div class="dynamic-island"></div>

    <div class="iphone-screen">

        <div class="status-bar">
            <div class="time" id="statusTime">9:41</div>
            <div class="icons">
                <span>📶</span>
                <span>📡</span>
                <span>🔋</span>
            </div>
        </div>

        <div class="screen-content">

            <div class="top-header glass">
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

            <div class="robot-main-card glass">

                <div class="robot-avatar-wrapper">
                    <div class="robot-status-ring">
                        <span class="robot-status-dot d1"></span>
                        <span class="robot-status-dot d2"></span>
                        <span class="robot-status-dot d3"></span>
                        <span class="robot-status-dot d4"></span>
                    </div>

                    <div class="robot-3d-stage">
                        <div class="robot-head-3d" id="robotHead3D">
                            <div class="robot-neck"></div>

                            <div class="robot-head-cube">
                                <div class="robot-face-3d">
                                    <div class="robot-eyes-3d">
                                        <div class="eye-3d"></div>
                                        <div class="eye-3d"></div>
                                    </div>

                                    <div class="robot-mouth-3d" id="robotMouth"></div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                <div class="status-badge">
                    <div class="dot"></div>
                    <span id="txtStatus">Online & Ready - متصل وجاهز</span>
                </div>

                <div class="chat-panel" id="chatBox">
                    <div class="msg-b" id="welcomeMsg">🤖 مرحباً، أنا C ROBOT AI روبوت ذكي متكلم حقيقي، كيف يمكنني مساعدتك اليوم؟</div>
                </div>

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

            <!-- 🧠 لوحة حل المشكلات العملية -->
            <div class="solver-panel glass" id="solverPanel">
                <div class="solver-head">
                    <div class="solver-title" id="solverTitle">حلّال المشكلات العملية</div>
                    <div class="solver-badge">AI Solver</div>
                </div>

                <textarea
                    id="problemInput"
                    class="problem-input"
                    placeholder="اكتب مشكلتك الحقيقية… مثال: عندي محل ولا أملك زبائن كفاية."></textarea>

                <button class="solve-btn" id="solveBtn" onclick="solveProblem()">
                    🧠 حلّل المشكلة وابنِ خطة عمل
                </button>

                <div class="solve-status" id="solveStatus"></div>

                <div class="solve-result" id="solveResult">
                    <div class="solve-block cause" id="blockCause">
                        <div class="solve-block-title" id="titleCause">🔍 السبب الجذري</div>
                        <div id="causeText" style="font-size:10.5px;color:#cbd5e1;line-height:1.55;"></div>
                    </div>

                    <div class="solve-block solutions" id="blockSolutions">
                        <div class="solve-block-title" id="titleSolutions">🧠 الحلول المقترحة</div>
                        <ul id="solutionsList"></ul>
                    </div>

                    <div class="solve-block plan" id="blockPlan">
                        <div class="solve-block-title" id="titlePlan">📋 خطة العمل</div>
                        <div id="planList"></div>
                    </div>

                    <div class="solve-block kpis" id="blockKpis">
                        <div class="solve-block-title" id="titleKpis">📊 مؤشرات القياس</div>
                        <ul id="kpisList"></ul>
                    </div>

                    <div class="solve-block fallback" id="blockFallback">
                        <div class="solve-block-title" id="titleFallback">🔄 خطة بديلة عند الفشل</div>
                        <div id="fallbackText" style="font-size:10.5px;color:#cbd5e1;line-height:1.55;"></div>
                    </div>

                    <button class="solve-btn" style="background:linear-gradient(135deg,rgba(14,165,233,0.9),rgba(168,85,247,0.85));" onclick="speakSolutionSummary()">
                        🔊 اسمع الملخص الصوتي
                    </button>
                </div>
            </div>

            <!-- 📊 شريط معلومات النظام الحية -->
            <div class="sys-info-strip">
                <span>🔋 <b id="sysBattery">—</b></span>
                <span>🌐 <b id="sysNetwork">—</b></span>
                <span>🎤 <b id="sysMic">—</b></span>
                <span>🤖 <b id="sysStatus">V6</b></span>
            </div>

            <div class="quick-actions">
                <div class="quick-btn" onclick="quickAction('weather')">
                    <div class="quick-icon">🌤️</div>
                    <div class="quick-text">الطقس</div>
                </div>
                <div class="quick-btn" onclick="quickAction('news')">
                    <div class="quick-icon">📰</div>
                    <div class="quick-text">الأخبار</div>
                </div>
                <div class="quick-btn" onclick="quickAction('translate')">
                    <div class="quick-icon">🌐</div>
                    <div class="quick-text">ترجمة</div>
                </div>
            </div>

            <div class="stats-row">
                <div class="stat-card">
                    <div class="stat-value" id="statUsers">1,247</div>
                    <div class="stat-label">المستخدمون</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value" id="statChats">8,392</div>
                    <div class="stat-label">المحادثات</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value" id="statOnline">●</div>
                    <div class="stat-label">متصل الآن</div>
                </div>
            </div>

            <div class="features-row">
                <div class="feature-box-v3 glass">
                    <div class="box-title">
                        <span id="lblEye">تتبع العين</span>
                        <span>👁️</span>
                    </div>
                    <img src="https://images.unsplash.com/photo-1534447677768-be436bb09401?q=80&w=300&auto=format&fit=crop" class="sub-preview" alt="Eye Tracking">
                    <div class="active-status-text" id="lblEyeActive">
                        <span class="dot"></span> نشط Active
                    </div>
                </div>
                <div class="feature-box-v3 glass">
                    <div class="box-title">
                        <span id="lblMouth">تحريك الفم</span>
                        <span>👄</span>
                    </div>
                    <img src="https://images.unsplash.com/photo-1509967419530-da38b4704bc6?q=80&w=300&auto=format&fit=crop" class="sub-preview" alt="Mouth Animation">
                    <div class="active-status-text" id="lblMouthActive">
                        <span class="dot"></span> نشط Active
                    </div>
                </div>
            </div>

            <div class="capabilities-list glass" id="capList">
                <div class="capability-item">🌐 يتحدث العربية والإنجليزية بطلاقة</div>
                <div class="capability-item">🧠 فهم الأسئلة المعقدة بدقة متناهية</div>
                <div class="capability-item">🎤 يستمع إلى صوتك ويرد فوراً</div>
            </div>

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
                C ROBOT AI V6 – Modern Tech Edition
            </div>

        </div>
    </div>
</div>

<script>
    let currentLang = 'ar';
    let wakeLock = null;
    let recognition = null;
    let isListening = false;
    let isSpeaking = false;
    let lastSolution = null;

    /* ============================================================
       🎛️ محرك الصوت الروبوتي (مع Web Audio Filters)
    ============================================================ */
    let audioCtx = null;
    function getAudioCtx() {
        if (!audioCtx) {
            try {
                audioCtx = new (window.AudioContext || window.webkitAudioContext)();
            } catch (e) {
                audioCtx = null;
            }
        }
        if (audioCtx && audioCtx.state === 'suspended') {
            audioCtx.resume();
        }
        return audioCtx;
    }

    /* نغمة روبوتية مع فلترة */
    function playRobotBeep(freq = 880, duration = 0.08, type = 'square', gain = 0.06) {
        const ctx = getAudioCtx();
        if (!ctx) return;
        const osc = ctx.createOscillator();
        const g = ctx.createGain();
        const filter = ctx.createBiquadFilter();

        filter.type = 'bandpass';
        filter.frequency.value = freq * 1.2;
        filter.Q.value = 8;

        osc.type = type;
        osc.frequency.setValueAtTime(freq, ctx.currentTime);
        osc.frequency.exponentialRampToValueAtTime(freq * 0.6, ctx.currentTime + duration);

        g.gain.setValueAtTime(0, ctx.currentTime);
        g.gain.linearRampToValueAtTime(gain, ctx.currentTime + 0.01);
        g.gain.exponentialRampToValueAtTime(0.0001, ctx.currentTime + duration);

        osc.connect(filter).connect(g).connect(ctx.destination);
        osc.start();
        osc.stop(ctx.currentTime + duration + 0.02);
    }

    function playRobotProcessing() {
        playRobotBeep(1200, 0.05, 'square', 0.05);
        setTimeout(() => playRobotBeep(900, 0.05, 'square', 0.05), 70);
        setTimeout(() => playRobotBeep(1400, 0.06, 'sawtooth', 0.045), 140);
    }

    /* ============================================================
       🗣️ محرك الكلام (إنجليزي روبوتي)
    ============================================================ */
    function pickRoboticEnglishVoice() {
        if (!('speechSynthesis' in window)) return null;
        const voices = window.speechSynthesis.getVoices();
        if (!voices || !voices.length) return null;
        const preferred = [
            /Google UK English Male/i,
            /Microsoft (David|Mark|George)/i,
            /Daniel/i,
            /Alex/i,
            /Google US English/i,
            /en-GB/i,
            /en-US/i,
            /en/i
        ];
        for (const pattern of preferred) {
            const v = voices.find(vv => pattern.test(vv.name) || pattern.test(vv.lang));
            if (v) return v;
        }
        return voices.find(v => v.lang && v.lang.toLowerCase().startsWith('en')) || voices[0];
    }

    function getEnglishVoice() {
        return pickRoboticEnglishVoice() || null;
    }

    if ('speechSynthesis' in window) {
        window.speechSynthesis.onvoiceschanged = () => { getEnglishVoice(); };
        window.speechSynthesis.getVoices();
    }

    function speakRobotEnglish(text) {
        const chatBox = document.getElementById('chatBox');
        chatBox.innerHTML += `<div class="msg-b">🤖 ${text}</div>`;
        chatBox.scrollTop = chatBox.scrollHeight;

        const head  = document.getElementById('robotHead3D');
        const mouth = document.getElementById('robotMouth');

        head.classList.remove('listening-head');
        head.classList.add('talking-head');
        mouth.classList.add('talking');
        isSpeaking = true;

        playRobotProcessing();
        vibrate([50, 30, 50]);

        const stopAnim = () => {
            head.classList.remove('talking-head');
            mouth.classList.remove('talking');
            isSpeaking = false;
        };

        if ('speechSynthesis' in window) {
            try { window.speechSynthesis.cancel(); } catch (e) {}

            const utter = new SpeechSynthesisUtterance(text);
            const v = getEnglishVoice();
            if (v) utter.voice = v;

            utter.lang = 'en-US';
            utter.pitch = 0.05;
            utter.rate = 0.82;
            utter.volume = 1.0;

            let pulseTimer = null;
            const startPulses = () => {
                pulseTimer = setInterval(() => {
                    playRobotBeep(700 + Math.random() * 900, 0.03, 'square', 0.02);
                }, 260);
            };

            utter.onstart = () => {
                playRobotBeep(1500, 0.06, 'square', 0.05);
                startPulses();
            };

            utter.onend = () => {
                if (pulseTimer) clearInterval(pulseTimer);
                playRobotBeep(400, 0.08, 'sawtooth', 0.05);
                stopAnim();
            };
            utter.onerror = () => {
                if (pulseTimer) clearInterval(pulseTimer);
                stopAnim();
            };

            window.speechSynthesis.speak(utter);
        } else {
            setTimeout(stopAnim, Math.max(1500, text.length * 60));
        }
    }

    /* ============================================================
       🎤 SpeechRecognition — الروبوت يسمعك فعلاً
    ============================================================ */
    function initRecognition() {
        const SR = window.SpeechRecognition || window.webkitSpeechRecognition;
        if (!SR) {
            document.getElementById('sysMic').textContent = 'N/A';
            document.getElementById('sysMic').className = 'warn';
            return null;
        }
        const r = new SR();
        r.continuous = false;
        r.interimResults = false;
        r.maxAlternatives = 1;
        r.lang = currentLang === 'ar' ? 'ar-SA' : 'en-US';

        r.onstart = () => {
            isListening = true;
            const btn = document.getElementById('talkBtn');
            btn.classList.add('listening');
            btn.innerHTML = '🔴 ' + (currentLang === 'ar' ? 'أستمع إليك...' : 'Listening...');
            const head = document.getElementById('robotHead3D');
            head.classList.remove('talking-head');
            head.classList.add('listening-head');
            document.getElementById('sysMic').textContent = 'ON';
            document.getElementById('sysMic').className = 'ok';
            playRobotBeep(1800, 0.05, 'sine', 0.04);
        };

        r.onresult = (e) => {
            const transcript = e.results[0][0].transcript;
            const chatBox = document.getElementById('chatBox');
            chatBox.innerHTML += `<div class="msg-u">👤 ${transcript}</div>`;
            chatBox.scrollTop = chatBox.scrollHeight;
            respondToUser(transcript);
        };

        r.onerror = (e) => {
            console.warn('Speech error:', e.error);
            resetListenUI();
            if (e.error === 'not-allowed') {
                addBotMsg(currentLang === 'ar'
                    ? 'الرجاء السماح بالوصول إلى الميكروفون.'
                    : 'Please allow microphone access.');
            }
        };

        r.onend = () => {
            resetListenUI();
        };

        return r;
    }

    function resetListenUI() {
        isListening = false;
        const btn = document.getElementById('talkBtn');
        btn.classList.remove('listening');
        btn.innerHTML = translations[currentLang].talkBtn;
        const head = document.getElementById('robotHead3D');
        head.classList.remove('listening-head');
        document.getElementById('sysMic').textContent = 'OFF';
        document.getElementById('sysMic').className = '';
    }

    function addBotMsg(text) {
        const chatBox = document.getElementById('chatBox');
        chatBox.innerHTML += `<div class="msg-b">🤖 ${text}</div>`;
        chatBox.scrollTop = chatBox.scrollHeight;
    }

    /* إرسال النص للخادم والحصول على رد */
    async function respondToUser(userText) {
        try {
            const res = await fetch('/api/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message: userText, lang: currentLang })
            });
            const data = await res.json();
            speak(data.reply || 'I did not understand.');
        } catch (e) {
            // fallback محلي
            speak(currentLang === 'ar'
                ? `لقد سمعت: ${userText}`
                : `I heard: ${userText}`);
        }
    }

    function triggerTalk() {
        getAudioCtx();
        acquireWakeLock();
        if (isListening) {
            try { recognition && recognition.stop(); } catch (e) {}
            return;
        }
        if (!recognition) recognition = initRecognition();
        if (!recognition) {
            speak("Speech recognition is not supported on this browser.");
            return;
        }
        try {
            recognition.lang = currentLang === 'ar' ? 'ar-SA' : 'en-US';
            recognition.start();
        } catch (e) {
            // already started
        }
    }

    /* ============================================================
       🧠 حلّال المشكلات — يربط بالـ /api/solve
    ============================================================ */
    async function solveProblem() {
        const input = document.getElementById('problemInput');
        const problem = (input.value || '').trim();
        const statusEl = document.getElementById('solveStatus');
        const btn = document.getElementById('solveBtn');

        if (!problem) {
            statusEl.textContent = currentLang === 'ar'
                ? '✍️ اكتب مشكلتك أولاً قبل التحليل.'
                : '✍️ Please write your problem first.';
            statusEl.className = 'solve-status error';
            return;
        }

        btn.classList.add('loading');
        btn.textContent = currentLang === 'ar' ? '⏳ جاري التحليل وبناء الخطة...' : '⏳ Analyzing & building plan...';
        statusEl.textContent = currentLang === 'ar'
            ? '🔬 يسمع → يحلل → يحدد السبب → يقترح → يخطط...'
            : '🔬 Listening → Analyzing → Root cause → Solutions → Plan...';
        statusEl.className = 'solve-status';

        playRobotBeep(1400, 0.06, 'square', 0.05);
        setTimeout(() => playRobotBeep(1000, 0.06, 'square', 0.05), 120);
        setTimeout(() => playRobotBeep(1600, 0.06, 'sawtooth', 0.05), 260);

        try {
            const res = await fetch('/api/solve', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ problem, lang: currentLang })
            });
            const data = await res.json();

            if (data.error) {
                statusEl.textContent = '❌ ' + (data.error_ar || data.error);
                statusEl.className = 'solve-status error';
                btn.classList.remove('loading');
                btn.textContent = translations[currentLang].solveBtn;
                return;
            }

            lastSolution = data;
            renderSolution(data);
            statusEl.textContent = currentLang === 'ar'
                ? '✅ تم بناء خطة العمل. يمكنك سماع الملخص أو متابعة التنفيذ.'
                : '✅ Plan is ready. You can listen to summary or proceed.';
            statusEl.className = 'solve-status done';

            // ملخص صوتي تلقائي
            speakSolutionSummary();

        } catch (e) {
            statusEl.textContent = '❌ ' + (currentLang === 'ar'
                ? 'تعذر الاتصال بالخادم، حاول مجدداً.'
                : 'Server connection failed, try again.');
            statusEl.className = 'solve-status error';
        } finally {
            btn.classList.remove('loading');
            btn.textContent = translations[currentLang].solveBtn;
        }
    }

    function renderSolution(data) {
        const t = translations[currentLang];
        document.getElementById('solveResult').classList.add('visible');

        document.getElementById('titleCause').textContent   = t.titleCause;
        document.getElementById('titleSolutions').textContent = t.titleSolutions;
        document.getElementById('titlePlan').textContent    = t.titlePlan;
        document.getElementById('titleKpis').textContent    = t.titleKpis;
        document.getElementById('titleFallback').textContent = t.titleFallback;

        document.getElementById('causeText').textContent = data.cause;

        const solutionsList = document.getElementById('solutionsList');
        solutionsList.innerHTML = '';
        (data.solutions || []).forEach(s => {
            const li = document.createElement('li');
            li.textContent = s;
            solutionsList.appendChild(li);
        });

        const planList = document.getElementById('planList');
        planList.innerHTML = '';
        (data.plan || []).forEach(p => {
            const row = document.createElement('div');
            row.className = 'plan-step';
            const lbl = document.createElement('div');
            lbl.className = 'plan-step-label';
            lbl.textContent = p.step;
            const tsk = document.createElement('div');
            tsk.className = 'plan-step-task';
            tsk.textContent = p.task;
            row.appendChild(lbl);
            row.appendChild(tsk);
            planList.appendChild(row);
        });

        const kpisList = document.getElementById('kpisList');
        kpisList.innerHTML = '';
        (data.kpis || []).forEach(k => {
            const li = document.createElement('li');
            li.textContent = k;
            kpisList.appendChild(li);
        });

        document.getElementById('fallbackText').textContent = data.fallback;
    }

    function speakSolutionSummary() {
        if (!lastSolution) {
            speak(currentLang === 'ar'
                ? 'لا توجد خطة حالياً. اكتب مشكلتك أولاً.'
                : 'No plan yet. Please write your problem first.');
            return;
        }
        // الملخص الصوتي دائماً بالإنجليزية كما هو محرك الروبوت الحالي
        const d = lastSolution;
        const enCause = d.cause;
        const enSummary = `Problem analysis complete. Root cause identified: ${enCause}. ` +
            `I generated ${d.solutions.length} solutions and a plan of ${d.plan.length} steps. ` +
            `Key performance indicators: ${d.kpis.join(', ')}. ` +
            `If the plan fails, fallback strategy: ${d.fallback}`;
        speak(enSummary);
    }

    /* ============================================================
       🔒 Wake Lock — الشاشة لا تنطفئ
    ============================================================ */
    async function acquireWakeLock() {
        try {
            if ('wakeLock' in navigator && !wakeLock) {
                wakeLock = await navigator.wakeLock.request('screen');
                wakeLock.addEventListener('release', () => { wakeLock = null; });
            }
        } catch (e) {}
    }

    /* ============================================================
       📳 Vibration API
    ============================================================ */
    function vibrate(pattern) {
        if ('vibrate' in navigator) {
            try { navigator.vibrate(pattern); } catch (e) {}
        }
    }

    /* ============================================================
       🔋 Battery + 🌐 Network APIs
    ============================================================ */
    async function initSystemInfo() {
        // Battery
        if ('getBattery' in navigator) {
            try {
                const b = await navigator.getBattery();
                const update = () => {
                    document.getElementById('sysBattery').textContent =
                        Math.round(b.level * 100) + '%' + (b.charging ? '⚡' : '');
                };
                update();
                b.addEventListener('levelchange', update);
                b.addEventListener('chargingchange', update);
            } catch (e) {}
        } else {
            document.getElementById('sysBattery').textContent = 'N/A';
        }

        // Network
        const conn = navigator.connection || navigator.mozConnection || navigator.webkitConnection;
        const updateNet = () => {
            if (conn) {
                document.getElementById('sysNetwork').textContent = (conn.effectiveType || 'on').toUpperCase();
            } else {
                document.getElementById('sysNetwork').textContent = navigator.onLine ? 'ON' : 'OFF';
            }
        };
        updateNet();
        if (conn) conn.addEventListener('change', updateNet);
        window.addEventListener('online', updateNet);
        window.addEventListener('offline', updateNet);

        // Mic
        if ('SpeechRecognition' in window || 'webkitSpeechRecognition' in window) {
            document.getElementById('sysMic').textContent = 'OK';
            document.getElementById('sysMic').className = 'ok';
        } else {
            document.getElementById('sysMic').textContent = 'N/A';
            document.getElementById('sysMic').className = 'warn';
        }
    }

    /* ============================================================
       🌐 الترجمة
    ============================================================ */
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
                "🎤 يستمع إلى صوتك ويرد فوراً"
            ],
            navs: ["محادثة ذكية", "ترجمة فورية", "مساعد شخصي", "بحث ذكي", "معلومات عامة", "إعدادات"],
            footer: "C ROBOT AI V6 – Modern Tech Edition",
            speechWelcome: "Hello, I am C ROBOT AI. The real talking AI robot. Systems online. Ready to assist you now.",
            solverTitle: "حلّال المشكلات العملية",
            problemPlaceholder: "اكتب مشكلتك الحقيقية… مثال: عندي محل ولا أملك زبائن كفاية.",
            solveBtn: "🧠 حلّل المشكلة وابنِ خطة عمل",
            titleCause: "🔍 السبب الجذري",
            titleSolutions: "🧠 الحلول المقترحة",
            titlePlan: "📋 خطة العمل",
            titleKpis: "📊 مؤشرات القياس",
            titleFallback: "🔄 خطة بديلة عند الفشل"
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
                "🎤 Listens to your voice and replies instantly"
            ],
            navs: ["Smart Chat", "Translate", "Assistant", "Smart Search", "Knowledge", "Settings"],
            footer: "C ROBOT AI V6 – Modern Tech Edition",
            speechWelcome: "Hello, I am C ROBOT AI. The real talking AI robot. Systems online. Ready to assist you now.",
            solverTitle: "Practical Problem Solver",
            problemPlaceholder: "Write your real problem… e.g. I have a shop with not enough customers.",
            solveBtn: "🧠 Analyze & Build Action Plan",
            titleCause: "🔍 Root Cause",
            titleSolutions: "🧠 Suggested Solutions",
            titlePlan: "📋 Action Plan",
            titleKpis: "📊 KPIs",
            titleFallback: "🔄 Fallback Strategy"
        }
    };

    function updateStatusTime() {
        const now = new Date();
        const hours = now.getHours();
        const minutes = String(now.getMinutes()).padStart(2, '0');
        document.getElementById('statusTime').innerText = `${hours}:${minutes}`;
    }
    updateStatusTime();
    setInterval(updateStatusTime, 30000);

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

        document.querySelectorAll('.capability-item').forEach((item, idx) => {
            item.innerText = t.caps[idx];
        });

        for (let i = 1; i <= 6; i++) {
            document.getElementById('nav' + i).innerText = t.navs[i - 1];
        }
        document.getElementById('footerText').innerText = t.footer;

        // Solver panel translations
        document.getElementById('solverTitle').innerText = t.solverTitle;
        document.getElementById('problemInput').placeholder = t.problemPlaceholder;
        document.getElementById('solveBtn').innerText = t.solveBtn;
        document.getElementById('titleCause').innerText = t.titleCause;
        document.getElementById('titleSolutions').innerText = t.titleSolutions;
        document.getElementById('titlePlan').innerText = t.titlePlan;
        document.getElementById('titleKpis').innerText = t.titleKpis;
        document.getElementById('titleFallback').innerText = t.titleFallback;

        speak(t.speechWelcome);
    }

    function speak(text) {
        speakRobotEnglish(text);
    }

    function quickAction(action) {
        const responses = {
            ar: {
                weather: "Weather update. Today is sunny, twenty four degrees Celsius. Ideal conditions for outdoor activity.",
                news: "Latest news. New breakthroughs in artificial intelligence have just been announced.",
                translate: "Instant translation module is online. Please provide the text to translate."
            },
            en: {
                weather: "Weather update. Today is sunny, twenty four degrees Celsius. Ideal conditions for outdoor activity.",
                news: "Latest news. New breakthroughs in artificial intelligence have just been announced.",
                translate: "Instant translation module is online. Please provide the text to translate."
            }
        };
        speak(responses[currentLang][action]);
    }

    function runAction(action) {
        const responses = {
            ar: {
                chat: "Smart chat module activated. I am ready for conversation.",
                translate: "Instant translation is now active.",
                assistant: "Your personal assistant is ready to serve.",
                search: "Smart search engine is now online.",
                knowledge: "General knowledge base is open.",
                settings: "Settings panel is now active."
            },
            en: {
                chat: "Smart chat module activated. I am ready for conversation.",
                translate: "Instant translation is now active.",
                assistant: "Your personal assistant is ready to serve.",
                search: "Smart search engine is now online.",
                knowledge: "General knowledge base is open.",
                settings: "Settings panel is now active."
            }
        };
        speak(responses[currentLang][action]);
    }

    function animateStats() {
        const users = document.getElementById('statUsers');
        const chats = document.getElementById('statChats');
        let u = 1247;
        let c = 8392;
        setInterval(() => {
            u += Math.floor(Math.random() * 3);
            c += Math.floor(Math.random() * 5);
            users.innerText = u.toLocaleString('en-US');
            chats.innerText = c.toLocaleString('en-US');
        }, 5000);
    }
    animateStats();

    /* تفاعل العينين مع المؤشر */
    (function robotHeadEnhancements() {
        const head = document.getElementById('robotHead3D');
        if (!head) return;
        setInterval(() => {
            if (head.classList.contains('talking-head') ||
                head.classList.contains('listening-head')) return;
            const rx = (Math.random() * 6 - 3).toFixed(2);
            const ry = (Math.random() * 16 - 8).toFixed(2);
            head.style.transition = 'transform 1.2s ease-in-out';
            head.style.transform = `rotateY(${ry}deg) rotateX(${rx}deg)`;
            setTimeout(() => { head.style.transform = ''; }, 1200);
        }, 5500);

        document.addEventListener('mousemove', (e) => {
            const pupils = document.querySelectorAll('.eye-3d');
            if (!pupils.length) return;
            const cx = window.innerWidth / 2;
            const cy = window.innerHeight / 2;
            const dx = (e.clientX - cx) / cx;
            const dy = (e.clientY - cy) / cy;
            pupils.forEach(p => {
                p.style.transform = `translate(${dx * 2}px, ${dy * 2}px)`;
            });
        });
    })();

    /* 📱 تسجيل Service Worker */
    if ('serviceWorker' in navigator) {
        window.addEventListener('load', () => {
            navigator.serviceWorker.register('/sw.js').catch(() => {});
        });
    }

    /* إعادة الحصول على Wake Lock عند العودة للصفحة */
    document.addEventListener('visibilitychange', () => {
        if (document.visibilityState === 'visible') {
            acquireWakeLock();
        }
    });

    /* تسخين AudioContext */
    document.addEventListener('click', () => { getAudioCtx(); }, { once: true });
    document.addEventListener('touchstart', () => { getAudioCtx(); }, { once: true });

    /* تشغيل معلومات النظام */
    initSystemInfo();

    console.log('%c🤖 C ROBOT AI V6 – Modern Tech Edition','color:#0ea5e9;font-size:16px;font-weight:bold;');
    console.log('%c✨ Speech Recognition · PWA · Wake Lock · Battery · Network','color:#a855f7;font-size:11px;');
    console.log('%c🧠 Practical Problem Solver Engine — Active','color:#ec4899;font-size:11px;font-weight:bold;');
</script>
</body>
</html>
"""


@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)


if __name__ == '__main__':
    port = int(os.environ.get('PORT', PORT))
    print(f"🤖 C ROBOT AI V6 يعمل على http://localhost:{port}")
    app.run(host='0.0.0.0', port=port, debug=False, threaded=True)
