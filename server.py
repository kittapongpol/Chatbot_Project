from flask import Flask, request, jsonify, render_template
import pandas as pd
from fuzzywuzzy import process  # ใช้ fuzzy matching (หรือใช้ rapidfuzz ก็ได้)

app = Flask(__name__)

# โหลดข้อมูล CSV
df = pd.read_csv("data.csv")

# ฟังก์ชันค้นหาคณะที่ใกล้เคียง
def rag_retrieve(faculty_name):
    faculty_list = df["คณะ"].unique().tolist()  # ดึงรายชื่อคณะที่มีทั้งหมด
    
    # ค้นหาคณะที่ใกล้เคียงที่สุดจากสิ่งที่ผู้ใช้พิมพ์
    best_match, score = process.extractOne(faculty_name, faculty_list)

    if score >= 60:  # ถ้าความคล้ายคลึงมากกว่า 60% ถือว่าตรง
        filtered_df = df[df["คณะ"] == best_match]
        branches = ", ".join(filtered_df["สาขา"].tolist())
        return f"คุณหมายถึง '{best_match}' ใช่หรือไม่? มีสาขาดังนี้: {branches}"
    else:
        return "ขออภัย ไม่พบข้อมูลที่ตรงกับสิ่งที่คุณค้นหา"

# หน้าเว็บหลัก
@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")

# API สำหรับค้นหาข้อมูล
@app.route("/ask", methods=["POST"])
def ask():
    data = request.json
    faculty_name = data.get("faculty", "").strip()

    if not faculty_name:
        return jsonify({"response": "โปรดระบุชื่อคณะ!"})

    response = rag_retrieve(faculty_name)
    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(port=5000, debug=True)
