import argparse
import os
import importlib.util
import imageio
import imghdr
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
parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)

# Add arguments for the filenames, fps, and size
parser.add_argument('filenames', nargs='+', help='list of filenames to include in the gif')
parser.add_argument('-n', '--name', default='animated.gif', help='The name of the GIF')
parser.add_argument('-f', '--fps', type=int, default=10, help='frame rate of the gif (frames per second)')
parser.add_argument('-s', '--size', type=int, nargs=2, default=(320, 320), help='width and height of the gif in pixels')
parser.add_argument('-o', '--output-directory', default=os.path.dirname(os.path.abspath(__file__)), help='The directory where the output GIF should be saved')
# Add the `--loop` flag
parser.add_argument('-l', '--loop', type=int, default=0, help='The number of times the GIF should loop, -1 = infinte, 0 = once, positive = number, cannot work with duration')
# Add the `--duration` flag
parser.add_argument('-d', '--duration', type=int, default=None, help='The total duration of the output GIF in seconds, cannot work with loop')
# Add the `--compression` flag
parser.add_argument('-c', '--compression', type=int, default=9987, help='The level of compression to be used for the output GIF, cannot work with target-size')
# Add the `--target-size` flag
parser.add_argument('-t', '--target-size', type=int, default=None, help='The target size of the output GIF in bytes, cannot work with compression')

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
        continue

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

# Check if both the --compression and --target-size flags were specified
if args.compression is not 9987 and args.target_size is not None:
    print('Error: The --compression and --target-size flags are mutually exclusive')
    exit()

# Check if the --compression flag was specified
if args.compression is 9987:
    # Calculate the total size of the input images in bytes
    total_size = 0
    for img in image_list:
        total_size += img.nbytes

    # Calculate the ratio of the target size to the total size of the input images
    size_ratio = args.target_size / total_size

    # Calculate the level of compression to use based on the size ratio
    compression = int(size_ratio * 100)
else:
    # Use the value of the --compression flag as the level of compression
    compression = args.compression


# Check if both the `--loop` and `--duration` flags were specified
if args.loop is not None and args.duration is not None:
    print('Error: The --loop and --duration flags cannot be used together')
    exit()

# Check if the `--loop` or `--duration` flags were specified
if args.loop is not None or args.duration is not None:
    # Set the `duration` argument to the duration of the output gif in seconds
    duration = args.duration
    if args.loop == -1:
        # Set the duration to None if the gif should loop indefinitely
        duration = None
    else:
        # Calculate the duration of the gif in seconds
        duration = len(image_list) / args.fps
        if args.loop > 0:
            # Multiply the duration by the number of times the gif should loop
            duration *= args.loop

# Create the output directory if it doesn't exist
if not os.path.isdir(args.output_directory):
    os.makedirs(args.output_directory)

if not os.path.isdir(args.output_directory):
    print(f'Error: {args.output_directory} is not a valid directory')
    exit(1)

output_path = os.path.abspath(args.output_directory)
imageio.mimwrite(os.path.join(output_path, args.name + '.gif'), image_list, fps=args.fps, loop=args.loop, compression=compression)



#usage
#python create_gif.py img1.jpg img2.png img3.jpeg -n my_gif.gif -f 15 -s 512 512 -o gif_output_dir -l -c 5
#python pypngtogif.py image1.png image2.png image3.png --name [name of output] --fps [fps of gif] --size [size of output gif] --output-directory [directory to save] -l 3 -c 5
#note!: the compression and target size flags cannot be used together, the program will exit
#note!: the duration and  size flags cannot be used together, the program will exitS