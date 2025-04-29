# app/views/drop_down_filter.py
from flask import Blueprint, jsonify
from source.models.model import MongoDB

mongo = MongoDB()

filter_options_sd = Blueprint('filter', __name__, url_prefix='/filter_options')

@filter_options_sd.route("/filter-options", methods=["GET"])
def get_filter_options():
    # Get distinct species
    species_names = mongo.forest_incidents.distinct("wild_animal")

    species_data = [
        {"id": idx + 1, "common_name": name, "scientific": None}
        for idx, name in enumerate(sorted(species_names))
    ]

    # Get distinct villages
    village_names = mongo.forest_incidents.distinct("village_name")

    village_data = [
        {"id": idx + 1, "name": name}
        for idx, name in enumerate(sorted(village_names))
    ]

    return jsonify({
        "species": species_data,
        "villages": village_data
    })
