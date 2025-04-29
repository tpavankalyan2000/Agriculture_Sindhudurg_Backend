from flask import Blueprint, request, jsonify
import pandas as pd
from datetime import datetime
from werkzeug.utils import secure_filename
from typing import Optional  # <-- added for backward compatibility
from source.models.model import MongoDB

mongo = MongoDB()
upload_sd = Blueprint("upload", __name__,url_prefix="/upload_doc")

# ─── Allowed Extensions ─────────────────────────────────
ALLOWED_EXTENSIONS = {"csv", "xls", "xlsx"}

def _ext(filename: str) -> Optional[str]:
    """Return lowercase extension without leading dot."""
    if "." not in filename:
        return None
    return filename.rsplit(".", 1)[1].lower()

def _allowed(filename: str) -> bool:
    """Check if the file extension is allowed."""
    return _ext(filename) in ALLOWED_EXTENSIONS

def safe_parse_date(date_str):
    """Parse date from string, return None if invalid."""
    try:
        return datetime.strptime(date_str, "%Y-%m-%d")
    except (ValueError, TypeError):
        return None

def safe_parse_float(value):
    """Parse float safely from string, handling commas and dashes."""
    if isinstance(value, str):
        value = value.replace(",", "").strip()
    try:
        return float(value)
    except (ValueError, TypeError):
        return 0.0

def ingest_dataframe(df: pd.DataFrame) -> int:
    """Transform the dataframe exactly like your script and insert into MongoDB."""
    records = []

    for _, row in df.iterrows():
        record = {
            "range": row.get("Range"),
            "financial_year": row.get("Financial\nYear"),
            "sr_no": int(row.get("Sr. No.", 0)),
            "village_name": row.get("Village"),
            "incident_date": safe_parse_date(row.get("Incident_Date")),
            "damage_category": row.get("Damage"),
            "wild_animal": row.get("Wild_Animaltype"),
            "damage_type": row.get("Type_of_Damage"),
            "damage_amount": safe_parse_float(row.get("Damage_Amount")),
            "taluka": row.get("TALUKA"),
            "forest_range": row.get("RANGE"),
            "round": row.get("ROUND"),
            "beat": row.get("BEAT"),
            "gaon": row.get("GAON"),
            "month": safe_parse_date(row.get("Month")),
        }
        records.append(record)

    if records:
        result = mongo.forest_incidents.insert_many(records)
        return len(result.inserted_ids)
    return 0

@upload_sd.route("/upload", methods=["POST"])
def upload_excel_or_csv():
    """Accept an Excel or CSV file and import into MongoDB."""
    if "file" not in request.files:
        return jsonify(error="No file part in request"), 400

    file = request.files["file"]

    if file.filename == "":
        return jsonify(error="No file selected"), 400

    if not _allowed(file.filename):
        return jsonify(error="Only .csv, .xls, or .xlsx files are accepted"), 415

    ext = _ext(file.filename)

    try:
        if ext == "csv":
            df = pd.read_csv(file)
        else:
            df = pd.read_excel(file)
    except Exception as exc:
        return jsonify(error=f"Could not parse the uploaded file: {exc}"), 422

    inserted_count = ingest_dataframe(df)

    return jsonify(message="Upload successful", rows_inserted=inserted_count), 201
