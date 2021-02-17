import numpy as np
from os import walk
from matplotlib import pyplot as plt
import colour


def get_images(path):
    f = []
    for (dirpath, dirnames, filenames) in walk(path):
        f.extend(filenames)
    return f


def imread(filename):
    '''Load a NetPBM image from a file.

    Parameters
    ----------
    filename : str
        image file name

    Returns
    -------
    numpy.ndarray
        a numpy array with the loaded image

    Raises
    ------
    ValueError
        if the image format is unknown or invalid
    '''

    # Read in the file
    if filename[-4:] == '.pbm':
        with open(filename, 'rb') as f:
            contents = f.read()
    else:
        with open(filename, 'rt') as f:
            contents = f.read()

    # Split the file contents in it's constituent tokens.
    tokens = contents.split()
    if tokens[0] == 'P2':
        # Get image dimensions
        width = int(tokens[1])
        height = int(tokens[2])
        maxval = int(tokens[3])

        # Convert all string tokens to integers.
        values = [int(token) for token in tokens[4:]]
        if maxval != 255:
            raise ValueError('Can only support 8-bit images. (ie pixel range 0 - 255)')

        # Create the numpy array, reshaping the data to match that of the image described
        image = np.array(values, dtype=np.uint8)
        return np.reshape(image, (height, width))

    elif tokens[0] == 'P3':
        # Get image dimensions
        width = int(tokens[1])
        height = int(tokens[2])
        maxval = int(tokens[3])

        # Convert all string tokens to integers.
        values = [int(token) for token in tokens[4:]]
        if maxval != 255:
            raise ValueError('Can only support 8-bit images. (ie pixel range 0 - 255)')

        # Create the numpy array, reshaping the data to match that of the image described
        image = np.array(values, dtype=np.uint8)
        return np.reshape(image, (height, width, 3))

    elif tokens[0] == b'P6' or "b'P3":
        width = int(tokens[1])
        height = int(tokens[2])
        maxval = int(tokens[3])

        # Convert all string tokens to integers.
        values = [int(token) for token in tokens[4:]]
        if maxval != 255:
            raise ValueError('Can only support 8-bit images. (ie pixel range 0 - 255)')

        # Create the numpy array, reshaping the data to match that of the image described
        image = np.array(values, dtype=np.uint8)
        return np.reshape(image, (height, width, 3))
    else:
        raise ValueError(f'Unknown format {tokens[0]}')


def imwrite(filename, image):
    '''Save a NetPBM image to a file.

    Parameters
    ----------
    filename : str
        image file name
    image : numpy.ndarray
        image being saved
    '''

    # Extract the image dimensions and check that it is 8bpc
    shape = image.shape
    if image.dtype != np.uint8:
        raise ValueError('Can only support 8-bit images.')

    # Convert the image values to strings.
    # values = image.astype(str)

    # Construct the file contents.
    rows = ''
    for i in range((len(image))):
        for j in range(len(image[i])):
            if type(image[i][j]) == np.ndarray:
                for k in range(len(image[i][j])):
                    rows = rows + (str(image[i][j][k]) + ' ')
            elif type(image[i][j]) == np.uint8:
                rows = rows + (str(image[i][j]) + ' ')
        rows = rows + "\n"

    if len(shape) == 2:
        id = 'P2'
    elif len(shape) == 3:
        id = 'P3'
    header = '\n'.join([id, str(shape[1]), str(shape[0]), str(255)])
    data = rows

    with open(filename, 'w') as f:
        f.write(header)
        f.write('\n')
        f.write(data)


if __name__ == "__main__":
    image_files = get_images('../samples')
    images = []
    saves = []

    # Issue with .read of the .pbm images file
    # image_files.remove('colour-binary.pbm')

    for image in image_files:
        print(image)
        images.append(imread('../samples/' + image))
        saves.append(imwrite('../samples/' + image, images[-1]))
        print('  Passed!')

    x = imread('../samples/rocket.ppm')
    x = colour.rgb2grey(x)

    y = imread('../samples/rocket-greyscale.pgm')
    y = colour.grey2rgb(y)

    plt.imshow(y)
    plt.show()
