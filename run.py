import base64
from flask import Flask, request, render_template, flash, redirect, session, url_for
from transformers import ViTImageProcessor, TFViTForImageClassification
from PIL import Image
import io
import tensorflow as tf
from dotenv import load_dotenv, dotenv_values
from app.utils import save_incorrect_prediction, get_nutrition_info, preprocess_nutrition_info

load_dotenv()

app = Flask(__name__)
app.secret_key = dotenv_values('.env').get('SECRET_KEY')

# processor and model setup
model = "google/vit-base-patch16-224"
processor = ViTImageProcessor.from_pretrained(model)
model = TFViTForImageClassification.from_pretrained(model)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict_photo():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url) # refresh page on an error
    
    file = request.files['file']
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    
    # file was attaached successfully
    if file:
        try:
            image = Image.open(io.BytesIO(file.read()))
            # Convert image for displaying in HTML
            img_io = io.BytesIO()
            image.save(img_io, 'JPEG', quality=70)
            img_io.seek(0)
            image_data = base64.b64encode(img_io.getvalue()).decode('utf-8')

            
            # process the image to be suitable for model
            inputs = processor(images=image, return_tensors="tf")
            
            outputs = model(**inputs)
            logits = outputs.logits
            predicted_class_idx = tf.argmax(logits, axis=1).numpy()[0].item()
            predicted_label = model.config.id2label[predicted_class_idx];
            
            return render_template('verify_prediction.html', predicted_label=predicted_label, image_data=image_data)
        except Exception as e:
            flash('Error processing the image')
            return redirect(request.url)
    return redirect(url_for('index'))

@app.route('/result', methods=['POST'])
def result():
    image_data = request.form['image_data']
    predicted_label = request.form['predicted_label']
    actual_label = request.form['actual_label']
    correct_prediction = request.form['is_correct'] == 'true'

    # if result is incorrect, save the incorrect prediction to database, generating dataset to fine tune on later
    if not correct_prediction:
        nutrition_info = get_nutrition_info(actual_label)
        food_id = nutrition_info.get('fdcId')
        save_incorrect_prediction(food_id, image_data, actual_label, nutrition_info)
        label = actual_label
    else:
        nutrition_info = get_nutrition_info(predicted_label)
        label = predicted_label
    
    processed_nutrition_info = preprocess_nutrition_info(nutrition_info)
    return render_template('result.html', image_data=image_data, food_label=label, correct_prediction=correct_prediction, nutrition_info=processed_nutrition_info)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=3000, debug=True)