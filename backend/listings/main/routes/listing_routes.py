from flask import Flask, request, jsonify, Blueprint
from main.models.listing_model import Listing, db

listing_bp = Blueprint('listing_bp', __name__)

@listing_bp.route('/listings', methods=['POST'])
def add_listing():
    """
    Create a new listing.
    """
    try:
        # Access form data for the text fields
        category = request.form.get('category')
        datetime = request.form.get('datetime')
        desc = request.form.get('desc')
        latitude = request.form.get('latitude')
        longitude = request.form.get('longitude')
        name = request.form.get('name')
        price = request.form.get('price')
        user_id = request.form.get('user_id')

        category = [category] 

        # Convert string values to appropriate types, e.g., latitude, longitude, and price
        latitude = float(latitude)
        longitude = float(longitude)
        price = float(price)

        # Access uploaded files
        image_files = request.files.getlist('images')

        # Create and save the new listing
        new_listing = Listing(
            category=category,
            datetime=datetime,
            desc=desc,
            latitude=latitude,
            longitude=longitude,
            name=name,
            price=price,
            user_id=user_id
        )
        new_listing.save(image_files=image_files)

        return jsonify({"message": "Listing added"}), 201
    except Exception as e:
        # Handle other exceptions
        return jsonify({"error": str(e)}), 500

@listing_bp.route('/listings/<int:user_id>', methods=['GET'])
def get_listings(user_id):
    """
    Retrieve all listings for a specific user.
    """
    try:
        listings = Listing.get_user_listings(user_id)  # Using the static method of the Listing model
        return jsonify(listings), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    

@listing_bp.route('/compare', methods=['POST'])
def compare_listings():
    """
    Compare two listings by their document IDs.
    """
    try:
        data = request.json
        product_id_1 = data.get('product_id_1')
        product_id_2 = data.get('product_id_2')

        listing_1 = Listing.get_listing_by_id(product_id_1)
        listing_2 = Listing.get_listing_by_id(product_id_2)

        if not listing_1 or not listing_2:
            return jsonify({"error": "One or both listings not found"}), 404

        # Return only the relevant details: name, description, and price
        result = {
            "listing_1": {
                "name": listing_1.get('name'),
                "desc": listing_1.get('desc'),
                "price": listing_1.get('price')
            },
            "listing_2": {
                "name": listing_2.get('name'),
                "desc": listing_2.get('desc'),
                "price": listing_2.get('price')
            }
        }
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    
@listing_bp.route('/listings', methods=['GET'])
def get_all_listings():
    """
    Retrieve all listings including their document IDs.
    """
    try:
        listings = Listing.get_all_listings()
        return jsonify(listings), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

