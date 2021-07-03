from flask import Flask, request, jsonify, send_from_directory, json

import watermark_pdf
from flask import Response

app=Flask(__name__)


@app.route('/upload/',methods=['GET', 'POST'])
def upload():
    fic=request.files['pdf']
    if fic.mimetype != 'application/pdf':
        return jsonify({"status":"error not a pdf file"})
    data = fic.stream.read()
    print(fic.mimetype)
    data2 = watermark_pdf.mark_pdf_bytes("Testing", watermark_pdf.make_temp_file(data))
    return Response(data2, mimetype='application/pdf')


if __name__ == "__main__":
	app.run(port=8000,debug=True)