""" Swagger definitions used in the views_*_.py decorators '@swagger_auto_schema(**object)'. Each parameter is given the
    name of the methods in views_*_.py prepended with 'as_' (auto_schema)
"""

from drf_yasg import openapi

from construction_work.serializers import ArticleSerializer
from construction_work.swagger.swagger_abstract_objects import query_id
from construction_work.views.views_messages import Messages

messages = Messages()


as_article = {
    # /api/v1/project/news swagger_auto_schema
    "methods": ["GET"],
    "manual_parameters": [query_id],
    "responses": {
        200: openapi.Response(
            "application/json",
            ArticleSerializer,
            examples={
                "application/json": {
                    "id": 23,
                    "foreign_id": 587690,
                    "active": True,
                    "last_seen": "2023-10-30T13:23:46.788091+01:00",
                    "title": "Elzenhagen Noord",
                    "intro": "<div><p>Elzenhagen Noord is een nieuwe woonwijk met ongeveer 590 huur- en koopwoningen. De ontwikkeling is in 2018 afgerond.</p></div>",
                    "body": '<div><h3 id="h507c9cae-2d12-43d1-94f1-bdbc5704d49c">Waar</h3><p>Elzenhagen Noord ligt in de driehoek van de straten B. Merkelbachsingel en  G.J. Scheurleerweg en de Ring Noord A10 (S116).</p><h3 id="h102a16f8-4f3a-4ed7-8e21-247edbaf83f6">Wanneer</h3><p>De ontwikkeling van Elzenhagen Noord is in 2018 afgerond. Elzenhagen Noord is het eerste gebied van Centrumgebied Amsterdam Noord dat klaar is.</p><h3 id="h98715c80-85ec-40e9-9157-0d7fdcc69e9a">Contact</h3><p>Gebiedsontwikkeling Centrum Amsterdam Noord <br /><a href="tel:0202544005">020 254 4005</a><br /><a href="mailto:ontwikkeling.centrumamsterdam-noord@amsterdam.nl">ontwikkeling.centrumamsterdam-noord@amsterdam.nl</a></p><h3 id="hbd3d2d33-0f1c-47a5-bc1a-80f53da5ae7d">Zie ook</h3><ul><li><a href="https://www.woneninelzenhagen.nl/" class="externLink">Wonen in Elzenhagen</a></li><li><a href="584340" itemtype="1" pagetype="subhome" class="siteLink ptsubhome">Centrumgebied Amsterdam Noord: nieuw stedelijk centrum</a></li></ul></div>',
                    "image": {
                        "id": 21002013,
                        "sources": [
                            {
                                "url": "/publish/pages/479259/hero_elzhnrd.jpg",
                                "width": 940,
                                "height": 415,
                            },
                            {
                                "url": "/publish/pages/479259/220px/hero_elzhnrd.jpg",
                                "width": 220,
                                "height": 97,
                            },
                            {
                                "url": "/publish/pages/479259/460px/hero_elzhnrd.jpg",
                                "width": 460,
                                "height": 203,
                            },
                            {
                                "url": "/publish/pages/479259/700px/hero_elzhnrd.jpg",
                                "width": 700,
                                "height": 309,
                            },
                            {
                                "url": "/publish/pages/479259/80px/hero_elzhnrd.jpg",
                                "width": 80,
                                "height": 35,
                            },
                        ],
                        "aspectRatio": 2.2650602409638556,
                        "alternativeText": None,
                    },
                    "type": "work",
                    "url": "http://www.amsterdam.nl/projecten/centrumgebied-amsterdam-noord/deelproject/elzenhagen-noord/",
                    "creation_date": "2012-10-22T12:13:00+02:00",
                    "modification_date": "2022-08-18T08:47:00+02:00",
                    "publication_date": "2022-08-18T08:47:00+02:00",
                    "expiration_date": None,
                    "projects": [446],
                }
            },
        ),
        403: openapi.Response(
            "application/json",
            examples={"application/json": messages.access_denied},
        ),
        400: openapi.Response(
            "application/json",
            examples={"application/json": messages.invalid_query},
        ),
        404: openapi.Response(
            "application/json",
            examples={"application/json": messages.no_record_found},
        ),
    },
    "tags": ["Projects"],
}


as_articles_get = {
    # /api/v1/articles
    "methods": ["GET"],
    "manual_parameters": [
        openapi.Parameter(
            "project-ids",
            openapi.IN_QUERY,
            "Query articles by project-identifier(s)",
            type=openapi.TYPE_ARRAY,
            items=openapi.Items(type=openapi.TYPE_STRING),
            required=False,
        ),
        openapi.Parameter(
            "limit",
            openapi.IN_QUERY,
            "Limit returned items",
            type=openapi.TYPE_INTEGER,
            format="<int>",
            required=False,
        ),
        openapi.Parameter(
            "sort-by",
            openapi.IN_QUERY,
            "Sort response (default: publication_date)",
            type=openapi.TYPE_STRING,
            format="<any key from model>",
            required=False,
        ),
        openapi.Parameter(
            "sort-order",
            openapi.IN_QUERY,
            "Sorting order (default: desc)",
            type=openapi.TYPE_STRING,
            format="<asc, desc>",
            required=False,
        ),
    ],
    "responses": {
        200: openapi.Response(
            "application/json",
            openapi.Schema(
                type=openapi.TYPE_ARRAY,
                items=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "identifier": openapi.Schema(
                            type=openapi.TYPE_STRING, description="identifier"
                        ),
                        "title": openapi.Schema(
                            type=openapi.TYPE_STRING, description="title"
                        ),
                        "publication_date": openapi.Schema(
                            type=openapi.TYPE_STRING, description="year-month-day"
                        ),
                        "type": openapi.Schema(
                            type=openapi.TYPE_STRING, description="<news|work|warning>"
                        ),
                        "image": openapi.Schema(
                            type=openapi.TYPE_OBJECT, properties={}
                        ),
                    },
                ),
            ),
            examples={"application/json": {"status": True, "result": {}}},
        )
    },
    "tags": ["Articles", "Projects"],
}
