from flask import request, jsonify
from app import app, db




# Create overlay
@app.route('/api/overlay', methods=['POST'])
def create_overlay():
    data = request.json
    db.overlays.insert_one(data)
    return jsonify({"message": "Overlay created!"}), 201



# Read overlays by userId
@app.route('/api/overlays', methods=['GET'])
def get_overlays():
    user_id = request.args.get('userId')  # Get userId from query parameters
    if user_id:
        overlays = list(db.overlays.find({"userId": user_id}))  # Filter by userId
    else:
        overlays = list(db.overlays.find())  # Return all overlays if no userId is provided
    return jsonify(overlays), 200

# Update overlay by userId
@app.route('/api/overlay', methods=['PUT'])
def update_overlay():
    user_id = request.json.get('userId')  # Get userId from the request body
    overlay_content = request.json.get('content')  # Assuming content is updated
    result = db.overlays.update_many({"userId": user_id}, {"$set": {"content": overlay_content}})
    
    if result.modified_count > 0:
        return jsonify({"message": "Overlay updated!"}), 200
    return jsonify({"message": "No overlays found for this user."}), 404

# Delete overlay by userId
@app.route('/api/overlay', methods=['DELETE'])
def delete_overlay():
    user_id = request.json.get('userId')  # Get userId from the request body
    result = db.overlays.delete_many({"userId": user_id})
    
    if result.deleted_count > 0:
        return jsonify({"message": "Overlay deleted!"}), 200
    return jsonify({"message": "No overlays found for this user."}), 404