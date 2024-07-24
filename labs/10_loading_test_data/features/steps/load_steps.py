# pylint: disable=function-redefined, missing-function-docstring
# flake8: noqa
"""
Pet Steps
Steps file for Pet.feature
For information on Waiting until elements are present in the HTML see:
    https://selenium-python.readthedocs.io/waits.html
"""
import requests
from behave import given

# Load data here


@given('the following pets')
def step_impl(context):
    """Load the database with new pets """
    for row in context.table:
        payload = {
            "name": row['name'],
            "category": row['category'],
            "available": row['available'] in ['True', 'true', '1']
        }

        context.resp = requests.post(
            f"{context.base_url}/pets",
            json=payload
        )
        assert context.resp.status_code is 201