# pylint: disable=too-many-arguments, line-too-long
""" Free-text search within TEXT or CHAR fields of any given model. At least three characters are required for this
    class to start searching. Each next query field counts for half the weight in the result score. Only results
    where the search query is found as-is (adjacent) are returned. The results are returned in descending score as
    a paginated result.

    For this class to function your database is required to support the extension 'pg_trgm' (TrigramWordSimilarity)
    and 'unaccent' (search agnostic for accents e.g. ü or u are equivalent)

    model: model object class
    query: string
    query_fields: comma separated string of model fields
    return_fields: comma separated string of model fields
    page_size: maximum number items in paginated result
    page: the result page
"""

from django.contrib.postgres.search import TrigramWordSimilarity
from django.db.models import Q

PAGE_SIZE = 10
MIN_QUERY_LENGTH = 3


def get_non_related_fields(model):
    model_fields = []
    for field in model._meta.get_fields():
        if not (field.is_relation and (field.one_to_many, field.many_to_one or field.one_to_one or field.many_to_many)):
            model_fields.append(field.name)
    return model_fields


def search_text_in_model(model, query, query_fields, return_fields):
    """Search for text in database model"""

    query_fields_list = query_fields.split(",")
    return_fields_list = None
    if return_fields is not None:
        return_fields_list = return_fields.split(",")

    threshold = 0.0  # only scores above this threshold are considered

    # Only start the search with at least three characters
    if len(query) < MIN_QUERY_LENGTH:
        return []

    # Dynamically get appropriate model fields and build a filter for the requested return fields
    model_fields = get_non_related_fields(model)

    if return_fields_list is not None:
        model_fields = [x for x in model_fields if x in return_fields_list]
    model_fields += ["score"]

    # Build a 'TrigramWordSimilarity' and 'accents agnostic adjacent characters' filter
    score = 0
    weight = 1.0
    objects_with_scores = []
    for query_field in query_fields_list:
        # Set half the weight for each next search field
        score += weight * TrigramWordSimilarity(query, query_field)
        weight = weight / 2

        # Build accents agnostic filter for adjacent characters in TrigramWordSimilarity search results
        q = Q(**{"{query_field}__unaccent__icontains".format(query_field=query_field): query})

        # Query and filter
        objects = model.objects.annotate(score=score).filter(score__gte=threshold).filter(q).order_by("-score")
        objects_with_scores.extend(objects)

    # Sort objects by score
    sorted_objects = sorted(objects_with_scores, key=lambda x: x.score, reverse=True)

    # Create a unique set of objects (sorted)
    seen = set()
    sorted_objects_unique = [seen.add(x.pk) or x for x in sorted_objects if x.pk not in seen]

    return sorted_objects_unique
