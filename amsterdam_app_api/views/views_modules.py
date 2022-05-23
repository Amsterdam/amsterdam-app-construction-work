from amsterdam_app_api.models import Modules
from amsterdam_app_api.models import ModulesByApp
from amsterdam_app_api.models import ModuleOrder
from amsterdam_app_api.serializers import ModulesSerializer
from amsterdam_app_api.serializers import ModulesByAppSerializer
from amsterdam_app_api.serializers import ModuleOrderSerializer
from amsterdam_app_api.GenericFunctions.IsAuthorized import IsAuthorized
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view
from amsterdam_app_api.GenericFunctions.Logger import Logger
from amsterdam_app_api.swagger.swagger_views_modules import as_module_order_get
from amsterdam_app_api.swagger.swagger_views_modules import as_module_order_post
from amsterdam_app_api.swagger.swagger_views_modules import as_module_order_patch
from amsterdam_app_api.swagger.swagger_views_modules import as_module_order_delete
from amsterdam_app_api.swagger.swagger_views_modules import as_modules_get
from amsterdam_app_api.swagger.swagger_views_modules import as_modules_post
from amsterdam_app_api.swagger.swagger_views_modules import as_modules_patch
from amsterdam_app_api.swagger.swagger_views_modules import as_modules_delete
from amsterdam_app_api.swagger.swagger_views_modules import as_modules_by_app_get
from amsterdam_app_api.swagger.swagger_views_modules import as_modules_by_app_post
from amsterdam_app_api.swagger.swagger_views_modules import as_modules_by_app_patch
from amsterdam_app_api.swagger.swagger_views_modules import as_modules_by_app_delete
from amsterdam_app_api.swagger.swagger_views_modules import as_modules_for_app_get
from amsterdam_app_api.api_messages import Messages


message = Messages()


@swagger_auto_schema(**as_module_order_get)
@swagger_auto_schema(**as_module_order_post)
@swagger_auto_schema(**as_module_order_patch)
@swagger_auto_schema(**as_module_order_delete)
@api_view(['GET', 'POST', 'PATCH', 'DELETE'])
def module_order(request):
    if request.method in ['GET']:
        result, status_code = module_order_get(request)
        return Response(result, status=status_code)
    elif request.method in ['POST', 'PATCH', 'DELETE']:
        result, status_code = module_order_ppd(request)
        return Response(result, status=status_code)


def module_order_get(request):
    app_version = request.GET.get('appVersion', None)
    module_order = ModuleOrder.objects.filter(appVersion=app_version).first()
    if module_order is not None:
        serializer = ModuleOrderSerializer(module_order, many=False)
        return {'status': True, 'result': serializer.data}, 200
    else:
        return {'status': False, 'result': message.no_record_found}, 404


@IsAuthorized
def module_order_ppd(request):
    data = dict(request.data)
    module_order = ModuleOrder.objects.filter(appVersion=data.get('appVersion')).first()
    if request.method in ['POST']:
        if module_order is None:
            module_order_object = ModuleOrder(**data)
            module_order_object.save()
            return {'status': True, 'result': 'Module order updated or created'}, 200
        else:
            return {'status': False, 'result': 'Object already exists'}, 422
    if request.method in ['PATCH']:
        if module_order is not None:
            ModuleOrder.objects.filter(appVersion=data.get('appVersion')).delete()
            module_order_object = ModuleOrder(**data)
            module_order_object.save()
            return {'status': True, 'result': 'Module order updated or created'}, 200
        else:
            return {'status': False, 'result': message.no_record_found}, 404
    else:
        # Delete record
        try:
            data = dict(request.data)
            ModuleOrder.objects.filter(appVersion=data.get('appVersion')).delete()
            return {'status': True, 'result': 'Module order deleted'}, 200
        except Exception as error:
            logger = Logger()
            logger.error('Module (DELETE): {error}'.format(error=error))
            return {'status': False, 'result': str(error)}, 500


@swagger_auto_schema(**as_modules_get)
@swagger_auto_schema(**as_modules_post)
@swagger_auto_schema(**as_modules_patch)
@swagger_auto_schema(**as_modules_delete)
@api_view(['GET', 'POST', 'PATCH', 'DELETE'])
def modules(request):
    if request.method in ['GET']:
        result, status_code = modules_get(request)
        return Response(result, status=status_code)
    elif request.method in ['POST']:
        result, status_code = modules_post(request)
        return Response(result, status=status_code)
    elif request.method in ['PATCH']:
        result, status_code = modules_patch(request)
        return Response(result, status=status_code)
    elif request.method in ['DELETE']:
        result, status_code = modules_delete(request)
        return Response(result, status=status_code)


