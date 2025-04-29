from flask import Blueprint, request, jsonify
from datetime import datetime
from source.models.model import MongoDB
from enum import Enum

filter_damage_sd = Blueprint('filtered_damage', __name__, url_prefix='/filter_damage')
mongo = MongoDB()


class DamageClass(Enum):
    TREES = "Damage to trees"
    SHEEP = "Sheep damage"
    LIVESTOCK = "Livestock loss"
    HUMAN = "human loss"

@filter_damage_sd.route("/filtered-damage-breakdown", methods=["GET"])
def get_filtered_damage_breakdown():
    args = request.args

    village = args.get("village")
    taluka = args.get("taluka")
    start_date = args.get("start_date")
    end_date = args.get("end_date")
    # species_ids = args.getlist("species_ids")
    species_names = args.getlist("species_names")
    damage_classes = args.getlist("damage_classes")

    query = {}


    
    # Safe parse dates
    def parse_date(val):
        try:
            return datetime.strptime(val, "%Y-%m-%d")
        except Exception:
            return None

    start_date = parse_date(start_date)
    end_date = parse_date(end_date)
    
    # Build Mongo query
    query = {}

    if village:
        query["village_name"] = village
    if taluka:
        query["taluka"] = taluka
    if species_names:
        query["wild_animal"] = {"$in": species_names}
    # if species_ids:
    #     query["wild_animal"] = {"$in": species_ids}
    if damage_classes:
        # If specific damage classes are requested, match on damage_category
        query["damage_category"] = {"$in": damage_classes}
    if start_date and end_date:
        query["incident_date"] = {"$gte": start_date, "$lte": end_date}
    elif start_date:
        query["incident_date"] = {"$gte": start_date}
    elif end_date:
        query["incident_date"] = {"$lte": end_date}

    # Aggregation to count by damage_category instead of damage_type
    pipeline = [
        {"$match": query},
        {"$group": {
            "_id": "$damage_category",
            "count": {"$sum": 1}
        }}
    ]

    results = list(mongo.forest_incidents.aggregate(pipeline))

    # Pre-fill all damage types with 0
    breakdown = {dc.value: 0 for dc in DamageClass}

    # Update counts from results
    for res in results:
        category = res["_id"]
        if category in breakdown:
            breakdown[category] = res["count"]

    return jsonify(breakdown)