from flask import Flask, jsonify, send_from_directory
import pandas as pd
import random
import os

app = Flask(__name__)

EXCEL_PATH = "جدول العام.xlsx"      # ← ملف Excel
DAYS  = ["الأحد", "الإثنين", "الثلاثاء", "الأربعاء", "الخميس"]
TIMES = ["8:00", "10:00", "12:00", "2:00"]


@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/style.css')
def css():
    return send_from_directory('.', 'style.css')

@app.route('/script.js')
def js():
    return send_from_directory('.', 'script.js')

# صورة الخلفيّة
@app.route('/bg.jpg')
def bg():
    return send_from_directory('.', 'bg.jpg')


#— تحميل Excel مرّة واحدة —#
try:
    DF_ALL = pd.read_excel(EXCEL_PATH, engine="openpyxl")
except Exception as e:
    print(f"خطأ في قراءة ملف Excel: {e}")
    DF_ALL = pd.DataFrame()


#— API الجدول —#
@app.route('/api/schedule/<student_id>')
def get_schedule(student_id):
    if DF_ALL.empty:
        return jsonify({"success": False, "message": "تعذّر تحميل جدول العام."})

    try:
        student_id_int = int(student_id)
    except ValueError:
        return jsonify({"success": False, "message": "رقم المتدرب غير صالح."})

    df = DF_ALL[DF_ALL["رقم المتدرب"] == student_id_int]

    if df.empty:
        return jsonify({"success": False, "message": "رقم المتدرب غير موجود."})

    name  = df.iloc[0]["إسم المتدرب"]
    major = df.iloc[0].get("التخصص", "")

    # توزيع عشوائي على الشبكة
    grid = [["" for _ in DAYS] for _ in TIMES]
    cells = [(t, d) for t in range(len(TIMES)) for d in range(len(DAYS))]
    random.shuffle(cells)

    for _, row in df.iterrows():
        target = cells.pop() if cells else (0, 0)
        t_idx, d_idx = target
        grid[t_idx][d_idx] = (
            f"{row['اسم المقرر']}<br><span>"
            f"{row['المقرر']} - {row['المدرب']}</span>"
        )

    # بناء HTML
    html  = "<div class='schedule-grid'>"
    html += "<div></div>" + "".join(f"<div class='day-header'>{d}</div>" for d in DAYS)
    for i, time in enumerate(TIMES):
        html += f"<div class='time-slot'>{time}</div>"
        for j in range(len(DAYS)):
            cell = grid[i][j]
            html += f"<div class='class-box'>{cell}</div>" if cell else "<div></div>"
    html += "</div>"

    return jsonify({
        "success": True,
        "scheduleHtml": html,
        "name": name,
        "major": major
    })


if __name__ == "__main__":
    port = int(os.environ.get("PORT",1000))
    app.run(host="0.0.0.0",port=port)
