import gradio as gr
from PIL import Image, ExifTags

def convert_image_format(image, output_format):
    image = Image.open(image)
    output_format = output_format.lower()
    output_file = f"./tmp/output.{output_format}"
    if output_format == 'jpg':
        image.save(output_file, format='JPEG')
    elif output_format == 'tif':
        image.save(output_file, format='TIFF')
    else:
        image.save(output_file, format=output_format.upper())
    return output_file

def rotate_image(image, angle):
    image = Image.open(image)
    rotated_image = image.rotate(angle)
    return rotated_image

def scale_image(image, scale_factor):
    image = Image.open(image)
    new_size = (int(image.width * scale_factor), int(image.height * scale_factor))
    scaled_image = image.resize(new_size)
    return scaled_image

def get_image_info(image):
    image = Image.open(image)
    info = {
        "Format": image.format,
        "Mode": image.mode,
        "Size": image.size,
        "Metadata": {ExifTags.TAGS.get(k, k): v for k, v in image._getexif().items()} if image._getexif() else "No metadata found"
    }
    return info

with gr.Blocks() as demo:
    with gr.Tab("Format Conversion"):
        with gr.Row():
            image_input = gr.Image(type="filepath")
            output_format = gr.Radio(choices=["png", "jpg", "bmp", "gif", "webp", "tif"], label="Output Format")
        convert_button = gr.Button("Convert")
        converted_image = gr.Image()
        convert_button.click(convert_image_format, inputs=[image_input, output_format], outputs=converted_image)

    with gr.Tab("Rotate Image"):
        with gr.Row():
            image_input = gr.Image(type="filepath")
            angle = gr.Slider(minimum=0, maximum=360, step=1, label="Rotation Angle")
        rotate_button = gr.Button("Rotate")
        rotated_image = gr.Image()
        rotate_button.click(rotate_image, inputs=[image_input, angle], outputs=rotated_image)

    with gr.Tab("Scale Image"):
        with gr.Row():
            image_input = gr.Image(type="filepath")
            scale_factor = gr.Slider(minimum=0.1, maximum=10, step=0.1, label="Scale Factor")
        scale_button = gr.Button("Scale")
        scaled_image = gr.Image()
        scale_button.click(scale_image, inputs=[image_input, scale_factor], outputs=scaled_image)

    with gr.Tab("Image Information"):
        image_input = gr.Image(type="filepath")
        info_button = gr.Button("Get Info")
        image_info = gr.JSON()
        info_button.click(get_image_info, inputs=image_input, outputs=image_info)

demo.launch()
