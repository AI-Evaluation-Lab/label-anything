import os
import json
import uuid
import io

from flask import Flask, request, jsonify, send_file
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import DeclarativeMeta
from sqlalchemy import MetaData
from sqlalchemy.exc import SQLAlchemyError
import numpy as np
from datetime import datetime
from pathlib import Path
from flask_cors import CORS
from PIL import Image as CVImage
import ast
from dotenv import load_dotenv
from tqdm import tqdm
import sys
import shutil

from embeddings import generate_embeddings, mask_predictor

app = Flask(__name__)
CORS(app)
load_dotenv()

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define Image model
class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_updated = db.Column(db.DateTime, default=datetime.utcnow)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    markers = db.Column(db.JSON, nullable=False, default={})
    marker_labels = db.Column(db.JSON, nullable=False, default={})
    masks = db.Column(db.JSON, nullable=False, default={})
    path = db.Column(db.String(255), nullable=False)
    embedding_path = db.Column(db.String(255))
    is_difficult = db.Column(db.Boolean, default=False)
    comments = db.Column(db.String, default="")

def to_dict(obj):
    if isinstance(obj.__class__, DeclarativeMeta):
        # an SQLAlchemy class
        fields = {}
        for field in [x for x in dir(obj) if not x.startswith('_') and x != 'metadata']:
            data = obj.__getattribute__(field)
            try:
                # If the field is a relationship, convert it to a dictionary recursively
                if isinstance(data.__class__, DeclarativeMeta):
                    fields[field] = to_dict(data)
                elif isinstance(data, datetime):
                    fields[field] = data.strftime('%Y-%m-%d %H:%M:%S')  # Convert datetime to string
                else:
                    # Check if the field is serializable to JSON
                    json.dumps(data)
                    fields[field] = data
            except TypeError:
                fields[field] = None
        return fields
    else:
        return obj

# Initialize Images from IMAGES_DIR
def initialize_images():
    IMAGES_DIR = os.getenv('IMAGES_DIR')
    EMBEDDINGS_DIR = os.getenv('EMBEDDINGS_DIR')
    masks_json_path = os.getenv('MASKS_JSON_PATH')
    if os.path.exists(IMAGES_DIR) and os.path.exists(masks_json_path):
        with open(masks_json_path, "r") as f:
            masks_data = json.load(f)
        for filename in tqdm(os.listdir(IMAGES_DIR), "Populating database"):
            path = os.path.join(IMAGES_DIR, filename)
            embedding_path = os.path.join(EMBEDDINGS_DIR, f"{filename.split('.png')[0]}.pt")  # Adjust this based on your implementation
            markers = {mask_data["type"]: [] for mask_data in masks_data}  # Initialize markers dictionary with keys based on type attribute
            marker_labels = {mask_data["type"]: [] for mask_data in masks_data}  # Initialize markers dictionary with keys based on type attribute
            masks = {mask_data["type"]: {"path":"", "background":mask_data["background"], "label":mask_data["label"], "description":mask_data["description"]} for mask_data in masks_data}  # Initialize markers dictionary with keys based on type attribute
            image = Image(date_created=datetime.now(), date_updated=datetime.now(), markers=markers, marker_labels=marker_labels, masks=masks, path=path, embedding_path=embedding_path)
            db.session.add(image)
        db.session.commit()

# GET all Images
@app.route('/images', methods=['GET'])
def get_images():
    images = Image.query.all()
    image_dicts = [to_dict(image) for image in images]
    return image_dicts

# GET an Image by id
@app.route('/images/<int:image_id>', methods=['GET'])
def get_image(image_id):
    image = Image.query.get(image_id)
    if image is None:
        return jsonify({'message': 'Image not found'}), 404
    return to_dict(image)

# Endpoint to serve an image as PNG
@app.route('/images/<int:image_id>/png', methods=['GET'])
def get_image_as_png(image_id):
    image = Image.query.get(image_id)
    if image is None:
        return jsonify({'message': 'Image not found'}), 404
    return send_file(image.path, mimetype='image/png')

# # Update is_difficult for an Image by id
# @app.route('/images/<int:image_id>/is_difficult', methods=['PATCH'])
# def update_is_difficult(image_id):
#     image = Image.query.get(image_id)
#     if image is None:
#         return jsonify({'message': 'Image not found'}), 404

#     data = request.get_json()
#     is_difficult = data.get('is_difficult')
#     if is_difficult is None:
#         return jsonify({'message': 'is_difficult data not provided'}), 400

#     image.is_difficult = is_difficult
#     db.session.commit()

#     return jsonify(to_dict(image))

# # Update comments for an Image by id
# @app.route('/images/<int:image_id>/comments', methods=['PATCH'])
# def update_comments(image_id):
#     image = Image.query.get(image_id)
#     if image is None:
#         return jsonify({'message': 'Image not found'}), 404

#     data = request.get_json()
#     comments = data.get('comments')
#     if comments is None:
#         return jsonify({'message': 'comments data not provided'}), 400

#     image.comments = comments
#     db.session.commit()

#     return jsonify(to_dict(image))

# @app.route('/images/<int:image_id>/markers/<string:marker_type>', methods=['PATCH'])
# def update_marker(image_id, marker_type):
#     try:
#         image = Image.query.get(image_id)
#         if image is None:
#             return jsonify({'message': 'Image not found'}), 404
        
#         data = request.get_json()
#         new_marker = data.get('new_marker')
#         if new_marker is None:
#             return jsonify({'message': 'New marker data not provided'}), 400

