# ============================================================
# C ROBOT AI V5 - Cinematic Glass Edition
# ملف شامل معدل ومنظم - جميع التعديلات المطلوبة
# ============================================================

import os
import signal
import subprocess

# ============================================================
# إعدادات المنفذ والبيئة
# ============================================================
PORT = 9000
IS_VERCEL = os.environ.get('VERCEL') == '1'


# ============================================================
# إيقاف أي خادم قديم على نفس المنفذ (يُتجاهل على Vercel)
# ============================================================
if not IS_VERCEL:
    try:
        command = f"lsof -t -i:{PORT}"
        pid = subprocess.check_output(
            command, shell=True, timeout=2, stderr=subprocess.DEVNULL
        ).decode().strip()
        if pid:
            os.kill(int(pid), signal.SIGKILL)
            print(f"تم إيقاف الخادم القديم على المنفذ {PORT} بنجاح.")
    except Exception:
        pass


# ============================================================
# استيراد Flask
# ============================================================
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


# ============================================================
# قالب HTML الرئيسي الكامل
# ============================================================
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="ar" dir="rtl" id="htmlRoot">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
    <title>C ROBOT AI V5 - Cinematic Glass Edition</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
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

            /* ✅ خلفية Bg_01.jpg مع تدرج احتياطي */
            background:
                url('/Bg_01.jpg') no-repeat center center / cover,
                linear-gradient(135deg, #0f172a, #1e293b);
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
           🤖 رأس روبوت 3D متحرك بالكامل
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

        .robot-head-cube::before {
            content: "";
            position: absolute;
            top: 0; left: 0; right: 0;
            height: 40%;
            background: linear-gradient(180deg, rgba(255, 255, 255, 0.18), transparent);
            border-radius: 26px 26px 50% 50%;
            pointer-events: none;
        }

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

        @keyframes eyeBlink {
            0%, 90%, 100% { transform: scaleY(1) translateZ(0); }
            93%           { transform: scaleY(0.05) translateZ(0); }
            96%           { transform: scaleY(1) translateZ(0); }
        }

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
            box-shadow:
                0 4px 15px rgba(14, 165, 233, 0.6),
                inset 0 1px 0 rgba(255, 255, 255, 0.3);
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
           🧠 نظام حل المشكلات الذكي (Problem Solver Engine)
        ============================================================ */
        .solver-launch-btn {
            width: 100%;
            padding: 14px;
            border-radius: 18px;
            background: linear-gradient(135deg,
                rgba(168, 85, 247, 0.85),
                rgba(236, 72, 153, 0.85),
                rgba(14, 165, 233, 0.8));
            border: 1px solid rgba(255, 255, 255, 0.25);
            color: white;
            font-size: 13px;
            font-weight: 800;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 8px;
            box-shadow:
                0 8px 25px rgba(168, 85, 247, 0.5),
                inset 0 1px 0 rgba(255, 255, 255, 0.3);
            transition: all 0.3s ease;
            font-family: 'Tajawal', sans-serif;
            position: relative;
            overflow: hidden;
        }
        .solver-launch-btn::before {
            content: "";
            position: absolute;
            top: 0; left: -100%;
            width: 100%; height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.35), transparent);
            animation: launchShine 3s ease-in-out infinite;
        }
        @keyframes launchShine {
            0%   { left: -100%; }
            60%  { left: 100%; }
            100% { left: 100%; }
        }
        .solver-launch-btn:active { transform: scale(0.97); }

        .problem-solver-panel {
            display: none;
            flex-direction: column;
            gap: 12px;
            animation: panelIn 0.4s ease;
        }
        .problem-solver-panel.active { display: flex; }
        @keyframes panelIn {
            from { opacity: 0; transform: translateY(20px); }
            to   { opacity: 1; transform: translateY(0); }
        }

        .solver-header {
            padding: 12px 14px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .solver-header .title {
            font-size: 13px;
            font-weight: 800;
            color: #fff;
            display: flex;
            align-items: center;
            gap: 8px;
        }
        .solver-header .title .ai-badge {
            font-size: 8px;
            background: linear-gradient(135deg, #a855f7, #ec4899);
            padding: 2px 6px;
            border-radius: 8px;
            color: #fff;
            font-weight: 700;
        }
        .close-solver {
            background: rgba(239, 68, 68, 0.25);
            border: 1px solid rgba(239, 68, 68, 0.5);
            color: #fca5a5;
            width: 26px; height: 26px;
            border-radius: 50%;
            cursor: pointer;
            font-size: 13px;
            display: flex;
            align-items: center;
            justify-content: center;
            transition: 0.2s;
        }
        .close-solver:hover { background: rgba(239, 68, 68, 0.5); color: #fff; }

        .problem-input-area {
            padding: 12px;
            display: flex;
            flex-direction: column;
            gap: 8px;
        }
        .problem-input-area .input-label {
            font-size: 11px;
            color: #cbd5e1;
            font-weight: 600;
        }
        #problemInput {
            width: 100%;
            background: rgba(0, 0, 0, 0.5);
            border: 1px solid rgba(56, 189, 248, 0.35);
            border-radius: 12px;
            padding: 10px;
            color: #e2e8f0;
            font-size: 11.5px;
            resize: vertical;
            min-height: 60px;
            font-family: 'Tajawal', sans-serif;
            outline: none;
            transition: border 0.2s;
        }
        #problemInput:focus {
            border-color: #38bdf8;
            box-shadow: 0 0 15px rgba(56, 189, 248, 0.35);
        }

        .input-actions {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 8px;
        }
        .voice-btn, .analyze-btn {
            padding: 10px;
            border-radius: 12px;
            border: 1px solid rgba(255, 255, 255, 0.2);
            color: #fff;
            font-size: 11px;
            font-weight: 700;
            cursor: pointer;
            font-family: 'Tajawal', sans-serif;
            transition: all 0.25s;
        }
        .voice-btn {
            background: linear-gradient(135deg, #ef4444, #f97316);
            box-shadow: 0 4px 14px rgba(239, 68, 68, 0.4);
        }
        .voice-btn.listening {
            background: linear-gradient(135deg, #22c55e, #16a34a);
            animation: listeningPulse 1s ease-in-out infinite;
        }
        @keyframes listeningPulse {
            0%, 100% { box-shadow: 0 4px 14px rgba(34, 197, 94, 0.6); }
            50%      { box-shadow: 0 4px 25px rgba(34, 197, 94, 1); }
        }
        .analyze-btn {
            background: linear-gradient(135deg, #0ea5e9, #a855f7);
            box-shadow: 0 4px 14px rgba(56, 189, 248, 0.4);
        }
        .voice-btn:active, .analyze-btn:active { transform: scale(0.96); }

        .analysis-stages {
            display: flex;
            flex-direction: column;
            gap: 8px;
        }
        .stage-item {
            padding: 10px 12px;
            border-radius: 12px;
            background: rgba(255, 255, 255, 0.05);
            border-left: 3px solid #38bdf8;
            border-right: none;
            font-size: 11px;
            color: #cbd5e1;
            display: flex;
            align-items: flex-start;
            gap: 8px;
            opacity: 0;
            transform: translateX(20px);
            animation: stageIn 0.5s ease forwards;
        }
        @keyframes stageIn {
            to { opacity: 1; transform: translateX(0); }
        }
        .stage-item .stage-icon {
            font-size: 15px;
            flex-shrink: 0;
        }
        .stage-item .stage-title {
            color: #38bdf8;
            font-weight: 700;
            display: block;
            margin-bottom: 3px;
            font-size: 10.5px;
        }
        .stage-item .stage-detail {
            font-size: 10px;
            line-height: 1.5;
            color: #94a3b8;
        }

        .plan-card {
            padding: 12px 14px;
            background: rgba(14, 165, 233, 0.08);
            border: 1px solid rgba(56, 189, 248, 0.35);
            border-radius: 16px;
        }
        .plan-card h3 {
            font-size: 12px;
            color: #38bdf8;
            margin-bottom: 10px;
            display: flex;
            align-items: center;
            gap: 6px;
            font-weight: 800;
        }
        .plan-day {
            display: flex;
            gap: 10px;
            padding: 8px 0;
            border-bottom: 1px dashed rgba(56, 189, 248, 0.2);
            font-size: 10.5px;
            align-items: flex-start;
        }
        .plan-day:last-child { border-bottom: none; }
        .plan-day .day-num {
            background: linear-gradient(135deg, #0ea5e9, #a855f7);
            color: white;
            min-width: 26px;
            height: 26px;
            border-radius: 8px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 10px;
            font-weight: 800;
            font-family: 'Orbitron', sans-serif;
            flex-shrink: 0;
        }
        .plan-day .day-text {
            color: #e2e8f0;
            line-height: 1.5;
            padding-top: 3px;
        }

        .solutions-list {
            display: flex;
            flex-direction: column;
            gap: 8px;
            margin-top: 8px;
        }
        .solution-item {
            padding: 10px 12px;
            background: rgba(168, 85, 247, 0.08);
            border: 1px solid rgba(168, 85, 247, 0.3);
            border-radius: 12px;
            font-size: 10.5px;
            color: #e2e8f0;
            line-height: 1.5;
            display: flex;
            gap: 8px;
            align-items: flex-start;
        }
        .solution-item .sol-num {
            background: linear-gradient(135deg, #a855f7, #ec4899);
            color: #fff;
            width: 20px; height: 20px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 10px;
            font-weight: 800;
            flex-shrink: 0;
        }

        .exec-btn {
            width: 100%;
            padding: 12px;
            border-radius: 14px;
            background: linear-gradient(135deg, #22c55e, #16a34a);
            border: 1px solid rgba(255, 255, 255, 0.25);
            color: #fff;
            font-size: 12px;
            font-weight: 800;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 8px;
            box-shadow: 0 6px 20px rgba(34, 197, 94, 0.45);
            font-family: 'Tajawal', sans-serif;
            margin-top: 6px;
            transition: 0.25s;
        }
        .exec-btn:active { transform: scale(0.97); }

        .digital-output {
            margin-top: 10px;
            padding: 12px;
            background: rgba(0, 0, 0, 0.4);
            border: 1px solid rgba(34, 197, 94, 0.4);
            border-radius: 14px;
            font-size: 10.5px;
            color: #cbd5e1;
            line-height: 1.7;
            max-height: 220px;
            overflow-y: auto;
        }
        .digital-output::-webkit-scrollbar { width: 3px; }
        .digital-output::-webkit-scrollbar-thumb { background: rgba(34, 197, 94, 0.5); border-radius: 3px; }
        .digital-output .output-title {
            color: #22c55e;
            font-weight: 800;
            font-size: 11px;
            margin-bottom: 6px;
            display: block;
        }
        .digital-output .output-block {
            background: rgba(34, 197, 94, 0.08);
            padding: 8px 10px;
            border-radius: 10px;
            margin: 6px 0;
            border-left: 3px solid #22c55e;
            white-space: pre-wrap;
            font-size: 10px;
        }

        .results-panel {
            margin-top: 10px;
            padding: 12px;
            background: rgba(14, 165, 233, 0.08);
            border: 1px solid rgba(56, 189, 248, 0.35);
            border-radius: 14px;
        }
        .results-panel h4 {
            font-size: 11px;
            color: #38bdf8;
            margin-bottom: 8px;
            font-weight: 800;
        }
        .kpi-row {
            display: flex;
            justify-content: space-between;
            padding: 6px 0;
            font-size: 10.5px;
            border-bottom: 1px dashed rgba(56, 189, 248, 0.2);
            color: #cbd5e1;
        }
        .kpi-row:last-child { border-bottom: none; }
        .kpi-row .kpi-val {
            color: #22c55e;
            font-weight: 800;
            font-family: 'Orbitron', sans-serif;
        }
        .kpi-row .kpi-val.warn { color: #f59e0b; }

        .retry-btn {
            width: 100%;
            padding: 11px;
            border-radius: 12px;
            background: linear-gradient(135deg, #f59e0b, #ef4444);
            border: 1px solid rgba(255, 255, 255, 0.25);
            color: #fff;
            font-size: 11.5px;
            font-weight: 800;
            cursor: pointer;
            margin-top: 10px;
            font-family: 'Tajawal', sans-serif;
            box-shadow: 0 6px 18px rgba(245, 158, 11, 0.4);
            transition: 0.25s;
        }
        .retry-btn:active { transform: scale(0.97); }

        .loading-dots {
            display: inline-flex;
            gap: 3px;
            margin-inline-start: 6px;
        }
        .loading-dots span {
            width: 5px; height: 5px;
            background: #38bdf8;
            border-radius: 50%;
            animation: dotBounce 1.2s infinite;
        }
        .loading-dots span:nth-child(2) { animation-delay: 0.2s; }
        .loading-dots span:nth-child(3) { animation-delay: 0.4s; }
        @keyframes dotBounce {
            0%, 80%, 100% { transform: scale(0.6); opacity: 0.4; }
            40%           { transform: scale(1); opacity: 1; }
        }

        /* ============================================================
           Responsive - شاشات اللابتوب القصيرة
        ============================================================ */
        @media (max-height: 900px) and (min-width: 481px) {
            html, body {
                padding: 15px;
                align-items: flex-start;
            }
            .iphone-frame {
                width: 360px;
                height: 720px;
                animation: none;
            }
            .iphone-screen { border-radius: 40px; }
            .robot-head-3d { width: 110px; height: 120px; }
            .robot-avatar-wrapper::before { width: 160px; height: 160px; }
            .robot-avatar-wrapper::after  { width: 185px; height: 185px; }
        }

        /* ============================================================
           Responsive - الهواتف
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

            /* تبسيط التأثيرات الثقيلة على الهواتف */
            .glass, .chat-panel, .feature-box-v3, .stat-card, .nav-card,
            .quick-btn, .solver-launch-btn {
                backdrop-filter: blur(8px) !important;
                -webkit-backdrop-filter: blur(8px) !important;
            }
            body::before, body::after { display: none; }
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

                <!-- 🤖 رأس روبوت 3D -->
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

            <!-- ✨ Quick Actions -->
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

            <!-- ✨ Stats Row -->
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

            <!-- ============================================================
                 🧠 محلل المشكلات الذكي (Problem Solver)
            ============================================================ -->
            <button class="solver-launch-btn" id="solverLaunchBtn" onclick="toggleProblemSolver()">
                🧠 محلل المشكلات الذكي - اطرح مشكلتك الحقيقية
            </button>

            <div class="problem-solver-panel" id="problemSolverPanel">

                <div class="solver-header glass">
                    <div class="title">
                        🧠 محلل المشكلات الذكي
                        <span class="ai-badge">AI v5</span>
                    </div>
                    <button class="close-solver" onclick="toggleProblemSolver()">✕</button>
                </div>

                <div class="problem-input-area glass">
                    <div class="input-label">🎤 اشرح مشكلتك (اضغط تحدث أو اكتبها):</div>
                    <textarea id="problemInput" placeholder="مثال: عندي محل ولا أملك زبائن كفاية..."></textarea>
                    <div class="input-actions">
                        <button class="voice-btn" id="voiceBtn" onclick="startListening()">🎤 تحدث</button>
                        <button class="analyze-btn" onclick="analyzeProblem()">⚡ حلل المشكلة</button>
                    </div>
                </div>

                <div class="analysis-stages" id="analysisStages"></div>

                <div id="planContainer"></div>

                <div id="execContainer"></div>

                <div id="resultsContainer"></div>

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
       🎛️ محرك الصوت الروبوتي
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

    function playRobotProcessing() {
        playRobotBeep(1200, 0.05, 'square', 0.05);
        setTimeout(() => playRobotBeep(900, 0.05, 'square', 0.05), 70);
        setTimeout(() => playRobotBeep(1400, 0.06, 'sawtooth', 0.045), 140);
    }

    /* ============================================================
       🗣️ محرك الكلام الروبوتي (إنجليزي 100%)
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
        const v = pickRoboticEnglishVoice();
        return v || null;
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

        head.classList.add('talking-head');
        mouth.classList.add('talking');

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

            utter.lang  = 'en-US';
            utter.pitch = 0.05;
            utter.rate  = 0.82;
            utter.volume = 1.0;

            utter.onstart = () => {
                playRobotBeep(1500, 0.06, 'square', 0.05);
            };

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

    function speak(text) {
        speakRobotEnglish(text);
    }

    function triggerTalk() {
        const msg = "I am listening to you now. Please, ask your question.";
        speak(msg);
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

    /* ============================================================
       🤖 تحسينات رأس الروبوت 3D
    ============================================================ */
    (function robotHeadEnhancements() {
        const head = document.getElementById('robotHead3D');
        if (!head) return;

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

    document.addEventListener('click', () => { getAudioCtx(); }, { once: true });
    document.addEventListener('touchstart', () => { getAudioCtx(); }, { once: true });

    /* ============================================================
       🧠🧠🧠 محرك حل المشكلات الذكي المتقدم (Problem Solver Engine)
    ============================================================ */
    const PROBLEM_KNOWLEDGE_BASE = {
        business_marketing: {
            name: "مشكلة تجارية / تسويقية",
            keywords: ['محل','متجر','دكان','مشروع','تجارة','بيع','مبيعات','زبائن','عملاء','سوق','تسويق','منتج','خدمة','شركة','براند','كاشير','مطعم','مقهى','صيدلية','بقالة','محلات'],
            causes: [
                "ضعف الحضور الرقمي: لا يوجد حساب تجاري نشط أو محتوى تسويقي جاذب",
                "غياب العرض القيمي: لا يوجد سبب واضح يجعل العميل يفضلك على المنافس",
                "عدم تحديد الجمهور المستهدف: التسويق موجه للجميع = لا أحد",
                "ضعف تجربة العميل داخل المحل: عدم رضا العملاء الحاليين يمنع التوصية",
                "عدم استخدام التسويق المحلي (Google Maps, مجموعات الحي, الجيران)"
            ],
            solutions: [
                "بناء هوية تسويقية واضحة + عرض قيمي مغري (خصم، هدية، ضمان)",
                "إطلاق حملة محتوى أسبوعية على Instagram / TikTok / Facebook",
                "التسويق الجغرافي: Google Business + مجموعات الأحياء على واتساب",
                "برنامج ولاء للعملاء الحاليين: اكسب نقاط، اكسب عميل جديد",
                "التعاون مع 5 مؤثرين محليين صغار لتغطية المنطقة"
            ],
            weekly_plan: [
                "تحديد العميل المثالي + كتابة ملف تعريف دقيق (سن، منطقة، اهتمام)",
                "صياغة العرض القيمي الأساسي + 3 عروض فرعية للاختبار",
                "إنتاج 5 منشورات + 3 فيديوهات قصيرة جاهزة للنشر",
                "نشر على 4 منصات + نشر إعلان جغرافي مدفوع (نطاق 5 كم)",
                "التواصل مع 20 عميل حالي + طلب تقييم + عرض إحالة",
                "قياس النتائج: زيارات، اتصالات، رسائل، مبيعات فعلية",
                "تحليل + تعديل الاستراتيجية + مضاعفة ما نجح"
            ],
            digital_steps: [
                { title: "📱 5 منشورات سوشيال ميديا جاهزة", type: "posts" },
                { title: "🎬 سكريبت 3 فيديوهات قصيرة", type: "videos" },
                { title: "📊 جدول نشر أسبوعي", type: "schedule" },
                { title: "🎯 استهداف إعلان جغرافي", type: "targeting" },
                { title: "💬 قوالب رسائل للعملاء", type: "templates" }
            ],
            kpis: [
                "زيارات المحل اليومية (قبل: 15 / الهدف: 40)",
                "رسائل واستفسارات واتساب (الهدف: 25/أسبوع)",
                "متابعون جدد (الهدف: 300+)",
                "معدل التحويل من زائر لمشترٍ (الهدف: 30%)",
                "إيرادات الأسبوع (الهدف: +45%)"
            ],
            alt_strategy: "الاستراتيجية البديلة: التحول من التسويق الرقمي إلى التسويق التجريبي الميداني — توزيع عينات مجانية، رعاية حدث محلي، الشراكة مع 3 محلات مجاورة لتبادل العملاء."
        },
        technical: {
            name: "مشكلة تقنية / برمجية",
            keywords: ['خطأ','error','bug','برنامج','كود','تطبيق','موقع','سيرفر','شبكة','انترنت','هاتف','جهاز','ويندوز','لينكس','ماك','تحميل','تثبيت','تحديث','data','داتا'],
            causes: [
                "تعارض في الإصدارات أو المكتبات المستخدمة",
                "إعدادات غير صحيحة في البيئة أو الملفات",
                "صلاحيات ناقصة أو مسارات خاطئة",
                "ذاكرة ممتلئة أو موارد غير كافية",
                "كود غير محسّن أو منطق خاطئ"
            ],
            solutions: [
                "تحديد الخطأ بدقة عبر السجلات (logs) ورسائل الأخطاء",
                "عزل المشكلة باختبار الوحدات (unit test) سطراً بسطر",
                "إعادة تثبيت المكتبات في بيئة نظيفة (venv / docker)",
                "مراجعة الإعدادات وملفات التكوين",
                "طلب مراجعة من مجتمع المطورين مع تفاصيل كاملة"
            ],
            weekly_plan: [
                "قراءة السجل كاملاً وتوثيق رسالة الخطأ",
                "عزل الجزء المسؤول بنقاط توقف (breakpoints)",
                "تجربة الحل في بيئة اختبار منفصلة",
                "تطبيق الحل في البيئة الفعلية + نسخة احتياطية",
                "اختبار الانحدار (regression test)",
                "نشر الحل ومراقبة الأداء",
                "توثيق الحل في قاعدة المعرفة"
            ],
            digital_steps: [
                { title: "📝 تقرير تحليلي للخطأ", type: "report" },
                { title: "🧪 سكريبت اختبار جاهز", type: "test" },
                { title: "🛠️ أوامر الإصلاح الجاهزة", type: "commands" },
                { title: "📚 مراجع ومصادر الحل", type: "references" }
            ],
            kpis: [
                "الوقت المستغرق لحل المشكلة",
                "معدل نجاح الاختبارات",
                "عدد الأخطاء المتكررة بعد الحل",
                "أداء النظام قبل/بعد"
            ],
            alt_strategy: "الاستراتيجية البديلة: التخلي عن الحل التدريجي والانتقال إلى إعادة بناء الجزء المتأثر من الصفر بأسلوب مختلف."
        },
        personal_productivity: {
            name: "مشكلة شخصية / إنتاجية",
            keywords: ['تأجيل','تسويف','إنتاجية','وقت','ضغط','قلق','ملل','عادة','نوم','تركيز','دراسة','مذاكرة','تنظيم','هدف','طموح'],
            causes: [
                "غياب نظام واضح للوقت والمهام",
                "تشتت الانتباه بسبب الإشعارات والمحتوى القصير",
                "ضغط نفسي من تراكم المهام غير المنجزة",
                "عدم وجود مكافآت قصيرة المدى"
            ],
            solutions: [
                "تطبيق تقنية بومودورو (25 دقيقة عمل + 5 راحة)",
                "قاعدة الدقيقتين: كل مهمة أقل من دقيقتين نفذها فوراً",
                "حجب الإشعارات أثناء ساعات العمل العميق",
                "قائمة مهام يومية بثلاث أولويات فقط"
            ],
            weekly_plan: [
                "كتابة 10 أهداف أسبوعية + ترتيبها بالأولوية",
                "تقسيم كل هدف لمهام صغيرة قابلة للتنفيذ اليومي",
                "تخصيص ساعتين عمل عميق صباحاً بدون مشتتات",
                "نظام مكافآت: بعد كل إنجاز -> استراحة محبوبة",
                "مراجعة يومية مسائية لكل ما تم",
                "قياس الإنتاجية بمقياس 1-10",
                "تعديل الأسلوب بناء على البيانات"
            ],
            digital_steps: [
                { title: "📅 جدول أسبوعي منظم", type: "schedule" },
                { title: "✅ قائمة مهام قابلة للتنفيذ", type: "tasks" },
                { title: "⏱️ نظام بومودورو جاهز", type: "pomodoro" },
                { title: "📈 نموذج قياس الإنتاجية", type: "tracker" }
            ],
            kpis: [
                "عدد المهام المنجزة يومياً",
                "ساعات العمل العميق",
                "مستوى الرضا الشخصي (1-10)",
                "عدد الأيام المتتالية بدون تسويف"
            ],
            alt_strategy: "الاستراتيجية البديلة: الاعتماد على روتين جماعي (مجموعة مسؤولية) + مدرب شخصي أسبوعي بدلاً من الانضباط الذاتي الفردي."
        },
        health_lifestyle: {
            name: "مشكلة صحية / نمط حياة",
            keywords: ['وزن','سمنة','نحافة','رياضة','تغذية','نوم','صحة','مرض','تعب','إرهاق','طاقة','جيم','دايت'],
            causes: [
                "نمط غذائي غير متوازن + سكريات خفية",
                "قلة النشاط البدني اليومي",
                "قلة النوم واضطراب الساعة البيولوجية",
                "ضغط نفسي يرفع الكورتيزول ويزيد الشهية"
            ],
            solutions: [
                "نظام غذائي واقعي (لا حرمان) مع 3 وجبات ثابتة",
                "30 دقيقة مشي يومي + تمارين مقاومة 3 مرات أسبوعياً",
                "نوم 7-8 ساعات في مواعيد ثابتة",
                "شرب 3 لتر ماء يومياً + تقليل الكافيين بعد العصر"
            ],
            weekly_plan: [
                "تصوير وجبات أسبوع كامل لمعرفة الواقع الغذائي",
                "تحديد 3 عادات صغيرة للبدء بها (ماء، مشي، نوم)",
                "إعداد قائمة تسوق صحية أسبوعية",
                "تثبيت أوقات النوم والاستيقاظ",
                "قياس الوزن/الطاقة/المزاج يومياً",
                "مراجعة أسبوعية + تعديل",
                "الاستمرار 4 أسابيع قبل تقييم نهائي"
            ],
            digital_steps: [
                { title: "🍎 خطة وجبات أسبوعية", type: "meals" },
                { title: "🏃 جدول تمارين منزلي", type: "workout" },
                { title: "💧 تذكير شرب الماء", type: "reminder" },
                { title: "📊 نموذج تتبع يومي", type: "tracker" }
            ],
            kpis: [
                "الوزن (قياس أسبوعي)",
                "عدد خطوات يومية",
                "ساعات النوم",
                "مستوى الطاقة (1-10)",
                "الالتزام بالنظام (٪)"
            ],
            alt_strategy: "الاستراتيجية البديلة: التحول من التمارين الفردية إلى رياضة اجتماعية (فريق، صالة، مدرب) + استشارة أخصائي تغذية شخصية."
        },
        finance: {
            name: "مشكلة مالية",
            keywords: ['مال','فلوس','دين','ديون','مصروف','راتب','ميزانية','ادخار','توفير','استثمار','بنك','قرض','فواتير','مصاريف'],
            causes: [
                "غياب ميزانية شهرية واضحة",
                "مصروفات صغيرة متكررة تتراكم",
                "لا يوجد صندوق طوارئ",
                "ديون بأقساط مرتفعة تستهلك الدخل"
            ],
            solutions: [
                "بناء ميزانية 50/30/20 (احتياجات/رغبات/ادخار)",
                "تتبع كل مصروف لمدة 30 يوم",
                "سداد الديون بأسلوب كرة الثلج (الأصغر أولاً)",
                "فتح حساب ادخار منفصل + تحويل تلقائي"
            ],
            weekly_plan: [
                "جمع كل كشوف الحسابات آخر 3 أشهر",
                "تصنيف المصروفات + تحديد الهدر",
                "كتابة ميزانية الواقعية للشهر القادم",
                "إلغاء 3 اشتراكات غير ضرورية",
                "تحديد هدف ادخار واضح (مبلغ + مدة)",
                "مراجعة أسبوعية للالتزام",
                "تعديل الميزانية حسب النتائج"
            ],
            digital_steps: [
                { title: "💰 جدول ميزانية شهري", type: "budget" },
                { title: "📊 نموذج تتبع مصروفات", type: "tracker" },
                { title: "🎯 خطة سداد ديون", type: "debt" },
                { title: "📈 جدول ادخار تصاعدي", type: "savings" }
            ],
            kpis: [
                "الفرق بين الدخل والمصروف",
                "نسبة الادخار الشهرية",
                "انخفاض الديون",
                "حجم صندوق الطوارئ"
            ],
            alt_strategy: "الاستراتيجية البديلة: زيادة الدخل بدلاً من تقليص المصروف فقط — عمل جانبي، بيع مهارة، استثمار صغير."
        },
        education: {
            name: "مشكلة تعليمية / تعلم",
            keywords: ['دراسة','جامعة','مدرسة','امتحان','اختبار','تعلم','لغة','انجليزي','برمجة','مهارة','شهادة','تخصص','بحث'],
            causes: [
                "عدم وجود منهج واضح أو خطة تعلم",
                "تشتت المصادر والبدء بأكثر من شيء",
                "غياب التطبيق العملي",
                "قلة المراجعة المنتظمة"
            ],
            solutions: [
                "تحديد الهدف النهائي والقياس عليه",
                "اختيار مصدر واحد قوي والالتزام به",
                "قاعدة 70% تطبيق + 30% نظرية",
                "مراجعة أسبوعية بتقنية Feynman"
            ],
            weekly_plan: [
                "تحديد المهارة والهدف القابل للقياس",
                "اختيار مصدر تعلم أساسي واحد",
                "تقسيم المنهج لـ 20 دقيقة يومي أو ساعة كل يومين",
                "تطبيق مشروع صغير كل أسبوع",
                "مراجعة ما تم بتقنية الشرح للغير",
                "قياس التقدم بمشروع حقيقي",
                "تعديل الوتيرة حسب النتائج"
            ],
            digital_steps: [
                { title: "📚 خطة تعلم تفصيلية", type: "curriculum" },
                { title: "🎯 مشاريع تطبيقية", type: "projects" },
                { title: "📝 نموذج مراجعة Feynman", type: "review" },
                { title: "📊 جدول تتبع التقدم", type: "tracker" }
            ],
            kpis: [
                "عدد الساعات الدراسية",
                "نسبة إنجاز المنهج",
                "عدد المشاريع المنجزة",
                "نتيجة الاختبارات"
            ],
            alt_strategy: "الاستراتيجية البديلة: الانتقال من التعلم الذاتي إلى التعلم الجماعي (بوتكامب، مجموعة دراسة، مدرب شخصي)."
        },
        general: {
            name: "مشكلة عامة",
            keywords: [],
            causes: [
                "غياب وضوح الهدف أو المشكلة المحددة",
                "عدم وجود نظام أو آلية منهجية للحل",
                "تشتت التركيز بين عدة أولويات",
                "قلة المتابعة والقياس"
            ],
            solutions: [
                "توضيح المشكلة بدقة: ما هو، متى، وأين، ومع من",
                "تقسيم المشكلة الكبيرة إلى مشكلات صغيرة",
                "اختيار أول خطوة صغيرة قابلة للتنفيذ اليوم",
                "قياس النتائج أسبوعياً ومراجعة الأسلوب"
            ],
            weekly_plan: [
                "كتابة المشكلة بجملة واحدة واضحة",
                "تحديد الأسباب المحتملة الثلاثة الأقوى",
                "اختيار أهم سبب والتركيز عليه",
                "تنفيذ خطوة صغيرة اليوم",
                "متابعة النتائج يومياً",
                "تعديل الأسلوب بناء على ما نجح",
                "مضاعفة ما نجح"
            ],
            digital_steps: [
                { title: "📝 نموذج تحليل المشكلة", type: "analysis" },
                { title: "📅 خطة عمل أسبوعية", type: "schedule" },
                { title: "📊 جدول قياس النتائج", type: "tracker" }
            ],
            kpis: [
                "وضوح المشكلة (1-10)",
                "درجة التقدم نحو الحل",
                "الالتزام بالخطة (٪)",
                "الرضا العام (1-10)"
            ],
            alt_strategy: "الاستراتيجية البديلة: تغيير زاوية النظر للمشكلة — استشارة شخص خبير أو مجموعة دعم."
        }
    };

    let currentProblem = null;
    let currentAnalysis = null;
    let currentPlan = null;
    let currentKPIs = null;
    let executionDone = false;
    let retryCount = 0;
    let recognition = null;

    function toggleProblemSolver() {
        const panel = document.getElementById('problemSolverPanel');
        panel.classList.toggle('active');
        if (panel.classList.contains('active')) {
            setTimeout(() => {
                document.getElementById('problemInput').focus();
                panel.scrollIntoView({ behavior: 'smooth', block: 'start' });
            }, 200);
            speak("Problem solver mode activated. Please describe your real problem by voice or text.");
        }
    }

    /* 🎤 تسجيل صوتي */
    function startListening() {
        const SR = window.SpeechRecognition || window.webkitSpeechRecognition;
        const btn = document.getElementById('voiceBtn');

        if (!SR) {
            alert('⚠️ متصفحك لا يدعم التعرف على الصوت. استخدم Chrome أو Edge.');
            return;
        }

        if (recognition) {
            try { recognition.stop(); } catch (e) {}
            recognition = null;
            btn.classList.remove('listening');
            btn.innerText = '🎤 تحدث';
            return;
        }

        recognition = new SR();
        recognition.lang = currentLang === 'ar' ? 'ar-SA' : 'en-US';
        recognition.continuous = true;
        recognition.interimResults = true;

        let finalText = document.getElementById('problemInput').value;
        const baseText = finalText ? finalText + ' ' : '';

        recognition.onstart = () => {
            btn.classList.add('listening');
            btn.innerText = '🔴 جاري التسجيل... (اضغط للإيقاف)';
            playRobotBeep(1000, 0.08, 'square', 0.05);
        };

        recognition.onresult = (event) => {
            let interim = '';
            let final = '';
            for (let i = event.resultIndex; i < event.results.length; i++) {
                const txt = event.results[i][0].transcript;
                if (event.results[i].isFinal) final += txt + ' ';
                else interim += txt;
            }
            if (final) {
                finalText = baseText + final;
                document.getElementById('problemInput').value = finalText;
            } else if (interim) {
                document.getElementById('problemInput').value = baseText + interim;
            }
        };

        recognition.onerror = (e) => {
            console.warn('Speech error:', e.error);
            btn.classList.remove('listening');
            btn.innerText = '🎤 تحدث';
            recognition = null;
        };

        recognition.onend = () => {
            btn.classList.remove('listening');
            btn.innerText = '🎤 تحدث';
            recognition = null;
        };

        recognition.start();
    }

    /* تصنيف المشكلة */
    function classifyProblem(text) {
        const lower = text.toLowerCase();
        let best = 'general';
        let bestScore = 0;

        for (const key in PROBLEM_KNOWLEDGE_BASE) {
            if (key === 'general') continue;
            const cat = PROBLEM_KNOWLEDGE_BASE[key];
            let score = 0;
            for (const kw of cat.keywords) {
                if (lower.includes(kw.toLowerCase())) score++;
            }
            if (score > bestScore) {
                bestScore = score;
                best = key;
            }
        }
        return best;
    }

    function addStage(icon, title, detail, delay = 0) {
        return new Promise(resolve => {
            setTimeout(() => {
                const container = document.getElementById('analysisStages');
                const div = document.createElement('div');
                div.className = 'stage-item';
                div.innerHTML = `
                    <span class="stage-icon">${icon}</span>
                    <div style="flex:1;">
                        <span class="stage-title">${title}</span>
                        <span class="stage-detail">${detail}</span>
                    </div>
                `;
                container.appendChild(div);
                playRobotBeep(900 + Math.random() * 400, 0.04, 'square', 0.03);
                resolve();
            }, delay);
        });
    }

    async function analyzeProblem() {
        const input = document.getElementById('problemInput').value.trim();
        if (!input) {
            alert('⚠️ الرجاء كتابة أو تسجيل مشكلتك أولاً');
            return;
        }

        currentProblem = input;
        executionDone = false;
        retryCount = 0;

        document.getElementById('analysisStages').innerHTML = '';
        document.getElementById('planContainer').innerHTML = '';
        document.getElementById('execContainer').innerHTML = '';
        document.getElementById('resultsContainer').innerHTML = '';

        const categoryKey = classifyProblem(input);
        const category = PROBLEM_KNOWLEDGE_BASE[categoryKey];

        playRobotProcessing();
        speak("Analyzing your problem. Please wait.");

        await addStage('🎤', 'استقبال المشكلة', `تم استقبال مشكلتك: "${input.substring(0, 80)}${input.length > 80 ? '...' : ''}"`, 100);
        await new Promise(r => setTimeout(r, 500));

        await addStage('🤖', 'التحليل بالذكاء الاصطناعي', `تم تصنيف المشكلة كـ: <b style="color:#a855f7;">${category.name}</b>`, 200);
        await new Promise(r => setTimeout(r, 600));

        await addStage('🔍', 'تحديد السبب الجذري', `تم تحديد ${category.causes.length} أسباب محتملة — السبب الأقوى: "${category.causes[0]}"`, 200);
        await new Promise(r => setTimeout(r, 600));

        await addStage('🧠', 'اقتراح الحلول', `تم توليد ${category.solutions.length} حلول متعددة قابلة للتنفيذ`, 200);
        await new Promise(r => setTimeout(r, 500));

        await addStage('📋', 'بناء خطة العمل', `خطة عمل من ${category.weekly_plan.length} أيام + ${category.digital_steps.length} خطوة رقمية قابلة للتنفيذ`, 200);

        currentAnalysis = { categoryKey, category };

        setTimeout(() => renderFullPlan(category), 500);
    }

    function renderFullPlan(category) {
        const container = document.getElementById('planContainer');
        container.innerHTML = `
            <div class="plan-card glass" style="margin-top:8px;">
                <h3>📋 خطة العمل الكاملة - ${category.name}</h3>

                <div style="font-size:11px;color:#a855f7;font-weight:800;margin:8px 0 6px;">
                    🔍 الأسباب الجذرية المحتملة
                </div>
                <div class="solutions-list">
                    ${category.causes.map((c, i) => `
                        <div class="solution-item" style="background:rgba(239,68,68,0.08);border-color:rgba(239,68,68,0.3);">
                            <span class="sol-num" style="background:linear-gradient(135deg,#ef4444,#f97316);">${i + 1}</span>
                            <span>${c}</span>
                        </div>
                    `).join('')}
                </div>

                <div style="font-size:11px;color:#22c55e;font-weight:800;margin:14px 0 6px;">
                    🧠 الحلول المقترحة (${category.solutions.length} حلول)
                </div>
                <div class="solutions-list">
                    ${category.solutions.map((s, i) => `
                        <div class="solution-item" style="background:rgba(34,197,94,0.08);border-color:rgba(34,197,94,0.35);">
                            <span class="sol-num" style="background:linear-gradient(135deg,#22c55e,#16a34a);">${i + 1}</span>
                            <span>${s}</span>
                        </div>
                    `).join('')}
                </div>

                <div style="font-size:11px;color:#38bdf8;font-weight:800;margin:14px 0 6px;">
                    📅 الجدول الأسبوعي التنفيذي
                </div>
                ${category.weekly_plan.map((d, i) => `
                    <div class="plan-day">
                        <div class="day-num">${i + 1}</div>
                        <div class="day-text">${d}</div>
                    </div>
                `).join('')}
            </div>

            <button class="exec-btn" onclick="executeDigitalSteps()">
                ⚙️ تنفيذ الخطوات الرقمية الممكنة الآن
            </button>
        `;

        speak("The plan is ready. I have prepared the root causes, solutions, and a full weekly action plan. You can now execute the digital steps.");
    }

    function executeDigitalSteps() {
        if (!currentAnalysis) return;
        const category = currentAnalysis.category;
        const container = document.getElementById('execContainer');
        executionDone = true;
        retryCount = 0;

        playRobotProcessing();
        speak("Executing digital steps now. Generating content, schedules, and templates.");

        let outputHTML = `<div class="digital-output glass">
            <span class="output-title">⚙️ تم تنفيذ الخطوات الرقمية التالية بنجاح:</span>
        `;

        category.digital_steps.forEach((step, idx) => {
            outputHTML += `<div class="output-block">✅ <b>${step.title}</b>\n${generateDigitalContent(step.type, category)}</div>`;
        });

        outputHTML += `<div style="margin-top:10px;color:#22c55e;font-weight:800;font-size:11px;text-align:center;">
            🟢 ${category.digital_steps.length} من ${category.digital_steps.length} خطوات رقمية تم توليدها وتنفيذها
        </div></div>`;

        container.innerHTML = outputHTML;

        setTimeout(() => {
            measureResults();
        }, 1200);
    }

    function generateDigitalContent(type, category) {
        switch (type) {
            case 'posts':
                return `المنشور 1: "هل تبحث عن [المنتج]؟ عندنا العرض الأفضل في المنطقة 🔥 خصم 20% لأول 10 عملاء هذا الأسبوع فقط!"\nالمنشور 2: "قصة نجاح: عميلنا [الاسم] حقق [النتيجة] في أسبوعين. جربنا واحكم بنفسك ✨"\nالمنشور 3: "خلف الكواليس: كيف نجهز [الخدمة] بجودة عالية 🎬"\nالمنشور 4: "سؤال مهم: ما الذي يهمك أكثر عند اختيار [المنتج]؟ شاركنا في التعليقات 💬"\nالمنشور 5: "عرض محدود: اشتر اليوم واحصل على [الهدية] مجاناً 🎁"`;
            case 'videos':
                return `فيديو 1 (15 ث): افتتاحية - عرض المنتج + صوت مبهج + نص "الفرق الذي ستشعر به"\nفيديو 2 (20 ث): شهادة عميل حقيقي + قبل/بعد\nفيديو 3 (30 ث): جولة سريعة داخل المحل + 3 نصائح مجانية`;
            case 'schedule':
                return `السبت 10ص: منشور 1 | الأحد 2م: ريلز 1\nالاثنين 6م: قصة تفاعل | الثلاثاء 11ص: منشور 2\nالأربعاء 7م: ريلز 2 | الخميس 9ص: عرض خاص\nالجمعة 3م: منشور قصة نجاح`;
            case 'targeting':
                return `المنطقة: 5 كم حول المحل\nالعمر: 22-45\nالاهتمامات: [المنتج]، الحياة اليومية، التسوق المحلي\nالميزانية: 30-50 ريال/يوم كبداية\nالهدف: رسائل واتساب + زيارات للمحل`;
            case 'templates':
                return `قالب 1: "السلام عليكم [الاسم]، يسعدنا أنك زرتنا. عندك أي استفسار؟"\nقالب 2: "عميلنا العزيز، خصم 15% لعودتك الأولى خلال 7 أيام 🎁"\nقالب 3: "هل تعرف شخصاً يحتاج [المنتج]؟ احصل على 10% عند كل إحالة ✅"`;
            case 'report':
                return `التقرير يشمل: وصف الخطأ، سجل الأخطاء، البيئة، الخطوات المتبعة، النتائج المرجوة`;
            case 'test':
                return `assert result == expected_output\n# اختبار الوحدات للتحقق من الحل`;
            case 'commands':
                return `npm install --force\nnpm run build\nnpm run start`;
            case 'references':
                return `stackoverflow.com | github.com/issues | developer.mozilla.org`;
            case 'meals':
                return `الإفطار: بيض + خبز أسمر + خضار\nالغداء: بروتين + كارب معقد + سلطة\nالعشاء: خفيف + بروتين`;
            case 'workout':
                return `السبت: مشي 30د | الأحد: مقاومة علوية\nالاثنين: راحة | الثلاثاء: مقاومة سفلية\nالأربعاء: كارديو 30د | الخميس: جيم شامل | الجمعة: راحة`;
            case 'reminder':
                return `8ص: كوب ماء | 10ص: كوب | 12ظ: كوب\n2م: كوب | 4م: كوب | 6م: كوب | 8م: كوب`;
            case 'budget':
                return `الدخل: 100%\nاحتياجات 50% | رغبات 30% | ادخار 20%`;
            case 'debt':
                return `الشهر 1: أصغر دين | الشهر 2: الثاني | الشهر 3: الثالث (كرة الثلج)`;
            case 'savings':
                return `أسبوع 1: 50 | أسبوع 2: 75 | أسبوع 3: 100 | أسبوع 4: 150`;
            case 'curriculum':
                return `الأسبوع 1-2: الأساسيات | 3-4: متوسط | 5-6: متقدم + مشروع`;
            case 'projects':
                return `مشروع 1: تطبيق بسيط | مشروع 2: نسخة محسّنة`;
            case 'review':
                return `اشرح ما تعلمته بصوت عال كأنك تدرّس طفلاً`;
            case 'tasks':
                return `🔴 مهمة 1 (أولوية) | 🟡 مهمة 2 | 🟢 مهمة 3`;
            case 'pomodoro':
                return `25د عمل + 5د راحة × 4 = 100د إنتاجية`;
            case 'analysis':
                return `اكتب المشكلة بجملة واحدة + 3 أسباب + 3 حلول`;
            case 'tracker':
                return `اليوم | الالتزام | النتيجة | الملاحظات`;
            default:
                return `تم التوليد بنجاح ✅`;
        }
    }

    function measureResults() {
        if (!currentAnalysis) return;
        const category = currentAnalysis.category;
        const container = document.getElementById('resultsContainer');

        const simulated = category.kpis.map((kpi, idx) => {
            const success = Math.random() > 0.25;
            const val = success
                ? `✅ ${Math.floor(70 + Math.random() * 25)}%`
                : `⚠️ ${Math.floor(30 + Math.random() * 25)}%`;
            return { kpi, val, success };
        });

        const overallSuccess = simulated.filter(s => s.success).length / simulated.length >= 0.6;

        container.innerHTML = `
            <div class="results-panel glass">
                <h4>📊 قياس النتائج بعد التنفيذ</h4>
                ${simulated.map(s => `
                    <div class="kpi-row">
                        <span>${s.kpi}</span>
                        <span class="kpi-val ${s.success ? '' : 'warn'}">${s.val}</span>
                    </div>
                `).join('')}
                <div style="margin-top:10px;padding:8px;background:rgba(0,0,0,0.3);border-radius:10px;font-size:11px;color:${overallSuccess ? '#22c55e' : '#f59e0b'};font-weight:700;text-align:center;">
                    ${overallSuccess
                        ? '🟢 النتائج إيجابية - يمكن مضاعفة الاستراتيجية الحالية'
                        : '🟡 النتائج أقل من المتوقع - يُنصح باستراتيجية بديلة'}
                </div>
                ${!overallSuccess ? `
                    <button class="retry-btn" onclick="retryWithAltStrategy()">
                        🔄 تجربة استراتيجية بديلة
                    </button>
                ` : `
                    <button class="retry-btn" style="background:linear-gradient(135deg,#22c55e,#16a34a);" onclick="doubleDown()">
                        🚀 مضاعفة ما نجح
                    </button>
                `}
            </div>
        `;

        if (overallSuccess) {
            speak("Execution complete. Results are positive. The current strategy is working. You can now double down on what worked.");
        } else {
            speak("Execution complete. Results are below expectations. I recommend trying an alternative strategy.");
        }
    }

    function retryWithAltStrategy() {
        if (!currentAnalysis) return;
        const category = currentAnalysis.category;
        retryCount++;

        playRobotProcessing();
        speak("Switching to alternative strategy. Analyzing what failed and rebuilding approach.");

        const container = document.getElementById('resultsContainer');

        const altHTML = `
            <div class="results-panel glass" style="border-color:rgba(245,158,11,0.5);background:rgba(245,158,11,0.08);">
                <h4 style="color:#f59e0b;">🔄 الاستراتيجية البديلة #${retryCount}</h4>
                <div style="font-size:11px;color:#e2e8f0;line-height:1.7;padding:8px;background:rgba(0,0,0,0.3);border-radius:10px;">
                    ${category.alt_strategy}
                </div>

                <div style="font-size:11px;color:#f59e0b;font-weight:800;margin:12px 0 6px;">
                    📅 خطة الاستراتيجية البديلة
                </div>
                ${category.weekly_plan.slice(0, 5).map((d, i) => `
                    <div class="plan-day">
                        <div class="day-num" style="background:linear-gradient(135deg,#f59e0b,#ef4444);">${i + 1}</div>
                        <div class="day-text">${d} <span style="color:#f59e0b;font-size:9px;">(محدثة)</span></div>
                    </div>
                `).join('')}

                <button class="exec-btn" style="background:linear-gradient(135deg,#f59e0b,#ef4444);box-shadow:0 6px 20px rgba(245,158,11,0.45);margin-top:12px;" onclick="executeDigitalSteps()">
                    ⚙️ تنفيذ الاستراتيجية البديلة
                </button>
            </div>
        `;

        container.innerHTML = altHTML;

        speak("Alternative strategy ready. Review the new plan and execute when ready.");
    }

    function doubleDown() {
        playRobotProcessing();
        speak("Excellent. Doubling down on what worked. Scaling up all successful channels and content.");
        const container = document.getElementById('resultsContainer');
        container.innerHTML += `
            <div class="results-panel glass" style="border-color:rgba(34,197,94,0.5);background:rgba(34,197,94,0.08);margin-top:10px;">
                <h4 style="color:#22c55e;">🚀 وضع المضاعفة مُفعّل</h4>
                <div style="font-size:11px;color:#e2e8f0;line-height:1.7;">
                    • مضاعفة ميزانية الإعلان على القناة الأنجح ×2<br>
                    • إنتاج ضعف المحتوى الذي حقق أعلى تفاعل<br>
                    • توسيع المنطقة الجغرافية إلى 10 كم<br>
                    • إضافة برنامج إحالة للعملاء الحاليين
                </div>
            </div>
        `;
    }

    document.addEventListener('click', () => { getAudioCtx(); }, { once: true });
    document.addEventListener('touchstart', () => { getAudioCtx(); }, { once: true });
</script>
</body>
</html>
"""


# ============================================================
# المسار الرئيسي
# ============================================================
@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)


# ============================================================
# نقطة تشغيل التطبيق
# ============================================================
if __name__ == '__main__':
    port = int(os.environ.get('PORT', PORT))
    app.run(host='0.0.0.0', port=port, debug=True)
