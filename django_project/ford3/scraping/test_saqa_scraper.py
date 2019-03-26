import unittest
from saqa_scraper import (
    get_offset_from_page,
    get_form_data,
    scrape_qualifications_results_page,
    scrape_qualification_page
)

from saqa_scrape_mocks import (
    mock_return_first_page_qualifications_results,
    mock_return_page_qualification
)


class TestSaqaScraper(unittest.TestCase):

    def test_get_offset_from_page(self):
        page = 0
        offset = get_offset_from_page(page)
        self.assertEqual(offset, 0)
        values = get_form_data(offset)
        self.assertEqual(values['searchResultsATfirst'], 0)

        page = 1
        offset = get_offset_from_page(page)
        self.assertEqual(offset, 21)
        values = get_form_data(offset)
        self.assertEqual(values['searchResultsATfirst'], 21)

        page = 2
        offset = get_offset_from_page(page)
        self.assertEqual(offset, 41)
        values = get_form_data(offset)
        self.assertEqual(values['searchResultsATfirst'], 41)

    def test_scrape_qualification_results_page(self):
        html = mock_return_first_page_qualifications_results()
        qualifications = scrape_qualifications_results_page(html)

        # the mock results page returns 20 results
        # but only 15 are valid.
        self.assertEqual(len(qualifications), 15)

    def test_scrape_qualification_page(self):
        html = mock_return_page_qualification()

        result = scrape_qualification_page(html)
        self.assertEqual(result, {
            'saqa_id': '94576',
            'name': 'Advanced Certificate in Facilities Maintenance Management',
            'type': 'Advanced Certificate',
            'field_study': 'Business, Commerce and Management Studies',
            'subfield_study': 'Generic Management'
        })


if __name__ == '__main__':
    unittest.main()
