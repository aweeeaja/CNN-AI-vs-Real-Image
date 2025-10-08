import os
from PIL import Image

# import logging
# from tensorflow.keras.models import load_model

# logging.basicConfig(level=logging.INFO)

# try:
#     model = load_model('model_terlatih.h5')
#     logging.info("Model berhasil dimuat.")
# except Exception as e:
#     logging.error(f"Model gagal dimuat: {str(e)}")


# model.summary()

UPLOAD_FOLDER = 'static/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # Pastikan folder ada
# a gambar (misalnya gambar.jpg)
image_path = 'Untitled-1.png'
image = Image.open(image_path)

# Menyimpan gambar ke dalam folder
new_image_path = os.path.join('static\uploads', "gambar_disimpan.png")
image.save(new_image_path)

print(f"Gambar telah disimpan di {new_image_path}")
