import os
from PIL import Image
from argparse import ArgumentParser

# Create an ArgumentParser object
parser = ArgumentParser()

# Add arguments for the GIF name and FPS
parser.add_argument('-n', '--name', default='animated.gif', help='The name of the GIF')
parser.add_argument('-f', '--fps', type=int, default=10, help='The FPS of the GIF')

# Parse the arguments
args = parser.parse_args()

# Get the list of images in the current directory
images = [f for f in os.listdir('.') if f.endswith('.jpg')]

# Open the first image and get the size
first_image = Image.open(images[0])
width, height = first_image.size

# Create an empty image with the same size
gif_image = Image.new('RGB', (width, height))

# Open all of the images and convert them to RGB mode
image_list = []
for image in images:
    img = Image.open(image)
    img = img.convert('RGB')
    image_list.append(img)

# Save the images as a GIF
gif_image.save(args.name, save_all=True, append_images=image_list, duration=1000//args.fps)
