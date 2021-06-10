import csv
import codecs
from io import StringIO

from django.core import files
from django.core.files.base import ContentFile
from django.utils import timezone, dateformat
from django.http import HttpResponse

from core.celery import app

from eligibility.models import EligibilityTest
from stats.models import AidEligibilityTestEvent
from exporting.models import DataExport


@app.task
def export_eligibility_tests_stats_as_csv(eligibility_tests_id_list, author_id, background=True):  # noqa
    """
    Method to write to csv and export all of the stats of an
    Eligibility Test.
    """
    eligibility_test = EligibilityTest.objects.get(id=eligibility_tests_id_list[0])  # noqa
    eligibility_test_questions = eligibility_test.eligibilitytestquestion_set \
        .select_related('question') \
        .all()
    eligibility_test_stats = AidEligibilityTestEvent.objects \
        .select_related('aid') \
        .filter(eligibility_test=eligibility_test)

    csv_buffer = StringIO()
    response = HttpResponse(content_type='text/csv')
    response.write(codecs.BOM_UTF8)
    csv_writer = csv.writer(csv_buffer if background else response, delimiter=',', dialect='excel')  # noqa

    # write header
    header = ['eligibility_test_name', 'aid_name']
    header_questions = []
    question_id_list = []
    for eligibility_question in eligibility_test_questions:
        question_id_list.append(eligibility_question.question_id)
        header_questions.append(eligibility_question.question)
    header_meta = ['answer_success', 'querystring', 'source', 'date_created']
    csv_writer.writerow(header + header_questions + header_meta)

    for eligibility_test_event in eligibility_test_stats:
        eligibility_test_event_row = [eligibility_test.name, eligibility_test_event.aid]  # noqa
        # we need to map the answers to the right questions
        eligibility_test_event_row_questions = []
        for question_id in question_id_list:
            answer = next((a for a in eligibility_test_event.answer_details if a['id'] == question_id), None)  # noqa
            answer_cleaned = answer['answer'] if answer else ''
            eligibility_test_event_row_questions.append(answer_cleaned)
        eligibility_test_event_row_meta = [getattr(eligibility_test_event, key) for key in header_meta]  # noqa
        csv_writer.writerow(eligibility_test_event_row + eligibility_test_event_row_questions + eligibility_test_event_row_meta)  # noqa

    file_name = 'export-test-eligibilite-{eligibility_test_id}-stats-{timestamp}'.format(  # noqa
        eligibility_test_id=eligibility_test.id,
        timestamp=dateformat.format(timezone.now(), 'Y-m-d_H-i-s'))

    if background:
        file_content = ContentFile(csv_buffer.getvalue().encode('utf-8'))
        file_object = files.File(file_content, name=f'{file_name}.csv')
        DataExport.objects.create(
            author_id=author_id,
            exported_file=file_object,
        )
        file_object.close()
        file_content.close()
    else:
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(file_name)  # noqa
        return response
