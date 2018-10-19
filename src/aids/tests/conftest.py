import pytest


@pytest.fixture
def aid_form_data(user, backer, perimeter):
    """Returns valid data to create an Aid object."""

    return {
        'name': 'Test aid',
        'author': user.id,
        'backers': [backer.id],
        'description': 'My aid description',
        'eligibility': 'Aid eligibility info',
        'perimeter': perimeter.id,
        'mobilization_steps': ['preop'],
        'targeted_audiances': ['department'],
        'aid_types': ['grant', 'loan'],
        'destinations': ['supply'],
        'publication_status': 'open',
        'status': 'published',
    }
