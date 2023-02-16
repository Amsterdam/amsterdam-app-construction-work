""" Views for VUE website """
import io
import mimetypes
import markdown
from PIL import Image as PILImage
from django.http import HttpResponse
from amsterdam_app_backend.settings import BASE_DIR


def readme(request):
    """ Show the README.md file online
    """
    readme_md = '{base_dir}/README.md'.format(base_dir=BASE_DIR)
    content = ''
    try:
        with open(readme_md, 'r') as f:
            content = f.read()
    except Exception as error:
        print('Caught error in reading {readme_md}: {error}'.format(readme_md=readme_md, error=error))

    md = markdown.Markdown(extensions=['extra', 'fenced_code'])
    return HttpResponse(md.convert(content))


def favicon(request):
    """ Favicon """
    try:
        with open('{base_dir}/static/favicon.ico'.format(base_dir=BASE_DIR), 'rb') as f:
            content = f.read()
        return HttpResponse(content, content_type='image/x-icon', status=200)
    except Exception:
        pass
    return HttpResponse(status=404)


def static(request):
    """ Static data """
    path = request.path
    save_path = path.replace('..', '')
    filepath = '{base_dir}{save_path}'.format(base_dir=BASE_DIR, save_path=save_path)
    mimetype = mimetypes.guess_type(filepath, strict=True)[0]
    try:
        with open(filepath, 'r') as f:
            content = f.read()
        return HttpResponse(content, content_type=mimetype, status=200)
    except Exception:
        pass

    try:
        with open(filepath, 'rb') as f:
            content = f.read()
        return HttpResponse(content, content_type=mimetype, status=200)
    except Exception:
        pass
    return HttpResponse(status=404)


def index(request):
    """ Index.html """
    path = '{base_dir}/static/dist'.format(base_dir=BASE_DIR)
    with open('{path}/index.html'.format(path=path), 'r') as f:
        content = f.read()
        return HttpResponse(content, content_type='text/html')


def css_files(request):
    """ css route """
    path = '{base_dir}/static/dist'.format(base_dir=BASE_DIR)
    with open('{path}/{filename}'.format(path=path, filename=request.path), 'r') as f:
        content = f.read()
        return HttpResponse(content, content_type='text/css')


def js_files(request):
    """ js route """
    path = '{base_dir}/static/dist'.format(base_dir=BASE_DIR)
    with open('{path}/{filename}'.format(path=path, filename=request.path), 'r') as f:
        content = f.read()
        return HttpResponse(content, content_type='text/javascript')


def img_files(request):
    """ images route """
    path = '{base_dir}/static/dist'.format(base_dir=BASE_DIR)
    with open('{path}/{filename}'.format(path=path, filename=request.path), 'rb') as f:
        data = f.read()
        if '.svg' in request.path:
            return HttpResponse(data, content_type='image/svg+xml')
        buffer = io.BytesIO(data)
        pil_image = PILImage.open(buffer)
        return HttpResponse(data, content_type=pil_image.get_format_mimetype())


def appstore(request):
    """ route for amsterdam app Appstore """
    content = '''<!DOCTYPE html>
                 <html lang="en">
                 <head>
                     <meta charset="utf-8">
                     <meta content="IE=edge" http-equiv="X-UA-Compatible">
                     <meta content="width=device-width,initial-scale=1.0" name="viewport">
                     <link href="<%= BASE_URL %>favicon.ico" rel="icon">
                     <link href="https://use.fontawesome.com/releases/v5.2.0/css/all.css" rel="stylesheet">
                     <title>Amsterdam App Backend</title>
                 </head>
                 <body>
                     Download eerst uw app in de appstore!!!
                 </body>
                 </html>'''
    return HttpResponse(content, content_type='text/html')
