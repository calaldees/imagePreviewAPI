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

TODO: resizing?

```bash
# I would have loved it if this was possible
echo "data:image/avif;base64,$(wget "image_url" -O - | avifenc --stdin - | base64)"
# Maybe this is possible with ffmpeg or imagemagik
```