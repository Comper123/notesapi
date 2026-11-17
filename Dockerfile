FROM python:3.13-alpine

WORKDIR /app
COPY app.py ./

RUN addgroup -S app && adduser -S -G app -u 10001 app \
    && mkdir /data && chown app:app /data

USER app
EXPOSE 8201

HEALTHCHECK --interval=10s --timeout=3s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:' + __import__('os').getenv('PORT', '8201') + '/health', timeout=2)"

CMD ["python", "app.py"]
