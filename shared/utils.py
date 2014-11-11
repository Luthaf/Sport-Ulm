def get_model_fields(model):
    ''' Returns all the fields of a model'''
    fields = {}
    options = model._meta
    for field in sorted(options.concrete_fields + \
                        options.many_to_many + \
                        options.virtual_fields):
        fields[field.name] = field
    return fields
