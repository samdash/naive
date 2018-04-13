# Naive Bayes Spam Filtering Rest Service

Sample Spam Filtering Rest Service using Naive Bayes Algorithm 
Added Integration with Nginx + Gunicorn and Flask

Once Nginx is installed , you need to place the nginxconfig file under /usr/local/etc/nginx/servers

Convert the app.py to use aiohttp for asynchronos processing

<pre>

import logging

import aiohttp_cors
from aiohttp import web
from aiojobs.aiohttp import setup
from discussion_utils import classify_data

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


async def handle_post(request):
    data = await request.json()
    logger.debug("processing request {}".format(data))

    input_class = classify_data(data['input_text'])["category"]
    json_data = {
        'input_class': input_class,
        'input_text': data['input_text'],
        'status': 200
    }
    return web.json_response(json_data)


async def handle_get(request):
    return web.Response(text="Huston we have a lift off")


app = web.Application()
cors = aiohttp_cors.setup(app)
setup(app)

cors.add(
    app.router.add_post('/api/classify/', handle_post), {
        "*": aiohttp_cors.ResourceOptions(
            expose_headers="*",
            allow_headers="*")
    })

cors.add(
    app.router.add_get('/', handle_get), {
        "*": aiohttp_cors.ResourceOptions(
            expose_headers="*",
            allow_headers="*")
    })


web.run_app(app, host='127.0.0.1', port=8000)
</pre>

