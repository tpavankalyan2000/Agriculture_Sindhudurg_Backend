from flask import Flask, request, jsonify, Blueprint
import pandas as pd
from io import BytesIO
import openpyxl
import os

parse_bp = Blueprint("parse",__name__,url_prefix="/parser")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FILE = os.path.abspath(os.path.join(BASE_DIR, '..', '..', '..', 'files', 'Agriculture_crop__dataset.xlsx'))

@parse_bp.route('/upload_excel', methods=['POST', 'GET'])
def upload_excel():
    file_path = UPLOAD_FILE
    # file_path = "/home/king_of_criminals/Downloads/Agriculture_crop__dataset.xlsx"

    try:
        # Read Excel with rows 2 and 3 (index 1 and 2) as multi-level header
        df = pd.read_excel(file_path, header=[1, 2])
        df = df.drop(index=2)

        # Flatten multi-level header
        df.columns = [
            f"{col[1]}" if 'Unnamed' not in col[1] else col[0]
            for col in df.columns
        ]
        df.columns = [col.strip() for col in df.columns]

        # Forward-fill merged cells (Taluka, Year, etc.)
        df = df.ffill()

        # Drop second column if empty
        if df.columns[1] == 'Unnamed: 1':
            df.drop(df.columns[1], axis=1, inplace=True)

        if 'Taluka' in df.columns:
            df['Taluka'] = df['Taluka'].astype(str)

        year_column = df.columns[3]
        column_5 = df.columns[4]

        final_extracted_data = {}
        print(df,'data')
        for taluka, group in df.groupby('Taluka'):
            year_data = {}
            years = group[year_column].unique()

            for year in years:
                year_group = group[group[year_column] == year]
                if not year_group.empty:
                    crops_info = {}

                    for _, row in year_group.iterrows():
                        parameter = row[column_5]
                        for col in year_group.columns[5:]:
                            crop_name = col.strip()
                            value = row[col]

                            if pd.notna(value):
                                if crop_name not in crops_info:
                                    crops_info[crop_name] = {}
                                crops_info[crop_name][parameter] = value

                    year_data[year] = crops_info

            final_extracted_data[taluka] = year_data

        final_extracted_data = {
            k: v for k, v in final_extracted_data.items()
            if not k.isdigit()
        }
        return jsonify(final_extracted_data)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

