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

from flask import Flask, render_template_string, send_from_directory

app = Flask(__name__)

# ============================================================
# مسار خدمة خلفيات Bg_XX.jpg من جذر المشروع
# ============================================================
@app.route('/Bg_<int:num>.jpg')
def serve_bg(num):
    if 1 <= num <= 55:
        return send_from_directory('.', f'Bg_{num:02d}.jpg')
    return "Image not found", 404

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="ar" dir="rtl" id="htmlRoot">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
    <title>C ROBOT AI V5 - Cinematic Glass Edition</title>
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
           شاشة iPhone مع خلفية Bg_01.jpg
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

            /* ✅ خلفية Bg_01.jpg */
            background: url('/Bg_01.jpg') no-repeat center center / cover;
        }

        /* طبقة تعتيم فوق الخلفية لتحسين القراءة */
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

        /* Dynamic Island */
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

        /* Status Bar */
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

        /* ============================================================
           محتوى الشاشة
        ============================================================ */
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

        /* Glass Card */
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

        /* Header */
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

        /* Robot Card */
        .robot-main-card {
            padding: 18px 14px;
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 12px;
        }

        /* ============================================================
           🤖 التطوير: رأس روبوت 3D متحرك بالكامل
           - منظور 3D perspective + preserve-3d
           - رأس يتحرك (يمين/يسار/فوق/تحت/ميل)
           - عينان ترمشان بشكل واقعي
           - فم ينفتح ويغلق بتزامن مع الكلام
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
            width: 140px;
            height: 150px;
            transform-style: preserve-3d;
            animation: headIdle 6s ease-in-out infinite;
            transform-origin: 50% 80%;
        }

        /* حركة الرأس في وضع الخمول */
        @keyframes headIdle {
            0%   { transform: rotateY(0deg)   rotateX(0deg)   translateY(0); }
            15%  { transform: rotateY(-12deg) rotateX(3deg)   translateY(-2px); }
            30%  { transform: rotateY(0deg)   rotateX(-2deg)  translateY(1px); }
            50%  { transform: rotateY(12deg)  rotateX(4deg)   translateY(-3px); }
            70%  { transform: rotateY(0deg)   rotateX(-1deg)  translateY(2px); }
            85%  { transform: rotateY(-6deg)  rotateX(2deg)   translateY(-1px); }
            100% { transform: rotateY(0deg)   rotateX(0deg)   translateY(0); }
        }

        /* حالة "يتكلم" – حركة رأس أكثر حيوية */
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

        /* قاعدة العنق / الجسم */
        .robot-neck {
            position: absolute;
            bottom: -14px;
            left: 50%;
            transform: translateX(-50%);
            width: 60px;
            height: 26px;
            border-radius: 12px;
            background: linear-gradient(180deg, #1e293b, #0b1220);
            border: 1px solid rgba(56, 189, 248, 0.35);
            box-shadow: inset 0 0 12px rgba(56, 189, 248, 0.25);
            z-index: -1;
        }

        /* الرأس نفسه – مكعب 3D */
        .robot-head-cube {
            position: relative;
            width: 100%;
            height: 100%;
            transform-style: preserve-3d;
            border-radius: 26px;
            background:
                linear-gradient(145deg, rgba(30, 41, 59, 0.95), rgba(11, 18, 32, 0.98)),
                radial-gradient(circle at 30% 20%, rgba(56, 189, 248, 0.25), transparent 60%);
            border: 1.5px solid rgba(56, 189, 248, 0.55);
            box-shadow:
                0 0 40px rgba(56, 189, 248, 0.45),
                0 20px 40px rgba(0, 0, 0, 0.5),
                inset 0 0 30px rgba(56, 189, 248, 0.2),
                inset 0 1px 0 rgba(255, 255, 255, 0.25);
            overflow: hidden;
        }

        /* لمعة زجاجية على الرأس */
        .robot-head-cube::before {
            content: "";
            position: absolute;
            top: 0; left: 0; right: 0;
            height: 40%;
            background: linear-gradient(180deg, rgba(255, 255, 255, 0.18), transparent);
            border-radius: 26px 26px 50% 50%;
            pointer-events: none;
        }

        /* خطوط تقنية على الرأس */
        .robot-head-cube::after {
            content: "";
            position: absolute;
            bottom: 12px; left: 12px; right: 12px;
            height: 3px;
            background: repeating-linear-gradient(90deg,
                rgba(56, 189, 248, 0.9) 0 6px,
                transparent 6px 12px);
            border-radius: 3px;
            opacity: 0.7;
            box-shadow: 0 0 8px rgba(56, 189, 248, 0.8);
        }

        /* الأذنان الجانبيتان للروبوت */
        .robot-ear {
            position: absolute;
            top: 50%;
            transform: translateY(-50%);
            width: 12px;
            height: 30px;
            border-radius: 6px;
            background: linear-gradient(180deg, #1e293b, #0b1220);
            border: 1px solid rgba(56, 189, 248, 0.5);
            box-shadow: 0 0 12px rgba(56, 189, 248, 0.5), inset 0 0 6px rgba(56, 189, 248, 0.4);
        }
        .robot-ear.left  { left: -7px; }
        .robot-ear.right { right: -7px; }
        .robot-ear::after {
            content: "";
            position: absolute;
            top: 50%; left: 50%;
            transform: translate(-50%, -50%);
            width: 4px; height: 4px;
            border-radius: 50%;
            background: #38bdf8;
            box-shadow: 0 0 8px #38bdf8;
            animation: earPulse 1.6s ease-in-out infinite;
        }
        @keyframes earPulse {
            0%, 100% { opacity: 1; transform: translate(-50%, -50%) scale(1); }
            50%      { opacity: 0.4; transform: translate(-50%, -50%) scale(1.4); }
        }

        /* الهوائي فوق الرأس */
        .robot-antenna {
            position: absolute;
            top: -26px;
            left: 50%;
            transform: translateX(-50%);
            width: 3px;
            height: 26px;
            background: linear-gradient(180deg, #38bdf8, #0b1220);
            border-radius: 2px;
            box-shadow: 0 0 8px rgba(56, 189, 248, 0.7);
        }
        .robot-antenna::before {
            content: "";
            position: absolute;
            top: -7px; left: 50%;
            transform: translateX(-50%);
            width: 10px; height: 10px;
            border-radius: 50%;
            background: radial-gradient(circle at 30% 30%, #67e8f9, #0284c7);
            box-shadow: 0 0 14px #38bdf8, 0 0 24px #38bdf8;
            animation: antennaGlow 1.4s ease-in-out infinite;
        }
        @keyframes antennaGlow {
            0%, 100% { opacity: 1;   transform: translateX(-50%) scale(1); }
            50%      { opacity: 0.6; transform: translateX(-50%) scale(1.25); }
        }

        /* الوجه (طبقة الأزرار والعيون) */
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
        }

        /* العينان */
        .robot-eyes-3d {
            display: flex;
            gap: 22px;
            transform: translateZ(10px);
        }
        .eye-3d {
            position: relative;
            width: 30px;
            height: 30px;
            border-radius: 50%;
            background:
                radial-gradient(circle at 50% 50%, #67e8f9 0%, #0ea5e9 35%, #0369a1 70%, #082f49 100%);
            box-shadow:
                0 0 18px #38bdf8,
                0 0 32px rgba(56, 189, 248, 0.8),
                inset 0 0 8px rgba(255, 255, 255, 0.7);
            overflow: hidden;
            animation: eyeBlink 4.5s infinite;
            transition: transform 0.15s ease;
        }
        /* بؤبؤ داخلي (يبدو كأنه يتحرك) */
        .eye-3d::before {
            content: "";
            position: absolute;
            top: 50%; left: 50%;
            width: 12px; height: 12px;
            border-radius: 50%;
            background: radial-gradient(circle, #ffffff 0%, #a5f3fc 60%, transparent 100%);
            transform: translate(-50%, -50%);
            box-shadow: 0 0 12px #ffffff;
            animation: pupilMove 3s ease-in-out infinite;
        }
        /* انعكاس ضوئي */
        .eye-3d::after {
            content: "";
            position: absolute;
            top: 5px; left: 7px;
            width: 8px; height: 8px;
            border-radius: 50%;
            background: rgba(255, 255, 255, 0.9);
            filter: blur(1px);
        }

        @keyframes pupilMove {
            0%, 100% { transform: translate(-50%, -50%); }
            25%      { transform: translate(-40%, -50%); }
            50%      { transform: translate(-50%, -40%); }
            75%      { transform: translate(-60%, -50%); }
        }

        /* رمش العين – مع تأثير ثلاثي الأبعاد */
        @keyframes eyeBlink {
            0%, 90%, 100% { transform: scaleY(1) translateZ(0); }
            93%           { transform: scaleY(0.05) translateZ(0); }
            96%           { transform: scaleY(1) translateZ(0); }
        }

        /* فم الروبوت */
        .robot-mouth-3d {
            position: relative;
            width: 46px;
            height: 8px;
            border-radius: 4px;
            background: linear-gradient(90deg, #38bdf8, #a855f7);
            box-shadow:
                0 0 12px #38bdf8,
                0 0 24px rgba(56, 189, 248, 0.5),
                inset 0 0 4px rgba(255, 255, 255, 0.8);
            transition: height 0.08s ease, width 0.08s ease, transform 0.08s ease;
        }
        .robot-mouth-3d.talking {
            animation: mouthTalk3D 0.18s ease-in-out infinite alternate;
        }
        @keyframes mouthTalk3D {
            0%   { height: 4px;  width: 30px; transform: translateZ(0); }
            50%  { height: 14px; width: 48px; transform: translateZ(6px); }
            100% { height: 6px;  width: 40px; transform: translateZ(0); }
        }

        /* الحاجبان */
        .robot-brow {
            position: absolute;
            top: 34px;
            width: 26px;
            height: 4px;
            border-radius: 3px;
            background: linear-gradient(90deg, #38bdf8, #a855f7);
            box-shadow: 0 0 8px rgba(56, 189, 248, 0.8);
            transition: transform 0.2s ease;
        }
        .robot-brow.left  { left: 22px; transform: rotate(-8deg); }
        .robot-brow.right { right: 22px; transform: rotate(8deg); }
        .robot-head-3d.talking-head .robot-brow.left  { transform: rotate(-14deg) translateY(-3px); }
        .robot-head-3d.talking-head .robot-brow.right { transform: rotate(14deg) translateY(-3px); }

        /* هالة دوران حول الرأس */
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
            width: 200px; height: 200px;
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
            width: 230px; height: 230px;
            border-radius: 50%;
            border: 1px dashed rgba(168, 85, 247, 0.3);
            animation: rotateRing 12s linear infinite reverse;
            pointer-events: none;
        }
        @keyframes rotateRing {
            from { transform: rotate(0deg); }
            to   { transform: rotate(360deg); }
        }

        /* مؤشرات الحالة الصغيرة حول الرأس */
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

        /* Chat Panel */
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

        /* Sound Wave */
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

        /* Talk Button */
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
            box-shadow:
                0 4px 15px rgba(14, 165, 233, 0.6),
                inset 0 1px 0 rgba(255, 255, 255, 0.3);
        }

        /* Quick Actions Row */
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

        /* Stats Row */
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

        /* Features Row */
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

        /* Capabilities List */
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

        /* Bottom Nav */
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

        /* Footer */
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
           Responsive
        ============================================================ */
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

        <!-- Status Bar -->
        <div class="status-bar">
            <div class="time" id="statusTime">9:41</div>
            <div class="icons">
                <span>📶</span>
                <span>📡</span>
                <span>🔋</span>
            </div>
        </div>

        <!-- Content -->
        <div class="screen-content">

            <!-- Header -->
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

            <!-- Robot Card -->
            <div class="robot-main-card glass">

                <!-- 🤖 رأس روبوت 3D جديد بالكامل -->
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
                            <div class="robot-antenna"></div>

                            <div class="robot-head-cube">
                                <div class="robot-ear left"></div>
                                <div class="robot-ear right"></div>

                                <div class="robot-face-3d">
                                    <span class="robot-brow left"></span>
                                    <span class="robot-brow right"></span>

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

            <!-- ✨ جديد: Quick Actions -->
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

            <!-- ✨ جديد: Stats Row -->
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

            <!-- Features Row -->
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

            <!-- Capabilities -->
            <div class="capabilities-list glass" id="capList">
                <div class="capability-item">🌐 يتحدث العربية والإنجليزية بطلاقة</div>
                <div class="capability-item">🧠 فهم الأسئلة المعقدة بدقة متناهية</div>
                <div class="capability-item">⚡ إجابات فورية وتفاعل بصوت وصورة</div>
            </div>

            <!-- Bottom Nav -->
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
                C ROBOT AI V5 – Cinematic Glass Edition
            </div>

        </div>
    </div>
</div>

<script>
    let currentLang = 'ar';

    /* ============================================================
       🎛️ محرك الصوت الروبوتي 100%
       - AudioContext لتوليد نغمات روبوتية
       - SpeechSynthesis بنبرة إنجليزية روبوتية (pitch منخفض جداً)
       - فلترة + ring modulation لمحاكاة صوت الروبوت
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

    /* نغمة روبوتية قصيرة (beep) قبل / بعد الكلام */
    function playRobotBeep(freq = 880, duration = 0.08, type = 'square', gain = 0.06) {
        const ctx = getAudioCtx();
        if (!ctx) return;
        const osc = ctx.createOscillator();
        const g = ctx.createGain();
        osc.type = type;
        osc.frequency.setValueAtTime(freq, ctx.currentTime);
        osc.frequency.exponentialRampToValueAtTime(freq * 0.6, ctx.currentTime + duration);
        g.gain.setValueAtTime(0, ctx.currentTime);
        g.gain.linearRampToValueAtTime(gain, ctx.currentTime + 0.01);
        g.gain.exponentialRampToValueAtTime(0.0001, ctx.currentTime + duration);
        osc.connect(g).connect(ctx.destination);
        osc.start();
        osc.stop(ctx.currentTime + duration + 0.02);
    }

    /* سلسلة نغمات "تشغيل/معالجة" روبوتية */
    function playRobotProcessing() {
        playRobotBeep(1200, 0.05, 'square', 0.05);
        setTimeout(() => playRobotBeep(900, 0.05, 'square', 0.05), 70);
        setTimeout(() => playRobotBeep(1400, 0.06, 'sawtooth', 0.045), 140);
    }

    /* ============================================================
       🗣️ محرك الكلام الروبوتي (إنجليزي 100% بنبرة روبوتية)
    ============================================================ */
    function pickRoboticEnglishVoice() {
        if (!('speechSynthesis' in window)) return null;
        const voices = window.speechSynthesis.getVoices();
        if (!voices || !voices.length) return null;

        // نبحث عن أفضل صوت إنجليزي روبوتي / ذكوري منخفض
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
        const v = pickRoboticEnglishVoice();
        return v || null;
    }

    // إعادة تحميل الأصوات عند توفرها
    if ('speechSynthesis' in window) {
        window.speechSynthesis.onvoiceschanged = () => { getEnglishVoice(); };
        // بعض المتصفحات تحتاج استدعاء مسبق
        window.speechSynthesis.getVoices();
    }

    /* تشغيل صوت روبوتي إنجليزي حقيقي 100% */
    function speakRobotEnglish(text) {
        const chatBox = document.getElementById('chatBox');
        chatBox.innerHTML += `<div class="msg-b">🤖 ${text}</div>`;
        chatBox.scrollTop = chatBox.scrollHeight;

        const head  = document.getElementById('robotHead3D');
        const mouth = document.getElementById('robotMouth');

        // حركة الرأس والفم
        head.classList.add('talking-head');
        mouth.classList.add('talking');

        // نغمة تحضير روبوتية قبل الكلام
        playRobotProcessing();

        const stopAnim = () => {
            head.classList.remove('talking-head');
            mouth.classList.remove('talking');
        };

        if ('speechSynthesis' in window) {
            try { window.speechSynthesis.cancel(); } catch (e) {}

            const utter = new SpeechSynthesisUtterance(text);
            const v = getEnglishVoice();
            if (v) utter.voice = v;

            // 🇬🇧 إنجليزي 100% بنبرة روبوتية
            utter.lang  = 'en-US';
            utter.pitch = 0.05;   // منخفض جداً => نبرة روبوتية عميقة
            utter.rate  = 0.82;   // أبطأ قليلاً => إحساس آلي
            utter.volume = 1.0;

            // نغمة "بدء الإرسال" روبوتية عند بداية الكلام
            utter.onstart = () => {
                playRobotBeep(1500, 0.06, 'square', 0.05);
            };

            // نبضات روبوتية أثناء الكلام (كل 260ms)
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
            // fallback: إيقاف الحركة بعد مدة تقديرية
            setTimeout(stopAnim, Math.max(1500, text.length * 60));
        }
    }

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
            footer: "C ROBOT AI V5 – Cinematic Glass Edition",
            speechWelcome: "Hello, I am C ROBOT AI. The real talking AI robot. Systems online. Ready to assist you now."
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
            footer: "C ROBOT AI V5 – Cinematic Glass Edition",
            speechWelcome: "Hello, I am C ROBOT AI. The real talking AI robot. Systems online. Ready to assist you now."
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

        const capItems = document.querySelectorAll('.capability-item');
        capItems.forEach((item, idx) => { item.innerText = t.caps[idx]; });

        for (let i = 1; i <= 6; i++) {
            document.getElementById('nav' + i).innerText = t.navs[i - 1];
        }
        document.getElementById('footerText').innerText = t.footer;

        speak(t.speechWelcome);
    }

    /* المحرك الرئيسي للكلام – يستخدم الصوت الروبوتي الإنجليزي */
    function speak(text) {
        speakRobotEnglish(text);
    }

    function triggerTalk() {
        const msg = "I am listening to you now. Please, ask your question.";
        speak(msg);
    }

    // ✨ جديد: إجراءات سريعة
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

    // ✨ تأثير تحديث الأرقام في الإحصائيات
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

    /* ============================================================
       🤖 تحسينات إضافية لرأس الروبوت 3D
       - حركة رأس عشوائية خفيفة حتى بدون كلام
       - تفاعل العينين مع المؤشر / اللمس
    ============================================================ */
    (function robotHeadEnhancements() {
        const head = document.getElementById('robotHead3D');
        if (!head) return;

        // نبضة رأس عشوائية كل فترة لإحياء الروبوت
        setInterval(() => {
            if (head.classList.contains('talking-head')) return;
            const rx = (Math.random() * 6 - 3).toFixed(2);
            const ry = (Math.random() * 16 - 8).toFixed(2);
            head.style.transition = 'transform 1.2s ease-in-out';
            head.style.transform = `rotateY(${ry}deg) rotateX(${rx}deg)`;
            setTimeout(() => {
                head.style.transform = '';
            }, 1200);
        }, 5500);

        // تفاعل العينين مع حركة المؤشر (تتبع بسيط)
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

    /* تسخين محرك الصوت عند أول تفاعل من المستخدم */
    document.addEventListener('click', () => { getAudioCtx(); }, { once: true });
    document.addEventListener('touchstart', () => { getAudioCtx(); }, { once: true });
</script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', PORT))
    app.run(host='0.0.0.0', port=port, debug=True)
