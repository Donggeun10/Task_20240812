# Backend Server
- Python FastAPI 기반의 RESTful API 서버 구현

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
- uvicorn test.train.app.application:app --host 0.0.0.0 --port 9084
- python test\train\app\application.py
  -  set PYTHONPATH=%PYTHONPATH%;%cd%
```

## 3. pyinstaller
```
- pyinstaller main.spec
```
## 4. Docker 실행 테스트
```
- docker build -t pyserver:local .  && docker run --gpus=all -p 9084:9083 pyserver:local --port 9083 
```



