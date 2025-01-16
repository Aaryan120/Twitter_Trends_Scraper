from flask import Blueprint, render_template, jsonify, request
from app.services.seleniumServices import login_and_fetch_x_trends
from app.services.mongoDB import save_trend, get_all_records
import os

main = Blueprint('main', __name__)


# @main.route('/')
# def home():
#     return render_template('index.html')


@main.route('/fetch_trends', methods=['GET'])
def fetch_trends():
    try:
        data = login_and_fetch_x_trends()
        print("Raw data:", data)
        if not data or len(data) != 3:
            return jsonify({
                'error': f'Error no data found'
            })

        ip_address, trends, timestamp = data
        print(f"IP: {ip_address}, Trends: {trends}, TimeStamp : {timestamp}")

        try:
            object_id = save_trend(trends, ip_address)
            print(f"MongoDB Object ID: {object_id}")
            mongoData = get_all_records(str(object_id))
        except Exception as e:
            # return render_template('index.html', trends=trends, ip_address=ip_address, error=f"MongoDB Error: {str(e)}")
            return jsonify({
                "error" : f'MongoDB error : {e}'
            }),500
        # return render_template('index.html', trends=trends, object_id=str(object_id), ip_address=ip_address)
        return jsonify({
            'trends': trends,
            'ip_address': ip_address,
            'object_id': str(object_id),
            'timestamp': timestamp,
            'mongoData': mongoData
        })
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({
            'error': f'Could not fetch trends {e}'
        })


# @main.route('/get', methods=['GET'])
# def dashboard():
#     try:
#         records = get_all_records()
#         return render_template('dashboard.html', records=records)
#     except Exception as e:
#         return render_template('dashboard.html', records=[], error=str(e))