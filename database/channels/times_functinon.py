def to_delete(db_data: list, entity_data: list):
    to_del = set(db_data) - set(entity_data)
    return to_del


def to_insert(db_data: list, entity_data: list):
    to_ins = set(entity_data) - set(db_data)
    return to_ins


