# pylint: disable=cyclic-import
"""Model utils"""


def create_id_dict(model_type, _id):
    """Create a dict with id and object type"""
    from construction_work.models.article import Article
    from construction_work.models.warning_and_notification import WarningMessage

    type_name = None
    if model_type == Article:
        type_name = "article"
    elif model_type == WarningMessage:
        type_name = "warning"

    if type_name is None:
        return {"id": _id}

    return {"id": _id, "type": type_name}
