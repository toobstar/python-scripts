import unittest
from cypher_basic import encrypt


class TestEncryptFunction(unittest.TestCase):

  def test_simple(self):
    self.assertEqual("xyz", "xyz")

  def test_encrypt_basic(self):
    self.assertEqual(encrypt(3, "abc"), "\`~")
    self.assertEqual(encrypt(5, "Hello"), "C~ggj")
    self.assertEqual(encrypt(10, "123"), "RST")

  def test_encrypt_with_special_characters(self):
    self.assertEqual(encrypt(2, "a!b@c"), "`.~!a")
    self.assertEqual(encrypt(4, "Hello, World!"), "Dahhk86Sknh~9")

  def test_encrypt_with_reverse(self):
    self.assertEqual(encrypt(3, "\`~", reverse=True), "abc")
    self.assertEqual(encrypt(5, "C~ggj", reverse=True), "Hello")
    self.assertEqual(encrypt(10, "RST", reverse=True), "123")

  def test_failing_encrypt_with_reverse(self):
    self.assertNotEqual(encrypt(4, "\`~", reverse=True), "abc")
    self.assertNotEqual(encrypt(6, "C~ggj", reverse=True), "Hello")
    self.assertNotEqual(encrypt(15, "RST", reverse=True), "123")

if __name__ == "__main__":
  unittest.main()