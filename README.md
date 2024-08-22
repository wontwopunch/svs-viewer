# SVS-Viewer
웹 브라우저에서 실행되는 SVS 뷰어 프로그램

#### 서버 측에서 파일을 처리하고, 클라이언트 측에서는 웹 기술을 사용해 이미지를 표시하고 메모 작성 및 공유 기능을 제공하는 방식

### 기술 스택
백엔드: Flask
프론트엔드: HTML, CSS, JavaScript(필요하다면 React)

### 파일 구조
- app.py : Flask 서버 코드 (메인 파일)
- openslide/bin/libopenslide-0.dll : Python에서 openslide를 사용 시 꼭 필요한 파일
- requirements.txt : 의존성 목록 (Flask 및 기타 패키지)
- uploads/ : 업로드된 파일을 저장할 디렉토리
- templates/ : HTML 템플릿 파일을 저장할 디렉토리
- templates/index.html : 메인 HTML 파일
- static/ : 정적 파일(CSS, JS, 이미지 등)을 저장할 디렉토리
- static/styles.css
- README.md

### 실행 환경
1. requirements.txt 설치
2. https://openslide.org/download/ - Windows 64-bit binary 다운로드
3. openslide/bin/libopenslide-0.dll, app.py os.add_dll_directory 코드 추가
4. 개발 시, $ python app.py
5. 배포 시, $ waitress-serve --host=127.0.0.1 --port=8000 app:app


### 진행 중
- 현재, openslide 구현까지 됨  
- svs 파일 용량 제한을 해결하기 위해 
- 서버 측에서는 프로덕션 환경의 WSGI 서버 (Gunicorn 사용 → Windows는 Waitress)
- 실행 $ waitress-serve --host=127.0.0.1 --port=8000 app:app
- 클라이언트 측에서는 이미지 타일링 기술을 사용(OpenSeadragon 사용)
- openseadragon 코드 index.html에 작성
- 이미지 타일링을 적용하려면 서버 측에서 이미지를 타일로 분할한 후, 해당 타일 경로를 OpenSeadragon에 지정해야 됨(▼)
- 1) 서버에서 Pillow 또는 ImageMagick을 사용해 이미지를 타일로 분할
- 2) 타일 이미지를 /static/tiles/ 경로에 저장.
- 3) OpenSeadragon의 tileSources 설정에 타일 이미지 경로를 지정.

### 좀 더 구체적으로 정리한 이미지 타일링 적용 방법
#### 1. 서버에서 Pillow 또는 ImageMagick을 사용해 이미지를 타일로 분할
- app.py 수정
- 사용자가 SVS 파일을 업로드하면 해당 파일이 uploads/ 폴더에 저장
- 파일이 저장된 후, generate_tiles() 함수가 호출되어 업로드된 SVS 파일을 타일로 분할하고, 이 타일들을 static/tiles/ 폴더에 저장
- 업로드된 SVS 파일을 OpenSlide로 열고, 지정된 크기(800x600)의 썸네일을 생성합니다. 생성된 썸네일은 메모리에 저장되며, send_file()을 통해 클라이언트로 반환
- generate_tiles() 함수는 Pillow 라이브러리를 사용하여 업로드된 이미지 파일을 256x256 크기의 타일로 분할하고, 이를 static/tiles/ 폴더에 저장

#### 2. 타일 이미지를 클라이언트에 제공
- 이미지 타일은 /static/tiles/ 경로로 접근
- Flask 서버 설정은 추가로 필요하지 않으며, 기본적으로 /static/ 경로에 저장된 파일들을 서빙

#### 3. OpenSeadragon에 타일링된 이미지를 로드
- index.html 파일에서 OpenSeadragon의 tileSources 설정을 사용해 타일링된 이미지를 로드하도록 설정

#### 결론
OpenSeadragon이 서버 측에서 생성된 타일 이미지를 로드하여 브라우저에서 대형 이미지를 효율적으로 표시
1. 서버 측: Pillow로 대형 이미지를 타일로 분할하여 저장 (generate_tiles()).
2. 타일 제공: Flask 서버는 static/tiles/ 경로에서 타일 이미지를 서빙
3. 클라이언트 측: OpenSeadragon은 타일 이미지를 로드하고, 전체 이미지를 줌 및 팬 기능으로 표시
→ 클라이언트에서 성능 저하 없이 표시할 수 있음!!!

### 사용 방법 
배포하기에는 사용인이 1인
1. 개인 노트북에 개발환경 구축 및 Git clone
2. 파일 저장 및 메모 포함 링크 생성 기능을 구현 → 타인에게 링크 공유