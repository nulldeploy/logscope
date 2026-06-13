# serve.py
from flask import Flask
import logging

logger = logging.getLogger(__name__)
app = Flask(__name__)


@app.route('/health')
def health():
    return 'Hello from Logscope...'

def run(args) -> None:
    logger.info('Starting Flask server...')
    app.run(host='0.0.0.0', port=5000)
    logger.info('Flask server stopped.')