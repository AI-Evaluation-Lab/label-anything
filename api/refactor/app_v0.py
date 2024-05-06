from flask import Flask, request, send_file, jsonify
import os
from PIL import Image, ImageDraw
import json
import random
import io
from io import BytesIO
import numpy as np
from flask_cors import CORS


from embeddings import generate_embeddings, mask_predictor


IMAGES_PATH = '/Users/arogya/play/sam-test/images'
EMBEDDINGS_PATH = '/Users/arogya/play/sam-test/embeddings'


## Uncomment to regenerate embeddings
# generate_embeddings()

app = Flask(__name__)
CORS(app)

@app.route('/listFiles')
def list_files():
    folder_path = IMAGES_PATH
    files = os.listdir(folder_path)
    return jsonify(files)




@app.route('/image/<path:image_name>')
def get_image(image_name):
    # Assuming images are stored in a folder named 'images'
    image_path = os.path.join(IMAGES_PATH, image_name)
    if os.path.exists(image_path):
        return send_file(image_path, mimetype='image/png')
    else:
        return 'Image not found', 404



# @app.route('/getMask/<image_id>', methods=['GET'])
# def get_mask(image_id):
#     markers = request.args.get('markers')
#     if markers:
#         markers = json.loads(markers)
#         # markers = np.array([[item['x'], item['y']] for item in markers])
#     else:
#         markers = []

#     mask_predictor.load_image_embedding(f'{EMBEDDINGS_PATH}/{image_id}.pt')

#     # print(markers)


#     m, s, l = mask_predictor.predict(
#         point_coords=markers,
#         point_labels=np.array([1 for item in markers]),
#         multimask_output=False,
#     )

#     m = m[0]

#     # mask_image_2 = np.where(m==True, 255, 0)
#     # print(type(mask_image_2))
#     # mask_image_2 = Image.fromarray(mask_image_2)
    
#     # # print
#     # Generate a random mask within an 800x800 region
#     mask_image = Image.new('L', (800, 800), 0)
#     draw = ImageDraw.Draw(mask_image)
#     for _ in range(2):  # Generate 100 random masks
#         x1 = random.randint(0, 700)
#         y1 = random.randint(0, 700)
#         x2 = x1 + 100
#         y2 = y1 + 100
#         draw.rectangle([x1, y1, x2, y2], fill=255)


   
#     # Save the mask image to a byte stream
#     mask_byte_array = io.BytesIO()
#     mask_image.save(mask_byte_array, format='PNG')
#     mask_byte_array.seek(0)

#     return send_file(mask_byte_array, mimetype='image/png')

@app.route('/getMask/<image_id>', methods=['GET'])
def get_mask(image_id):
    markers = request.args.get('markers')
    if markers:
        markers = json.loads(markers)
        markers = np.array([[item['x'], item['y']] for item in markers])

    else:
        markers = []


    mask_predictor.load_image_embedding(f'{EMBEDDINGS_PATH}/{image_id}.pt')
    m, s, l = mask_predictor.predict(
        point_coords=markers,
        point_labels=np.array([1 for item in markers]),
        multimask_output=False,
    )

    # Create mask image
    im2 = np.array(m[0], dtype=np.uint8) * 255
    im2 = Image.fromarray(im2)

    # Save the mask image to a byte stream
    mask_byte_array = io.BytesIO()
    im2.save(mask_byte_array, format='PNG')
    mask_byte_array.seek(0)

    return send_file(mask_byte_array, mimetype='image/png')



if __name__ == '__main__':
    app.run(debug=True)