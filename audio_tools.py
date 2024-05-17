import gradio as gr
from pydub import AudioSegment
from mutagen.easyid3 import EasyID3
from mutagen.mp3 import MP3
import os

# Function to get audio information and metadata
def get_audio_info(file):
    audio = AudioSegment.from_file(file)
    duration = len(audio) / 1000  # duration in seconds
    channels = audio.channels
    frame_rate = audio.frame_rate
    sample_width = audio.sample_width

    try:
        audio_file = MP3(file, ID3=EasyID3)
        metadata = audio_file.pprint()
    except Exception as e:
        metadata = str(e)

    info = {
        "Duration (s)": duration,
        "Channels": channels,
        "Frame Rate": frame_rate,
        "Sample Width": sample_width,
        "Metadata": metadata,
    }

    return info

# Function to convert audio format and sampling rate
def convert_audio(file, output_format, sampling_rate, custom_rate):
    audio = AudioSegment.from_file(file)
    # Use custom rate if provided and not None, otherwise use selected sampling rate
    rate = int(custom_rate) if custom_rate is not None and custom_rate != 0 else int(sampling_rate)
    audio = audio.set_frame_rate(rate)
    output_file = f"./tmp/output.{output_format}"
    audio.export(output_file, format=output_format)
    return output_file

# Function to trim audio
def trim_audio(file, start_time, end_time):
    audio = AudioSegment.from_file(file)
    trimmed_audio = audio[start_time*1000:end_time*1000]  # times in milliseconds
    output_file = "trimmed_output.mp3"
    trimmed_audio.export(output_file, format="mp3")
    return output_file

# Function to add metadata to audio
def add_metadata(file, title, artist, album):
    # Ensure the file is an MP3
    if not file.lower().endswith('.mp3'):
        return "Error: Only MP3 files are supported for adding metadata."

    try:
        audio = MP3(file, ID3=EasyID3)
        audio['title'] = title
        audio['artist'] = artist
        audio['album'] = album
        audio.save()
        return "Metadata added successfully"
    except Exception as e:
        return f"Error: {str(e)}"

with gr.Blocks() as demo:
    with gr.Tab("Audio Information"):
        with gr.Row():
            audio_input = gr.Audio(type="filepath")
        info_button = gr.Button("Get Info")
        audio_info = gr.JSON()
        info_button.click(get_audio_info, inputs=audio_input, outputs=audio_info)

    with gr.Tab("Convert Audio"):
        with gr.Row():
            audio_input = gr.Audio(type="filepath")
            output_format = gr.Radio(choices=["mp3", "wav", "ogg", "flac"], label="Output Format")
            sampling_rate = gr.Dropdown(choices=["48000", "44100", "96000", "192000", "22000"], label="Sampling Rate")
            custom_rate = gr.Number(label="Custom Sampling Rate (optional)", value=0)
        convert_button = gr.Button("Convert")
        converted_audio = gr.Audio()
        convert_button.click(convert_audio, inputs=[audio_input, output_format, sampling_rate, custom_rate], outputs=converted_audio)

    """
    with gr.Tab("Trim Audio"):
        with gr.Row():
            audio_input = gr.Audio(type="filepath")
            start_time = gr.Number(label="Start Time (seconds)")
            end_time = gr.Number(label="End Time (seconds)")
        trim_button = gr.Button("Trim")
        trimmed_audio = gr.Audio()
        trim_button.click(trim_audio, inputs=[audio_input, start_time, end_time], outputs=trimmed_audio)

    with gr.Tab("Add Metadata"):
        with gr.Row():
            audio_input = gr.Audio(type="filepath")
            title = gr.Textbox(label="Title")
            artist = gr.Textbox(label="Artist")
            album = gr.Textbox(label="Album")
        metadata_button = gr.Button("Add Metadata")
        metadata_output = gr.Text()
        metadata_button.click(add_metadata, inputs=[audio_input, title, artist, album], outputs=metadata_output)
    """

demo.launch()
