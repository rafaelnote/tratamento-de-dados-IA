import os
import cv2
import numpy as np
from PIL import Image

def elastic_transform(image, alpha, sigma, random_state=None):
    if random_state is None:
        random_state = np.random.RandomState(None)
    
    shape = image.shape
    shape_size = shape[:2]
    
    dx = random_state.rand(*shape_size) * 2 - 1
    dy = random_state.rand(*shape_size) * 2 - 1
    
    dx = cv2.GaussianBlur(dx * alpha, (17, 17), sigma)
    dy = cv2.GaussianBlur(dy * alpha, (17, 17), sigma)
    
    x, y = np.meshgrid(np.arange(shape[1]), np.arange(shape[0]))
    map_x = (x + dx).astype(np.float32)
    map_y = (y + dy).astype(np.float32)
    
    distorted_image = cv2.remap(image, map_x, map_y, interpolation=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT_101)
    return distorted_image

def apply_elastic_transform_to_directory(directory):
    alpha = 34
    sigma = 4
    
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
            
            transformed = elastic_transform(img_array, alpha, sigma)
            
            transformed_img = Image.fromarray(transformed.astype(np.uint8))
            
            base_name = os.path.splitext(os.path.basename(image_path))[0]
            
            transformed_img.save(os.path.join(directory, f'{base_name}_elastic.jpg'))

# Diretório contendo as imagens originais
directory = 'papel'
apply_elastic_transform_to_directory(directory)
