import os
import cv2
import numpy as np
from PIL import Image

def apply_geometric_transformations(image):
    rows, cols, ch = image.shape
    
    # Translação
    M_translation = np.float32([[1, 0, 50], [0, 1, 50]])
    translated = cv2.warpAffine(image, M_translation, (cols, rows))
    
    # Rotação
    M_rotation = cv2.getRotationMatrix2D((cols/2, rows/2), 45, 1)
    rotated = cv2.warpAffine(image, M_rotation, (cols, rows))
    
    # Escala
    scaled = cv2.resize(image, None, fx=1.5, fy=1.5, interpolation=cv2.INTER_LINEAR)
    
    # Cisalhamento
    M_shear = np.float32([[1, 0.5, 0], [0.5, 1, 0]])
    sheared = cv2.warpAffine(image, M_shear, (cols + int(rows * 0.5), rows + int(cols * 0.5)))
    
    return translated, rotated, scaled, sheared

def apply_transformations_to_directory(directory):
    for filename in os.listdir(directory):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif')):
            image_path = os.path.join(directory, filename)
            
            img = Image.open(image_path)
            img_array = np.array(img)
            
            # Converte a imagem para o modo RGB se não estiver nesse modo
            if img_array.ndim == 2:
                img_array = cv2.cvtColor(img_array, cv2.COLOR_GRAY2RGB)
            elif img_array.shape[2] == 4:
                img_array = cv2.cvtColor(img_array, cv2.COLOR_RGBA2RGB)
            
            translated, rotated, scaled, sheared = apply_geometric_transformations(img_array)
            
            base_name = os.path.splitext(os.path.basename(image_path))[0]
            if len(base_name) > 50:
                base_name = base_name[:50]
            
            Image.fromarray(translated).save(os.path.join(directory, f'{base_name}_translated.jpg'))
            Image.fromarray(rotated).save(os.path.join(directory, f'{base_name}_rotated.jpg'))
            Image.fromarray(scaled).save(os.path.join(directory, f'{base_name}_scaled.jpg'))
            Image.fromarray(sheared).save(os.path.join(directory, f'{base_name}_sheared.jpg'))

# Diretório contendo as imagens originais
directory = 'papel'
apply_transformations_to_directory(directory)
