

import os
import subprocess
import threading
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from pymongo import MongoClient
import logging  
from flask_pymongo import PyMongo


app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})  # Adjust as necessary
app.config["MONGO_URI"] = "mongodb://127.0.0.1:27017/streamapp"
mongo = PyMongo(app)


# Define the path where FFmpeg will output the HLS files
HLS_OUTPUT_DIR = 'C:\\Users\\jambh\\Desktop\\Job hunt\\LiveSitter\\StreamingApp\\pipe'

# Global variable to hold FFmpeg thread
ffmpeg_thread = None

@app.route('/')
def index():
    return "Welcome to the Streaming App!"

# Function to run FFmpeg in a separate thread
def run_ffmpeg():
    if not os.path.exists(HLS_OUTPUT_DIR):
        os.makedirs(HLS_OUTPUT_DIR)

    command = [
        'C:\\ffmpeg\\ffmpeg-2024-09-19-git-0d5b68c27c-essentials_build\\bin\\ffmpeg.exe',
        '-i', 'rtsp://rtspstream:92c11903409e78ea2a838653424e91d7@zephyr.rtsp.stream/movie',
        '-f', 'hls',
        '-hls_time', '2',
        '-hls_list_size', '0',
        '-hls_flags', 'delete_segments',
        os.path.join(HLS_OUTPUT_DIR, 'pipe.m3u8')
    ]

    subprocess.run(command)

@app.route('/stream')
def stream():
    global ffmpeg_thread
    if ffmpeg_thread is not None and ffmpeg_thread.is_alive():
        return "Streaming is already running."
    
    ffmpeg_thread = threading.Thread(target=run_ffmpeg)
    ffmpeg_thread.start()
    return "Streaming started in a separate thread!"

@app.route('/hls/<filename>')
def hls(filename):
    return send_from_directory(HLS_OUTPUT_DIR, filename)

# Create overlay
@app.route('/api/overlay', methods=['POST'])
def create_overlay():
    data = request.json
    print(data)
    mongo.db.overlays.insert_one(data)
    return jsonify({"message": "Overlay created!"}), 201


@app.route('/api/overlays', methods=['POST'])
def get_overlays():
    data = request.get_json()  # Get JSON data from the request body
    user_id = data.get('userId')  # Get user ID from the JSON body

    overlays = list(mongo.db.overlays.find({"userId": user_id}))  # Filter overlays by user ID
    
    # Convert ObjectId to string for each overlay
    for overlay in overlays:
        overlay['_id'] = str(overlay['_id'])  # Convert ObjectId to string
        # If there are any other ObjectId fields, convert them as needed

    return jsonify(overlays), 200

from bson.objectid import ObjectId
from flask import jsonify, request




