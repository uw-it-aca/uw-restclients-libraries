from unittest import TestCase
from uw_libraries.subject_guides import (
    get_subject_guide_for_section_params, get_subject_guide_for_section,
    get_subject_guide_for_canvas_course_sis_id, get_default_subject_guide)
from uw_libraries.util import fdao_subject_guide_override
from restclients_core.exceptions import DataFailureException
from uw_sws.models import Section, Term
from datetime import date


@fdao_subject_guide_override
class SubjectGuideTest(TestCase):
    def test_subject_guide_with_bad_section_params(self):
        # Valid curriculum, with no file
        self.assertRaises(DataFailureException,
                          get_subject_guide_for_section_params,
                          year=2012, quarter='aut', curriculum_abbr='B ARTS',
                          course_number='197', section_id='A')

        # Missing params
        self.assertRaises(TypeError, get_subject_guide_for_section_params)

        # URL capitalization and quoting
        try:
            # Using a non-existant section so we can inspect the url
            guide = get_subject_guide_for_section_params(
                year=1990, quarter='aut', curriculum_abbr='A B&C',
                course_number='101', section_id='a')
        except DataFailureException as ex:
            self.assertEquals(
                ex.url,
                '/currics_db/api/v1/data/course/1990/AUT/A%20B%26C/101/A',
                'Quoted curriculum abbr')

    def test_subject_guide_for_section_params(self):
        guide = get_subject_guide_for_section_params(
            year=2015, quarter='aut', curriculum_abbr='MATH',
            course_number='309', section_id='A')

        self.assertEquals(guide.discipline, 'Mathematics')
        self.assertEquals(
            guide.contact_url, 'http://www.lib.washington.edu/about/contact')
        self.assertEquals(
            guide.find_librarian_url,
            'http://guides.lib.uw.edu/research/subject-librarians')
        self.assertEquals(
            guide.guide_url,
            'http://guides.lib.uw.edu/friendly.php?s=research/math')
        self.assertEquals(
            guide.faq_url, 'http://guides.lib.uw.edu/research/faq')
        self.assertEquals(guide.is_default_guide, False)
        self.assertEquals(len(guide.libraries), 1)
        self.assertEquals(
            guide.libraries[0].name, 'Mathematics Research Library')
        self.assertEquals(
            guide.libraries[0].url, 'http://www.lib.washington.edu/math')
        self.assertEquals(len(guide.librarians), 2)
        self.assertEquals(guide.librarians[0].email, 'javerage@uw.edu')
        self.assertEquals(guide.librarians[0].name, 'J Average')
        self.assertEquals(
            guide.librarians[0].url,
            'http://guides.lib.washington.edu/Javerage')
        self.assertEquals(guide.librarians[1].email, 'baverage@uw.edu')
        self.assertEquals(guide.librarians[1].name, 'B Average')
        self.assertEquals(
            guide.librarians[1].url,
            'http://guides.lib.washington.edu/Baverage')
        self.assertEquals(
            guide.course_guide.guide_url,
            'http://guides.lib.uw.edu/seattle/math307smith')
        self.assertEquals(
            guide.course_guide.guide_text,
            'MATH 307: Introduction To Differential Equations (Smith)')

    def test_subject_guide_for_section(self):
        term = Term(year=2015, quarter='autumn')
        section = Section(term=term, curriculum_abbr='MATH',
                          course_number='309', section_id='A')

        guide = get_subject_guide_for_section(section)

        self.assertEquals(guide.discipline, 'Mathematics')
        self.assertEquals(
            guide.contact_url, 'http://www.lib.washington.edu/about/contact')
        self.assertEquals(
            guide.find_librarian_url,
            'http://guides.lib.uw.edu/research/subject-librarians')
        self.assertEquals(
            guide.guide_url,
            'http://guides.lib.uw.edu/friendly.php?s=research/math')
        self.assertEquals(
            guide.faq_url, 'http://guides.lib.uw.edu/research/faq')
        self.assertEquals(guide.is_default_guide, False)
        self.assertEquals(len(guide.libraries), 1)
        self.assertEquals(
            guide.libraries[0].name, 'Mathematics Research Library')
        self.assertEquals(
            guide.libraries[0].url, 'http://www.lib.washington.edu/math')
        self.assertEquals(len(guide.librarians), 2)
        self.assertEquals(guide.librarians[0].email, 'javerage@uw.edu')
        self.assertEquals(guide.librarians[0].name, 'J Average')
        self.assertEquals(
            guide.librarians[0].url,
            'http://guides.lib.washington.edu/Javerage')
        self.assertEquals(guide.librarians[1].email, 'baverage@uw.edu')
        self.assertEquals(guide.librarians[1].name, 'B Average')
        self.assertEquals(
            guide.librarians[1].url,
            'http://guides.lib.washington.edu/Baverage')
        self.assertEquals(
            guide.course_guide.guide_url,
            'http://guides.lib.uw.edu/seattle/math307smith')
        self.assertEquals(
            guide.course_guide.guide_text,
            'MATH 307: Introduction To Differential Equations (Smith)')

    def test_subject_guide_for_canvas_course_sis_id(self):
        sis_id = '2015-autumn-MATH-309-A'
        guide = get_subject_guide_for_canvas_course_sis_id(sis_id)

        self.assertEquals(guide.discipline, 'Mathematics')
        self.assertEquals(
            guide.contact_url, 'http://www.lib.washington.edu/about/contact')
        self.assertEquals(
            guide.find_librarian_url,
            'http://guides.lib.uw.edu/research/subject-librarians')
        self.assertEquals(
            guide.guide_url,
            'http://guides.lib.uw.edu/friendly.php?s=research/math')
        self.assertEquals(guide.faq_url, 'http://guides.lib.uw.edu/research/faq')
        self.assertEquals(guide.is_default_guide, False)
        self.assertEquals(len(guide.libraries), 1)
        self.assertEquals(
            guide.libraries[0].name, 'Mathematics Research Library')
        self.assertEquals(
            guide.libraries[0].url, 'http://www.lib.washington.edu/math')
        self.assertEquals(len(guide.librarians), 2)
        self.assertEquals(guide.librarians[0].email, 'javerage@uw.edu')
        self.assertEquals(guide.librarians[0].name, 'J Average')
        self.assertEquals(
            guide.librarians[0].url,
            'http://guides.lib.washington.edu/Javerage')
        self.assertEquals(guide.librarians[1].email, 'baverage@uw.edu')
        self.assertEquals(guide.librarians[1].name, 'B Average')
        self.assertEquals(
            guide.librarians[1].url,
            'http://guides.lib.washington.edu/Baverage')
        self.assertEquals(
            guide.course_guide.guide_url,
            'http://guides.lib.uw.edu/seattle/math307smith')
        self.assertEquals(
            guide.course_guide.guide_text,
            'MATH 307: Introduction To Differential Equations (Smith)')

    def test_default_subject_guide(self):
        guide = get_default_subject_guide(campus='tacoma')

        self.assertEquals(guide.discipline, 'your discipline')
        self.assertEquals(
            guide.contact_url, 'http://www.tacoma.uw.edu/library/contact-us')
        self.assertEquals(
            guide.find_librarian_url,
            'http://www.tacoma.uw.edu/library/subject-librarians')
        self.assertEquals(guide.guide_url, 'http://guides.lib.uw.edu/tacoma')
        self.assertEquals(guide.faq_url, 'http://guides.lib.uw.edu/research')
        self.assertEquals(guide.is_default_guide, True)
        self.assertEquals(guide.default_guide_campus, 'tacoma')
        self.assertEquals(len(guide.libraries), 1)
        self.assertEquals(guide.libraries[0].name, 'UW Tacoma Library')
        self.assertEquals(
            guide.libraries[0].url, 'http://www.tacoma.uw.edu/library')
