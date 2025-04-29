# app/views/village_counts.py

from flask import Blueprint, request, jsonify
from datetime import datetime
from source.models.model import MongoDB

mongo = MongoDB()

village_counts_sd = Blueprint("village_counts", __name__, url_prefix='/village_counts')

@village_counts_sd.route("/village-incident-counts", methods=["GET"])
def village_incident_counts():
    # ─── Parse optional filters ───
    start_date = request.args.get("start_date")
    end_date = request.args.get("end_date")
    species_names = request.args.getlist("species_names")  # 👈 change here!

    def parse_date(s):
        try:
            return datetime.strptime(s, "%Y-%m-%d")
        except Exception:
            return None

    start_date = parse_date(start_date)
    end_date = parse_date(end_date)

    # ─── Build Mongo query ───
    query = {}

    if species_names:
        query["wild_animal"] = {"$in": species_names}  # 👈 match wild_animal by names

    if start_date and end_date:
        query["incident_date"] = {"$gte": start_date, "$lte": end_date}
    elif start_date:
        query["incident_date"] = {"$gte": start_date}
    elif end_date:
        query["incident_date"] = {"$lte": end_date}

    # ─── Fetch events from MongoDB ───
    attack_events = mongo.forest_incidents.find(query, {"village_name": 1})

    # ─── Count by village ───
    counts_by_name = {}
    for event in attack_events:
        village = event.get("village_name")
        if village:
            counts_by_name[village] = counts_by_name.get(village, 0) + 1

    # ─── Return JSON ───
    return jsonify({"village_counts": counts_by_name})
