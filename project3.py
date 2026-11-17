# CPS121 Project 3
#   Can be done using just getPixels()
#   Y Altering colors of the image
#   Y Grayscale
#   N Making darker or lighter
#   Y Sepia-toned
#   Y Posterized
#   Need nested loops
#   Y Mirrorizing
#   Y Edge detection
#   N Chromakey (change background)
#   N Blurring
#   Need nested loops and alter size or shape
#   Y Rotation
#   N Cropping
#   N Shifting
#   Other transformations
#   Y Inverting RGB values (negative)
#   N Additional transformation
#   N Additional transformation
# ============================================================================

import GCPictureTools as pgt
import pygame as pg
import os, sys
import traceback

# ============================================================================
# ================ Start making changes after this comment ===================
# ============================================================================

def recolor(picture, effect):
    """Return a copy with a color effect applied to each pixel.

    Args:
        picture (Picture): Source image.
        effect (str): gray, sepia, poster, cool, or negative.
    Returns:
        Picture: The transformed copy.
    Raises:
        ValueError: If the effect is unknown.
    """
    if effect not in ("gray", "sepia", "poster", "cool", "negative"):
        raise ValueError("Unknown color effect: " + effect)

    result = pgt.Picture(picture)
    for pixel in result.getPixels():
        red, green, blue = pixel.getColorRGB()
        gray = (30 * red + 59 * green + 11 * blue) // 100

        if effect == "gray":
            color = (gray, gray, gray)
        elif effect == "sepia":
            color = (min(255, int(gray * 1.16)),
                     int(gray * 0.98), int(gray * 0.76))
        elif effect == "poster":
            color = (min(255, (red // 64) * 85),
                     min(255, (green // 64) * 85),
                     min(255, (blue // 64) * 85))
        elif effect == "cool":
            color = (int(red * 0.78), min(255, green + 12),
                     min(255, blue + 32))
        else:
            color = (255 - red, 255 - green, 255 - blue)
        pixel.setColor(color)
    return result


def rearrange(picture, effect):
    """Return a mirror image or a 180-degree rotation.

    Args:
        picture (Picture): Source image.
        effect (str): mirror or rotate.
    Returns:
        Picture: The transformed copy, with the source dimensions.
    Raises:
        ValueError: If the effect is unknown.
    """
    if effect not in ("mirror", "rotate"):
        raise ValueError("Unknown position effect: " + effect)
    width, height = picture.getWidth(), picture.getHeight()
    result = pgt.Picture(width, height)

    for row in range(height):
        new_row = row
        if effect == "rotate":
            new_row = height - 1 - row
        for col in range(width):
            new_col = width - 1 - col
            result.setColor(new_col, new_row, picture.getColor(col, row))
    return result


def findEdges(picture, threshold):
    """Highlight brightness changes between neighboring pixels.

    Args:
        picture (Picture): Source image.
        threshold (int): Minimum brightness difference that draws an edge.
    Returns:
        Picture: Light blue edges on a dark blue background.
    """
    gray = recolor(picture, "gray")
    width, height = gray.getWidth(), gray.getHeight()
    result = pgt.Picture(width, height, (19, 37, 52))

    for row in range(height - 1):
        for col in range(width - 1):
            center = gray.getRed(col, row)
            right = gray.getRed(col + 1, row)
            below = gray.getRed(col, row + 1)
            difference = max(abs(center - right), abs(center - below))
            if difference >= threshold:
                strength = min(255, 100 + 3 * difference)
                result.setColor(col, row, (strength // 2, strength, strength))
    return result


def createCollage():
    """Build a six-panel collage from the original mountain-lake image.

    Returns:
        Picture: The completed 700-by-950 collage.
    Raises:
        FileNotFoundError: If the source image is missing.
        pygame.error: If pygame cannot load the source image.
    """
    source = os.path.join(os.path.dirname(__file__), "mountain-lake.png")
    original = pgt.Picture(source)
    collage = pgt.Picture(700, 950, (234, 226, 211))

    variants = [
        (original, (216, 131, 93)),
        (recolor(rearrange(original, "mirror"), "cool"), (68, 135, 153)),
        (recolor(original, "sepia"), (163, 111, 66)),
        (recolor(original, "poster"), (114, 81, 156)),
        (recolor(rearrange(original, "rotate"), "negative"), (41, 106, 133)),
        (findEdges(original, 14), (54, 111, 128)),
    ]
    for index, (picture, accent) in enumerate(variants):
        col = 32 + (index % 2) * 332
        row = 66 + (index // 2) * 284
        width, height = picture.getWidth(), picture.getHeight()
        collage.addRectFilled(width + 8, height + 16, col - 4, row - 4,
                              (248, 243, 231))
        picture.copyInto(collage, col, row)
        collage.addRectFilled(width, 5, col, row + height + 3, accent)

    collage.addLine((131, 108, 87), 32, 43, 668, 43)
    collage.addLine((131, 108, 87), 32, 914, 668, 914)
    return collage


def createWebPage(imageFile, webPageFile):
    from html import escape
    from urllib.parse import quote

    if len(sys.argv) > 2 and __name__ == "__main__":
        webPageFile = sys.argv[2]
    page_folder = os.path.dirname(os.path.abspath(webPageFile))
    image_path = os.path.relpath(imageFile, page_folder).replace(os.sep, "/")
    image_url = escape(quote(image_path), quote=True)

    with open(webPageFile, "w", encoding="utf-8") as htmlFile:
        htmlFile.write("<!doctype html>\n")
        htmlFile.write("<head>\n")
        htmlFile.write('<meta charset="utf-8">\n')
        htmlFile.write("<title>Project3</title>\n")
        htmlFile.write("</head>\n")
        htmlFile.write("<body>\n")
        htmlFile.write("<h1>Project3</h1>\n")
        htmlFile.write("<p>Six versions of a mountain lake.</p>\n")
        htmlFile.write(f'<img src="{image_url}" alt="Mountain lake collage">\n')
        htmlFile.write("</body>\n")
        htmlFile.write("</html>\n")
    print("output file:", webPageFile)


# ============================================================================
# ============== Do NOT make any changes below this comment ==================
# ============================================================================

if __name__ == '__main__':

    # first command line argument, if any, is name of image file for output
    # second command line argument, if any, is name of the output html file name
    collageFile = None
    htmlFileName = "webpage.html"  #Default name

    if len(sys.argv) > 1:
        collageFile = sys.argv[1]
    if len(sys.argv) > 2:
        htmlFile = sys.argv[2]    

    # temporarily set media path to project directory
    scriptDir = os.path.dirname(os.path.realpath(sys.argv[0]))

    # create the collage
    
    collage = createCollage()
    #collage.display()

    try:
        # either show collage on screen or write it to file
        if collageFile is None:
            collage.display()
            input('Press Enter to quit...')
        else:
            print(f'Saving collage to {collageFile}')
            collage.save(collageFile)
            createWebPage(collageFile, htmlFileName)
    except:
        print('Could not show or save picture')

