from math import ceil
from django.db.models import Q
from django.contrib.postgres.search import TrigramWordSimilarity
from amsterdam_app_api.api_messages import Messages
messages = Messages()


class TextSearch:
    def __init__(self, model, query, query_fields, return_fields=None, page_size=10, page=0):
        self.model = model
        self.query = query
        self.query_fields = query_fields.split(',')
        self.return_fields = None if return_fields is None else return_fields.split(',')
        self.threshold = 0.1
        self.page_size = page_size
        self.page = page
        self.pages = 0
        self.result = []

    def search(self):
        # Character Filter
        if len(self.query) < 3:
            return {'page': self.result, 'pages': self.pages}

        # Get appropriate model fields
        model_fields = [x.name for x in self.model._meta.get_fields() if x.name != 'data']

        # Build filter and query
        score = 0
        weight = 1.0
        condition = None
        for query_field in self.query_fields:
            score += weight * TrigramWordSimilarity(self.query, query_field)

            weight = weight / 2  # Next item has half the weight of the previous item
            q = Q(**{'{query_field}__unaccent__icontains'.format(query_field=query_field): self.query})
            if condition:
                condition = condition | q
            else:
                condition = q

        # Query and filter
        objects = self.model.objects.annotate(score=score).filter(score__gte=self.threshold).filter(condition).order_by('-score')
        sorted_objects = list(objects)

        # Create page (sorted_objects[start_index:stop_index]) and count pages
        page = sorted_objects[self.page * self.page_size:self.page * self.page_size + self.page_size]
        self.pages = int(ceil(len(sorted_objects) / float(self.page_size)))

        # Build field list for given model
        if self.return_fields is not None:
            model_fields = [x for x in model_fields if x in self.return_fields]

        # Filter field from search_results (functions as a serializer)
        for item in page:
            data = {}
            for model_field in model_fields:
                data[model_field] = getattr(item, model_field)
            self.result.append(data)

        # Return result
        return {'page': self.result, 'pages': self.pages}
