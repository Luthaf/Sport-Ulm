def get_model_fields(model):
    ''' Returns all the fields of a model'''
    fields = {}
    options = model._meta
    for field in sorted(list(options.concrete_fields) + \
                        list(options.many_to_many) + \
                        list(options.virtual_fields)):
        fields[field.name] = field
    return fields
