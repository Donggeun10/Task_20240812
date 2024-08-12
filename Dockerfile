FROM python:3.12-alpine AS builder
LABEL authors="leedg17"

RUN sed 's/https/http/g' -i /etc/apk/repositories
RUN apk update && apk --no-cache add binutils

# 1-1) alpine 계정 세팅
RUN addgroup -S appgroup && adduser -S appuser -G appgroup
COPY test/requirements.txt /

RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r /requirements.txt
    #pip install --no-cache-dir FastAPI uvicorn pyinstaller sqlalchemy flatbuffers google-cloud-pubsub

USER appuser

WORKDIR /home/appuser
COPY test/train/app/ test/train/app/
COPY test/main.spec ./

EXPOSE 9084
ENV GOOGLE_CLOUD_PROJECT="nm-stg-usw2-crashreport"
ENV PYTHONPATH="/home/appuser"

RUN pyinstaller main.spec

#CMD ["--port", "9084"]
#ENTRYPOINT ["python", "-m", "uvicorn", "test.train.app.application:app", "--host", "0.0.0.0"]

FROM python:3.12-alpine

#RUN sed 's/https/http/g' -i /etc/apk/repositories
#RUN apk update && apk --no-cache add htop

# 1-1) alpine 계정 세팅
RUN addgroup -S appgroup && adduser -S appuser -G appgroup
USER appuser

# 2) Native 실행 파일 복사
COPY --from=builder /home/appuser/dist/ /home/appuser/

# 3) 변수 설정
EXPOSE 9084
ENV GOOGLE_CLOUD_PROJECT="nm-stg-usw2-crashreport"

# 4) 실행
WORKDIR /home/appuser
ENTRYPOINT ["./main/main"]