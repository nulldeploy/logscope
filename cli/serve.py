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
    app.run()
    logger.info('Flask server stopped.')