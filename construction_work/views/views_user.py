""" View for VUE route change password """
from django.contrib.auth import get_user_model
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from construction_work.api_messages import Messages
from construction_work.generic_functions.is_authorized import IsAuthorized
from construction_work.swagger.swagger_views_user import as_change_password

messages = Messages()


@swagger_auto_schema(**as_change_password)
@api_view(["POST"])
@IsAuthorized
def change_password(request):
    """Change user password (VUE)"""
    username = request.data.get("username", None)
    old_password = request.data.get("old_password", None)
    password = request.data.get("password", None)
    password_verify = request.data.get("password_verify", None)

    if None in [username, old_password, password, password_verify]:
        return Response(messages.invalid_query, status.HTTP_400_BAD_REQUEST)

    if password_verify != password:
        return Response(messages.do_not_match, status.HTTP_400_BAD_REQUEST)

    UserModel = get_user_model()
    user = UserModel.objects.filter(username=username).first()
    if user is None or not user.check_password(old_password):
        return Response(messages.invalid_username_or_password, status.HTTP_400_BAD_REQUEST)

    # Change user password
    user.set_password(password)
    user.save()

    return Response("password updated", status.HTTP_200_OK)
