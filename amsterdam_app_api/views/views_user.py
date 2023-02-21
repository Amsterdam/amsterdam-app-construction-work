""" View for VUE route change password """
from django.contrib.auth import get_user_model
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view
from rest_framework.response import Response
from amsterdam_app_api.api_messages import Messages
from amsterdam_app_api.swagger.swagger_views_user import as_change_password
from amsterdam_app_api.GenericFunctions.IsAuthorized import IsAuthorized

messages = Messages()


@swagger_auto_schema(**as_change_password)
@api_view(['POST'])
@IsAuthorized
def change_password(request):
    """ Change user password (VUE) """
    username = request.data.get('username', None)
    old_password = request.data.get('old_password', None)
    password = request.data.get('password', None)
    password_verify = request.data.get('password_verify', None)

    if None in [username, old_password, password, password_verify]:
        return Response({'status': False, 'result': messages.invalid_query}, 422)

    if password_verify != password:
        return Response({'status': False, 'result': messages.do_not_match}, 401)

    UserModel = get_user_model()
    user = UserModel.objects.filter(username=username).first()
    if user is None or not user.check_password(old_password):
        return Response({'status': False, 'result': messages.invalid_username_or_password}, 401)

    # Change user password
    user.set_password(password)
    user.save()

    return Response({'status': True, 'result': 'password updated'})
