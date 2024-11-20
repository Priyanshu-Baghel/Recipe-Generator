from flask import render_template ,url_for,flash,redirect,request
from Foodimg2Ing import app
from Foodimg2Ing.output import output
import os
import logging

logging.basicConfig(level=logging.DEBUG)

@app.route('/',methods=['GET'])
def home():
    return render_template('home.html')

@app.route('/about',methods=['GET'])
def about():
    return render_template('about.html')

@app.route('/', methods=['POST', 'GET'])
def predict():
    try:
        imagefile = request.files.get('imagefile')
        if not imagefile:
            return "No file uploaded", 400
        
        # Ensure the directory exists
        image_dir = os.path.join(app.root_path, 'static', 'images', 'demo_imgs')
        os.makedirs(image_dir, exist_ok=True)

        # Construct the image path
        image_path = os.path.join(image_dir, imagefile.filename)
        
        # Remove existing file if any
        if os.path.exists(image_path):
            os.remove(image_path)
        
        # Save the uploaded file
        imagefile.save(image_path)

        # Generate response data
        img = f"/images/demo_imgs/{imagefile.filename}"
        title, ingredients, recipe = output(image_path)
        return render_template('predict.html', title=title, ingredients=ingredients, recipe=recipe, img=img)

    except PermissionError as e:
        return f"Permission error: {e}", 500
    except Exception as e:
        return f"Unexpected error: {e}", 500


@app.route('/<samplefoodname>')
def predictsample(samplefoodname):
    imagefile=os.path.join(app.root_path,'static\\images',str(samplefoodname)+".jpg")
    img="/images/"+str(samplefoodname)+".jpg"
    title,ingredients,recipe = output(imagefile)
    return render_template('predict.html',title=title,ingredients=ingredients,recipe=recipe,img=img)