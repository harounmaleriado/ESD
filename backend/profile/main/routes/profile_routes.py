from flask import Blueprint, request, jsonify
from main.models.profile_models import Profile

profile_bp = Blueprint('profile_bp', __name__)

@profile_bp.route('/profile/<int:user_id>', methods=['PUT'])
def update_profile(user_id):
    data = request.get_json()
    
    # Attempt to retrieve the existing profile by user_id
    existing_profile = Profile.get_by_user_id(user_id)
    if existing_profile:
        profile = existing_profile[0]
        
        # Update profile with new data
        profile_data = {
            'user_id': user_id,
            'name': data.get('name', profile.name),  
            'email': data.get('email', profile.email),  
            'contact_details': data.get('contact_details', profile.contact_details),  
            'bio': data.get('bio', profile.bio),
            'profile_pic': data.get('profile_pic', profile.profile_pic)
        }
        # Update the profile document in Firestore
        Profile.update(profile_data)
        return jsonify({"message": "Profile updated successfully"}), 200
    else:
        return jsonify({"message": "Profile not found"}), 404

@profile_bp.route('/profile/<int:user_id>', methods=['GET'])
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

