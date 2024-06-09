from app import app
from PIL import Image
import secrets
import os


def save_picture(form_picture):
    hex = secrets.token_hex(8)
    _, ext = os.path.splitext(form_picture.filename)
    picture_fn = hex + ext
    picture_path = os.path.join(app.root_path, 'static', 'profile_pics', picture_fn)

    print("Picture Path:", picture_path)
    print("Absolute Path:", os.path.abspath(os.path.join(app.root_path, 'static', 'profile_pics')))

    os.makedirs(os.path.abspath(os.path.join(app.root_path, 'static', 'profile_pics')), exist_ok=True)

    image = Image.open(form_picture)
    image.thumbnail((150, 150))
    image.save(picture_path)
    return picture_fn