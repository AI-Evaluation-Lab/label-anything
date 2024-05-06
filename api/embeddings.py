import os
import torch
from segment_anything import sam_model_registry, SamPredictor
import cv2
from pathlib import Path

from tqdm import tqdm

DEVICE = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
CHECKPOINT_PATH='models/sam_vit_h_4b8939.pth'
MODEL_TYPE = "vit_h"

IMAGES_PATH = 'images'
EMBEDDINGS_PATH = 'embeddings'

class SamPredictorExtended(SamPredictor):
    """Extend SamPredictor to enable loading and saving images from files."""

    def save_image_embedding(self, path):
        if not self.is_image_set:
            raise RuntimeError("An image must be set with .set_image(...) before embedding saving.")
        res = {
            'original_size': self.original_size,
            'input_size': self.input_size,
            'features': self.features,
            'is_image_set': True,
        }
        torch.save(res, path)

    def load_image_embedding(self, path):
        res = torch.load(path, self.device)
        for k, v in res.items():
            setattr(self, k, v)


sam = sam_model_registry[MODEL_TYPE](checkpoint=CHECKPOINT_PATH).to(device=DEVICE)  
mask_predictor = SamPredictorExtended(sam)

def generate_embeddings(images_path=IMAGES_PATH, out_dir=EMBEDDINGS_PATH):

    Path(out_dir).mkdir(exist_ok=True, parents=False)
    images = os.listdir(images_path)

    for image in tqdm(images, desc= "Generating embeddings"):
        im = cv2.imread(f'{images_path}/{image}')
        im_rgb = cv2.cvtColor(im, cv2.COLOR_BGR2RGB)

        mask_predictor.set_image(im_rgb)
        embedding_name =  image.split('.png')[0]
        mask_predictor.save_image_embedding(f'{out_dir}/{embedding_name}.pt')
        print('Saved embedding:', f'{out_dir}/{embedding_name}.pt')
