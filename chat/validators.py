from rest_framework import serializers


def min_list_length(length: int):
    def wrapper_function(value):
        if len(value) < length:
            raise serializers.ValidationError(
                "This field must have at least %d item." % length
            )

    return wrapper_function
