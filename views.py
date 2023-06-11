import os


from response import HttpResponse

from settings import BASE_DIR


# Default Not Found View
def http404_view(request):
    with open(os.path.join(BASE_DIR, "templates", "http404.html")) as f:
        file = f.read()
    return HttpResponse(request, file, status=404)

# View handling static files
def static_files_view(request, dir, file_name):
    content_type = {
        "png": "image/png",
        "css": "text/css",
    }
    name, extension = file_name.split(".")
    file_path = os.path.join(BASE_DIR, "static", dir, file_name)
    with open(file_path, "rb") as f:
        file = f.read()

    headers = {
        "Content-Length": len(file),
    }
    if file_type := content_type.get(extension):
        headers["Content-Type"] = file_type

    return HttpResponse(request, file, status=200, **headers)

# Views
def index_view(request):
    headers = {
        "Content-Type": "text/html",
    }

    file_path = os.path.join(BASE_DIR, "templates", "index.html")
    with open(file_path, "r") as f:
        file = f.read()

    return HttpResponse(request, file, **headers)

def download_file_view(request):
    headers = {
        "Content-Type": "text/html",
    }
    tile_template = """
    <div class="file--tile">

        <div class="file--left">
            <div class="file--name">
                {}
            </div>
        </div>
        <div class="file--right">
            <a href="/files/{}/" class="file--download" download="{}">Download</a>
        </div>

    </div>
    """

    with open(os.path.join(BASE_DIR, "templates", "file.html")) as f:
        html = f.read()

    content = ""
    for dir_path, dirnames, files in os.walk(os.path.join(BASE_DIR, "files")):
        for file_name in files:
            content += tile_template.format(file_name, file_name, file_name)

    content = html.format(content)
    return HttpResponse(request, content, status=200, **headers)

def downloader_view(request, file_name):
    file_path = os.path.join(BASE_DIR, "files", file_name)
    with open(file_path, "rb") as f:
        file = f.read()

    headers = {
        "Connection": "Keep-Alive",
        "Content-Type": "application/octet-stream",
        "Content-Length": len(file)
    }
    return HttpResponse(request, file, **headers)