# Backend Server
- Python FastAPI 기반의 RESTful API 서버 구현
- Sqlite Database 를 이용한 데이터 저장 및 조회
- SQLAlchemy JPA 를 이용한 데이터 CRUD
- ~~LockModeType.PESSIMISTIC_WRITE 를 이용한 데이터 동시성 제어~~
- Docker 를 이용한 이미지 생성 및 실행

## 1. Frameworks And Tools
- Python 3.12
- FastAPI
- Uvicorn
- Pydantic
- SQLAlchemy
- SQLite
- Docker
- Swagger UI

## 2. Local 실행 테스트
```
- uvicorn train.app.application:app --host 0.0.0.0 --port 9084
- python train\app\application.py
  -  set PYTHONPATH=%PYTHONPATH%;%cd%
```
## 3. pyinstaller 실행 파일 생성 - 윈도즈 환경
```
- pyinstaller main.spec
```
## 4. Docker 실행 테스트
```
- docker build -t pyserver:local .  && docker run --gpus=all -p 9084:9083 pyserver:local --port 9083 
```



