import argparse
import imageio
import importlib
import subprocess
from PIL import Image

# Check if the imageio and Pillow libraries are installed
if importlib.find_loader('imageio') is None or importlib.find_loader('Pillow') is None:
    # Install the libraries if they are not installed
    subprocess.run(['pip', 'install', 'imageio'])
    subprocess.run(['pip', 'install', 'Pillow'])

# Create an ArgumentParser object
parser = argparse.ArgumentParser()

# Add arguments for the filenames, fps, and size
parser.add_argument('filenames', nargs='+', help='list of filenames to include in the gif')
parser.add_argument('-n', '--name', default='animated.gif', help='The name of the GIF')
parser.add_argument('-f', '--fps', type=int, default=10, help='frame rate of the gif (frames per second)')
parser.add_argument('-s', '--size', type=int, nargs=2, default=(320, 320), help='width and height of the gif in pixels')

# Parse the command-line arguments
args = parser.parse_args()

# Create an empty list to hold the images
image_list = []

# Iterate over the list of filenames
for filename in args.filenames:
    try:
        # Load each image into memory
        img = Image.open(filename)
    except FileNotFoundError:
        # Print an error message if the file does not exist
        print(f'File not found: {filename}')
        continue
    except IOError:
        # Print an error message if there is a problem reading the file
        print(f'Error reading file: {filename}')
        continue
    try:
        # Resize the image to the specified size
        img = img.resize(args.size)
        # Convert the resized image to a NumPy array
        img = imageio.v2.imread(filename)
        # Add the image to the list of images
        image_list.append(img)
    except:
        # Print an error message if there was a problem loading the image
        print(f'Failed to load image: {filename}')

# Save the image list as a gif
imageio.mimwrite(args.name + '.gif', image_list, fps=args.fps)
