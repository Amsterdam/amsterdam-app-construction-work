""" UNITTEST TEST DATA """
# pylint: disable=line-too-long, too-many-lines
import datetime


class TestData:
    """ Unittest test data """
    def __init__(self):
        self.assets = [
            {
                "identifier": "0000000000",
                "url": "https://localhost/test0.pdf",
                "mime_type": "application/pdf",
                "data": b""
            },
            {
                "identifier": "0000000001",
                "url": "https://localhost/test1.pdf",
                "mime_type": "application/pdf",
                "data": b""
            }
        ]

        self.images = [
            {
                "identifier": "0000000000",
                "size": "orig",
                "url": "https://localhost/image0.jpg",
                "filename": "image.jpg",
                "description": "",
                "mime_type": "image/jpg",
                "data": b""
            },
            {
                "identifier": "0000000001",
                "size": "orig",
                "url": "https://localhost/image1.jpg",
                "filename": "image.jpg",
                "description": "",
                "mime_type": "image/jpg",
                "data": b""
            }
        ]

        self.project_images = [
            {
                "type": "banner",
                "sources": {
                    "orig": {
                        "url": "https://localhost/image.jpg",
                        "size": "orig",
                        "filename": "image.jpg",
                        "image_id": "0000000000",
                        "description": ""
                    }
                }
            },
            {
                "type": "additional",
                "sources": {
                    "orig": {
                        "url": "https://localhost/image.jpg",
                        "size": "orig",
                        "filename": "image.jpg",
                        "image_id": "0000000001",
                        "description": ""
                    }
                }
            }
        ]

        self.projects = [
            {
                "identifier": "0000000000",
                "project_type": "kade",
                "active": True,
                "district_id": 0,
                "district_name": "West",
                "title": "title",
                "subtitle": "subtitle",
                "content_html": "html content",
                "content_text": "text content",
                "images": self.project_images,
                "publication_date": "1970-01-01",
                "modification_date": "1970-01-01",
                "source_url": "https://localhost/test0/"
            },
            {
                "identifier": "0000000001",
                "project_type": "brug",
                "active": True,
                "district_id": 1,
                "district_name": "Oost",
                "title": "title",
                "subtitle": "subtitle",
                "content_html": "html content",
                "content_text": "text content",
                "images": self.project_images,
                "publication_date": "1970-01-02",
                "modification_date": "1970-01-02",
                "source_url": "https://localhost/test1/"
            }
        ]

        self.project_details = [
            {
                "identifier": "0000000000",
                "project_type": "brug",
                "active": True,
                "body": {
                    "what": [{"html": "html content", "text": "text content", "title": "title"}],
                    "when": [{"html": "html content", "text": "text content", "title": "title"}],
                    "work": [{"html": "html content", "text": "text content", "title": "title"}],
                    "where": [{"html": "html content", "text": "text content", "title": "title"}],
                    "contact": [{"html": "html content", "text": "text content", "title": "title"}],
                    "timeline": {},
                    "more-info": [{"html": "html content", "text": "text content", "title": "title"}]
                },
                "contacts": [],
                "coordinates": {"lat": 0.0, "lon": 0.0},
                "district_id": 0,
                "district_name": "West",
                "images": self.project_images,
                "news": [
                    {
                        "url": "https://localhost/news/0",
                        "identifier": "00000000000",
                        "project_identifier":
                            "00000000000"
                    }
                ],
                "page_id": 0,
                "title": "test0",
                "subtitle": "subtitle",
                "rel_url": "project/0",
                "url": "https://localhost/project/0"
            },
            {
                "identifier": "0000000001",
                "project_type": "brug",
                "active": True,
                "body": {
                    "what": [{"html": "html content", "text": "text content", "title": "title"}],
                    "when": [{"html": "html content", "text": "text content", "title": "title"}],
                    "work": [{"html": "html content", "text": "text content", "title": "title"}],
                    "where": [{"html": "html content", "text": "text content", "title": "title"}],
                    "contact": [{"html": "html content", "text": "text content", "title": "title"}],
                    "timeline": {},
                    "more-info": [{"html": "html content", "text": "text content", "title": "title"}]
                },
                "contacts": [],
                "coordinates": {"lat": 1.0, "lon": 1.0},
                "district_id": 0,
                "district_name": "West",
                "images": self.project_images,
                "news": [],
                "page_id": 0,
                "title": "test0",
                "subtitle": "subtitle",
                "rel_url": "project/0",
                "url": "https://localhost/project/0"
            }
        ]

        self.news = [
            {
                "last_seen": datetime.datetime.strptime('1970-01-01T00:00:00.000000', '%Y-%d-%mT%H:%M:%S.000000'),
                "active": True,
                "project_type": "kade",
                "identifier": "0000000000",
                "project_identifier": "0000000000",
                "url": "https://localhost/news0",
                "title": "title0",
                "publication_date": "1970-01-01",
                "body": {
                    "content": {
                        "html": "html content",
                        "text": "text content"
                    },
                    "preface": {
                        "html": "html content",
                        "text": "text content"
                    },
                    "summary": {
                        "html": "html content",
                        "text": "text content"
                    }
                },
                "images": self.project_images,
                "assets": [
                    {
                        "url": "https://localhost/test0.pdf",
                        "title": "title",
                        "filename": "test0.pdf",
                        "mime_type": "application/pdf",
                        "identifier": "0000000000"
                    }
                ]
            },
            {
                "last_seen": datetime.datetime.strptime('1970-01-01T00:00:00.000000', '%Y-%d-%mT%H:%M:%S.000000'),
                "active": True,
                "project_type": "kade",
                "identifier": "0000000001",
                "project_identifier": "0000000001",
                "url": "https://localhost/news1",
                "title": "title1",
                "publication_date": "1970-01-02",
                "body": {
                    "content": {
                        "html": "html content",
                        "text": "text content"
                    },
                    "preface": {
                        "html": "html content",
                        "text": "text content"
                    },
                    "summary": {
                        "html": "html content",
                        "text": "text content"
                    }
                },
                "images": self.project_images,
                "assets": [
                    {
                        "url": "https://localhost/test1.pdf",
                        "title": "title",
                        "filename": "test1.pdf",
                        "mime_type": "application/pdf",
                        "identifier": "0000000001"
                    }
                ]
            }
        ]

        self.image_download_jobs = [
            {
                'url': 'valid_url',
                'image_id': '0',
                'filename': 'mock0.jpg',
                'description': '',
                'size': 'orig'
            },
            {
                'url': 'invalid_url',
                'image_id': '1',
                'filename': 'mock1.jpg',
                'description': '',
                'size': 'orig'
            }
        ]

        self.iprox_recursion = {
            "Nam": "Target",
            "cluster": [
                {"Nam": "Target", "cluster": [{"Nam": "Target", "veld": []}]},
                {"Nam": "Target", "cluster": {"Nam": "Target", "veld": {}}},
                {"Nam": "Invalid Target", "cluster": {}}
            ]
        }

        self.iprox_project_detail = {
            "item": {
                "ItmIdt": "1209781",
                "Url": "https://www.amsterdam.nl/verkeersprojecten/kademuren/maatregelen-vernieuwen/herengracht-213-243/",
                "resolved": "true",
                "relUrl": "verkeersprojecten/kademuren/maatregelen-vernieuwen/herengracht-213-243",
                "page": {
                    "lang": "nl",
                    "PagIdt": "970738",
                    "ItmIdt": "1209781",
                    "pagetype": "subhome",
                    "interactive": "0",
                    "Cmp": "1",
                    "cluster-stripped": "true",
                    "CorDtm": "20210831",
                    "CreGebNam": "Jacqueline Schermer",
                    "LstPubGebNam": "Jacqueline Schermer",
                    "title": "Herengracht 213 tot 243: maatregelen door slechte kademuur",
                    "Lbl": "Herengracht 213 tot 243: maatregelen door slechte kademuur",
                    "_": "\r\n  ",
                    "cluster": [
                        {
                            "PagClsIdt": "16090097",
                            "VlgNum": "0",
                            "Opt": "0",
                            "RepTyp": "1",
                            "DefVlgNum": "0",
                            "ProTypIdt": "51",
                            "Nam": "Meta",
                            "ProTypNam": "Meta",
                            "ProTypAka": "meta",
                            "_": "\r\n    ",
                            "cluster": {
                                "PagClsIdt": "16090098",
                                "ParIdt": "16090097",
                                "VlgNum": "0",
                                "Opt": "0",
                                "RepTyp": "1",
                                "DefVlgNum": "0",
                                "Nam": "Meta",
                                "_": "\r\n      ",
                                "cluster": [
                                    {
                                        "PagClsIdt": "16090101",
                                        "ParIdt": "16090098",
                                        "VlgNum": "0",
                                        "Opt": "0",
                                        "RepTyp": "1",
                                        "DefVlgNum": "0",
                                        "Nam": "Gegevens",
                                        "_": "\r\n        ",
                                        "veld": [
                                            {
                                                "PagVldIdt": "21621950",
                                                "VlgNum": "0",
                                                "GgvTyp": "1",
                                                "Nam": "Gebruik Amsterdamse kaartmateriaal",
                                                "Wrd": "0",
                                                "_": "\r\n          ",
                                                "script": {
                                                    "type": "text/javascript"
                                                },
                                                "style": {
                                                    "resolved": "true"
                                                }
                                            },
                                            {
                                                "PagVldIdt": "21621951",
                                                "VlgNum": "1",
                                                "GgvTyp": "1",
                                                "Nam": "Geen share-buttons",
                                                "Wrd": "0",
                                                "_": "\r\n          ",
                                                "script": {
                                                    "type": "text/javascript"
                                                },
                                                "style": {
                                                    "resolved": "true"
                                                }
                                            },
                                            {
                                                "PagVldIdt": "21621952",
                                                "VlgNum": "2",
                                                "GgvTyp": "2",
                                                "Nam": "Auteur",
                                                "Wrd": "Mischa Tiebie",
                                                "_": "\r\n          ",
                                                "script": {
                                                    "type": "text/javascript"
                                                },
                                                "style": {
                                                    "resolved": "true"
                                                }
                                            },
                                            {
                                                "PagVldIdt": "21621955",
                                                "VlgNum": "8",
                                                "GgvTyp": "10",
                                                "Nam": "Basis afbeelding",
                                                "FilNam": "herengracht213_1.jpg",
                                                "_": "\r\n          ",
                                                "Src": {
                                                    "resolved": "true",
                                                    "_": "/publish/pages/970738/herengracht213_1.jpg"
                                                },
                                                "Txt": "\r\n              <div>\r\n                <img src=\"/publish/pages/970738/herengracht213_1.jpg\" width=\"620\" data-sources=\"[{&quot;width&quot;:80,&quot;height&quot;:45,&quot;src&quot;:&quot;/publish/pages/970738/80px/herengracht213_1.jpg&quot;,&quot;sizeClass&quot;:&quot;size_80px&quot;},{&quot;width&quot;:220,&quot;height&quot;:123,&quot;src&quot;:&quot;/publish/pages/970738/220px/herengracht213_1.jpg&quot;,&quot;sizeClass&quot;:&quot;size_220px&quot;},{&quot;width&quot;:620,&quot;height&quot;:348,&quot;src&quot;:&quot;/publish/pages/970738/herengracht213_1.jpg&quot;}]\" data-original=\"{&quot;width&quot;:940,&quot;height&quot;:415,&quot;src&quot;:&quot;/publish/pages/970738/orig/herengracht213_1.jpg&quot;,&quot;sizeClass&quot;:&quot;size_orig&quot;}\" data-original-src=\"/publish/pages/970738/orig/herengracht213_1.jpg\" height=\"348\" alt=\"\" data-id=\"970738\" data-hoffset=\"0\" data-voffset=\"0\" id=\"img_pagvld_21621955_0\" class=\"img-bitmap img_pagvld_21621955_0\" resolved=\"true\" />\r\n              </div>\r\n            ",
                                                "asset": [
                                                    {
                                                        "FilNam": "herengracht213_1.jpg",
                                                        "_": "\r\n            ",
                                                        "Src": {
                                                            "resolved": "true",
                                                            "_": "/publish/pages/970738/220px/herengracht213_1.jpg"
                                                        }
                                                    },
                                                    {
                                                        "FilNam": "herengracht213_1.jpg",
                                                        "_": "\r\n            ",
                                                        "Src": {
                                                            "resolved": "true",
                                                            "_": "/publish/pages/970738/80px/herengracht213_1.jpg"
                                                        }
                                                    },
                                                    {
                                                        "FilNam": "herengracht213_1.jpg",
                                                        "_": "\r\n            ",
                                                        "Src": {
                                                            "resolved": "true",
                                                            "_": "/publish/pages/970738/orig/herengracht213_1.jpg"
                                                        }
                                                    }
                                                ],
                                                "script": {
                                                    "type": "text/javascript"
                                                },
                                                "style": {
                                                    "resolved": "true",
                                                    "_": "#img_pagvld_21621955_0, .img_pagvld_21621955_0 {\r\n        width:620px; max-width:620px; height:348px; max-height:348px; \r\n      }\r\n      .achtergrond_img_pagvld_21621955_0 {\r\n        background-image: url( /publish/pages/970738/herengracht213_1.jpg );\r\n      }\r\n\r\n      #img_pagvld_21621955_0.size_220px, .img_pagvld_21621955_0.size_220px {\r\n            width:220px;max-width:220px;height:123px;max-height:123px;\r\n          }\r\n          .achtergrond_img_pagvld_21621955_0.size_220px {\r\n            background-image: url( /publish/pages/970738/220px/herengracht213_1.jpg );\r\n          }\r\n        #img_pagvld_21621955_0.size_80px, .img_pagvld_21621955_0.size_80px {\r\n            width:80px;max-width:80px;height:45px;max-height:45px;\r\n          }\r\n          .achtergrond_img_pagvld_21621955_0.size_80px {\r\n            background-image: url( /publish/pages/970738/80px/herengracht213_1.jpg );\r\n          }\r\n        #img_pagvld_21621955_0.size_orig, .img_pagvld_21621955_0.size_orig {\r\n            width:940px;max-width:940px;height:415px;max-height:415px;\r\n          }\r\n          .achtergrond_img_pagvld_21621955_0.size_orig {\r\n            background-image: url( /publish/pages/970738/orig/herengracht213_1.jpg );\r\n          }\r\n        "
                                                },
                                                "styleattributes": {
                                                    "forclass": "img_pagvld_21621955_0"
                                                }
                                            },
                                            {
                                                "PagVldIdt": "21621954",
                                                "VlgNum": "10",
                                                "GgvTyp": "5",
                                                "Nam": "Samenvatting",
                                                "_": "\r\n          ",
                                                "Txt": "\r\n              <div>\r\n                <p>We nemen maatregelen om kademuur Herengracht 213 tot 243 veilig te houden en levensduur te verlengen. We willen juli 2021 starten met het versterken.</p>\r\n              </div>\r\n            ",
                                                "script": {
                                                    "type": "text/javascript"
                                                },
                                                "style": {
                                                    "resolved": "true"
                                                }
                                            },
                                            {
                                                "PagVldIdt": "21621953",
                                                "VlgNum": "15",
                                                "GgvTyp": "7",
                                                "Nam": "Brondatum",
                                                "Dtm": "20210504",
                                                "_": "\r\n          ",
                                                "script": {
                                                    "type": "text/javascript"
                                                },
                                                "style": {
                                                    "resolved": "true"
                                                }
                                            }
                                        ]
                                    },
                                    {
                                        "PagClsIdt": "16090100",
                                        "ParIdt": "16090098",
                                        "VlgNum": "0",
                                        "Opt": "0",
                                        "RepTyp": "1",
                                        "DefVlgNum": "1",
                                        "Nam": "Typering",
                                        "_": "\r\n        ",
                                        "veld": {
                                            "PagVldIdt": "21621949",
                                            "VlgNum": "4",
                                            "GgvTyp": "1",
                                            "Nam": "Opnemen in AmsterdamMail",
                                            "Wrd": "0",
                                            "_": "\r\n          ",
                                            "script": {
                                                "type": "text/javascript"
                                            },
                                            "style": {
                                                "resolved": "true"
                                            }
                                        }
                                    },
                                    {
                                        "PagClsIdt": "16090099",
                                        "ParIdt": "16090098",
                                        "VlgNum": "0",
                                        "Opt": "1",
                                        "RepTyp": "2",
                                        "DefVlgNum": "2",
                                        "Nam": "Speciale trefwoorden",
                                        "_": "\r\n        "
                                    },
                                    {
                                        "PagClsIdt": "16090102",
                                        "ParIdt": "16090098",
                                        "VlgNum": "0",
                                        "Opt": "0",
                                        "RepTyp": "2",
                                        "DefVlgNum": "3",
                                        "Nam": "Kenmerken",
                                        "_": "\r\n        ",
                                        "veld": {
                                            "PagVldIdt": "21621956",
                                            "SelItmIdt": "5398",
                                            "VlgNum": "0",
                                            "GgvTyp": "252",
                                            "Nam": "Kenmerk",
                                            "Wrd": "Centrum",
                                            "Src": "Stadsdeel",
                                            "SelWrd": "Centrum",
                                            "_": "\r\n          ",
                                            "item": {
                                                "SelItmIdt": "5398",
                                                "Wrd": "Centrum",
                                                "_": "\r\n            "
                                            },
                                            "script": {
                                                "type": "text/javascript"
                                            },
                                            "style": {
                                                "resolved": "true"
                                            }
                                        }
                                    },
                                    {
                                        "PagClsIdt": "16090103",
                                        "ParIdt": "16090098",
                                        "VlgNum": "1",
                                        "Opt": "0",
                                        "RepTyp": "2",
                                        "DefVlgNum": "3",
                                        "Nam": "Kenmerken",
                                        "_": "\r\n        ",
                                        "veld": {
                                            "PagVldIdt": "21621957",
                                            "SelItmIdt": "6075",
                                            "VlgNum": "0",
                                            "GgvTyp": "252",
                                            "Nam": "Kenmerk",
                                            "Wrd": "Tunnels, bruggen, kades, oevers",
                                            "Src": "Soort project",
                                            "SelWrd": "Tunnels, bruggen, kades, oevers",
                                            "_": "\r\n          ",
                                            "item": {
                                                "SelItmIdt": "6075",
                                                "Wrd": "Tunnels, bruggen, kades, oevers",
                                                "_": "\r\n            "
                                            },
                                            "script": {
                                                "type": "text/javascript"
                                            },
                                            "style": {
                                                "resolved": "true"
                                            }
                                        }
                                    }
                                ]
                            }
                        },
                        {
                            "PagClsIdt": "16090139",
                            "VlgNum": "0",
                            "Opt": "0",
                            "RepTyp": "1",
                            "DefVlgNum": "1",
                            "Nam": "Instellingen",
                            "_": "\r\n    ",
                            "veld": {
                                "PagVldIdt": "21622036",
                                "VlgNum": "0",
                                "GgvTyp": "1",
                                "Nam": "Kaart verbergen",
                                "Wrd": "0",
                                "_": "\r\n      ",
                                "script": {
                                    "type": "text/javascript"
                                },
                                "style": {
                                    "resolved": "true"
                                }
                            }
                        },
                        {
                            "PagClsIdt": "16090104",
                            "VlgNum": "0",
                            "Opt": "1",
                            "RepTyp": "2",
                            "DefVlgNum": "2",
                            "Nam": "Blok",
                            "_": "\r\n    ",
                            "cluster": [
                                {
                                    "PagClsIdt": "16090135",
                                    "ParIdt": "16090104",
                                    "VlgNum": "22",
                                    "Opt": "0",
                                    "RepTyp": "1",
                                    "DefVlgNum": "3",
                                    "Nam": "Afbeelding",
                                    "_": "\r\n      ",
                                    "cluster": [
                                        {
                                            "PagClsIdt": "16090136",
                                            "ParIdt": "16090135",
                                            "VlgNum": "0",
                                            "Opt": "0",
                                            "RepTyp": "1",
                                            "DefVlgNum": "0",
                                            "Nam": "Afbeelding",
                                            "_": "\r\n        ",
                                            "veld": [
                                                {
                                                    "PagVldIdt": "21622033",
                                                    "VlgNum": "1",
                                                    "GgvTyp": "1",
                                                    "Nam": "Kleine kop",
                                                    "Wrd": "0",
                                                    "_": "\r\n          ",
                                                    "script": {
                                                        "type": "text/javascript"
                                                    },
                                                    "style": {
                                                        "resolved": "true"
                                                    }
                                                },
                                                {
                                                    "PagVldIdt": "21822730",
                                                    "VlgNum": "2",
                                                    "GgvTyp": "10",
                                                    "Nam": "Afbeelding",
                                                    "FilNam": "940x415_herengracht.jpg",
                                                    "_": "\r\n          ",
                                                    "Src": {
                                                        "resolved": "true",
                                                        "_": "/publish/pages/970738/940x415_herengracht.jpg"
                                                    },
                                                    "Txt": "\r\n              <div>\r\n                <img src=\"/publish/pages/970738/940x415_herengracht.jpg\" width=\"940\" data-sources=\"[{&quot;width&quot;:80,&quot;height&quot;:35,&quot;src&quot;:&quot;/publish/pages/970738/80px/940x415_herengracht.jpg&quot;,&quot;sizeClass&quot;:&quot;size_80px&quot;},{&quot;width&quot;:220,&quot;height&quot;:97,&quot;src&quot;:&quot;/publish/pages/970738/220px/940x415_herengracht.jpg&quot;,&quot;sizeClass&quot;:&quot;size_220px&quot;},{&quot;width&quot;:460,&quot;height&quot;:203,&quot;src&quot;:&quot;/publish/pages/970738/460px/940x415_herengracht.jpg&quot;,&quot;sizeClass&quot;:&quot;size_460px&quot;},{&quot;width&quot;:700,&quot;height&quot;:309,&quot;src&quot;:&quot;/publish/pages/970738/700px/940x415_herengracht.jpg&quot;,&quot;sizeClass&quot;:&quot;size_700px&quot;},{&quot;width&quot;:940,&quot;height&quot;:415,&quot;src&quot;:&quot;/publish/pages/970738/940x415_herengracht.jpg&quot;}]\" height=\"415\" alt=\"\" data-id=\"970738\" id=\"img_pagvld_21822730_0\" class=\"img-bitmap img_pagvld_21822730_0\" resolved=\"true\" />\r\n              </div>\r\n            ",
                                                    "asset": [
                                                        {
                                                            "FilNam": "940x415_herengracht.jpg",
                                                            "_": "\r\n            ",
                                                            "Src": {
                                                                "resolved": "true",
                                                                "_": "/publish/pages/970738/460px/940x415_herengracht.jpg"
                                                            }
                                                        },
                                                        {
                                                            "FilNam": "940x415_herengracht.jpg",
                                                            "_": "\r\n            ",
                                                            "Src": {
                                                                "resolved": "true",
                                                                "_": "/publish/pages/970738/80px/940x415_herengracht.jpg"
                                                            }
                                                        },
                                                        {
                                                            "FilNam": "940x415_herengracht.jpg",
                                                            "_": "\r\n            ",
                                                            "Src": {
                                                                "resolved": "true",
                                                                "_": "/publish/pages/970738/220px/940x415_herengracht.jpg"
                                                            }
                                                        },
                                                        {
                                                            "FilNam": "940x415_herengracht.jpg",
                                                            "_": "\r\n            ",
                                                            "Src": {
                                                                "resolved": "true",
                                                                "_": "/publish/pages/970738/700px/940x415_herengracht.jpg"
                                                            }
                                                        }
                                                    ],
                                                    "script": {
                                                        "type": "text/javascript"
                                                    },
                                                    "style": {
                                                        "resolved": "true",
                                                        "_": "#img_pagvld_21822730_0, .img_pagvld_21822730_0 {\r\n        width:940px; max-width:940px; height:415px; max-height:415px; \r\n      }\r\n      .achtergrond_img_pagvld_21822730_0 {\r\n        background-image: url( /publish/pages/970738/940x415_herengracht.jpg );\r\n      }\r\n\r\n      #img_pagvld_21822730_0.size_460px, .img_pagvld_21822730_0.size_460px {\r\n            width:460px;max-width:460px;height:203px;max-height:203px;\r\n          }\r\n          .achtergrond_img_pagvld_21822730_0.size_460px {\r\n            background-image: url( /publish/pages/970738/460px/940x415_herengracht.jpg );\r\n          }\r\n        #img_pagvld_21822730_0.size_80px, .img_pagvld_21822730_0.size_80px {\r\n            width:80px;max-width:80px;height:35px;max-height:35px;\r\n          }\r\n          .achtergrond_img_pagvld_21822730_0.size_80px {\r\n            background-image: url( /publish/pages/970738/80px/940x415_herengracht.jpg );\r\n          }\r\n        #img_pagvld_21822730_0.size_220px, .img_pagvld_21822730_0.size_220px {\r\n            width:220px;max-width:220px;height:97px;max-height:97px;\r\n          }\r\n          .achtergrond_img_pagvld_21822730_0.size_220px {\r\n            background-image: url( /publish/pages/970738/220px/940x415_herengracht.jpg );\r\n          }\r\n        #img_pagvld_21822730_0.size_700px, .img_pagvld_21822730_0.size_700px {\r\n            width:700px;max-width:700px;height:309px;max-height:309px;\r\n          }\r\n          .achtergrond_img_pagvld_21822730_0.size_700px {\r\n            background-image: url( /publish/pages/970738/700px/940x415_herengracht.jpg );\r\n          }\r\n        "
                                                    },
                                                    "styleattributes": {
                                                        "forclass": "img_pagvld_21822730_0"
                                                    }
                                                }
                                            ]
                                        },
                                        {
                                            "PagClsIdt": "16090137",
                                            "ParIdt": "16090135",
                                            "VlgNum": "0",
                                            "Opt": "1",
                                            "RepTyp": "2",
                                            "DefVlgNum": "1",
                                            "Nam": "Verwijzing",
                                            "_": "\r\n        "
                                        }
                                    ]
                                },
                                {
                                    "PagClsIdt": "16090127",
                                    "ParIdt": "16090104",
                                    "VlgNum": "24",
                                    "Opt": "0",
                                    "RepTyp": "1",
                                    "DefVlgNum": "30",
                                    "Nam": "Start groepering",
                                    "_": "\r\n      ",
                                    "veld": [
                                        {
                                            "PagVldIdt": "21622012",
                                            "SelItmIdt": "6864",
                                            "VlgNum": "1",
                                            "GgvTyp": "3",
                                            "Nam": "Achtergrondkleur",
                                            "SelWrd": "Heel lichtgrijs",
                                            "SelAka": "neutral-grey1",
                                            "_": "\r\n        ",
                                            "item": {
                                                "SelItmIdt": "6864",
                                                "Wrd": "Heel lichtgrijs",
                                                "Aka": "neutral-grey1",
                                                "_": "\r\n          "
                                            },
                                            "script": {
                                                "type": "text/javascript"
                                            },
                                            "style": {
                                                "resolved": "true"
                                            }
                                        },
                                        {
                                            "PagVldIdt": "21622011",
                                            "VlgNum": "2",
                                            "GgvTyp": "1",
                                            "Nam": "Paginabreed",
                                            "Wrd": "1",
                                            "_": "\r\n        ",
                                            "script": {
                                                "type": "text/javascript"
                                            },
                                            "style": {
                                                "resolved": "true"
                                            }
                                        }
                                    ]
                                },
                                {
                                    "PagClsIdt": "16090105",
                                    "ParIdt": "16090104",
                                    "VlgNum": "27",
                                    "Opt": "0",
                                    "RepTyp": "1",
                                    "DefVlgNum": "0",
                                    "Nam": "Lijst",
                                    "_": "\r\n      ",
                                    "cluster": [
                                        {
                                            "PagClsIdt": "16090107",
                                            "ParIdt": "16090105",
                                            "VlgNum": "0",
                                            "Opt": "0",
                                            "RepTyp": "1",
                                            "DefVlgNum": "0",
                                            "Nam": "Omschrijving",
                                            "_": "\r\n        ",
                                            "veld": [
                                                {
                                                    "PagVldIdt": "21622174",
                                                    "VlgNum": "0",
                                                    "GgvTyp": "2",
                                                    "Nam": "Titel",
                                                    "Wrd": "Wat er gaat gebeuren",
                                                    "_": "\r\n          ",
                                                    "script": {
                                                        "type": "text/javascript"
                                                    },
                                                    "style": {
                                                        "resolved": "true"
                                                    }
                                                },
                                                {
                                                    "PagVldIdt": "21621958",
                                                    "VlgNum": "1",
                                                    "GgvTyp": "1",
                                                    "Nam": "Kleine kop",
                                                    "Wrd": "0",
                                                    "_": "\r\n          ",
                                                    "script": {
                                                        "type": "text/javascript"
                                                    },
                                                    "style": {
                                                        "resolved": "true"
                                                    }
                                                },
                                                {
                                                    "PagVldIdt": "21621962",
                                                    "VlgNum": "2",
                                                    "GgvTyp": "5",
                                                    "Nam": "Tekst",
                                                    "_": "\r\n          ",
                                                    "Txt": "\r\n              <div>\r\n                <p>De kademuur ter hoogte van Herengracht 213 tot en met 243 is in slechte staat. Dit is de kade tussen de Raadhuisstraat en de Gasthuismolensteeg. Op lange termijn gaan we kademuur helemaal vernieuwen. We hebben tijdelijke maatregelen genomen om de kademuur veilig te houden tot de vernieuwing.</p>\r\n                <p>In 2021 is op basis van onderzoek en metingen vastgesteld dat de houten fundering onder de kademuur op meerdere plekken gebreken vertoont. Zoals funderingspalen die scheef onder de kademuur staan. In het metselwerk van de kademuur zitten scheuren. De kademuur bewoog op meerdere punten richting het water.</p>\r\n              </div>\r\n            ",
                                                    "script": {
                                                        "type": "text/javascript"
                                                    },
                                                    "style": {
                                                        "resolved": "true"
                                                    }
                                                },
                                                {
                                                    "PagVldIdt": "21621959",
                                                    "VlgNum": "8",
                                                    "GgvTyp": "1",
                                                    "Nam": "Kolommen",
                                                    "Wrd": "0",
                                                    "_": "\r\n          ",
                                                    "script": {
                                                        "type": "text/javascript"
                                                    },
                                                    "style": {
                                                        "resolved": "true"
                                                    }
                                                },
                                                {
                                                    "PagVldIdt": "21621960",
                                                    "VlgNum": "10",
                                                    "GgvTyp": "1",
                                                    "Nam": "Vaste hoogte",
                                                    "Wrd": "0",
                                                    "_": "\r\n          ",
                                                    "script": {
                                                        "type": "text/javascript"
                                                    },
                                                    "style": {
                                                        "resolved": "true"
                                                    }
                                                },
                                                {
                                                    "PagVldIdt": "21621961",
                                                    "VlgNum": "11",
                                                    "GgvTyp": "1",
                                                    "Nam": "Geen ezelsoor",
                                                    "Wrd": "0",
                                                    "_": "\r\n          ",
                                                    "script": {
                                                        "type": "text/javascript"
                                                    },
                                                    "style": {
                                                        "resolved": "true"
                                                    }
                                                },
                                                {
                                                    "PagVldIdt": "21791064",
                                                    "SelItmIdt": "7055",
                                                    "VlgNum": "12",
                                                    "GgvTyp": "3",
                                                    "Nam": "App categorie",
                                                    "SelWrd": "Wat",
                                                    "SelAka": "what",
                                                    "_": "\r\n          ",
                                                    "item": {
                                                        "SelItmIdt": "7055",
                                                        "Wrd": "Wat",
                                                        "Aka": "what",
                                                        "_": "\r\n            "
                                                    },
                                                    "script": {
                                                        "type": "text/javascript"
                                                    },
                                                    "style": {
                                                        "resolved": "true"
                                                    }
                                                }
                                            ]
                                        },
                                        {
                                            "PagClsIdt": "16090106",
                                            "ParIdt": "16090105",
                                            "VlgNum": "0",
                                            "Opt": "1",
                                            "RepTyp": "2",
                                            "DefVlgNum": "1",
                                            "Nam": "Verwijzing",
                                            "_": "\r\n        "
                                        }
                                    ]
                                },
                                {
                                    "PagClsIdt": "16090116",
                                    "ParIdt": "16090104",
                                    "VlgNum": "30",
                                    "Opt": "0",
                                    "RepTyp": "1",
                                    "DefVlgNum": "0",
                                    "Nam": "Lijst",
                                    "_": "\r\n      ",
                                    "cluster": [
                                        {
                                            "PagClsIdt": "16090118",
                                            "ParIdt": "16090116",
                                            "VlgNum": "0",
                                            "Opt": "0",
                                            "RepTyp": "1",
                                            "DefVlgNum": "0",
                                            "Nam": "Omschrijving",
                                            "_": "\r\n        ",
                                            "veld": [
                                                {
                                                    "PagVldIdt": "21621994",
                                                    "VlgNum": "0",
                                                    "GgvTyp": "2",
                                                    "Nam": "Titel",
                                                    "Wrd": "Maatregelen",
                                                    "_": "\r\n          ",
                                                    "script": {
                                                        "type": "text/javascript"
                                                    },
                                                    "style": {
                                                        "resolved": "true"
                                                    }
                                                },
                                                {
                                                    "PagVldIdt": "21621990",
                                                    "VlgNum": "1",
                                                    "GgvTyp": "1",
                                                    "Nam": "Kleine kop",
                                                    "Wrd": "0",
                                                    "_": "\r\n          ",
                                                    "script": {
                                                        "type": "text/javascript"
                                                    },
                                                    "style": {
                                                        "resolved": "true"
                                                    }
                                                },
                                                {
                                                    "PagVldIdt": "21621995",
                                                    "VlgNum": "2",
                                                    "GgvTyp": "5",
                                                    "Nam": "Tekst",
                                                    "_": "\r\n          ",
                                                    "Txt": "\r\n              <div>\r\n                <ul>\r\n                  <li>Van 10 mei tot 27 augustus 2021 was de Herengracht tussen de Raadhuisstraat en de Gasthuismolensteeg afgesloten voor gemotoriseerd verkeer.</li>\r\n                  <li>Van 12 juli tot 26 augustus 2021 is de kademuur versterkt met een veiligheidsconstructie van damwanden die in het water voor de kade is geplaatst.</li>\r\n                  <li>Op de rand van de kade staat een laag, groen hek. Dit is een bescherming om te voorkomen dat mensen hier van de kade, op de veiligheidsconstructie vallen. Het hek blijft staan tot de vernieuwing van de kademuur.</li>\r\n                  <li>Ter hoogte van Herengracht 213 tot en met 243 geldt een afmeerverbod. De veiligheidsconstructie voor de kade is niet berekend op het afmeren van vaartuigen.</li>\r\n                  <li>In het najaar van 2021 zetten we planten in het zand tussen de veiligheidsconstructie en de kademuur. Zo geven we de kade een groenere aanblik en stimuleren we de biodiversiteit.</li>\r\n                  <li>We blijven de kademuur voorlopig volgen met metingen.</li>\r\n                </ul>\r\n              </div>\r\n            ",
                                                    "script": {
                                                        "type": "text/javascript"
                                                    },
                                                    "style": {
                                                        "resolved": "true"
                                                    }
                                                },
                                                {
                                                    "PagVldIdt": "21621991",
                                                    "VlgNum": "8",
                                                    "GgvTyp": "1",
                                                    "Nam": "Kolommen",
                                                    "Wrd": "0",
                                                    "_": "\r\n          ",
                                                    "script": {
                                                        "type": "text/javascript"
                                                    },
                                                    "style": {
                                                        "resolved": "true"
                                                    }
                                                },
                                                {
                                                    "PagVldIdt": "21621992",
                                                    "VlgNum": "10",
                                                    "GgvTyp": "1",
                                                    "Nam": "Vaste hoogte",
                                                    "Wrd": "0",
                                                    "_": "\r\n          ",
                                                    "script": {
                                                        "type": "text/javascript"
                                                    },
                                                    "style": {
                                                        "resolved": "true"
                                                    }
                                                },
                                                {
                                                    "PagVldIdt": "21621993",
                                                    "VlgNum": "11",
                                                    "GgvTyp": "1",
                                                    "Nam": "Geen ezelsoor",
                                                    "Wrd": "0",
                                                    "_": "\r\n          ",
                                                    "script": {
                                                        "type": "text/javascript"
                                                    },
                                                    "style": {
                                                        "resolved": "true"
                                                    }
                                                },
                                                {
                                                    "PagVldIdt": "21791065",
                                                    "SelItmIdt": "7062",
                                                    "VlgNum": "12",
                                                    "GgvTyp": "3",
                                                    "Nam": "App categorie",
                                                    "SelWrd": "Werkzaamheden / Maatregelen",
                                                    "SelAka": "work",
                                                    "_": "\r\n          ",
                                                    "item": {
                                                        "SelItmIdt": "7062",
                                                        "Wrd": "Werkzaamheden / Maatregelen",
                                                        "Aka": "work",
                                                        "_": "\r\n            "
                                                    },
                                                    "script": {
                                                        "type": "text/javascript"
                                                    },
                                                    "style": {
                                                        "resolved": "true"
                                                    }
                                                }
                                            ]
                                        },
                                        {
                                            "PagClsIdt": "16090117",
                                            "ParIdt": "16090116",
                                            "VlgNum": "0",
                                            "Opt": "1",
                                            "RepTyp": "2",
                                            "DefVlgNum": "1",
                                            "Nam": "Verwijzing",
                                            "_": "\r\n        "
                                        }
                                    ]
                                },
                                {
                                    "PagClsIdt": "16233213",
                                    "ParIdt": "16090104",
                                    "VlgNum": "33",
                                    "Opt": "0",
                                    "RepTyp": "1",
                                    "DefVlgNum": "0",
                                    "Nam": "Lijst",
                                    "_": "\r\n      ",
                                    "cluster": [
                                        {
                                            "PagClsIdt": "16233215",
                                            "ParIdt": "16233213",
                                            "VlgNum": "0",
                                            "Opt": "0",
                                            "RepTyp": "1",
                                            "DefVlgNum": "0",
                                            "Nam": "Omschrijving",
                                            "_": "\r\n        ",
                                            "veld": [
                                                {
                                                    "PagVldIdt": "21819506",
                                                    "VlgNum": "0",
                                                    "GgvTyp": "2",
                                                    "Nam": "Titel",
                                                    "Wrd": "Wanneer",
                                                    "_": "\r\n          ",
                                                    "script": {
                                                        "type": "text/javascript"
                                                    },
                                                    "style": {
                                                        "resolved": "true"
                                                    }
                                                },
                                                {
                                                    "PagVldIdt": "21819205",
                                                    "VlgNum": "1",
                                                    "GgvTyp": "1",
                                                    "Nam": "Kleine kop",
                                                    "Wrd": "0",
                                                    "_": "\r\n          ",
                                                    "script": {
                                                        "type": "text/javascript"
                                                    },
                                                    "style": {
                                                        "resolved": "true"
                                                    }
                                                },
                                                {
                                                    "PagVldIdt": "21819507",
                                                    "VlgNum": "2",
                                                    "GgvTyp": "5",
                                                    "Nam": "Tekst",
                                                    "_": "\r\n          ",
                                                    "Txt": "\r\n              <div>\r\n                <p>Op lange termijn vernieuwen we de hele kademuur. Wanneer dit gebeurt, is op dit moment nog niet bekend.</p>\r\n              </div>\r\n            ",
                                                    "script": {
                                                        "type": "text/javascript"
                                                    },
                                                    "style": {
                                                        "resolved": "true"
                                                    }
                                                },
                                                {
                                                    "PagVldIdt": "21819206",
                                                    "VlgNum": "8",
                                                    "GgvTyp": "1",
                                                    "Nam": "Kolommen",
                                                    "Wrd": "0",
                                                    "_": "\r\n          ",
                                                    "script": {
                                                        "type": "text/javascript"
                                                    },
                                                    "style": {
                                                        "resolved": "true"
                                                    }
                                                },
                                                {
                                                    "PagVldIdt": "21819207",
                                                    "VlgNum": "10",
                                                    "GgvTyp": "1",
                                                    "Nam": "Vaste hoogte",
                                                    "Wrd": "0",
                                                    "_": "\r\n          ",
                                                    "script": {
                                                        "type": "text/javascript"
                                                    },
                                                    "style": {
                                                        "resolved": "true"
                                                    }
                                                },
                                                {
                                                    "PagVldIdt": "21819208",
                                                    "VlgNum": "11",
                                                    "GgvTyp": "1",
                                                    "Nam": "Geen ezelsoor",
                                                    "Wrd": "0",
                                                    "_": "\r\n          ",
                                                    "script": {
                                                        "type": "text/javascript"
                                                    },
                                                    "style": {
                                                        "resolved": "true"
                                                    }
                                                }
                                            ]
                                        },
                                        {
                                            "PagClsIdt": "16233214",
                                            "ParIdt": "16233213",
                                            "VlgNum": "0",
                                            "Opt": "1",
                                            "RepTyp": "2",
                                            "DefVlgNum": "1",
                                            "Nam": "Verwijzing",
                                            "_": "\r\n        "
                                        }
                                    ]
                                },
                                {
                                    "PagClsIdt": "16090128",
                                    "ParIdt": "16090104",
                                    "VlgNum": "35",
                                    "Opt": "0",
                                    "RepTyp": "1",
                                    "DefVlgNum": "31",
                                    "Nam": "Eind groepering",
                                    "_": "\r\n      ",
                                    "veld": {
                                        "PagVldIdt": "21622013",
                                        "VlgNum": "0",
                                        "GgvTyp": "1",
                                        "Nam": "Horizontale separator",
                                        "Wrd": "0",
                                        "_": "\r\n        ",
                                        "script": {
                                            "type": "text/javascript"
                                        },
                                        "style": {
                                            "resolved": "true"
                                        }
                                    }
                                },
                                {
                                    "PagClsIdt": "16090111",
                                    "ParIdt": "16090104",
                                    "VlgNum": "38",
                                    "Opt": "0",
                                    "RepTyp": "1",
                                    "DefVlgNum": "0",
                                    "Nam": "Lijst",
                                    "_": "\r\n      ",
                                    "cluster": [
                                        {
                                            "PagClsIdt": "16090114",
                                            "ParIdt": "16090111",
                                            "VlgNum": "0",
                                            "Opt": "0",
                                            "RepTyp": "1",
                                            "DefVlgNum": "0",
                                            "Nam": "Omschrijving",
                                            "_": "\r\n        ",
                                            "veld": [
                                                {
                                                    "PagVldIdt": "21621976",
                                                    "VlgNum": "0",
                                                    "GgvTyp": "2",
                                                    "Nam": "Titel",
                                                    "Wrd": "Meer informatie",
                                                    "_": "\r\n          ",
                                                    "script": {
                                                        "type": "text/javascript"
                                                    },
                                                    "style": {
                                                        "resolved": "true"
                                                    }
                                                },
                                                {
                                                    "PagVldIdt": "21621972",
                                                    "VlgNum": "1",
                                                    "GgvTyp": "1",
                                                    "Nam": "Kleine kop",
                                                    "Wrd": "0",
                                                    "_": "\r\n          ",
                                                    "script": {
                                                        "type": "text/javascript"
                                                    },
                                                    "style": {
                                                        "resolved": "true"
                                                    }
                                                },
                                                {
                                                    "PagVldIdt": "21621973",
                                                    "VlgNum": "8",
                                                    "GgvTyp": "1",
                                                    "Nam": "Kolommen",
                                                    "Wrd": "0",
                                                    "_": "\r\n          ",
                                                    "script": {
                                                        "type": "text/javascript"
                                                    },
                                                    "style": {
                                                        "resolved": "true"
                                                    }
                                                },
                                                {
                                                    "PagVldIdt": "21621974",
                                                    "VlgNum": "10",
                                                    "GgvTyp": "1",
                                                    "Nam": "Vaste hoogte",
                                                    "Wrd": "0",
                                                    "_": "\r\n          ",
                                                    "script": {
                                                        "type": "text/javascript"
                                                    },
                                                    "style": {
                                                        "resolved": "true"
                                                    }
                                                },
                                                {
                                                    "PagVldIdt": "21621975",
                                                    "VlgNum": "11",
                                                    "GgvTyp": "1",
                                                    "Nam": "Geen ezelsoor",
                                                    "Wrd": "0",
                                                    "_": "\r\n          ",
                                                    "script": {
                                                        "type": "text/javascript"
                                                    },
                                                    "style": {
                                                        "resolved": "true"
                                                    }
                                                },
                                                {
                                                    "PagVldIdt": "21791063",
                                                    "SelItmIdt": "7059",
                                                    "VlgNum": "12",
                                                    "GgvTyp": "3",
                                                    "Nam": "App categorie",
                                                    "SelWrd": "Meer info",
                                                    "SelAka": "more-info",
                                                    "_": "\r\n          ",
                                                    "item": {
                                                        "SelItmIdt": "7059",
                                                        "Wrd": "Meer info",
                                                        "Aka": "more-info",
                                                        "_": "\r\n            "
                                                    },
                                                    "script": {
                                                        "type": "text/javascript"
                                                    },
                                                    "style": {
                                                        "resolved": "true"
                                                    }
                                                }
                                            ]
                                        },
                                        {
                                            "PagClsIdt": "16090112",
                                            "ParIdt": "16090111",
                                            "VlgNum": "0",
                                            "Opt": "1",
                                            "RepTyp": "2",
                                            "DefVlgNum": "1",
                                            "Nam": "Verwijzing",
                                            "_": "\r\n        ",
                                            "cluster": {
                                                "PagClsIdt": "16090113",
                                                "ParIdt": "16090112",
                                                "VlgNum": "0",
                                                "Opt": "0",
                                                "RepTyp": "1",
                                                "DefVlgNum": "1",
                                                "Nam": "Intern",
                                                "_": "\r\n          ",
                                                "veld": [
                                                    {
                                                        "PagVldIdt": "21621971",
                                                        "VlgNum": "0",
                                                        "GgvTyp": "13",
                                                        "Nam": "Link",
                                                        "Wrd": "Kademuren: maatregelen en vernieuwing",
                                                        "_": "\r\n            ",
                                                        "link": {
                                                            "NarItmIdt": "1090797",
                                                            "SitItmIdt": "11417139",
                                                            "pagetype": "subhome",
                                                            "resolved": "true",
                                                            "Url": "https://www.amsterdam.nl/projecten/kademuren/"
                                                        },
                                                        "script": {
                                                            "type": "text/javascript"
                                                        },
                                                        "style": {
                                                            "resolved": "true"
                                                        }
                                                    },
                                                    {
                                                        "PagVldIdt": "21621970",
                                                        "SelItmIdt": "2173",
                                                        "VlgNum": "1",
                                                        "GgvTyp": "3",
                                                        "Nam": "Openen in",
                                                        "SelWrd": "Huidig venster",
                                                        "SelAka": "self",
                                                        "_": "\r\n            ",
                                                        "item": {
                                                            "SelItmIdt": "2173",
                                                            "Wrd": "Huidig venster",
                                                            "Aka": "self",
                                                            "_": "\r\n              "
                                                        },
                                                        "script": {
                                                            "type": "text/javascript"
                                                        },
                                                        "style": {
                                                            "resolved": "true"
                                                        }
                                                    }
                                                ]
                                            }
                                        }
                                    ]
                                },
                                {
                                    "PagClsIdt": "16090131",
                                    "ParIdt": "16090104",
                                    "VlgNum": "40",
                                    "Opt": "0",
                                    "RepTyp": "1",
                                    "DefVlgNum": "30",
                                    "Nam": "Start groepering",
                                    "_": "\r\n      ",
                                    "veld": [
                                        {
                                            "PagVldIdt": "21622028",
                                            "SelItmIdt": "6675",
                                            "VlgNum": "1",
                                            "GgvTyp": "3",
                                            "Nam": "Achtergrondkleur",
                                            "SelWrd": "Rood",
                                            "SelAka": "red",
                                            "_": "\r\n        ",
                                            "item": {
                                                "SelItmIdt": "6675",
                                                "Wrd": "Rood",
                                                "Aka": "red",
                                                "_": "\r\n          "
                                            },
                                            "script": {
                                                "type": "text/javascript"
                                            },
                                            "style": {
                                                "resolved": "true"
                                            }
                                        },
                                        {
                                            "PagVldIdt": "21622027",
                                            "VlgNum": "2",
                                            "GgvTyp": "1",
                                            "Nam": "Paginabreed",
                                            "Wrd": "1",
                                            "_": "\r\n        ",
                                            "script": {
                                                "type": "text/javascript"
                                            },
                                            "style": {
                                                "resolved": "true"
                                            }
                                        }
                                    ]
                                },
                                {
                                    "PagClsIdt": "16090108",
                                    "ParIdt": "16090104",
                                    "VlgNum": "43",
                                    "Opt": "0",
                                    "RepTyp": "1",
                                    "DefVlgNum": "0",
                                    "Nam": "Lijst",
                                    "_": "\r\n      ",
                                    "cluster": [
                                        {
                                            "PagClsIdt": "16090110",
                                            "ParIdt": "16090108",
                                            "VlgNum": "0",
                                            "Opt": "0",
                                            "RepTyp": "1",
                                            "DefVlgNum": "0",
                                            "Nam": "Omschrijving",
                                            "_": "\r\n        ",
                                            "veld": [
                                                {
                                                    "PagVldIdt": "21621968",
                                                    "VlgNum": "0",
                                                    "GgvTyp": "2",
                                                    "Nam": "Titel",
                                                    "Wrd": "Contact",
                                                    "_": "\r\n          ",
                                                    "script": {
                                                        "type": "text/javascript"
                                                    },
                                                    "style": {
                                                        "resolved": "true"
                                                    }
                                                },
                                                {
                                                    "PagVldIdt": "21621964",
                                                    "VlgNum": "1",
                                                    "GgvTyp": "1",
                                                    "Nam": "Kleine kop",
                                                    "Wrd": "0",
                                                    "_": "\r\n          ",
                                                    "script": {
                                                        "type": "text/javascript"
                                                    },
                                                    "style": {
                                                        "resolved": "true"
                                                    }
                                                },
                                                {
                                                    "PagVldIdt": "21621969",
                                                    "VlgNum": "2",
                                                    "GgvTyp": "5",
                                                    "Nam": "Tekst",
                                                    "_": "\r\n          ",
                                                    "Txt": "\r\n              <div>\r\n                <ul>\r\n                  <li>\r\n                    <p>Ester Seinen, omgevingsmanager<br /><a href=\"mailto:e.seijnen@amsterdam.nl\">e.seijnen@amsterdam.nl</a><br /><a href=\"tel:0657875986\" class=\"externLink\">06 5787 5986</a></p>\r\n                  </li>\r\n                </ul>\r\n              </div>\r\n            ",
                                                    "script": {
                                                        "type": "text/javascript"
                                                    },
                                                    "style": {
                                                        "resolved": "true"
                                                    }
                                                },
                                                {
                                                    "PagVldIdt": "21621965",
                                                    "VlgNum": "8",
                                                    "GgvTyp": "1",
                                                    "Nam": "Kolommen",
                                                    "Wrd": "0",
                                                    "_": "\r\n          ",
                                                    "script": {
                                                        "type": "text/javascript"
                                                    },
                                                    "style": {
                                                        "resolved": "true"
                                                    }
                                                },
                                                {
                                                    "PagVldIdt": "21621966",
                                                    "VlgNum": "10",
                                                    "GgvTyp": "1",
                                                    "Nam": "Vaste hoogte",
                                                    "Wrd": "0",
                                                    "_": "\r\n          ",
                                                    "script": {
                                                        "type": "text/javascript"
                                                    },
                                                    "style": {
                                                        "resolved": "true"
                                                    }
                                                },
                                                {
                                                    "PagVldIdt": "21621967",
                                                    "VlgNum": "11",
                                                    "GgvTyp": "1",
                                                    "Nam": "Geen ezelsoor",
                                                    "Wrd": "1",
                                                    "_": "\r\n          ",
                                                    "script": {
                                                        "type": "text/javascript"
                                                    },
                                                    "style": {
                                                        "resolved": "true"
                                                    }
                                                },
                                                {
                                                    "PagVldIdt": "21791062",
                                                    "SelItmIdt": "7057",
                                                    "VlgNum": "12",
                                                    "GgvTyp": "3",
                                                    "Nam": "App categorie",
                                                    "SelWrd": "Contact",
                                                    "SelAka": "contact",
                                                    "_": "\r\n          ",
                                                    "item": {
                                                        "SelItmIdt": "7057",
                                                        "Wrd": "Contact",
                                                        "Aka": "contact",
                                                        "_": "\r\n            "
                                                    },
                                                    "script": {
                                                        "type": "text/javascript"
                                                    },
                                                    "style": {
                                                        "resolved": "true"
                                                    }
                                                }
                                            ]
                                        },
                                        {
                                            "PagClsIdt": "16090109",
                                            "ParIdt": "16090108",
                                            "VlgNum": "0",
                                            "Opt": "1",
                                            "RepTyp": "2",
                                            "DefVlgNum": "1",
                                            "Nam": "Verwijzing",
                                            "_": "\r\n        "
                                        }
                                    ]
                                },
                                {
                                    "PagClsIdt": "16090132",
                                    "ParIdt": "16090104",
                                    "VlgNum": "45",
                                    "Opt": "0",
                                    "RepTyp": "1",
                                    "DefVlgNum": "31",
                                    "Nam": "Eind groepering",
                                    "_": "\r\n      ",
                                    "veld": {
                                        "PagVldIdt": "21622029",
                                        "VlgNum": "0",
                                        "GgvTyp": "1",
                                        "Nam": "Horizontale separator",
                                        "Wrd": "0",
                                        "_": "\r\n        ",
                                        "script": {
                                            "type": "text/javascript"
                                        },
                                        "style": {
                                            "resolved": "true"
                                        }
                                    }
                                }
                            ]
                        },
                        {
                            "PagClsIdt": "16090138",
                            "VlgNum": "0",
                            "Opt": "0",
                            "RepTyp": "1",
                            "DefVlgNum": "3",
                            "Nam": "Diagram",
                            "_": "\r\n    ",
                            "veld": {
                                "PagVldIdt": "21622035",
                                "LayIdt": "14",
                                "VlgNum": "0",
                                "GgvTyp": "24",
                                "Nam": "Lay-out",
                                "_": "\r\n      ",
                                "layout": {
                                    "columns": "12",
                                    "block-columns": "1",
                                    "gutter": "0",
                                    "padding": "10",
                                    "grid-column-width": "80",
                                    "Nam": "4 koloms, 1x4 blokken + extra zones",
                                    "Aka": "4koloms14blokkenetrazones",
                                    "Toe": "4:4|1",
                                    "DimSiz": "960",
                                    "MinSiz": "80",
                                    "MaxSiz": "960",
                                    "_": "\r\n        ",
                                    "zone": [
                                        {
                                            "columns": "12",
                                            "Nam": "Subnavigatie",
                                            "Aka": "subnav",
                                            "VlgNum": "0",
                                            "Toe": "Voor superlinks",
                                            "DimSiz": "960",
                                            "_": "\r\n          ",
                                            "row": {
                                                "number": "1",
                                                "_": "\r\n            ",
                                                "element": {
                                                    "name": "Afbeelding",
                                                    "id": "16090135",
                                                    "columns": "12",
                                                    "DimSiz": "960"
                                                }
                                            }
                                        },
                                        {
                                            "columns": "12",
                                            "Nam": "kolom 1-4_2",
                                            "Aka": "kolom1-4_2",
                                            "type": "multizone",
                                            "VlgNum": "2",
                                            "DimSiz": "960",
                                            "_": "\r\n          ",
                                            "row": [
                                                {
                                                    "number": "1",
                                                    "_": "\r\n            ",
                                                    "element": {
                                                        "name": "Start groepering",
                                                        "id": "16090127",
                                                        "columns": "12",
                                                        "DimSiz": "960"
                                                    }
                                                },
                                                {
                                                    "number": "2",
                                                    "_": "\r\n            ",
                                                    "element": {
                                                        "name": "Lijst",
                                                        "id": "16090105",
                                                        "columns": "9",
                                                        "DimSiz": "720",
                                                        "suffix": "3"
                                                    }
                                                },
                                                {
                                                    "number": "3",
                                                    "_": "\r\n            ",
                                                    "element": {
                                                        "name": "Lijst",
                                                        "id": "16090116",
                                                        "columns": "9",
                                                        "DimSiz": "720",
                                                        "suffix": "3"
                                                    }
                                                },
                                                {
                                                    "number": "4",
                                                    "_": "\r\n            ",
                                                    "element": {
                                                        "name": "Lijst",
                                                        "id": "16233213",
                                                        "columns": "9",
                                                        "DimSiz": "720",
                                                        "suffix": "3"
                                                    }
                                                },
                                                {
                                                    "number": "5",
                                                    "_": "\r\n            ",
                                                    "element": {
                                                        "name": "Eind groepering",
                                                        "id": "16090128",
                                                        "columns": "12",
                                                        "DimSiz": "960"
                                                    }
                                                }
                                            ]
                                        },
                                        {
                                            "columns": "12",
                                            "Nam": "kolom 1-4_3",
                                            "Aka": "kolom1-4_3",
                                            "type": "multizone",
                                            "VlgNum": "3",
                                            "DimSiz": "960",
                                            "_": "\r\n          ",
                                            "row": {
                                                "number": "6",
                                                "_": "\r\n            ",
                                                "element": {
                                                    "name": "Lijst",
                                                    "id": "16090111",
                                                    "columns": "6",
                                                    "DimSiz": "480",
                                                    "suffix": "6"
                                                }
                                            }
                                        },
                                        {
                                            "columns": "12",
                                            "Nam": "kolom 1-4_4",
                                            "Aka": "kolom1-4_4",
                                            "type": "multizone",
                                            "VlgNum": "4",
                                            "DimSiz": "960",
                                            "_": "\r\n          ",
                                            "row": [
                                                {
                                                    "number": "7",
                                                    "_": "\r\n            ",
                                                    "element": {
                                                        "name": "Start groepering",
                                                        "id": "16090131",
                                                        "columns": "12",
                                                        "DimSiz": "960"
                                                    }
                                                },
                                                {
                                                    "number": "8",
                                                    "_": "\r\n            ",
                                                    "element": {
                                                        "name": "Lijst",
                                                        "id": "16090108",
                                                        "columns": "9",
                                                        "DimSiz": "720",
                                                        "suffix": "3"
                                                    }
                                                },
                                                {
                                                    "number": "9",
                                                    "_": "\r\n            ",
                                                    "element": {
                                                        "name": "Eind groepering",
                                                        "id": "16090132",
                                                        "columns": "12",
                                                        "DimSiz": "960"
                                                    }
                                                }
                                            ]
                                        },
                                        {
                                            "columns": "12",
                                            "Nam": "Doorkijk",
                                            "Aka": "slot",
                                            "VlgNum": "2",
                                            "Toe": "Voor gerelateerde inhoud",
                                            "DimSiz": "960"
                                        }
                                    ]
                                },
                                "script": {
                                    "type": "text/javascript"
                                },
                                "style": {
                                    "resolved": "true"
                                }
                            }
                        },
                        {
                            "PagClsIdt": "16090140",
                            "VlgNum": "0",
                            "Opt": "0",
                            "RepTyp": "2",
                            "DefVlgNum": "5",
                            "Nam": "Coordinaten",
                            "_": "\r\n    ",
                            "veld": {
                                "PagVldIdt": "21622037",
                                "VlgNum": "0",
                                "GgvTyp": "25",
                                "Nam": "Coordinaten",
                                "_": "\r\n      ",
                                "Txt": {
                                    "_": "\r\n        ",
                                    "geo": {
                                        "_": "\r\n          ",
                                        "json": [
                                            {
                                                "type": "EPSG:28992",
                                                "_": "{\"type\":\"FeatureCollection\",\"features\":[{\"type\":\"Feature\",\"properties\":null,\"geometry\":{\"type\":\"Point\",\"coordinates\":[120957.72860244672,487334.7077594542]}}]}"
                                            },
                                            {
                                                "type": "EPSG:4326",
                                                "_": "{\"type\":\"FeatureCollection\",\"features\":[{\"type\":\"Feature\",\"geometry\":{\"type\":\"Point\",\"coordinates\":[4.8873162716572942,52.372831707583551]},\"properties\":null}]}"
                                            }
                                        ],
                                        "gml": [
                                            {
                                                "type": "EPSG:28992",
                                                "_": "\r\n            ",
                                                "gml:featureMembers": {
                                                    "xsi:schemaLocation": "http://www.opengis.net/gml http://schemas.opengis.net/gml/3.1.1/profiles/gmlsfProfile/1.0.0/gmlsf.xsd",
                                                    "_": "\r\n              ",
                                                    "feature:null": {
                                                        "_": "\r\n                ",
                                                        "feature:geometry": {
                                                            "_": "\r\n                  ",
                                                            "feature:Point": {
                                                                "feature:pos": "120957.72860244672 487334.7077594542",
                                                                "_": "\r\n                    "
                                                            }
                                                        }
                                                    }
                                                }
                                            },
                                            {
                                                "type": "EPSG:4326",
                                                "_": "\r\n            ",
                                                "gml:featureMembers": {
                                                    "xsi:schemaLocation": "http://www.opengis.net/gml http://schemas.opengis.net/gml/3.1.1/profiles/gmlsfProfile/1.0.0/gmlsf.xsd",
                                                    "_": "\r\n              ",
                                                    "feature:null": {
                                                        "_": "\r\n                ",
                                                        "feature:geometry": {
                                                            "_": "\r\n                  ",
                                                            "feature:Point": {
                                                                "feature:pos": "4.88731627165729 52.3728317075836",
                                                                "_": "\r\n                    "
                                                            }
                                                        }
                                                    }
                                                }
                                            }
                                        ]
                                    }
                                },
                                "script": {
                                    "type": "text/javascript"
                                },
                                "style": {
                                    "resolved": "true"
                                }
                            }
                        }
                    ],
                    "prototype": {
                        "ProTypIdt": "51",
                        "Nam": "Meta",
                        "Aka": "meta"
                    }
                },
                "coords": {
                    "pregenerated": "static"
                },
                "data": {
                    "type": "subhome"
                },
                "spec": {
                    "pagetype": "subhome"
                }
            }
        }

        self.iprox_projects = [{
            "category": "Algemeen",
            "feedid": "https://www.amsterdam.nl/projecten/kademuren/maatregelen-vernieuwen/baarsjesweg-216-313/",
            "publication_date": "2020-06-27",
            "modification_date": "2021-08-31",
            "image_url": "https://www.amsterdam.nl/publish/varianten/368/logo_voor_social.png",
            "title": "Baarsjesweg 216 - 313: vernieuwen kademuur",
            "content": "<div><p>De kademuur ter hoogte van de Baarsjesweg 216 tot 313, tussen de Postjesweg en Surinamestraat, is in slechte staat. We nemen tijdelijke maatregelen.</p></div>",
            "source_url": "https://www.amsterdam.nl/projecten/kademuren/maatregelen-vernieuwen/baarsjesweg-216-313/",
            "related_articles": "",
            "author": "",
            "photo_author": "",
            "images": []
        }]

        self.iprox_stadsloketten = {
            "item": {
                "page": {
                    "pagetype": "subhome",
                    "cluster": [
                        {
                            "Nam": "Blok",
                            "cluster": [
                                {
                                    "Nam": "Superlink",
                                    "cluster": [
                                        {
                                            "Nam": "Verwijzing",
                                            "cluster": {
                                                "Nam": "Intern",
                                                "veld": [
                                                    {
                                                        "Nam": "Link",
                                                        "Wrd": "loketten",
                                                        "link": {
                                                            "Url": "https://sub-page/"
                                                        },
                                                    }
                                                ]
                                            }
                                        }
                                    ]
                                },
                                {
                                    "Nam": "Lijst",
                                    "cluster": [
                                        {
                                            "Nam": "Omschrijving",
                                            "veld": [
                                                {
                                                    "Nam": "Titel",
                                                    "Wrd": "contact",
                                                },
                                                {
                                                    "Nam": "Tekst",
                                                    "Txt": "text"
                                                }
                                            ]
                                        }
                                    ]
                                }
                            ]
                        }
                    ]
                }
            }
        }

        self.iprox_stadsloket = {
            "item": {
                "page": {
                    "pagetype": "subhome",
                    "cluster": [
                        {
                            "Nam": "Meta",
                            "cluster": {
                                "Nam": "Meta",
                                "cluster": [
                                    {
                                        "Nam": "Gegevens",
                                        "veld": [
                                            {
                                                "Nam": "Samenvatting",
                                                "Txt": "text"
                                            }
                                        ]
                                    }
                                ]
                            }
                        },
                        {
                            "Nam": "Blok",
                            "cluster": [
                                {
                                    "Nam": "Afbeelding",
                                    "cluster": [
                                        {
                                            "Nam": "Afbeelding",
                                            "veld": [
                                                {
                                                    "Nam": "Afbeelding",
                                                    "FilNam": "test_orig.jpg",
                                                    "Src": {
                                                        "_": "/1/2/3/test_orig.jpg"
                                                    },
                                                    "asset": [
                                                        {
                                                            "FilNam": "test.jpg",
                                                            "Src": {
                                                                "_": "/1/2/3/1px/text.jpg"
                                                            }
                                                        },
                                                        {
                                                            "FilNam": None,
                                                            "Src": {
                                                                "_": None
                                                            }
                                                        }
                                                    ]
                                                }
                                            ]
                                        }
                                    ]
                                },
                                {
                                    "Nam": "Leestekst",
                                    "veld": [
                                        {
                                            "Nam": "Titel",
                                            "Wrd": "Stadsloket Centrum",
                                        },
                                        {
                                            "Nam": "Tekst",
                                            "Txt": "text",
                                        }
                                    ]
                                },
                                {
                                    "Nam": "Lijst",
                                    "cluster": [
                                        {
                                            "Nam": "Omschrijving",
                                            "veld": [
                                                {
                                                    "Nam": "Titel",
                                                    "Wrd": "Openingstijden",
                                                },
                                                {
                                                    "Nam": "Tekst",
                                                    "Txt": "text",
                                                }
                                            ]
                                        }
                                    ]
                                },
                                {
                                    "Nam": "Lijst",
                                    "cluster": [
                                        {
                                            "Nam": "Omschrijving",
                                            "veld": [
                                                {
                                                    "Nam": "Tekst",
                                                    "Txt": "text",
                                                },
                                            ]
                                        }
                                    ]
                                },
                                {
                                    "Nam": "Lijst",
                                    "cluster": [
                                        {
                                            "Nam": "Omschrijving",
                                            "veld": [
                                                {
                                                    "Nam": "Titel",
                                                    "Wrd": "Mailen",
                                                },
                                                {
                                                    "Nam": "Tekst",
                                                    "Txt": "text",
                                                },
                                            ]
                                        }
                                    ]
                                }
                            ]
                        }
                    ]
                }
            }
        }

        self.project_manager = [
            {
                "email": "mock0@amsterdam.nl",
                "identifier": "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa",
                "projects": ["0000000000"]
            },
            {
                "email": "mock1@amsterdam.nl",
                "identifier": "bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb",
                "projects": ["0000000002", "0000000003"]
            }
        ]

        self.project_manager_invalid = {
            "email": "mock@invalid.domain",
            "identifier": "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa",
            "projects": ["0000000000", "0000000001"]
        }

        self.mobile_devices = [
            {
                "deviceid": "0",
                "firebasetoken": "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa",
                "os": "android"
            },
            {
                "deviceid": "1",
                "firebasetoken": "bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb",
                "os": "ios"
            }
        ]

        self.followed_projects = [
            {
                "deviceid": '0',
                "projectid": '0000000000'
            },
            {
                "deviceid": '0',
                "projectid": '0000000001'
            },
            {
                "deviceid": '1',
                "projectid": '0000000000'
            }
        ]

        self.warning_message = {
            'title': 'title',
            'body': 'Body text',
            'project_identifier': '0000000000',
            'project_manager_id': 'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa',
            'images': []
        }
