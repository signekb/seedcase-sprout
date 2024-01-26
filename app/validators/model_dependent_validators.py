"""This script contains validators that uses models for their validation. 
Because they are dependent on models in their validation, they cannot be 
included as validators in the models (circular definitions)."""

from app.models import TableMetadata


def does_table_name_exist_in_db(name):
    if TableMetadata.objects.filter(name=name).exists():
        return True
    else:
        return False
