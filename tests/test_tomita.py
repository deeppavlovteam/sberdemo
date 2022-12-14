import json
import unittest

import os

# from tomita import Tomita
from tomita.tomita import Tomita
from tomita.name_parser import NameParser


class TomitaTestCase(unittest.TestCase):
    def test_tomita(self):
        wd = os.path.realpath(os.path.join('tomita', 'test'))
        tomita = Tomita(os.environ['TOMITA_PATH'], os.path.join(wd, 'config.proto'), cwd=wd)

        r = tomita.communicate('ул. Маяковского, c, пятница, 22 апреля 2014 года').decode('UTF8')
        self.assertTrue(r.startswith('<document'), r)
        self.assertTrue(r.strip().endswith('</document>'), r)

        r = tomita.get_json('ул. Маяковского, c, пятница, 22 апреля 2014 года')
        # print(json.dumps(r, indent=2, ensure_ascii=False))
        d = r['facts']['Date']
        self.assertEqual(d['DayOfWeek']['@val'], 'ПЯТНИЦА')
        self.assertEqual(d['Day']['@val'], '22')
        self.assertEqual(d['Month']['@val'], 'АПРЕЛЬ')

        r = tomita.get_json('Юрий Гагарин')
        # print(json.dumps(r, indent=2, ensure_ascii=False))
        self.assertEqual(r, [], 'expected empty array')

        print('end')

    def test_name_parser(self):
        parser = NameParser()

        r = parser.parse('Николаев Сергей Петрович')
        self.assertEqual(1, len(r))
        self.assertEqual(r[0]['formal'], 'Сергей Петрович')

        self.assertEqual(parser.parse('Владлен увидел картину и ужаснулся')[0]['formal'], 'Владлен')


if __name__ == '__main__':
    unittest.main()
