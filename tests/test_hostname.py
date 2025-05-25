from unittest import TestCase

from utils.hostname import get_next_hostname
from utils.hostname import get_next_letter

test_config: dict = {
    'hostname_suffix': '-r',
    'hosts_in_series': 4
}

non_series_test_config: dict = {
        'hostname_suffix': '-r',
        'hosts_in_series': 0
}

test_hostnames: list[str] = [
    'hostname123',
    'hostname123a',
    'hostname123b',
    'hostname123-r',
    'hostname123a-r',
    'hostname123b-r',
    'hostname123d',
    'hostname123d-r',
    'hostname0099',
    'hostname0099-r'
]

expected_next_hostnames: list[str] = [
    'hostname124-r',
    'hostname123b-r',
    'hostname123c-r',
    'hostname124-r',
    'hostname123b-r',
    'hostname123c-r',
    'hostname124a-r',
    'hostname124a-r',
    'hostname0100-r',
    'hostname0100-r'
]

class TestGetNextLetter(TestCase):
    def test_series_returns_correct_next_letter(self):
        current_hostname: str = 'hostname123d'
        expected_next_letter: str ='a'
        actual_next_letter: str = get_next_letter(test_config, current_hostname)
        self.assertEqual(expected_next_letter, actual_next_letter)
    def test_non_series_returns_correct_next_letter(self):
        current_hostname: str = 'hostname123d'
        expected_next_letter: str ='e'
        actual_next_letter: str = get_next_letter(non_series_test_config, current_hostname)
        self.assertEqual(expected_next_letter, actual_next_letter)

class TestGetNextHostname(TestCase):
    def test_returns_string(self):
        for test_hostname in test_hostnames:
            next_hostname: str = get_next_hostname(test_config, test_hostname)
            self.assertIsInstance(next_hostname, str)
    
    def test_returns_correct_next_hostname(self):
        for index, test_hostname in enumerate(test_hostnames):
            next_hostname: str = get_next_hostname(test_config, test_hostname)
            expected_next_hostname: str = expected_next_hostnames[index]
            self.assertEqual(next_hostname, expected_next_hostname)

    def test_does_not_wrap_around(self):
        test_hostname: str = 'hostname123d-r'
        expected_hostname: str = 'hostname123e-r'
        test_wrap_around_config: dict = {'hosts_in_series' : 0, 'hostname_suffix': '-r'}
        actual_hostname: str = get_next_hostname(test_wrap_around_config, test_hostname)
        self.assertEqual(actual_hostname, expected_hostname)