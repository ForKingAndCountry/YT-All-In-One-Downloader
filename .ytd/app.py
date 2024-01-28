from flask import Flask, request, jsonify, render_template
from flask_socketio import SocketIO, emit
from pytube import YouTube
import os
import threading

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app) 


#Getting the default download Path of Operating Systems(Windows, Linux for now )
def get_default_download_dir():
    # Platform-specific logic to determine default download directory
    if os.name == 'nt':  # For Windows
        return os.path.join(os.path.expanduser('~'), 'Downloads')
    elif os.name == 'posix':  # For Linux/Unix
        return os.path.join(os.path.expanduser('~'), 'Downloads')
    else:
    # For other operating systems, provide a default path
        return '/default/path/'  # Replace with a default path for other systems

# Emit progress via SocketIO
# @socketio.on('progress_update')
# def send_progress(progress):
#     socketio.emit('download_progress', {'progress': progress})

# Function to download video
def download_video(video_url, download_path):
    try:
        yt = YouTube(video_url)
        video_stream = yt.streams.get_highest_resolution()

        @video_stream.on_progress
        def progress_callback(stream, chunk, bytes_remaining):
            file_size = stream.filesize
            bytes_downloaded = file_size - bytes_remaining
            percentage = (bytes_downloaded / file_size) * 100
            # send_progress(percentage)  # Emit progress during download

        video_stream.download(output_path=download_path)
        return True  # Download successful

    except Exception as e:
        print(f"Error during download: {e}")
        return False  # Download failed
    
# @app.route('/')
# def index():
#     return render_template('index.html')
    
@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('message')
def handle_message(videoLink):
    print('Received message:', videoLink)
    # Broadcast the message to all connected clients
    socketio.emit('message', videoLink)

# @app.route('/download', methods=['POST', 'GET'])
# def received_data():
    # if request.method == 'POST':
    #     print(request.get_json)
    #     print(request.get_data)
    #     json_data = request.get_json()
    #     video_info = json_data
    #     video_url = video_info['videoLink']
        

    #     try:
    #         download_path = get_default_download_dir()
    #         download_thread = threading.Thread(target=download_video, args=(video_url, download_path))
    #         download_thread.start()
    #     except Exception as e:
    #         print(f"Error: {str(e)}")

    #     return jsonify({'message': 'Download started'})

if __name__ == '__main__':
    socketio.run(app, debug=True)
