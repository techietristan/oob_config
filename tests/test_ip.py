from unittest import TestCase

from utils.ip import is_valid_ip, is_valid_subnet_mask, get_gateway_validator, get_next_ip, get_subnet_mask, get_default_gateway

class TestIsValidIp(TestCase):
    def test_returns_false_for_invalid_ip(self):
        self.assertFalse(is_valid_ip('not_valid_ip123'))
        self.assertFalse(is_valid_ip('256.256.0.0'))
        self.assertFalse(is_valid_ip('0.2'))
    
    def test_returns_true_for_valid_ip(self):
        self.assertTrue(is_valid_ip('192.168.1.1'))
        self.assertTrue(is_valid_ip('100.100.100.100'))
        self.assertTrue(is_valid_ip('255.255.255.128'))
        self.assertTrue(is_valid_ip('255.255.255.192'))

class TestIsValidSubnetMask(TestCase):
    def test_returns_false_for_invalid_input(self):
        self.assertFalse(is_valid_subnet_mask('192.168.1.1'))
        self.assertFalse(is_valid_subnet_mask('0.0.0.225'))
        self.assertFalse(is_valid_subnet_mask('0.2'))
        self.assertFalse(is_valid_subnet_mask('0'))
        self.assertFalse(is_valid_subnet_mask('33'))
        self.assertFalse(is_valid_subnet_mask('this is a string'))
    
    def test_returns_true_for_valid_input(self):
        self.assertTrue(is_valid_subnet_mask('255.0.0.0'))
        self.assertTrue(is_valid_subnet_mask('255.255.255.0'))
        self.assertTrue(is_valid_subnet_mask('255.128.0.0'))
        self.assertTrue(is_valid_subnet_mask('255.255.192.0'))
        self.assertTrue(is_valid_subnet_mask(' 255.255.255.240'))
        self.assertTrue(is_valid_subnet_mask('255.255.255.248 '))
        self.assertTrue(is_valid_subnet_mask(' 255.255.255.252 '))
        self.assertTrue(is_valid_subnet_mask('/2'))
        self.assertTrue(is_valid_subnet_mask('/24'))
        self.assertTrue(is_valid_subnet_mask('/24'))
        self.assertTrue(is_valid_subnet_mask('2'))
        self.assertTrue(is_valid_subnet_mask('24'))
        self.assertTrue(is_valid_subnet_mask('32'))
        self.assertTrue(is_valid_subnet_mask(' 2 '))
        self.assertTrue(is_valid_subnet_mask(' 24 '))

class TestGetGatewayValidator(TestCase):
    def test_gateway_validator_returns_false_for_invalid_input(self):
        self.assertFalse(get_gateway_validator('192.168.0.130', '27')('192.168.0.10'))
        self.assertFalse(get_gateway_validator('192.168.0.130', '27')('192.168.0.128'))
        self.assertFalse(get_gateway_validator('192.168.0.130', '27')('192.168.0.159'))
        self.assertFalse(get_gateway_validator('192.168.0.130', '27')('192.168.0.255'))
        self.assertFalse(get_gateway_validator('192.168.0.130', '27')('192.168.0.130'))

    def test_gateway_validator_returns_true_for_valid_input(self):
        self.assertTrue(get_gateway_validator('192.168.0.130', '27')('192.168.0.129'))
        self.assertTrue(get_gateway_validator('192.168.0.130', '27')('192.168.0.158'))

class TestGetNextIp(TestCase):
    def test_returns_false_if_ip_invalid(self):
        self.assertFalse(get_next_ip('not_valid_ip123'))
        self.assertFalse(get_next_ip('256.256.0.0'))
    
    def test_returns_correct_next_ip(self):
        self.assertEqual(get_next_ip('192.168.1.1'), '192.168.1.2')
        self.assertEqual(get_next_ip('192.168.1.255'), '192.168.2.0')
        self.assertEqual(get_next_ip('10.0.1.1'), '10.0.1.2')

class TestGetSubnetMask(TestCase):
    def test_returns_false_if_invalid_subnet_format(self):
        self.assertFalse(get_subnet_mask({}, '192.168.1.1'))
        self.assertFalse(get_subnet_mask({}, '0.0.0.225'))
        self.assertFalse(get_subnet_mask({}, '0.2'))
        self.assertFalse(get_subnet_mask({}, '0'))
        self.assertFalse(get_subnet_mask({}, '33'))
        self.assertFalse(get_subnet_mask({}, 'this is a string'))
    
    def test_returns_correct_subnet_if_valid_subnet_format(self):
        self.assertEqual(get_subnet_mask({}, '24'), '255.255.255.0')
        self.assertEqual(get_subnet_mask({}, '/24'), '255.255.255.0')
        self.assertEqual(get_subnet_mask({}, '/27'), '255.255.255.224')
        self.assertEqual(get_subnet_mask({}, ' /28 '), '255.255.255.240')
        self.assertEqual(get_subnet_mask({}, '30 '), '255.255.255.252')
        self.assertEqual(get_subnet_mask({}, '/24'), '255.255.255.0')
        self.assertEqual(get_subnet_mask({}, ' 255.255.255.0'), '255.255.255.0')
        self.assertEqual(get_subnet_mask({}, ' 255.255.255.0'), '255.255.255.0')
        self.assertEqual(get_subnet_mask({}, '255.255.255.0 '), '255.255.255.0')
        self.assertEqual(get_subnet_mask({}, '255.255.255.252'), '255.255.255.252')

class TestGetDefaultGateway(TestCase):
    def test_returns_correct_default_gateway(self):
        self.assertEqual(get_default_gateway('192.168.1.100', '255.255.255.0'), '192.168.1.1')
        self.assertEqual(get_default_gateway('10.0.0.10', '255.0.0.0'), '10.0.0.1')
        self.assertEqual(get_default_gateway('192.168.0.130', '255.255.255.224'), '192.168.0.129')