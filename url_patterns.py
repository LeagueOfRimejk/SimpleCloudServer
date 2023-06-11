from route import RoutePattern

import views

# URL's
url_patterns = [
    # Static Files main Route
    RoutePattern.add_route("/static/<str:directory>/<str:filename>", views.static_files_view),

    # Routes
    RoutePattern.add_route("/", views.index_view),
    RoutePattern.add_route("/files/", views.download_file_view),
    RoutePattern.add_route("/files/<str:filename>/", views.downloader_view),
]