import imageio

# Create an array of image filenames
images = ['image1.png', 'image2.png', 'image3.png']

# Create an empty list to hold the images
image_list = []

# Iterate over the list of images
for image in images:
    # Load each image into memory
    img = imageio.imread(image)
    # Add the image to the list of images
    image_list.append(img)

# Save the image list as a gif
imageio.mimwrite('animated.gif', image_list, fps=10)
