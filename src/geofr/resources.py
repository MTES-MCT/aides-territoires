from import_export import resources

from geofr.models import Perimeter


class PerimeterResource(resources.ModelResource):
    class Meta:
        model = Perimeter
        import_id_fields = "id"
        fields = ("code", "name", "scale", "population", "date_created", "is_obsolete")

    def dehydrate_scale(self, obj):
        return obj.get_scale_display()
