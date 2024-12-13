import asyncio
import base64
import tempfile
from io import BytesIO
from pathlib import Path
from collections import ChainMap

import sanic
from sanic.log import logger as log

app = sanic.Sanic("imagePreview")

# https://stackoverflow.com/a/69567335/3356840
# avifenc --min 0 --max 63 -a end-usage=q -a cq-level=18 -a tune=ssim
# avifenc --min 30 --max 63 --speed 10 --yuv 420 -d 8 --codec aom input.png output.avif


async def cmd(*args, hide_output=False):
    args = tuple(map(str,args))
    log.debug(' '.join(args))
    proc = await asyncio.create_subprocess_exec(
        *args,
        stdout=asyncio.subprocess.PIPE if hide_output else None,
        stderr=asyncio.subprocess.PIPE if hide_output else None,
    )
    stdout, stderr = await proc.communicate()


async def image_url_to_avif_base64(url):
    with tempfile.TemporaryDirectory() as tempdir:
        tempdir = Path(tempdir)

        # Download image input
        file_input = tempdir.joinpath("in")
        await cmd("wget", url, "-O", file_input.absolute())
        assert file_input.exists(), f"${file_input.absolute()} should have been created"

        # Convert to avif
        file_output = tempdir.joinpath("out.avif")
        await cmd(
            "avifenc",
            file_input.absolute(),
            file_output.absolute(),
            "--min","63",
            "--max","63",
        )
        assert file_output.exists(), f"${file_output.absolute()} should have been created"

        # Base64 encode
        buffer = BytesIO()
        buffer.write(b"data:image/avif;base64,")
        with file_output.open("rb") as out:
            base64.encode(out, buffer)
        return buffer.getvalue()


@app.route("/", methods=["GET", "POST"])
async def root(request):
    url = ChainMap(request.args, request.json).get("url", "")
    log.info(url)
    return sanic.response.raw(await image_url_to_avif_base64(url), content_type="text/plain")
