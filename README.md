sanicImagePreview
=================

Service to make base64 encoded avif images

```bash
make

curl "http://localhost:8000/?url=http://calaldees.uk/responsive_portfolio_assets/images/projects/paratrooper.png"

curl \
    --request POST \
    --url localhost:8000 \
    --header "Content-Type: application/json" \
    --data '{"url": "https://images.musicrad.io/resizer/?image=aHR0cHM6Ly9zZXMub25haXIudGhpc2lzZ2xvYmFsLmNvbS9zZXMvYXNzZXRzL2ltYWdlcy8yZTBmOGY4OC0xZTNkLTRhMTItYWM0MS04ZjVhYjM5M2QxY2E%3D&width=500&signature=YONayF5M_POsxxBeSE6SaxQh644="}'
```

GIMP has much better quality settings. Investigate
TODO: resizing?

https://linuxcommandlibrary.com/man/avifenc

```bash
# I would have loved it if this was possible
echo "data:image/avif;base64,$(wget "image_url" -O - | avifenc --stdin - | base64)"
# Maybe this is possible with ffmpeg or imagemagik
```

https://superuser.com/a/1765767
```bash
ffmpeg -f lavfi -i "color=color=#000000@0:size=550x60,format=yuva420p,drawtext=text='Hello how are you?':fontcolor=black:fontsize=55:x=(W-tw)/2:y=(H-th)/2" -map 0 -map 0 -filter:v:1 alphaextract -frames:v 1 -c:v libaom-av1 -still-picture 1 hello.avif
```

https://stackoverflow.com/a/65207419/3356840
```
ffmpeg -f mp3 -i - -c:a pcm_s16le -f s16le - < file.mp3
```

https://linuxconfig.org/converting-images-to-avif-on-linux-including-jpg-png-and-webp-formats
```
ffmpeg -i image.png -c:v libaom-av1 -crf 30 -pix_fmt yuv420p image_ffmpeg.avif
```

https://nixsanctuary.com/ffmpeg-now-supports-jpeg-xl-and-avif-how-to-convert-images/
```
ffmpeg -i image.png -c:v libaom-av1 -still-picture 1 image.avif
```

Could I return image/avif+base64?
https://stackoverflow.com/questions/7285372/is-content-transfer-encoding-an-http-header
https://www.iana.org/assignments/media-type-structured-suffix/media-type-structured-suffix.xhtml

---

```bash
alias ffmpeg='docker run -i --rm --volume $(PWD):/data/ --workdir=/data/ linuxserver/ffmpeg'


# Can't use tempfile/mktemp because the docker mount is only the current directory
#   on a local system we can probably use tempfile/mktemp
# TEMPFILE="$(gmktemp --suffix=.avif)" && \


URL_IMAGE="https://placecats.com/neo/300/200" && \
TEMPFILE="$(openssl rand -hex 3).avif" && \
BASE64_IMAGE=$( \
    wget -q "${URL_IMAGE}" -O - \
    | ffmpeg \
        -hide_banner -loglevel error \
        -i - \
        -c:v libaom-av1 -filter:v scale=200:-2 -crf 45 -pix_fmt yuv420p \
        ${TEMPFILE} \
    && cat ${TEMPFILE} \
    | base64 \
) \
&& echo "data:image/avif;base64,${BASE64_IMAGE}" \
&& rm ${TEMPFILE}
```


Considered: Neither work
 `Content-Transfer-Encoding: base64`
 `Content-Type: application/pdf+base64`
https://stackoverflow.com/a/68366520/3356840