@app.route('/api/updateOverlay', methods=['POST'])
def update_overlay():
    try:
        # Get the overlay data from the request
        overlay_data = request.json
        print(overlay_data) 
        # Ensure the overlay ID is provided
        overlay_id = overlay_data.get('_id')
        if not overlay_id:
            return jsonify({"error": "Overlay ID is required."}), 400

        # Update the overlay in the database
        result = mongo.db.overlays.update_one(
            {'_id': ObjectId(overlay_id)},
            {
                '$set': {
                    'position': overlay_data.get('position'),
                    'size': overlay_data.get('size'),
                    'content': overlay_data.get('content')
                }
            }
        )

        print(result)
        # Check if the overlay was modified
        if result.matched_count == 0:
            return jsonify({"error": "Overlay not found."}), 404
        elif result.modified_count == 0:
            return jsonify({"message": "Overlay not modified."}), 200

        return jsonify({"message": "Overlay updated successfully."}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
    
    
    
    
    

from bson import ObjectId

@app.route('/api/delete', methods=['DELETE'])
def delete_overlay():
    data = request.get_json()
    overlay_id_str = data.get('overlayId')  # Get overlayId from the request body

    try:
        overlay_id = ObjectId(overlay_id_str)  # Convert string to ObjectId
    except Exception as e:
        return jsonify({"message": "Invalid overlayId format!"}), 400

    # Delete the overlay by its _id
    result = mongo.db.overlays.delete_one({"_id": overlay_id})

    if result.deleted_count > 0:
        return jsonify({"message": "Overlay deleted!"}), 200
    else:
        return jsonify({"message": "Overlay not found!"}), 404



if __name__ == '__main__':
    app.run(debug=True)












# import os
# import subprocess
# import threading
# from flask import Flask, request, jsonify, send_from_directory
# from flask_cors import CORS
# from flask_pymongo import PyMongo
# from bson.objectid import ObjectId
# from dotenv import load_dotenv

# # Load environment variables from .env file
# load_dotenv()

# app = Flask(__name__)

# # Enable CORS for the frontend URL defined in the environment variable
# CORS(app, resources={r"/*": {"origins": os.getenv('FRONTEND_URL')}})

# # Set MongoDB URI from environment variable
# app.config["MONGO_URI"] = os.getenv('MONGO_URI')
# mongo = PyMongo(app)

# # Define the path where FFmpeg will output the HLS files from environment variable
# HLS_OUTPUT_DIR = os.getenv('HLS_OUTPUT_DIR')

# # Get RTSP URL and FFmpeg path from environment variables
# RTSP_URL = os.getenv('RTSP_URL')
# FFMPEG_PATH = os.getenv('FFMPEG_PATH')

# # Global variable to hold FFmpeg thread
# ffmpeg_thread = None

# @app.route('/')
# def index():
#     return "Welcome to the Streaming App!"

# # Function to run FFmpeg in a separate thread
# def run_ffmpeg():
#     if not os.path.exists(HLS_OUTPUT_DIR):
#         os.makedirs(HLS_OUTPUT_DIR)

#     command = [
#         FFMPEG_PATH,
#         '-i', RTSP_URL,
#         '-f', 'hls',
#         '-hls_time', '2',
#         '-hls_list_size', '0',
#         '-hls_flags', 'delete_segments',
#         os.path.join(HLS_OUTPUT_DIR, 'pipe.m3u8')
#     ]

#     subprocess.run(command)

# @app.route('/stream')
# def stream():
#     global ffmpeg_thread
#     if ffmpeg_thread is not None and ffmpeg_thread.is_alive():
#         response = jsonify({"message": "Streaming is already running."})
#         response.headers['Access-Control-Allow-Origin'] = os.getenv('FRONTEND_URL')
#         return response
    
#     ffmpeg_thread = threading.Thread(target=run_ffmpeg)
#     ffmpeg_thread.start()

#     response = jsonify({"message": "Streaming started in a separate thread!"})
#     response.headers['Access-Control-Allow-Origin'] = os.getenv('FRONTEND_URL')
#     return response






# @app.route('/hls/<filename>')
# def hls(filename):
#     response = send_from_directory(HLS_OUTPUT_DIR, filename)
#     response.headers['Access-Control-Allow-Origin'] = os.getenv('FRONTEND_URL')
#     return response


# # Create overlay
# @app.route('/api/overlay', methods=['POST'])
# def create_overlay():
#     data = request.json
#     mongo.db.overlays.insert_one(data)
#     return jsonify({"message": "Overlay created!"}), 201

# # Get overlays by user ID
# @app.route('/api/overlays', methods=['POST'])
# def get_overlays():
#     data = request.get_json()
#     user_id = data.get('userId')
#     overlays = list(mongo.db.overlays.find({"userId": user_id}))
    
#     for overlay in overlays:
#         overlay['_id'] = str(overlay['_id'])  # Convert ObjectId to string

#     return jsonify(overlays), 200

# # Update overlay by ID
# @app.route('/api/updateOverlay', methods=['POST'])
# def update_overlay():
#     try:
#         overlay_data = request.json
#         overlay_id = overlay_data.get('_id')
#         if not overlay_id:
#             return jsonify({"error": "Overlay ID is required."}), 400

#         result = mongo.db.overlays.update_one(
#             {'_id': ObjectId(overlay_id)},
#             {
#                 '$set': {
#                     'position': overlay_data.get('position'),
#                     'size': overlay_data.get('size'),
#                     'content': overlay_data.get('content')
#                 }
#             }
#         )

#         if result.matched_count == 0:
#             return jsonify({"error": "Overlay not found."}), 404
#         elif result.modified_count == 0:
#             return jsonify({"message": "Overlay not modified."}), 200

#         return jsonify({"message": "Overlay updated successfully."}), 200

#     except Exception as e:
#         return jsonify({"error": str(e)}), 500

# # Delete overlay by ID
# @app.route('/api/delete', methods=['DELETE'])
# def delete_overlay():
#     data = request.get_json()
#     overlay_id_str = data.get('overlayId')

#     try:
#         overlay_id = ObjectId(overlay_id_str)
#     except Exception as e:
#         return jsonify({"message": "Invalid overlayId format!"}), 400

#     result = mongo.db.overlays.delete_one({"_id": overlay_id})

#     if result.deleted_count > 0:
#         return jsonify({"message": "Overlay deleted!"}), 200
#     else:
#         return jsonify({"message": "Overlay not found!"}), 404

# if __name__ == '__main__':
#     app.run(debug=True)
