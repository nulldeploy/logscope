FROM python:3.12 AS builder

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

FROM python:3.12-slim 

ARG APP_VERSION=1.0.0
LABEL VERSION="${APP_VERSION}"

WORKDIR /app
COPY --from=builder /install /usr/local
ENV PORT=5000

RUN useradd -r -s /bin/false appuser

HEALTHCHECK --interval=15s --timeout=15s --start-period=5s --retries=2 \
	CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:5000/health')" || exit 1

COPY --chown=appuser:appuser . .
USER appuser

EXPOSE 5000
CMD ["python", "logscope.py", "serve"]
