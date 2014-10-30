import django

def init():
    """
    Create default instances of groups.

    This function should be executed at startup to check and create the BDS group 
    """
    try:
        from django.contrib.auth.models import Group, Permission
        from django.contrib.contenttypes.models import ContentType

        BDS, created = Group.objects.get_or_create(name="BDS")

        if created:
            contents = ContentType.objects.filter(app_label__in=["bds", "profilENS"])
            permissions = Permission.objects.filter(content_type__in=contents)
            BDS.permissions.add(*permissions)
            BDS.save()
    except django.db.utils.OperationalError:
        # Fail silently if there is any issue. This piece of code is going to
        # be executed lot of times in any case.
        pass
