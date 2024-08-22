import os
from flask import Flask, render_template, request, jsonify, send_file, redirect, url_for

os.add_dll_directory(r"C:\workspace\svs-viewer\openslide\bin")
import openslide
from PIL import Image
import io

app = Flask(__name__)

# 경로 설정
UPLOAD_FOLDER = 'uploads'
TILE_FOLDER = 'static/tiles'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
if not os.path.exists(TILE_FOLDER):
    os.makedirs(TILE_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['TILE_FOLDER'] = TILE_FOLDER


# 타일 생성 함수
def generate_tiles(image_path, tile_size=256, output_dir='static/tiles'):
    os.makedirs(output_dir, exist_ok=True)

    image = Image.open(image_path)
    width, height = image.size

    # 타일 생성 루프
    for x in range(0, width, tile_size):
        for y in range(0, height, tile_size):
            box = (x, y, min(x + tile_size, width), min(y + tile_size, height))
            tile = image.crop(box)
            tile.save(os.path.join(output_dir, f"tile_{x}_{y}.png"))


# SVS 파일 업로드 및 처리
@app.route('/upload', methods=['POST'])
def upload_svs():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    # 파일 저장
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(file_path)

    # OpenSlide로 썸네일 생성
    slide = openslide.OpenSlide(file_path)
    thumbnail = slide.get_thumbnail((800, 600))  # 썸네일 크기 설정
    byte_io = io.BytesIO()
    thumbnail.save(byte_io, 'PNG')
    byte_io.seek(0)

    # 타일 생성 (썸네일이 아닌 전체 이미지에 대해 생성할 수 있습니다)
    generate_tiles(file_path)

    return send_file(byte_io, mimetype='image/png')


# 메인 페이지 렌더링
@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
