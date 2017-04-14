"""
This is the interface for interacting with the UW Libraries Subject Guide
Web Service.
"""

from uw_libraries.dao import SubjectGuide_DAO
from uw_libraries.models import (
    SubjectGuide, CourseGuide, Library, Librarian)
from restclients_core.exceptions import DataFailureException
try:
    from urllib import quote
except ImportError:
    from urllib.parse import quote
import json


subject_guide_url_prefix = '/currics_db/api/v1/data'


def get_subject_guide_for_section_params(
        year, quarter, curriculum_abbr, course_number, section_id=None):
    """
    Returns a SubjectGuide model for the passed section params:

    year: year for the section term (4-digits)
    quarter: quarter (AUT, WIN, SPR, or SUM)
    curriculum_abbr: curriculum abbreviation
    course_number: course number
    section_id: course section identifier (optional)
    """

    quarter = quarter.upper()[:3]

    url = '%s/%s/%s/%s/%s/%s/%s' % (
        subject_guide_url_prefix, 'course', year, quarter,
        quote(curriculum_abbr.upper()), course_number, section_id.upper())
    headers = {'Accept': 'application/json'}

    response = SubjectGuide_DAO().getURL(url, headers)

    if response.status != 200:
        raise DataFailureException(url, response.status, response.data)

    data = json.loads(response.data)
    return _subject_guide_from_json(data)


def get_subject_guide_for_section(section):
    """
    Returns a SubjectGuide model for the passed SWS section model.
    """
    return get_subject_guide_for_section_params(
        section.term.year, section.term.quarter, section.curriculum_abbr,
        section.course_number, section.section_id)


def get_subject_guide_for_canvas_course_sis_id(course_sis_id):
    """
    Returns a SubjectGuide model for the passed Canvas course SIS ID.
    """
    (year, quarter, curriculum_abbr, course_number,
        section_id) = course_sis_id.split('-', 4)
    return get_subject_guide_for_section_params(
        year, quarter, curriculum_abbr, course_number, section_id)


def get_default_subject_guide(campus='seattle'):
    """
    Returns a default SubjectGuide model for the passed campus:
        seattle, bothell, tacoma
    """
    url = '%s/%s/%s' % (subject_guide_url_prefix, 'defaultGuide', campus)
    headers = {'Accept': 'application/json'}

    response = SubjectGuide_DAO().getURL(url, headers)

    if response.status != 200:
        raise DataFailureException(url, response.status, response.data)

    data = json.loads(response.data)
    return _subject_guide_from_json(data)


def _subject_guide_from_json(data):
    subject_data = data['subjectGuide']
    subject_guide = SubjectGuide()
    subject_guide.contact_url = subject_data.get('askUsLink', None)
    subject_guide.contact_text = subject_data.get('askUsText', None)
    subject_guide.discipline = subject_data.get('discipline', None)
    subject_guide.find_librarian_url = subject_data.get(
        'findLibrarianLink', None)
    subject_guide.find_librarian_text = subject_data.get(
        'findLibrarianText', None)
    subject_guide.guide_url = subject_data.get('guideLink', None)
    subject_guide.guide_text = subject_data.get('guideText', None)
    subject_guide.faq_url = subject_data.get('howDoILink', None)
    subject_guide.faq_text = subject_data.get('howDoIText', None)
    subject_guide.writing_guide_url = subject_data.get(
        'writingGuideLink', None)
    subject_guide.writing_guide_text = subject_data.get(
        'writingGuideText', None)

    default_guide_campus = subject_data.get('defaultGuideForCampus', None)
    if default_guide_campus is not None:
        subject_guide.is_default_guide = True
        subject_guide.default_guide_campus = default_guide_campus
    else:
        subject_guide.is_default_guide = False

    subject_guide.libraries = []
    subject_guide.librarians = []

    for libdata in subject_data.get('libraries', []):
        library = Library()
        library.name = libdata.get('name', None)
        library.description = libdata.get('description', None)
        library.url = libdata.get('url', None)
        subject_guide.libraries.append(library)

    for libdata in subject_data.get('librarians', []):
        librarian = Librarian()
        librarian.name = libdata.get('name', None)
        librarian.email = libdata.get('email', None)
        librarian.phone = libdata.get('telephone', None)
        librarian.url = libdata.get('url', None)
        subject_guide.librarians.append(librarian)

    if 'courseGuide' in data:
        course_data = data['courseGuide']
        subject_guide.course_guide = CourseGuide()
        subject_guide.course_guide.guide_url = course_data.get(
            'guideLink', None)
        subject_guide.course_guide.guide_text = course_data.get(
            'guideText', None)

    return subject_guide
