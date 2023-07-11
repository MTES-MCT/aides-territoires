import pytest
from aids.models import AidWorkflow


@pytest.fixture
def aid_form_data(user, backer, perimeter, category):
    """Returns valid data to create an Aid object."""

    return {
        "name": "Test aid",
        "slug": "",
        "author": user.id,
        "financers": [backer.id],
        "description": "My aid description",
        "project_examples": "",
        "eligibility": "Aid eligibility info",
        "contact": "Some contact data",
        "perimeter": perimeter.id,
        "recurrence": "oneoff",
        "origin_url": "https://ademe.fr",
        "mobilization_steps": ["preop_strategy"],
        "targeted_audiences": ["department"],
        "aid_types": ["grant", "loan"],
        "destinations": ["supply"],
        "start_date": "01/01/2019",
        "submission_deadline": "01/01/2042",
        "publication_status": "open",
        "is_call_for_project": True,
        "categories": [category.id],
        "status": AidWorkflow.states.published,
    }
