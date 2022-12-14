import argparse
import os
import importlib.util
import imageio
import imghdr
import subprocess
import numpy
from PIL import Image

# Check if the imageio library is installed using importlib.util.find_spec
spec = importlib.util.find_spec('imageio')
if spec is None:
    # Install the imageio library if it is not installed
    subprocess.run(['pip', 'install', 'imageio'])
else:
    # Import the imageio library if it is installed
    import imageio

# Check if the Pillow library is installed using importlib.util.find_spec
spec = importlib.util.find_spec('Pillow')
if spec is None:
    # Install the Pillow library if it is not installed
    subprocess.run(['pip', 'install', 'Pillow'])
else:
    # Import the Pillow library if it is installed
    from PIL import Image

# Create an ArgumentParser object
parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)



# Add arguments for the filenames, fps, size and loop
parser.add_argument('filenames', nargs='+', help='list of filenames to include in the gif')
parser.add_argument('-n', '--name', default='animated.gif', help='The name of the GIF')
parser.add_argument('-f', '--fps', type=int, default=10, help='frame rate of the gif (frames per second)')
parser.add_argument('-s', '--size', type=int, nargs=2, default=(320, 320), help='width and height of the gif in pixels')
parser.add_argument('-o', '--output-directory', default=os.path.dirname(os.path.abspath(__file__)), help="The directory where the output GIF should be saved, it should make it if it doesn't exist")
parser.add_argument('-l', '--loop', type=int, default=0, help='The number of times the GIF should loop, 0 = infinte, positive = number')
# # Add the `--duration` flag
# parser.add_argument('-d', '--duration', type=int, default=None, help='The total duration of the output GIF in seconds, cannot work with loop')
# # Add the `--compression` flag
# parser.add_argument('-c', '--compression', type=int, default=9987, help='The level of compression to be used for the output GIF, cannot work with target-size')
# # Add the `--target-size` flag
# parser.add_argument('-t', '--target-size', type=int, default=None, help='The target size of the output GIF in bytes, cannot work with compression')

# Parse the command-line arguments
args = parser.parse_args()

# Check that the output directory is a string
if not isinstance(args.output_directory, str):
    print(f'Error: The output directory must be a string, but got: {type(args.output_directory)}')
    exit(1)

# Create an empty list to hold the images
image_list = []

# Check the file type of each input image
for filename in args.filenames:
    file_type = imghdr.what(filename)
    if file_type is None:
        print(f'{filename} is not a valid image file')
        print('sometimes it works anyway but it might look scuffed :)')
        continue

# Iterate over the list of filenames
for filename in args.filenames:
    # Load each image into memory
    try:
        # Read the image file using imageio
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
        # Convert the image to a PIL Image object
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

# # Check if both the --compression and --target-size flags were specified
# if args.compression != 9987 and args.target_size is not None:
#     print('Error: The --compression and --target-size flags are mutually exclusive')
#     exit()

# # Check if the --compression flag was specified
# if args.compression == 9987:
#     # Calculate the total size of the input images in bytes
#     total_size = 0
#     for img in image_list:
#         total_size += img.nbytes

#     # Calculate the ratio of the target size to the total size of the input images
#     size_ratio = args.target_size / total_size

#     # Calculate the level of compression to use based on the size ratio
#     cmp = int(size_ratio * 100)
# else:
#     # Use the value of the --compression flag as the level of compression
#     cmp = args.compression


# # Check if both the `--loop` and `--duration` flags were specified
# if args.loop != 0 and args.duration is not None:
#     print('Error: The --loop and --duration flags cannot be used together')
#     exit()

# # Check if the `--loop` or `--duration` flags were specified
# if args.loop != 0 or args.duration is not None:
#     # Set the `duration` argument to the duration of the output gif in seconds
#     if args.duration is not None:
#         duration_var = args.duration
#     elif args.loop == -1:
#         # Set the duration to None if the gif should loop indefinitely
#         duration_var = None
#     else:
#         # Calculate the duration of the gif in seconds
#         duration_var = len(image_list) / args.fps
#         if args.loop > 0:
#             # Multiply the duration by the number of times the gif should loop
#             duration_var *= args.loop

# Check if the output directory exists
# If not, create it
if not os.path.isdir(args.output_directory):
    os.makedirs(args.output_directory)

# Check if the output directory is valid
if not os.path.isdir(args.output_directory):
    print(f'Error: {args.output_directory} is not a valid directory')
    exit(1)

# Create the absolute path for the output file
output_path = os.path.abspath(args.output_directory)

# Write the images in image_list to the output file
imageio.mimwrite(os.path.join(output_path, args.name + '.gif'), image_list, fps=args.fps, loop=args.loop)

#usage
#python create_gif.py img1.jpg img2.png img3.jpeg -n my_gif.gif -f 15 -s 512 512 -o C:\ -l 3
# options:
#   -h, --help            
#       show this help message and exit
#   -n NAME, --name NAME  
#       The name of the GIF (default: animated.gif)
#   -f FPS, --fps FPS     
#       frame rate of the gif (frames per second) (default: 10)
#   -s SIZE SIZE, --size SIZE SIZE
#       width and height of the gif in pixels (default: (320, 320))
#   -o OUTPUT_DIRECTORY, --output-directory OUTPUT_DIRECTORY
#       The directory where the output GIF should be saved, it should make it if it doesn't exist (default: C:\Users\tharo_ui4bg5f\Documents\GitHub\random-ass-scripts\imagetogif)
#   -l LOOP, --loop LOOP  
#       The number of times the GIF should loop, 0 = infinte, positive = number (default: 0)