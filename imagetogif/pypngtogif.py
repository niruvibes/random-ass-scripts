import argparse
import importlib.util
import imageio
import subprocess
import numpy
from PIL import Image

# Check for the presence of the imageio library using importlib.util.find_spec
spec = importlib.util.find_spec('imageio')
if spec is None:
    # Install the library imageio if it is not installed
    subprocess.run(['pip', 'install', 'imageio'])
else:
    # Import the imageio library if it is installed
    import imageio

# Check for the presence of the Pillow library using importlib.util.find_spec
spec = importlib.util.find_spec('Pillow')
if spec is None:
    # Install the library pillow if it is not installed
    subprocess.run(['pip', 'install', 'Pillow'])
else:
    # Import the Pillow library if it is installed
    from PIL import Image

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
    # Load each image into memory
    try:
        img = imageio.v2.imread(filename)
    except FileNotFoundError:
        # Print an error message if the file does not exist
        print(f'File not found: {filename}')
        continue
    except IOError:
        # Print an error message if there is a problem reading the file
        print(f'Error reading file: {filename}')
        continue
    
    # Convert the image to a NumPy array and resize it
    try:
        # Convert to regular image
        img_image = Image.fromarray(img)
        # Resize the image to the specified size
        img_resize = img_image.resize(args.size)
        # Convert the resized image to a NumPy array
        img_array = numpy.asarray(img_resize)
        # Add the image to the list of images
        image_list.append(img_array)
    except:
        # Print an error message if there was a problem loading the image
        print(f'Failed to load image: {filename}')

# Save the image list as a gif
imageio.mimwrite(args.name + '.gif', image_list, fps=args.fps)
