from flask import Flask, request, jsonify
from utils.bolt import process_bolt_csv_files

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return "CSV Uploader API is running!"

@app.route('/upload-bolt-csvs', methods=['POST'])
def upload_bolt_csvs():
    files = request.files.getlist("files")
    if not files:
        return jsonify({"error": "No files uploaded"}), 400

    try:
        file_list = [(f.filename, f.read()) for f in files]
        df = process_bolt_csv_files(file_list)

        # You can insert into DB here if needed
        # insert_to_db(df)

        return jsonify({
            "message": "Bolt CSVs processed successfully",
            "files_processed": len(file_list),
            "rows_combined": len(df)
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500
