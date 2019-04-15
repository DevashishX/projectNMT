import unittest
import driver 

class TestDriver(unittest.TestCase):
    def test_driver_post_apos(self):
        ip = "&apos; "
        op = driver.post_process(ip)
        eop = "'"
        self.assertEqual(op, eop, "Should be" + eop)

    def test_driver_post_atat(self):
        ip = "@@"
        op = driver.post_process(ip)
        eop = ""
        self.assertEqual(op, eop, "Should be" + eop)
    
    def test_driver_post_n(self):
        ip = "\n"
        op = driver.post_process(ip)
        eop = " "
        self.assertEqual(op, eop, "Should be" + eop)

    def test_driver_post_atdat(self):
        ip = "@-@"
        op = driver.post_process(ip)
        eop = ""
        self.assertEqual(op, eop, "Should be" + eop)

    def test_driver_trans_nos(self):
        ip = "123456879"
        op = driver.trans_process(ip)
        eop = "         "
        self.assertEqual(op, eop, "Should be" + eop)

    def test_driver_trans_nos_dash(self):
        ip = "12345687--9"
        op = driver.trans_process(ip)
        eop = "           "
        self.assertEqual(op, eop, "Should be" + eop)


    def test_driver_trans_nos(self):
        ip = "123456879"
        op = driver.trans_process(ip)
        eop = "         "
        self.assertEqual(op, eop, "Should be" + eop)

if __name__ == '__main__':
    unittest.main()
