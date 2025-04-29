
from flask import Blueprint, request, jsonify
from source.models.model import MongoDB


predictions_sd = Blueprint("predictions", __name__, url_prefix='/prediction')
mongo = MongoDB()


@predictions_sd.route("/predictions", methods=["GET"])
def list_predictions():
    # ─────── Parse query param ───────
    village_id = request.args.get("village_id", type=int)

    # ─────── Build MongoDB filter ───────
    query_filter = {}
    if village_id is not None:
        query_filter["village_id"] = village_id

    # ─────── Query MongoDB ───────
    cursor = mongo.forest_prediction.find(query_filter).sort("predicted_date", -1)  # -1 for descending

    # ─────── Format response ───────
    predictions = []
    for pred in cursor:
        predictions.append({
            "id": str(pred["_id"]),
            "predicted_date": pred.get("predicted_date"),
            "village": pred.get("village"),
            "taluka": pred.get("taluka"),
            "species": pred.get("wild_animal_type"),
            "month": pred.get("month"),
            "predicted_crop": pred.get("predicted_crop")
        })

    return jsonify(predictions)

