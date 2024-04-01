from flask import Blueprint, request, jsonify
from main.models.profile_models import Profile

profile_bp = Blueprint('profile_bp', __name__)

@profile_bp.route('/profile/<user_id>', methods=['PUT'])
def update_profile(user_id):
    data = request.form
    file =request.files.get('profile_pic')
    if file:
        print(f"Received file: {file.filename}")
    else:
        print("No file received")
    
    # Attempt to retrieve the existing profile by user_id
    existing_profile = Profile.get_by_user_id(user_id)
    if existing_profile:
        profile_pic_url = Profile.upload_file_to_firebase_storage(file, user_id)
        print(f"Profile pic URL: {profile_pic_url}")
        # Update profile with new data
        profile_data = {
            'user_id': user_id,  
            'name': data.get('name', existing_profile.name),
            'email': data.get('email', existing_profile.email),
            'contact_details': data.get('contact_details', existing_profile.contact_details),
            'bio': data.get('bio', existing_profile.bio),
            'profile_pic': profile_pic_url or existing_profile.profile_pic
        }
        print(f"Profile data: {profile_data}")
        # Update the profile document in Firestore
        Profile.update(profile_data)
        return jsonify({"message": "Profile updated successfully"}), 200
    else:
        return jsonify({"message": "Profile not found"}), 404

@profile_bp.route('/profile/<user_id>', methods=['GET'])
def get_profile(user_id):
    profile = Profile.get_by_user_id(user_id)
    if profile:
        return jsonify({
            "user_id": profile.user_id,
            "name": profile.name,
            "email": profile.email,
            "contact_details": profile.contact_details,
            "bio": profile.bio,
            "profile_pic": profile.profile_pic
        }), 200
    else:
        return jsonify({"message": "Profile not found"}), 404

