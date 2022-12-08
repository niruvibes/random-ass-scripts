import argparse
import imageio
import importlib.util
import subprocess

# Check if the imageio library is installed
if importlib.util.find_spec('imageio') is None:
    # Install the library if it is not installed
    subprocess.run(['pip', 'install', 'imageio'])

# Create an ArgumentParser object
parser = argparse.ArgumentParser()

# Add arguments for the filenames and fps
parser.add_argument('filenames', nargs='+', help='list of filenames to include in the gif')
parser.add_argument('--fps', type=int, default=10, help='frame rate of the gif (frames per second)')

# Parse the command-line arguments
args = parser.parse_args()

# Create an empty list to hold the images
image_list = []

# Iterate over the list of filenames
for filename in args.filenames:
    # Load each image into memory
    img = imageio.imread(filename)
    # Add the image to the list of images
    image_list.append(img)

# Save the image list as a gif
imageio.mimwrite('animated.gif', image_list, fps=args.fps)
