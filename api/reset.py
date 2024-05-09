# from sqlalchemy import MetaData
# from flask_app import db, initialize_images, app
# from dotenv import load_dotenv
# import shutil
# import os
# from pathlib import Path
# from embeddings import generate_embeddings


# load_dotenv()
# # Dropping all files

# def delete_contents(folder):
#     folder = os.getenv(folder)
#     print(f'Cleaning up: {folder}')
#     shutil.rmtree(folder)
#     Path(folder).mkdir(exist_ok=True, parents=True)

# # for folder in ['MASKS_DIR', 'EMBEDDINGS_DIR']:
# delete_contents('MASKS_DIR')

# # delete_contents('EMBEDDINGS_DIR')
# # generate_embeddings(os.getenv('IMAGES_DIR'), os.getenv('EMBEDDINGS_DIR'))
# # initialize_images()


# # Resetting database
# with app.app_context():
#     print("Here")
#     meta = MetaData()
#     meta.reflect(bind=db.engine)
#     meta.drop_all(bind=db.engine)

#     # Recreate tables
#     db.create_all()
