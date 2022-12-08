import argparse
import imageio.v2 as imageio
import importlib.util
import subprocess
from PIL import Image

# Check if the imageio and Pillow libraries are installed
if importlib.util.find_spec('imageio') is None or importlib.util.find_spec('Pillow') is None:
    # Install the libraries if they are not installed
    subprocess.run(['pip', 'install', 'imageio'])
    subprocess.run(['pip', 'install', 'Pillow'])

# Create an ArgumentParser object
parser = argparse.ArgumentParser()

# Add arguments for the filenames, fps, and size
parser.add_argument('filenames', nargs='+', help='list of filenames to include in the gif')
parser.add_argument('--fps', type=int, default=10, help='frame rate of the gif (frames per second)')
parser.add_argument('--size', type=int, nargs=2, default=(640, 480), help='width and height of the gif in pixels')

# Parse the command-line arguments
args = parser.parse_args()

# Create an empty list to hold the images
image_list = []

# Iterate over the list of filenames
for filename in args.filenames:
    # Load each image into memory
    img = Image.open(filename)
    # Resize the image to the specified size
    img = img.resize(args.size)
    # Convert the image to a NumPy array
    img = imageio.imread(filename)
    # Add the image to the list of images
    image_list.append(img)

# Save the image list as a gif (for some reason this wont support v3)
imageio.mimwrite('animated.gif', image_list, fps=args.fps)
