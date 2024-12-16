import asyncio
from collections import ChainMap
from textwrap import dedent

import sanic
from sanic.log import logger as log

app = sanic.Sanic("imagePreview")


async def shell(cmd):
    proc = await asyncio.create_subprocess_shell(
        cmd,
        stdout = asyncio.subprocess.PIPE,
        stderr = asyncio.subprocess.PIPE,
    )
    return await proc.communicate()  # stdout, stderr


async def image_url_to_avif_base64(url):
    stdout, _ = await shell(dedent(r"""
        URL_IMAGE="__URL__" && \
        TEMPFILE=$(mktemp --suffix=.avif) && \
        BASE64_IMAGE=$( \
            wget -q "${URL_IMAGE}" -O - \
            | ffmpeg \
                -hide_banner -loglevel error \
                -i - \
                -c:v libaom-av1 -filter:v scale=200:-2 -crf 45 -pix_fmt yuv420p \
                -y ${TEMPFILE} \
            && cat ${TEMPFILE} \
            | base64 \
        ) \
        && echo "data:image/avif;base64,${BASE64_IMAGE}" \
        && rm ${TEMPFILE}
    """.replace('__URL__', url)))
    return stdout


@app.route("/", methods=["GET", "POST"])
async def root(request):
    url = ChainMap(request.args, request.json).get("url", "")
    log.info(url)
    return sanic.response.raw(await image_url_to_avif_base64(url), content_type="text/plain")
