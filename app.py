from flask import Flask, request, jsonify
import cv2
import numpy as np
import os

app = Flask(__name__)

def compare_faces(image1_path, image2_path):
    # Load images
    img1 = cv2.imread(image1_path)
    img2 = cv2.imread(image2_path)
    
    # Convert images to grayscale
    gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
    
    # Load face detector
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    
    # Detect faces
    faces1 = face_cascade.detectMultiScale(gray1, 1.3, 5)
    faces2 = face_cascade.detectMultiScale(gray2, 1.3, 5)
    
    # Compare number of faces detected
    return len(faces1) == len(faces2)

@app.route('/compare', methods=['POST'])
def compare():
    file1 = request.files['file1']
    file2 = request.files['file2']
    
    # Define temporary paths in the mounted volume
    temp_dir = '/app/temp'
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)
        
    image1_path = os.path.join(temp_dir, file1.filename)
    image2_path = os.path.join(temp_dir, file2.filename)
    
    file1.save(image1_path)
    file2.save(image2_path)
    
    try:
        # Compare images
        result = compare_faces(image1_path, image2_path)
    finally:
        # Clean up temporary files
        os.remove(image1_path)
        os.remove(image2_path)
    
    return jsonify({
        'status': True,
        'message': f'Match result is {result}'
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