@IsAuthorized
def modules_post(request):
    try:
        data = dict(request.data)
        modules = Modules(**data)
        modules.save()
        return {'status': True, 'result': 'Module created'}, 200
    except Exception as error:
        return {'status': False, 'result': str(error)}, 422


@IsAuthorized
def modules_patch(request):
    data = dict(request.data)
    modules = Modules.objects.filter(slug=data.get('slug'), version=data.get('version')).first()
    if modules is not None:
        modules.partial_update(**data)
        return {'status': True, 'result': 'Module patched'}, 200
    else:
        return {'status': True, 'result': message.no_record_found}, 404


@IsAuthorized
def modules_delete(request):
    data = dict(request.data)
    modules = Modules.objects.filter(slug=data.get('slug'), version=data.get('version')).first()
    if modules is not None:
        modules.delete()
        return {'status': True, 'result': 'Module deleted'}, 200
    else:
        return {'status': True, 'result': message.no_record_found}, 404


def modules_get(request):
    slug = request.GET.get('slug')
    modules = list(Modules.objects.filter(slug=slug).all())
    serializer = ModulesSerializer(modules, many=True)
    return {'status': True, 'result': serializer.data}, 200


@swagger_auto_schema(**as_modules_by_app_get)
@swagger_auto_schema(**as_modules_by_app_post)
@swagger_auto_schema(**as_modules_by_app_patch)
@swagger_auto_schema(**as_modules_by_app_delete)
@api_view(['GET', 'POST', 'PATCH', 'DELETE'])
def modules_by_app(request):
    if request.method in ['GET']:
        result, status_code = modules_by_app_get(request)
        return Response(result, status=status_code)
    elif request.method in ['POST']:
        result, status_code = modules_by_app_post(request)
        return Response(result, status=status_code)
    elif request.method in ['PATCH']:
        result, status_code = modules_by_app_patch(request)
        return Response(result, status=status_code)
    elif request.method in ['DELETE']:
        result, status_code = modules_by_app_delete(request)
        return Response(result, status=status_code)


@IsAuthorized
def modules_by_app_post(request):
    data = dict(request.data)
    modules = ModulesByApp(**data)
    modules.save()
    return {'status': True, 'result': 'ModuleByApp created'}, 200


@IsAuthorized
def modules_by_app_patch(request):
    data = dict(request.data)
    modules = ModulesByApp.objects.filter(moduleSlug=data.get('moduleSlug'), appVersion=data.get('appVersion')).first()
    if modules is not None:
        modules.partial_update(**data)
        return {'status': True, 'result': 'ModuleByApp patched'}, 200
    else:
        return {'status': True, 'result': message.no_record_found}, 404


@IsAuthorized
def modules_by_app_delete(request):
    data = dict(request.data)
    modules = ModulesByApp.objects.filter(moduleSlug=data.get('moduleSlug'), appVersion=data.get('appVersion')).first()
    if modules is not None:
        modules.delete()
        return {'status': True, 'result': 'ModuleByApp deleted'}, 200
    else:
        return {'status': True, 'result': message.no_record_found}, 404


def modules_by_app_get(request):
    app_version = request.GET.get('appVersion')
    modules = list(ModulesByApp.objects.filter(appVersion=app_version).all())
    serializer = ModulesByAppSerializer(modules, many=True)
    return {'status': True, 'result': serializer.data}, 200


@swagger_auto_schema(**as_modules_for_app_get)
@api_view(['GET'])
def modules_for_app_get(request):
    app_version = request.GET.get('appVersion')
    modules_by_app = list(ModulesByApp.objects.filter(appVersion=app_version).all())
    module_order = ModuleOrder.objects.filter(appVersion=app_version).first()

    modules = list()
    for module_by_app in modules_by_app:
        module = Modules.objects.filter(slug=module_by_app.moduleSlug).first()
        if module is not None:
            modules.append({
                'description': module.description,
                'icon': module.icon,
                'slug': module.slug,
                'status': module_by_app.status,
                'title': module.title,
                'version': module.version
            })

    modules_ordered = list()
    if module_order is not None:
        for slug in module_order.order:
            for i in range(len(modules) - 1, -1, -1):
                if slug == modules[i]['slug']:
                    modules_ordered.append(modules[i])
                    modules.pop(i)

    result = modules_ordered + modules
    return Response({'status': True, 'result': result}, status=200)
