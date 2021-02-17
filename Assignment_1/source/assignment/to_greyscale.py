import numpy as np
import sys
import os


def rgb2grey(image):
    '''Convert a RGB colour image into a greyscale image.

    The image is converted into RGB by taking a weighted sum of the three colour
    channels.  I.e.,

    .. math::

        I(x,y) = 0.299 R(x,y) + 0.587 G(x,y) + 0.114 B(x,y).

    The image should be converted to floating point prior to the calculation so
    that it's on [0, 1].  After generating the greyscale image, it should be
    converted back to 8bpc.

    Parameters
    ----------
    image : numpy.ndarray
        a 3-channel, RGB image

    Returns
    -------
    numpy.ndarray
        a single channel, monochome image derived from the original

    Raises
    ------
    ValueError
        if the image is already greyscale or if the input image isn't 8bpc
    '''
    if len(image.shape) == 2:
        raise ValueError('Image is already monochrome')
    if image.dtype != np.uint8:
        raise ValueError('Can only support 8-bit images.')

    for i in range(len(image)):
        for j in range(len(image[i])):
            image[i][j] = 0.299 * image[i][j][0] + 0.587 * image[i][j][1] + 0.114 * image[i][j][2]

    return image


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
    '''
    Save a NetPBM image to a file.
    Parameters
    ----------
    filename : str
        image file name
    image : numpy.ndarray
        image being saved
    '''

    try:
        os.mknod(filename)
    except:
        print('This file already exists')

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
        print('Image saved as... ' + filename)


def main():
    # Checks that input is
    print(sys.argv)
    if len(sys.argv) != 2:
        raise ValueError("This file must take two arguments...\nex --> python3 to_greyscale.py /path/to/image /path/to/target/directory/")

    input_image = sys.argv[0]
    output_image = sys.argv[1]

    # Checks if input image exists
    if os.path.exists(input_image):
        pass
    else:
        print(f"Image '{input_image}' does not exist")
        exit()

    # Checks format of input image (.ppm)
    if input_image[-4:] != '.ppm':
        raise ValueError('Image must be .ppm format.')
        exit()

    # Converts the image to greyscale
    greyscale_image = rgb2grey(imread(input_image))

    # Save the grey scale image
    imwrite(output_image, greyscale_image)


if __name__ == "__main__":
    # sys.argv = ['../samples/rocket.ppm', 'rocket_greyscale.pgm']
    main()
    '''input = '../samples/rocket.ppm'

    image = imread(input)
    file = imwrite(input, image)

    # os.mknod('test')'''
