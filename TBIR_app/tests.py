from django.test import TestCase
from TBIR_app.searcher import Searcher
# python manage.py test


class SearcherTests(TestCase):
    def test_caption_embedding(self):
        searcher = Searcher()
        self.assertEqual(searcher.initialize_caption_embedding(), [])
