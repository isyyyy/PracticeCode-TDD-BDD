"""
AccountFactory class using FactoryBoy

Documentation on Faker Providers:
    https://faker.readthedocs.io/en/master/providers/baseprovider.html

Documentation on Fuzzy Attributes:
    https://factoryboy.readthedocs.io/en/stable/fuzzy.html

"""
import factory
from datetime import date, datetime
from factory.fuzzy import FuzzyChoice, FuzzyDate
from models.account import Account


class AccountFactory(factory.Factory):
    """ Creates fake Accounts """

    class Meta:
        model = Account

    # Add attributes here...
    id = factory.Sequence(lambda n: n)
    name = factory.Faker("name")
    email = factory.Faker("email")
    phone_number = factory.Faker("phone_number")
    disabled = FuzzyChoice([True, False])
    # date_joined = factory.LazyFunction(datetime.utcnow)
    date_joined = FuzzyDate(date(2020, 1, 1), date(2021, 1, 1))