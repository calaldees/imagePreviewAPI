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


type Url = str

async def image_url_to_avif_base64(url: Url, width: int=200) -> bytes:
    stdout, _ = await shell(dedent(r"""
        URL_IMAGE="__URL__" && \
        TEMPFILE=$(mktemp --suffix=.avif) && \
        BASE64_IMAGE=$( \
            wget -q "${URL_IMAGE}" -O - \
            | ffmpeg \
                -hide_banner -loglevel error \
                -i - \
                -c:v libaom-av1 -filter:v scale=__IMAGE_WIDTH__:-2 -crf 45 -pix_fmt yuv420p \
                -y ${TEMPFILE} \
            && cat ${TEMPFILE} \
            | base64 \
        ) \
        && echo "data:image/avif;base64,${BASE64_IMAGE}" \
        && rm ${TEMPFILE}
    """.replace('__URL__', url).replace('__IMAGE_WIDTH__', str(width))))
    return stdout.replace(b'\n', b'')


@app.route("/", methods=["GET", "POST"])
async def root(request):
    kwargs = ChainMap(request.args or {}, request.json or {})
    url = kwargs.get("url", "")
    # TODO: Take binary image from upload/POST?
    log.info(url)
    return sanic.response.raw(await image_url_to_avif_base64(url), content_type="text/plain")
