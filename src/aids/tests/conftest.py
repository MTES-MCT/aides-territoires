import pytest


@pytest.fixture
def aid_form_data(user, backer, perimeter):
    """Returns valid data to create an Aid object."""

    return {
        'name': 'Test aid',
        'author': user.id,
        'financers': [backer.id],
        'description': 'My aid description',
        'eligibility': 'Aid eligibility info',
        'perimeter': perimeter.id,
        'recurrence': 'oneoff',
        'mobilization_steps': ['preop'],
        'targeted_audiances': ['department'],
        'aid_types': ['grant', 'loan'],
        'destinations': ['supply'],
        'start_date': '01/01/2019',
        'publication_status': 'open',
        'status': 'published',
    }
