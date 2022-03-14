from flask import Flask, request, Response
import firebase_admin
from firebase_admin import credentials, firestore
from pipeline import get_data, get_metadata

app = Flask(__name__)

cred = credentials.Certificate('serviceAccount.json')
firebase_admin.initialize_app(cred)
db = firestore.client()

@app.route('/form', methods=('POST'))
def add_form():
    cik = request.form.get('cik')
    form_type = request.form.get('form_type')
    year = request.form.get('year')
    quarter = request.form.get('quarter',0)
    if form_type not in ("10k","10q","8k"):
        return Response("invalid form type",status=401)

    form_uid = year
    try:
        if not 0<int(quarter)<=4:
            raise Exception
        else:
            form_uid = year+"_"+quarter
    except Exception:
        return Response("invalid quarter number",status=401)

    data = get_data(cik, form_type, year, quarter)

    db.collection("company").document(cik).collection(form_type).document(form_uid).set(data)
    return Response(status=200)

@app.route('/company', methods=('POST'))
def add_company():
    cik = request.form.get('cik')
    data = get_metadata(cik)
    db.collection("company").document(cik).set(data)
    return Response(status=401)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000)