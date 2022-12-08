from PIL import Image

# Open the first image and get the size
first_image = Image.open('image1.jpg')
width, height = first_image.size

# Create an empty image with the same size
gif_image = Image.new('RGB', (width, height))

# Open all of the images and convert them to RGB mode
image_list = []
for i in range(1, 10):
    image = Image.open(f'image{i}.jpg')
    image = image.convert('RGB')
    image_list.append(image)

# Save the images as a GIF
gif_image.save('animated.gif', save_all=True, append_images=image_list)
