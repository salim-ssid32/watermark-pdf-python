#!/usr/bin/python3
# This code is written by ssid32

print("give me a bottle of rum!")

from os.path import exists
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from PIL import ImageEnhance
from pdf2image import convert_from_path, convert_from_bytes
from wand.image import Image as wimage
import io


def text2image(text):
    width=854
    height=480
    opacity=0.8
    black = (0,0,0)
    white = (255,255,255)
    transparent = (0,0,0,0)
    assert exists('Arial.ttf'), "Missing Font File Arial.ttf"
    font = ImageFont.truetype('Arial.ttf',100)
    wm = Image.new('RGBA',(width,height),transparent)
    im = Image.new('RGBA',(width,height),transparent) # Change this line too.

    draw = ImageDraw.Draw(wm)
    w,h = draw.textsize(text, font)
    draw.text(((width-w)/2,(height-h)/2),text,black,font)
    
    en = ImageEnhance.Brightness(wm)
    mask = en.enhance(1-opacity)
    im.paste(wm,(25,25),mask)
    return im



def load_pdf(path):
    assert exists(path), "Your PDF file doesn't exist"
    return convert_from_path(path)


def load_pdf2(filepath):
    assert exists(filepath), "Your PDF file doesn't exist"
    page_images = []
    with wimage(filename=filepath, resolution=200) as img:
        for page_wand_image_seq in img.sequence:
            page_wand_image = wimage(page_wand_image_seq)
            page_jpeg_bytes = page_wand_image.make_blob(format="jpeg")
            page_jpeg_data = io.BytesIO(page_jpeg_bytes)
            page_image = Image.open(page_jpeg_data)
            page_images.append(page_image)
    return page_images

def create_watermark2(main, mark):
    print("starting...")
    #mask = mark.convert('L').point(lambda x: min(x, 25))
    #mark.putalpha(mask)

    mark_width, mark_height = mark.size
    main_width, main_height = main.size
    aspect_ratio = mark_width / mark_height
    new_mark_width = main_width * 0.25
    mark.thumbnail((new_mark_width, new_mark_width / aspect_ratio), Image.ANTIALIAS)

    tmp_img = Image.new('RGB', main.size)

    for i in range(0, tmp_img.size[0], mark.size[0]):
        for j in range(0, tmp_img.size[1], mark.size[1]):
            main.paste(mark, (i, j), mark)
            main.thumbnail((8000, 8000), Image.ANTIALIAS)


def mark_pdf(text, pdf_file, output):
    assert output.endswith(".pdf"), "Your output file extension must be pdf"
    text_img = text2image(text)
    pdf_imgs = load_pdf2(pdf_file)
    for i in pdf_imgs:
        create_watermark2(i, text_img)
    pdf_imgs[0].save(output, save_all=True, append_images=pdf_imgs[1:])


