# Stage 1: Build
FROM python:3.12-slim AS builder

WORKDIR /build

COPY requirements.txt .
RUN pip install --no-cache-dir --no-compile --user -r requirements.txt

# Stage 2: Runtime
FROM python:3.12-slim AS runtime

RUN groupadd -r kcw && useradd -r -g kcw -d /app -s /sbin/nologin kcw

WORKDIR /app

COPY --from=builder /root/.local /usr/local
COPY . .

RUN chown -R kcw:kcw /app && chmod -R 755 /app

USER kcw

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=10s --start-period=15s --retries=3 \
    CMD python -c "import http.client; c=http.client.HTTPConnection('localhost',8000,timeout=5); c.request('GET','/health'); r=c.getresponse(); assert r.status==200; r.read(); c.close()"

CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4", "--limit-max-requests", "10000", "--timeout-keep-alive", "65", "--no-access-log", "--proxy-headers", "--forwarded-allow-ips", "*"]