#         marker_types = image.marker_types
#         if marker_type not in marker_types:
#             return jsonify({'message': f'Marker type "{marker_type}" not found for this image'}), 404

#         updated_markers = {}
#         for key in marker_types:
#             if key == marker_type:
#                 updated_markers[key]= new_marker
#             else:
#                 updated_markers[key] = marker_types[key]

#         image.date_updated = datetime.utcnow()
#         image.markers = updated_markers
#         db.session.commit()

#         return jsonify(to_dict(image))
#     except SQLAlchemyError as e:
#         # Log the error for debugging
#         print(f"Failed to update marker: {e}")
#         # Rollback changes if an error occurs
#         db.session.rollback()
#         return jsonify({'message': 'Failed to update marker'}), 500

@app.route('/images/<int:image_id>/mask', methods=['GET'])
def get_mask(image_id):
    image = Image.query.get(image_id)
    point_coords = request.args.get('markers')
    point_labels = request.args.get('labels')
    
    if point_coords:
        point_coords = json.loads(point_coords)
        point_coords = np.array([[item['x'], item['y']] for item in point_coords])
        point_labels = json.loads(point_labels)
    else:
        point_coords = []
        point_labels = []

    mask_predictor.load_image_embedding(image.embedding_path)
    m, s, l = mask_predictor.predict(
        point_coords=point_coords,
        point_labels=point_labels,
        multimask_output=False,
    )

    # Create mask image
    mask_image = np.array(m[0], dtype=np.uint8) * 255
    mask_image = CVImage.fromarray(mask_image)

    # Save the mask image to a byte stream
    mask_byte_array = io.BytesIO()
    mask_image.save(mask_byte_array, format='PNG')
    mask_byte_array.seek(0)

    return send_file(mask_byte_array, mimetype='image/png')

@app.route('/images/<int:image_id>/mask', methods=['PATCH'])
def update_mask(image_id):
    image = Image.query.get(image_id)

    data = request.get_json()
    point_coords = data.get('markers')
    point_labels= data.get('labels')
    mask_type = data.get('type')
    print('### - point_coords received', point_coords)
    print('### - point_labels received', point_labels, type(json.loads(point_labels)))

    
    
    if point_coords:
        point_coords = json.loads(point_coords)
        point_coords = np.array([[item['x'], item['y']] for item in point_coords])
        point_labels = json.loads(point_labels)
    else:
        point_coords = []
        point_labels = []

    mask_predictor.load_image_embedding(image.embedding_path)
    m, s, l = mask_predictor.predict(
        point_coords=point_coords,
        point_labels=point_labels,
        multimask_output=False,
    )

    # Create mask image
    mask_image = np.array(m[0], dtype=np.uint8) * 255
    mask_image = CVImage.fromarray(mask_image)

    mask_image.save('mask.png', format='PNG')
    # persist_image_mask(image_id, mask_type, mask_image, point_coords, point_labels)

    image_name = image.path.split("/")[-1].split(".png")[0]
    MASKS_DIR = f"{os.getenv('MASKS_DIR')}/{image_name}.png"
    Path(MASKS_DIR).mkdir(exist_ok=True, parents=True)

    mask_image_path = f"{MASKS_DIR}/{mask_type}.png"
    mask_image.save(mask_image_path, format="PNG")

    updated_markers = {}
    for marker in image.markers:
        if marker == mask_type:
            updated_markers[marker] = point_coords.tolist()
        else:
            updated_markers[marker] = image.markers[marker]
    image.markers = updated_markers

    updated_marker_labels = {}
    for marker_label in image.marker_labels:
        if marker_label == mask_type:
            updated_marker_labels[marker_label] = point_labels
        else:
            updated_marker_labels[marker_label] = image.marker_labels[marker_label]
    image.marker_labels = updated_marker_labels

    updated_masks = {}
    for mask in image.masks:
        if mask == mask_type:
            updated_masks[mask] = {}
            updated_masks[mask]['background'] = image.masks[mask]['background']
            updated_masks[mask]['description'] = image.masks[mask]['description']
            updated_masks[mask]['label'] = image.masks[mask]['label']
            updated_masks[mask]['path'] = mask_image_path
        else:
            updated_masks[mask] = image.masks[mask]
    image.masks = updated_masks

    image.date_updated = datetime.utcnow()

    db.session.commit()
    return jsonify(to_dict(image))

def delete_contents(folder):
    folder = os.getenv(folder)
    print(f'Cleaning up: {folder}')
    for f in os.listdir(folder):
        os.remove(f'{folder}/{f}')
    Path(folder).mkdir(exist_ok=True, parents=True)

def reset(reset=False):
    if reset:
        print('Reset detected, reinitializing everything..')
        delete_contents('MASKS_DIR')
        # delete_contents('EMBEDDINGS_DIR')

        generate_embeddings(os.getenv('IMAGES_DIR'), os.getenv('EMBEDDINGS_DIR'))
        
        meta = MetaData()
        meta.reflect(bind=db.engine)
        meta.drop_all(bind=db.engine)
        # Recreate tables
        db.create_all()
        initialize_images()


with app.app_context():
    # if len(os.listdir(os.getenv('EMBEDDINGS_DIR'))) != len(os.listdir(os.getenv('IMAGES_DIR'))):
    reset(True)


if __name__ == '__main__':
    # initialize_images()
    app.run(debug=True)

