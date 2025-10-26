# -*- coding: utf-8 -*-
"""
📘 Sahl Scraper API
-------------------
هذا الكود ينشئ API بسيط باستخدام Flask و BeautifulSoup
يقوم بقراءة دروس أي صف ومادة من موقع سهل التعليمي (sahl.io)
ثم يعيد قائمة الدروس بصيغة JSON ليستخدمها نموذج GPT عبر الإجراءات (Actions)
"""

from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route("/sahl-scraper", methods=["POST"])
def scrape_sahl():
    data = request.get_json()
    grade = data.get("grade")     # مثل: "أول-ثانوي"
    subject = data.get("subject") # مثل: "فيزياء"

    # إنشاء الرابط الديناميكي
    url = f"https://sahl.io/sa/book/63/{grade}/{subject}"
    headers = {"User-Agent": "Mozilla/5.0"}

    try:
        res = requests.get(url, headers=headers, timeout=10)
        res.raise_for_status()
    except Exception as e:
        return jsonify({"error": f"فشل في الوصول إلى الموقع: {str(e)}"}), 500

    soup = BeautifulSoup(res.text, "html.parser")
    lessons = []

    # البحث عن جميع روابط الدروس
    for link in soup.select("a.book-unit-link"):
        title = link.text.strip()
        href = link.get("href")
        if href:
            lessons.append({
                "title": title,
                "url": "https://sahl.io" + href
            })

    if not lessons:
        return jsonify({"message": "لم يتم العثور على دروس لهذا الصف أو المادة"}), 404

    return jsonify({
        "grade": grade,
        "subject": subject,
        "lesson_count": len(lessons),
        "lessons": lessons
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

# pip install flask requests beautifulsoup4
