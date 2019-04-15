import unittest
import rest_server as rs

class TestRestServer(unittest.TestCase):
    def test_allowed_fname_txt(self):
        ip = "dev.txt"
        op = str(rs.allowed_file(ip))
        eop = str(True)
        self.assertEqual(op, eop, "Should be" + eop)

    def test_allowed_fname_pdf(self):
        ip = "dev.pdf"
        op = str(rs.allowed_file(ip))
        eop = str(True)
        self.assertEqual(op, eop, "Should be" + eop)

    def test_allowed_fname_png(self):
        ip = "dev.png"
        op = str(rs.allowed_file(ip))
        eop = str(True)
        self.assertEqual(op, eop, "Should be" + eop)

    def test_allowed_fname_jpg(self):
        ip = "dev.jpg"
        op = str(rs.allowed_file(ip))
        eop = str(True)
        self.assertEqual(op, eop, "Should be" + eop)

    def test_allowed_fname_jpeg(self):
        ip = "dev.jpeg"
        op = str(rs.allowed_file(ip))
        eop = str(True)
        self.assertEqual(op, eop, "Should be" + eop)

    def test_allowed_fname_txt(self):
        ip = "dev.txt"
        op = str(rs.allowed_file(ip))
        eop = str(True)
        self.assertEqual(op, eop, "Should be" + eop)

    def test_is_txt(self):
        ip = "dev.txt"
        op = str(rs.is_textfile(ip))
        eop = str(True)
        self.assertEqual(op, eop, "Should be" + eop)

    def test_is_pdf(self):
        ip = "dev.pdf"
        op = str(rs.is_pdffile(ip))
        eop = str(True)
        self.assertEqual(op, eop, "Should be" + eop)

    def test_is_img(self):
        ip = "dev.png"
        op = str(rs.is_imagefile(ip))
        eop = str(True)
        self.assertEqual(op, eop, "Should be" + eop)


    def test_txt_to_txt(self):
        ip = "unit_test_trial.txt"
        op = str(rs.text_to_text(ip))
        eop = "This is a command line entry point. It means that if you execute the script alone by running python test.py at the command line, it will call unittest.main(). This executes the test runner by discovering all classes in this file that inherit from unittest.TestCase."
        self.assertEqual(op, eop, "Should be" + eop)