import markdown
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
