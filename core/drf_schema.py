from drf_spectacular.openapi import AutoSchema as SpectacularAutoSchema


class AutoSchema(SpectacularAutoSchema):
    def get_operation_id(self) -> str:
        """Get an operation ID that includes the version number.

        This prevents conflicts on auto-generated operation IDs.
        """
        operation_id = super().get_operation_id()
        version, _ = self.view.determine_version(self.view.request, **self.view.kwargs)
        return f'{version}_{operation_id}'
