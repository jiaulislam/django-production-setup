SPECTACULAR_SETTINGS = {
    "OAS_VERSION": "3.1.0",
    "TITLE": r"Django Production RestAPI",
    "DESCRIPTION": "Demonstration of a production grade RestAPI",
    "VERSION": "",
    "SERVE_INCLUDE_SCHEMA": False,
    "SCHEMA_PATH_PREFIX": r"/api/v[0-9]",
    "SERVE_AUTHENTICATION": None,
    "SWAGGER_UI_SETTINGS": {
        "swagger": "2.0",
        "deepLinking": True,
        "filter": True,
        "persistAuthorization": True,
        "displayOperationId": True,
    },
    "POSTPROCESSING_HOOKS": [
        "drf_spectacular.hooks.postprocess_schema_enums",
    ],
    "COMPONENT_SPLIT_REQUEST": True,
}
