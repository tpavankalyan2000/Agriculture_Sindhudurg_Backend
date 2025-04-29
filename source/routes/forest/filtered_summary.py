from flask import Blueprint, request, jsonify
from datetime import datetime
from source.models.model import MongoDB

mongo = MongoDB()
filtered_summary_sd = Blueprint('filtered', __name__,url_prefix='/filtered_summary')

@filtered_summary_sd.route("/filtered-summary", methods=["GET"])
def filtered_summary():
    # ─────── Parse filters ───────
    args = request.args
    village = args.get("village")
    taluka = args.get("taluka")
    start_date = args.get("start_date")
    end_date = args.get("end_date")
    species_names = args.getlist("species_names")
    damage_classes = args.getlist("damage_classes")

    query = {}

    # ─────── Helper: Safe parse date ───────
    def parse_date(val):
        try:
            return datetime.strptime(val, "%Y-%m-%d")
        except (ValueError, TypeError):
            return None

    # ─────── Build Mongo Query ───────
    if village:
        query["village_name"] = village
    if taluka:
        query["taluka"] = taluka

    start_date = parse_date(start_date)
    end_date = parse_date(end_date)

    if start_date and end_date:
        query["incident_date"] = {"$gte": start_date, "$lte": end_date}
    elif start_date:
        query["incident_date"] = {"$gte": start_date}
    elif end_date:
        query["incident_date"] = {"$lte": end_date}

    if species_names:
        query["wild_animal"] = {"$in": species_names}
    if damage_classes:
        query["damage_type"] = {"$in": damage_classes}

    # ─────── Fetch data from MongoDB ───────
    try:
        attack_events = list(mongo.forest_incidents.find(query))
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    # ─────── Format MongoDB documents into response ───────
    events_list = []
    for doc in attack_events:
        damage_amount = doc.get("damage_amount", 0.0)
        est_loss_val = f"{float(damage_amount):.2f}" if damage_amount else "0.00"

        event = {
            "id": str(doc["_id"]),
            "village_id": None,
            "species_id": None,
            "occurred_at": doc.get("incident_date").isoformat() if doc.get("incident_date") else None,
            "reporter": None,
            "notes": None,
            "fin_year": doc.get("financial_year"),
            "species": {
                "common_name": doc.get("wild_animal"),
                "id": None,
                "scientific": None,
            },
            "damages": [
                {
                    "est_loss_val": est_loss_val,
                    "id": str(doc["_id"]),
                    "item": {
                        "name": doc.get("damage_type"),
                        "damage_class": doc.get("damage_category"),   # 👈 corrected here
                        "id": None,
                    },
                    "item_id": None,
                    "quantity": "None",
                    "unit": None,
                }
            ],
            "village": {
                "id": None,
                "name": doc.get("village_name"),
            },
        }
        events_list.append(event)

    return jsonify({
        "total_incidents": len(events_list),
        "primary_species": {},
        "losses": {},
        "attack_events": events_list,
    })
