from PIL import Image

image = Image.open('delete_picture.png')
size = (800, 768)

if (image.size[0] < size[0]) or (image.size[-1] < size[-1]):
    print('No')
else:
    print('Yes')
