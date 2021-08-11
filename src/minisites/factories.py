import factory

from search.factories import SearchPageFactory


class MinisiteFactory(SearchPageFactory):

    color_1 = '#cccccc'
    color_2 = '#cccccc'
    color_3 = '#cccccc'
    color_4 = '#cccccc'
    color_5 = '#cccccc'
    logo = factory.Faker('file_path')
    logo_link = factory.Faker('url')
