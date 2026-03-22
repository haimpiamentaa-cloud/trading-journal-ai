from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai
import pandas as pd
import os

app = Flask(__name__)
CORS(app)

# הגדרת ה-API של Gemini
# תוציא מפתח בחינם כאן: https://aistudio.google.com/app/apikey
genai.configure(api_key="הכנס_כאן_את_המפתח_שלך")
model = genai.GenerativeModel('gemini-1.5-flash')

@app.route('/ask', methods=['POST'])
def ask_ai():
    try:
        data = request.json
        user_query = data.get('query')
        
        # ניסיון לקרוא נתונים אם קיים קובץ trades.csv
        summary = "לא נמצא קובץ נתונים. המערכת פועלת במצב ניתוח כללי."
        if os.path.exists('trades.csv'):
            df = pd.read_csv('trades.csv')
            summary = f"נתוני מסחר נוכחיים: {len(df)} עסקאות. רווח מצטבר: {df['PnL'].sum() if 'PnL' in df else 'N/A'}."

        prompt = f"{summary}\nהמשתמש שואל: {user_query}\nענה בעברית מקצועית של סוחרים, תהיה תמציתי וחד."
        
        response = model.generate_content(prompt)
        return jsonify({"response": response.text})
    except Exception as e:
        return jsonify({"response": f"שגיאה בשרת: {str(e)}"}), 500

if __name__ == '__main__':
    print("\n" + "="*50)
    print("🚀 שרת QUANT AI של יומן המסחר באוויר!")
    print("המערכת ממתינה לפקודות מהיומן בפורט 5000...")
    print("="*50 + "\n")
    if __name__ == '__main__':
    # Render מגדיר את הפורט אוטומטית, אנחנו רק צריכים לקרוא אותו
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)