from unittest import TestCase

from utils.hostname import get_next_letter, get_next_hostname, get_bare_hostname, format_case, format_hostname

test_config: dict = {
    'hostname_suffix': '-r',
    'enforce_case': 'lower',
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

class TestGetBareHostname(TestCase):
    def test_returns_bare_hostname(self):
        self.assertEqual(get_bare_hostname(test_config, 'hostname-r'), 'hostname')
        self.assertEqual(get_bare_hostname(test_config, 'HOSTNAME-R'), 'HOSTNAME')
        self.assertEqual(get_bare_hostname(test_config, 'hostname-R'), 'hostname')
        self.assertEqual(get_bare_hostname(test_config, 'HOSTNAME-r'), 'HOSTNAME')
        self.assertEqual(get_bare_hostname(test_config, 'host-r-name'), 'host-r-name')

class TestFormatCase(TestCase):
    test_config_no_case: dict = test_config | {
        'enforce_case': 'none'
    }

    test_config_enforce_upper: dict = test_config | {
        'enforce_case': 'upper'
    }

    def test_returns_lower(self):
        self.assertEqual(format_case(test_config, 'hostname'), 'hostname')
        self.assertEqual(format_case(test_config, 'HOSTNAME '), 'hostname')
        self.assertEqual(format_case(test_config, 'hOsTnAmE'), 'hostname')

    def test_returns_same(self):
        self.assertEqual(format_case(self.test_config_no_case, 'hostname'), 'hostname')
        self.assertEqual(format_case(self.test_config_no_case, 'HOSTNAME'), 'HOSTNAME')
        self.assertEqual(format_case(self.test_config_no_case, ' hOsTnAmE '), 'hOsTnAmE')

    def test_returns_upper(self):
        self.assertEqual(format_case(self.test_config_enforce_upper, 'hostname'), 'HOSTNAME')
        self.assertEqual(format_case(self.test_config_enforce_upper, 'HOSTNAME'), 'HOSTNAME')
        self.assertEqual(format_case(self.test_config_enforce_upper, ' hOsTnAmE'), 'HOSTNAME')

class TestFormatHostname(TestCase):
    test_config_no_case: dict = test_config | {
        'enforce_case': 'none'
    }

    test_config_enforce_upper: dict = test_config | {
        'enforce_case': 'upper'
    }

    test_config_no_suffix: dict = test_config | {
        'hostname_suffix': ''
    }

    test_config_different_suffix: dict = test_config | {
        'hostname_suffix': '-s'
    }

    def test_returns_lower_case(self):
        self.assertEqual(format_hostname(test_config, 'TestHostname-r'), 'testhostname-r')
        self.assertEqual(format_hostname(test_config, 'TESTHOSTNAME-R'), 'testhostname-r')
        self.assertEqual(format_hostname(test_config, 'TESTHOSTNAME'), 'testhostname-r')
    
    def test_returns_upper_case(self):
        self.assertEqual(format_hostname(self.test_config_enforce_upper, 'TestHostname-r'), 'TESTHOSTNAME-R')
        self.assertEqual(format_hostname(self.test_config_enforce_upper, 'TESTHOSTNAME-r'), 'TESTHOSTNAME-R')
        self.assertEqual(format_hostname(self.test_config_enforce_upper, 'testhostname'), 'TESTHOSTNAME-R')

    def test_returns_same_case(self):
        self.assertEqual(format_hostname(self.test_config_no_case, 'TestHostname-r'), 'TestHostname-r')
        self.assertEqual(format_hostname(self.test_config_no_case, 'TESTHOSTNAME-R'), 'TESTHOSTNAME-r')
        self.assertEqual(format_hostname(self.test_config_no_case, 'testhostname'), 'testhostname-r')
    
    def test_returns_same_suffix(self):
        self.assertEqual(format_hostname(self.test_config_no_suffix, 'TestHostname-s'), 'testhostname-s')
        self.assertEqual(format_hostname(self.test_config_no_suffix, 'TESTHOSTNAME-R'), 'testhostname-r')
        self.assertEqual(format_hostname(self.test_config_no_suffix, 'TESTHOSTNAME'), 'testhostname')

    def test_returns_different_suffix(self):
        self.assertEqual(format_hostname(self.test_config_different_suffix, 'TestHostname-s'), 'testhostname-s')
        self.assertEqual(format_hostname(self.test_config_different_suffix, 'TESTHOSTNAME-S'), 'testhostname-s')
        self.assertEqual(format_hostname(self.test_config_different_suffix, 'TESTHOSTNAME'), 'testhostname-s')