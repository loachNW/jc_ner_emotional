# -*- coding: utf-8 -*-
# filename: main.py

from flask import Flask, jsonify, request
from Region import Region
import logging.handlers

models = Region()
server = Flask(__name__)
handler = logging.handlers.TimedRotatingFileHandler(filename='app.log', when='midnight', backupCount=30,
                                                    encoding='utf8')
handler.setFormatter(logging.Formatter('[%(asctime)s] [%(levelname)s] %(message)s'))
server.logger.addHandler(handler)

@server.route('/', methods=['post'])
def reg():
    content = request.values.get('content')
    if (content is not None) and (content != ""):
        result = jsonify({"result": models.prdected(content),"state":"1"})
        server.logger.info(result)
        return result
    else:
        server.logger.error('输入有误')
        return jsonify({"state":"0"})

server.run(host='0.0.0.0', port=5004, debug=True, use_reloader=False)
