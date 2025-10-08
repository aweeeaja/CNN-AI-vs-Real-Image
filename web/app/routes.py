from app import app
from flask import Flask, request, render_template, redirect, url_for
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array
from PIL import Image
import numpy as np
import os
# try:
#     model = load_model('model.h5')
#     model_loaded = True
# except Exception as e:
#     model_loaded = False
#     load_error = str(e)

# Memuat model CNN yang telah dilatih
model = load_model('model_terlatih.h5')

# Mapping label kelas (sesuaikan dengan model Anda)
class_labels = {0: 'AI', 1: 'Real'}

# Fungsi untuk preprocessing gambar
def preprocess_image(image, target_size=(64, 64)):
    """
    Mengubah ukuran gambar, mengonversinya menjadi array numpy, dan menormalkannya.
    """
    image = image.resize(target_size)  # Ubah ukuran gambar
    image = img_to_array(image)       # Konversi ke array numpy
    image = np.expand_dims(image, axis=0) / 255.0  # Tambahkan dimensi batch dan normalisasi
    return image

def prediction(processed_image):
    # Prediksi menggunakan model
    prediction = model.predict(processed_image)
    prob_class_1 = prediction[0][0]  # Ambil probabilitas untuk kelas 1
    
    # Probabilitas untuk kelas 0 adalah 1 - prob_class_1
    prob_class_0 = 1 - prob_class_1

    # Tentukan kelas dengan probabilitas lebih besar
    if prob_class_1 > prob_class_0:
        predicted_label = class_labels[1]  # Kelas 1
        # confidence = prob_class_1
    else:
        predicted_label = class_labels[0]  # Kelas 0
        # confidence = prob_class_0
    return predicted_label


@app.route('/', methods=['GET'])
def welcome():
    return render_template('welcome.html')

@app.route('/single-upload', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Pastikan file diunggah
        if 'file' not in request.files:
            return render_template('index.html', error='No file uploaded')
        file = request.files['file']
        if file.filename == '':
            return render_template('index.html', error='No file selected')

        # Membaca gambar yang diunggah
        try:
            image = Image.open(file.stream)  # Membaca gambar
            processed_image = preprocess_image(image)  # Preprocessing gambar
            predicted_class = prediction(processed_image)
            # prediction = model.predict(processed_image)
            
            # predicted_class = np.argmax(prediction, axis=-1)[0]  # Ambil kelas dengan probabilitas tertinggi
            # predicted_label = class_labels[predicted_class]

            # Render hasil prediksi
            return render_template('index.html', prediction=predicted_class)
        except Exception as e:
            return render_template('index.html', error=f'Error processing image: {str(e)}')

    return render_template("index.html")


@app.route('/multi-upload', methods=['GET', 'POST'])
def multi_upload():

    if request.method == 'POST':
        # Periksa apakah file diunggah
        if 'files' not in request.files:
            return render_template('multi_upload.html', error='No files uploaded')

        files = request.files.getlist('files')

        # Periksa jumlah file yang diunggah
        if len(files) < 2:
            return render_template('multi_upload.html', error='Please upload at least 2 images')

        predictions = []
        for file in files:
            if file.filename == '':
                return render_template('multi_upload.html', error='One or more files are empty.')

            # Tentukan path untuk menyimpan file
            file_path = os.path.join('app/static/uploads', file.filename)

            try:
                # Simpan file
                file.save(file_path)

                # Proses gambar
                image = Image.open(file_path)
                processed_image = preprocess_image(image)  # Preprocessing gambar
                predicted_class = prediction(processed_image)  # Prediksi gambar
                
                # Append hasil (path gambar dan prediksi)
                predictions.append((url_for('static', filename=f'uploads/{file.filename}'), predicted_class))
            except Exception as e:
                return render_template('multi_upload.html', error=f'Error processing image: {str(e)}')

        # Render hasil prediksi
        return render_template('multi_upload.html', predictions=predictions)
    return render_template('multi_upload.html')

# @app.route('/model-summary')
# def model_summary():
#     if model_loaded:
#         summary = []
#         model.summary(print_fn=lambda x: summary.append(x))
#         return jsonify(summary)
#     else:
#         return "Model belum dimuat."
    
# from flask import render_template

# @app.route('/')
# def index():
#     if model_loaded:
#         message = "Model berhasil dimuat dan siap digunakan!"
#     else:
#         message = f"Model gagal dimuat: {load_error}"
#     return render_template('coba.html', message=message)
