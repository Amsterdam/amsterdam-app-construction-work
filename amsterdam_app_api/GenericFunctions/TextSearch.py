from math import ceil
from django.contrib.postgres.search import TrigramSimilarity
from amsterdam_app_api.api_messages import Messages

messages = Messages()


class TextSearch:
    def __init__(self, model, query, query_fields, return_fields=None, page_size=10, page=0):
        self.model = model
        self.query = query
        self.query_fields = query_fields.split(',')
        self.return_fields = None if return_fields is None else return_fields.split(',')
        self.threshold = 0.03
        self.page_size = page_size
        self.page = page

    def search(self):
        # Get appropriate model and filter
        model_fields = [x.name for x in self.model._meta.get_fields() if x.name != 'data'] + ['similarity']

        # Build filter and query
        similarity = 0
        weight = 1.0
        for query_field in self.query_fields:
            similarity += weight * TrigramSimilarity(query_field, self.query)
            weight = weight / 2  # Next item has half the weight of the previous item

        # Query and filter
        objects = self.model.objects.annotate(similarity=similarity).filter(similarity__gte=self.threshold).order_by('-similarity')
        sorted_objects = list(objects)
        page = sorted_objects[self.page * self.page_size:self.page * self.page_size + self.page_size]
        pages = int(ceil(len(sorted_objects) / float(self.page_size)))

        # Build field list for given model
        if self.return_fields is not None:
            model_fields = [x for x in model_fields if x in self.return_fields]

        # Filter field from search_results
        result = list()
        for item in page:
            data = {}
            for model_field in model_fields:
                data[model_field] = getattr(item, model_field)
            result.append(data)

        # Return result
        return {'page': result, 'pages': pages}


if __name__ == '__main__':
    import os
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "amsterdam_app_backend.settings")
    import django
    django.setup()

    from amsterdam_app_api.models import ProjectDetails as Model
    ts = TextSearch(Model, 'bullebak', 'title,subtitle', return_fields='title,identifier', page_size=7, page=0)
    print(ts.search())
