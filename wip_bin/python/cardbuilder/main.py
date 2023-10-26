from openpyxl import load_workbook
from PIL import Image, ImageDraw, ImageFont

from typing import Optional

def load_template(path: str) -> Image.Image:
    return Image.open(path)

def insert_text(card: Image.Image, x: int, y: int, text: str, font: ImageFont.FreeTypeFont) -> None:
    draw = ImageDraw.Draw(card)
    draw.text((x, y), text, font=font, fill="black")

def insert_image(card: Image.Image, x: int, y: int, image_path: str) -> None:
    with Image.open(image_path) as img:
        # resize image: 
        # https://stackoverflow.com/questions/273946/how-do-i-resize-an-image-using-pil-and-maintain-its-aspect-ratio
        aspect_ratio = img.width / img.height
        new_width = int(card.width * 0.6)  # e.g., 60% of card width
        new_height = int(new_width / aspect_ratio)
        img = img.resize((new_width, new_height))
        card.paste(img, (x, y))

def create_card(template: Image.Image, name: str, description: str, image_path: Optional[str]) -> Image.Image:
    card = template.copy()
    
    # Define the font and size
    # font = ImageFont.truetype("arial.ttf", size=55)
    font = ImageFont.truetype("CURLZ___.TTF", size=55)
    
    # Insert title in top-middle centered
    text_bbox = font.getbbox(name)
    text_width, text_height = text_bbox[2] - text_bbox[0], text_bbox[3] - text_bbox[1]
    insert_text(card, (card.width - text_width) // 2, 10, name, font)
    
    # Insert image top-center under title
    if image_path:
        box_width = int(card.width * 0.2)  # 90% of card width
        box_height = box_width  # Assuming you want a square box for simplicity
        
        with Image.open(image_path) as img:
            aspect_ratio = img.width / img.height
            
            if aspect_ratio > 1:  # Image is wider than tall
                new_width = box_width
                new_height = int(box_width / aspect_ratio)
            else:  # Image is taller than wide or square
                new_height = box_height
                new_width = int(box_height * aspect_ratio)
                
            # img = img.resize((new_width, new_height))
            # HELLO TODO FIXME, insertme doesnt work..
            img = img.resize((400, 400))
            # insert_image(card, (card.width - new_width) // 2, 10 + text_height + 10, image_path)
            insert_image(card, card.width//10, 10 + text_height + 10, image_path)



    # # Insert image top-center under title
    # if image_path:
    #     with Image.open(image_path) as img:
    #         aspect_ratio = img.width / img.height
    #         new_width = int(card.width * 0.6)  # e.g., 60% of card width
    #         new_height = int(new_width / aspect_ratio)
    #         img = img.resize((new_width, new_height))
    #         insert_image(card, (card.width - new_width) // 2, 10 + text_height + 10, image_path)
    
    # Insert description in the bottom-lower part
    # insert_text(card, (card.width - text_width) // 2, card.height - 50, description, font)
    insert_text(card, card.width // 10, card.height - 100, description, font)
    # insert_text(card, 10, card.height - 50, description, font)
    
    return card


def generate_cards_from_sheet(sheet, template_path: str, save_path: str) -> None:
    template = load_template(template_path)
    
    for row in sheet.iter_rows(min_row=2, values_only=True):
        card_name, card_description, card_image_path = row[0], row[1], row[2]
        card = create_card(template, card_name, card_description, card_image_path)
        card.save(f'{save_path}/{card_name}.png')

# Usage
# save_path = 'path_to_save'
# template_path = '../templates/vertical_card.png'
# generate_cards_from_sheet(sheet, template_path, save_path)

template_path = './templates/vertical_card.png'
template = load_template(template_path)
card = create_card(template, 'teast_card', 'description LOREM IPSUM', './images/placeholder_image.png')
# card = create_card(template, 'test_card', 'description LOREM IPSUM', None)
card.save('./out/test_card.png')
