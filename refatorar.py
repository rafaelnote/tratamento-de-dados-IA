from PIL import Image, ImageOps
import os

def augment_image_in_directory(directory):
    # Lista todos os arquivos no diretório
    for filename in os.listdir(directory):
        # Verifica se o arquivo é uma imagem suportada pelo PIL
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif')):
            # Caminho completo da imagem
            image_path = os.path.join(directory, filename)
            
            # Abre a imagem
            img = Image.open(image_path)
            
            # Converte a imagem para o modo RGB se não estiver nesse modo
            if img.mode != 'RGB':
                img = img.convert('RGB')
            
            # Extrai o nome base do arquivo sem a extensão
            base_name = os.path.splitext(os.path.basename(image_path))[0]
            
            # Gira a imagem para a esquerda
            left_rotated = img.rotate(90, expand=True)
            left_rotated.save(os.path.join(directory, f'{base_name}_esquerda.jpg'))
            
            # Gira a imagem para a direita
            right_rotated = img.rotate(-90, expand=True)
            right_rotated.save(os.path.join(directory, f'{base_name}_direita.jpg'))
            
            # Gira a imagem de cabeça para baixo
            upside_down = img.rotate(180, expand=True)
            upside_down.save(os.path.join(directory, f'{base_name}_cabeça_para_baixo.jpg'))
            
            # Converte a imagem para preto e branco
            black_white = ImageOps.grayscale(img)
            black_white.save(os.path.join(directory, f'{base_name}_black_white.jpg'))

# Diretório contendo as imagens originais
directory = 'papel'
augment_image_in_directory(directory)
