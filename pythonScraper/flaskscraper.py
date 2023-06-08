from flask import Flask, jsonify, request, make_response, send_file
from flask_cors import CORS
import MusicalInstrumentsScraper
import os
from datetime import datetime

current_time = datetime.now().strftime("%Y-%m-%d %H-%M") 
filename = "MusicalInstrumentsScraper" + current_time

# get the absolute path of the script file
script_dir = os.path.dirname(os.path.abspath(__file__))

# construct the path to save the Excel file
file_path = os.path.join(script_dir, filename + ".xlsx")

#import sys

#sys.path.append(".")

app = Flask(__name__)

CORS(app)

@app.route("/")
def index():
    return jsonify({"message": "Musical Instruments Scraper is Ready"})

@app.route("/websites")
def websites():
    webs = MusicalInstrumentsScraper.getAllowedWebsites()
    try:
        js = jsonify(webs)
    except Exception as e:
        print(webs)
        print(e)
        js = webs
    return js

@app.route("/scrap", methods=['POST'])
def scrap():
    print("called scrap")
    webs_to_scrap = request.get_json().get('webs_to_scrap')
    print("react returned webs:")
    print(webs_to_scrap)
    #generate the excel
    if not webs_to_scrap:
        return jsonify({"server_answer": "fail"})
    try:
        MusicalInstrumentsScraper.scrapToExcel(webs_to_scrap, filename=file_path)
    except Exception as e:
        print("exception in trying to scrap")
        return jsonify({"server_answer": "fail", "server_error": "uknown"}), 400
    return jsonify({"server_answer": "success", "server_error": "none", "filename": filename}), 200


@app.route("/download")
def download():
    print("received a download request")
    return send_file(file_path, as_attachment=True)


if __name__ == '__main__':
    app.run(debug=True)