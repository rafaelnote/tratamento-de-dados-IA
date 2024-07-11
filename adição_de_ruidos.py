import os
import cv2
import numpy as np
from PIL import Image

def add_gaussian_noise(image, mean=0, std=25):
    """Adiciona ruído gaussiano a uma imagem."""
    row, col, ch = image.shape
    gauss = np.random.normal(mean, std, (row, col, ch)).astype(np.uint8)
    noisy = cv2.add(image, gauss)
    return noisy

def apply_noise_to_directory(directory):
    mean = 0
    std = 25  # Standard deviation of the Gaussian noise
    
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
            
            noisy_image = add_gaussian_noise(img_array, mean, std)
            
            noisy_img = Image.fromarray(noisy_image)
            
            base_name = os.path.splitext(os.path.basename(image_path))[0]
            # Trunca o nome base se for muito longo
            if len(base_name) > 50:
                base_name = base_name[:50]
            
            noisy_img.save(os.path.join(directory, f'{base_name}_noisy.jpg'))

# Diretório contendo as imagens originais
directory = 'papel'
apply_noise_to_directory(directory)


