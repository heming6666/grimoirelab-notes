# -*- coding: utf-8 -*-
#
# Copyright (C) 2015-2019 Bitergia
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
# Authors:
#     Alvaro del Castillo <acs@bitergia.com>
#     Valerio Cosentino <valcos@bitergia.com>
#
import logging
import unittest

from base import TestBaseBackend
from grimoire_elk.enriched.utils import REPO_LABELS
from grimoire_elk.enriched.confluence import NO_ANCESTOR_TITLE


class TestConfluence(TestBaseBackend):
    """Test Confluence backend"""

    connector = "confluence"
    ocean_index = "test_" + connector
    enrich_index = "test_" + connector + "_enrich"

    def test_has_identites(self):
        """Test value of has_identities method"""

        enrich_backend = self.connectors[self.connector][2]()
        self.assertTrue(enrich_backend.has_identities())

    def test_items_to_raw(self):
        """Test whether JSON items are properly inserted into ES"""

        result = self._test_items_to_raw()

        self.assertEqual(result['items'], 4)
        self.assertEqual(result['raw'], 4)

        # Check enriched data
        enrich_backend = self.connectors[self.connector][2]()

        item = self.items[0]
        eitem = enrich_backend.get_rich_item(item)
        self.assertListEqual(eitem['ancestors_titles'],
                             ['Title 1', 'Title 2', 'Title 3'])
        self.assertListEqual(eitem['ancestors_links'],
                             ['/spaces/TEST/title1', '/spaces/TEST/title2', '/spaces/TEST/title3'])

        item = self.items[1]
        eitem = enrich_backend.get_rich_item(item)
        self.assertListEqual(eitem['ancestors_titles'], [NO_ANCESTOR_TITLE])
        self.assertListEqual(eitem['ancestors_links'], ['/spaces/TEST/title1'])

        item = self.items[2]
        eitem = enrich_backend.get_rich_item(item)
        self.assertListEqual(eitem['ancestors_titles'], ['Title 3'])
        self.assertListEqual(eitem['ancestors_links'], ['/spaces/TEST/title3'])

        item = self.items[3]
        eitem = enrich_backend.get_rich_item(item)
        self.assertListEqual(eitem['ancestors_titles'],
                             ['Title 1', 'Title 2', 'Title 3'])
        self.assertListEqual(eitem['ancestors_links'],
                             ['/spaces/TEST/title1', '/spaces/TEST/title2', '/spaces/TEST/title3'])

    def test_raw_to_enrich(self):
        """Test whether the raw index is properly enriched"""

        result = self._test_raw_to_enrich()
        self.assertEqual(result['raw'], 4)
        self.assertEqual(result['enrich'], 4)

    def test_enrich_repo_labels(self):
        """Test whether the field REPO_LABELS is present in the enriched items"""

        self._test_raw_to_enrich()
        enrich_backend = self.connectors[self.connector][2]()

        for item in self.items:
            eitem = enrich_backend.get_rich_item(item)
            self.assertIn(REPO_LABELS, eitem)

    def test_raw_to_enrich_sorting_hat(self):
        """Test enrich with SortingHat"""

        result = self._test_raw_to_enrich(sortinghat=True)
        self.assertEqual(result['raw'], 4)
        self.assertEqual(result['enrich'], 4)

    def test_raw_to_enrich_projects(self):
        """Test enrich with Projects"""

        result = self._test_raw_to_enrich(projects=True)
        self.assertEqual(result['raw'], 4)
        self.assertEqual(result['enrich'], 4)

    def test_refresh_identities(self):
        """Test refresh identities"""

        result = self._test_refresh_identities()
        # ... ?

    def test_refresh_project(self):
        """Test refresh project field for all sources"""

        result = self._test_refresh_project()
        # ... ?


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(message)s')
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    logging.getLogger("requests").setLevel(logging.WARNING)
    unittest.main(warnings='ignore')