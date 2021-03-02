import unittest
from template import template

class TestTemplate(unittest.TestCase):

    def setUp(self):
        pass

    def test_substitute_code_and_altcode(self):
        self.assertEqual( template('Code is %CODE%; alt code is %ALTCODE%', '5678901234'), 'Code is 5678901234; alt code is 56789-012')

    def test_validate_req_id(self):
        self.assertEqual(template('Code is %CODE%; alt code is %ALTCODE%', '1234'), None, 'req_id should be has len of 10')

    def test_validate_code(self):
        self.assertEqual(template('Code is %COD%; alt code is %ALTCODE%', '1234567891'), None, '%CODE% must appear in source_template')

    def test_validate_altcode(self):
        self.assertEqual(template('Code is %CODE%; alt code is %ACODE%', '1234567891'), None, '%ALTCODE% must appear in source_template')



if __name__ == '__main__':
    unittest.main()
