from unittest import TestCase

from utils.ip import get_next_ip, is_valid_ip

class TestIsValidIp(TestCase):
    def test_returns_false_for_invalid_ip(self):
        self.assertFalse(is_valid_ip('not_valid_ip123'))
        self.assertFalse(is_valid_ip('256.256.0.0'))
    
    def test_returns_true_for_valid_ip(self):
        self.assertTrue(is_valid_ip('192.168.1.1'))
        self.assertTrue(is_valid_ip('100.100.100.100'))

class TestGetNextIp(TestCase):
    def test_returns_false_if_ip_invalid(self):
        self.assertFalse(get_next_ip('not_valid_ip123'))
        self.assertFalse(get_next_ip('256.256.0.0'))
    
    def test_returns_correct_next_ip(self):
        self.assertEqual(get_next_ip('192.168.1.1'), '192.168.1.2')
        self.assertEqual(get_next_ip('192.168.1.255'), '192.168.2.0')
        self.assertEqual(get_next_ip('10.0.1.1'), '10.0.1.2')