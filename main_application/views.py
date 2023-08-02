""" Views for VUE website """
from django.http import HttpResponse


def appstore(request):
    """route for amsterdam app Appstore"""
    content = """<!DOCTYPE html>
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
                 </html>"""
    return HttpResponse(content, content_type="text/html")
