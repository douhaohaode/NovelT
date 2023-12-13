from PIL import Image, ImageDraw, ImageFont
import real_gan

def cover(title="打造最强宗门", subtitle="第一集", context_title="门下是万 个个是妖孽",
          image_path="./source/image/1697308132.jpg"):
    image = Image.open(image_path)
    image = image.convert("RGB")
    image_width, image_height = image.size
    draw = ImageDraw.Draw(image)
    text_color = (246, 228, 50)
    text_stroke_color = (44, 89, 251)
    stroke_fill = (134, 134, 134)
    #context_color = (233, 233, 233)
    context_stroke_fill = (233, 233, 233)

    text_font = ImageFont.truetype("./source/asset/Songti_1.ttc", 60)
    text_width = draw.textlength(title,  text_font)

    subtitle_font = ImageFont.truetype("./source/asset/Songti_1.ttc", 38)
    subtitle_width = draw.textlength(subtitle, subtitle_font)

    context_title_font = ImageFont.truetype("./source/asset/Songti_1.ttc", 30)
    context_title_width = draw.textlength(context_title, context_title_font)

    text_x = (image_width - text_width) // 2
    text_y = image_height // 2 - 150
    subtitle_x = (image_width - subtitle_width) // 2
    subtitle_y =  image_height // 2 - 30
    context_title_x = image_width / 2 - context_title_width/2
    context_title_y = image_height // 2 + 60


    draw.text((text_x, text_y), title, fill=text_color, spacing=10, align="center",
              font= text_font, font_features=["bold"], stroke_width=10,
              stroke_fill=text_stroke_color)

    draw.text((subtitle_x, subtitle_y), subtitle, fill=text_color, align="center",
              font_features=["expanded"],
              font=subtitle_font, stroke_width=2,
              stroke_fill=text_stroke_color)

    draw.text((context_title_x, context_title_y), context_title, align="center",
              fill=text_stroke_color, font=context_title_font, stroke_width=5,
              stroke_fill=context_stroke_fill)
    image.save("./source/cover/output_image.jpg")
    real_gan.inference_gan("./source/cover/output_image.jpg")


