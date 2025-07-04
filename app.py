import asyncio
from types import MappingProxyType
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

FORMAT_LOOKUP_ENCODER = MappingProxyType({
    'avif': 'libaom-av1',
})

async def image_url_to_avif_base64(url: Url, width: int=-1, crf=45, format='avif') -> bytes:
    stdout, _ = await shell(dedent(r"""
        URL_IMAGE="__URL__" && \
        TEMPFILE=$(mktemp --suffix=.avif) && \
        BASE64_IMAGE=$( \
            wget -q "${URL_IMAGE}" -O - \
            | ffmpeg \
                -hide_banner -loglevel error \
                -i - \
                -c:v __ENCODER__ \
                -filter:v scale=__IMAGE_WIDTH__:-2 \
                -crf __CRF__ \
                -pix_fmt yuv420p \
                -y ${TEMPFILE} \
            && cat ${TEMPFILE} \
            | base64 \
        ) \
        && echo "data:image/__FORMAT__;base64,${BASE64_IMAGE}" \
        && rm ${TEMPFILE}
    """
        .replace('__URL__', url)
        .replace('__IMAGE_WIDTH__', str(width))
        .replace('__CRF__', str(crf))
        .replace('__FORMAT__', format)
        .replace('__ENCODER__', FORMAT_LOOKUP_ENCODER[format])
    ))
    return stdout.replace(b'\n', b'')


@app.route("/", methods=["GET", "POST"])
async def root(request):
    kwargs = ChainMap({k:request.args.get(k) for k in request.args.keys()} or {}, request.json or {})
    # TODO: Take binary image from upload/POST?
    log.info(kwargs)
    return sanic.response.raw(await image_url_to_avif_base64(**kwargs), content_type="text/plain")
