import markdown
from django.http import HttpResponse
from amsterdam_app_backend.settings import BASE_DIR
import mimetypes


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
    try:
        with open('{base_dir}/static/favicon.ico'.format(base_dir=BASE_DIR), 'rb') as f:
            content = f.read()
        return HttpResponse(content, content_type='image/x-icon', status=200)
    except Exception as error:
        pass
    return HttpResponse(status=404)


def static(request):
    path = request.path
    save_path = path.replace('..', '')
    filepath = '{base_dir}{save_path}'.format(base_dir=BASE_DIR, save_path=save_path)
    mimetype = mimetypes.guess_type(filepath, strict=True)[0]
    try:
        with open(filepath, 'r') as f:
            content = f.read()
        return HttpResponse(content, content_type=mimetype, status=200)
    except Exception as error:
        pass

    try:
        with open(filepath, 'rb') as f:
            content = f.read()
        return HttpResponse(content, content_type=mimetype, status=200)
    except Exception as error:
        pass
    return HttpResponse(status=404)
