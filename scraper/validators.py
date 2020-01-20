from django.core.validators import URLValidator


class CustomURLValidator(URLValidator):
    """
    Accept url without required schema.
    """

    def __call__(self, value):
        if '://' not in value:
            value = 'https://' + value
        super(CustomURLValidator, self).__call__(value)


def validate_url_address(url):
    """
    The method validate URL.
    """
    validate = URLValidator()
    validate(url)
