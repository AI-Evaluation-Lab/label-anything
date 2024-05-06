from flask import jsonify, send_file, request
from models import Image, db
from utils import to_dict
from embeddings import mask_predictor

import numpy as np
import io
from PIL import Image as CVImage
import json
from pathlib import Path
import datetime

def setup_routes(app):
    # GET all Images
    @app.route('/images', methods=['GET'])
    def get_images():
        images = Image.query.all()
        image_dicts = [to_dict(image) for image in images]
        print(image_dicts)
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
    
    @app.route('/images/<int:image_id>/mask', methods=['GET'])
    def get_mask(image_id):
        image = Image.query.get(image_id)
        point_coords = request.args.get('markers')
        point_labels = request.args.get('labels')

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

        MASKS_DIR = f"/Users/arogya/play/sam-test/masks/{image.path.split("/")[-1].split(".png")[0]}"
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

        image.date_updated = datetime.now()

        db.session.commit()
        return jsonify(to_dict(image))

