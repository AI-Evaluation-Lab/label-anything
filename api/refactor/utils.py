import json
from datetime import datetime
from sqlalchemy.ext.declarative import DeclarativeMeta
import os
from models import db, Image


def to_dict(obj):
    # Implementation remains the same
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

def initialize_images():
    # Implementation remains the same
    IMAGES_DIR = "/Users/arogya/play/sam-test/images"
    EMBEDDINGS_DIR = "/Users/arogya/play/sam-test/embeddings"
    masks_json_path = "/Users/arogya/play/sam-test/api/masks.json"
    if os.path.exists(IMAGES_DIR) and os.path.exists(masks_json_path):
        if not os.path.exists(EMBEDDINGS_DIR):
            os.makedirs(EMBEDDINGS_DIR)
        with open(masks_json_path, "r") as f:
            masks_data = json.load(f)
        for filename in os.listdir(IMAGES_DIR):
            path = os.path.join(IMAGES_DIR, filename)
            embedding_path = os.path.join(EMBEDDINGS_DIR, f"{filename.split('.png')[0]}.pt")  # Adjust this based on your implementation
            markers = {mask_data["type"]: [] for mask_data in masks_data}  # Initialize markers dictionary with keys based on type attribute
            marker_labels = {mask_data["type"]: [] for mask_data in masks_data}  # Initialize markers dictionary with keys based on type attribute
            masks = {mask_data["type"]: {"path":"", "background":mask_data["background"], "label":mask_data["label"], "description":mask_data["description"]} for mask_data in masks_data}  # Initialize markers dictionary with keys based on type attribute
            image = Image(date_created=datetime.now(), date_updated=datetime.now(), markers=markers, marker_labels=marker_labels, masks=masks, path=path, embedding_path=embedding_path)
            # Generate embedding and save to embedding_path
            # generate_embedding(path, embedding_path)
            db.session.add(image)
            print("Added image")
        db.session.commit()
