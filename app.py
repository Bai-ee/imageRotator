from flask import Flask, request, send_file, render_template_string
from PIL import Image
import moviepy.editor as mpy
import os

app = Flask(__name__)

@app.route('/')
def index():
    print("Index route accessed")
    return render_template_string('''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Rotate Image</title>
    </head>
    <body>
        <h1>Upload an Image to Rotate</h1>
        <form action="/upload" method="post" enctype="multipart/form-data">
            <input type="file" name="image" accept="image/*" required><br><br>
            <label for="size">Size (e.g., 300x300):</label>
            <input type="text" name="size" id="size" required><br><br>
            <label for="speed">Speed (degrees per second):</label>
            <input type="number" name="speed" id="speed" required><br><br>
            <label for="duration">Duration (seconds):</label>
            <input type="number" name="duration" id="duration" required><br><br>
            <button type="submit">Upload and Rotate</button>
        </form>
    </body>
    </html>
    ''')

@app.route('/upload', methods=['POST'])
def upload():
    print("Upload route accessed")
    image = request.files['image']
    size = request.form['size']
    speed = int(request.form['speed'])
    duration = int(request.form['duration'])

    width, height = map(int, size.split('x'))
    image = Image.open(image)
    image = image.resize((width, height))

    frames = []
    for t in range(0, duration * 30):
        frame = image.rotate(t * speed / 30)
        frame_path = f'frame_{t}.png'
        frame.save(frame_path)
        frames.append(frame_path)

    clip = mpy.ImageSequenceClip(frames, fps=30)
    clip_path = 'output.mp4'
    clip.write_videofile(clip_path, codec='libx264')

    for frame in frames:
        os.remove(frame)

    return send_file(clip_path, as_attachment=True)

if __name__ == '__main__':
    print("Starting Flask app")
    app.run(debug=True, host='0.0.0.0', port=5003)
