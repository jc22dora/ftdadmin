import unittest, os
from unittest.mock import MagicMock, patch
import ftdadminmod
test_row = {'SETTLEMENT DATE': 20210204, 'CUSIP':'112E45', 'SYMBOL':'TSLA', 'QUANTITY (FAILS)':12, 'DESCRIPTION':'RHRH', 'PRICE':4.55}

class TestDict(unittest.TestCase):
    def test_process_dict(self):
        test_row1 = {'SETTLEMENT ATE': 20210204, 'CUSIP':'112E45', 'SYMBOL':'TSLA', 'QUANTITY (FAILS)':12, 'DESCRIPTION':'RHRH', 'PRICE':4.55}
        test_row2 = {'SETTLEMENT DATE': 20210204, 'USIP':'112E45', 'SYMBOL':'TSLA', 'QUANTITY (FAILS)':12, 'DESCRIPTION':'RHRH', 'PRICE':4.55}
        test_row3 = {'SETTLEMENT DATE': 20210204, 'CUSIP':'112E45', 'YMBOL':'TSLA', 'QUANTITY (FAILS)':12, 'DESCRIPTION':'RHRH', 'PRICE':4.55}
        test_row4 = {'SETTLEMENT DATE': 20210204, 'CUSIP':'112E45', 'SYMBOL':'TSLA', 'UANTITY (FAILS)':12, 'DESCRIPTION':'RHRH', 'PRICE':4.55}
        test_row5 = {'SETTLEMENT DATE': 20210204, 'CUSIP':'112E45', 'SYMBOL':'TSLA', 'QUANTITY (FAILS)':12, 'ESCRIPTION':'RHRH', 'PRICE':4.55}
        test_row6 = {'SETTLEMENT DATE': 20210204, 'CUSIP':'112E45', 'SYMBOL':'TSLA', 'QUANTITY (FAILS)':12, 'DESCRIPTION':'RHRH', 'RICE':4.55}

        with self.assertRaises(KeyError):
            ftdadminmod.process_dict(test_row1)
            ftdadminmod.process_dict(test_row2)
            ftdadminmod.process_dict(test_row3)
            ftdadminmod.process_dict(test_row4)
            ftdadminmod.process_dict(test_row5)
            ftdadminmod.process_dict(test_row6)



class TestPrice(unittest.TestCase):
    def test_process_price(self):
        test_row1 = {'SETTLEMENT DATE': 20210204, 'CUSIP':'112E45', 'SYMBOL':'TSLA', 'QUANTITY (FAILS)':12, 'DESCRIPTION':'RHRH', 'PRICE\r\n':44.55}
        test_row2 = {'SETTLEMENT DATE': 20210204, 'CUSIP':'112E45', 'SYMBOL':'TSLA', 'QUANTITY (FAILS)':12, 'DESCRIPTION':'RHRH', 'PRICE\n':44.55}
        test_row3 = {'SETTLEMENT DATE': 20210204, 'CUSIP':'112E45', 'SYMBOL':'TSLA', 'QUANTITY (FAILS)':12, 'DESCRIPTION':'RHRH', 'PRICE':44.55}
        test_row4 = {'SETTLEMENT DATE': 20210204, 'CUSIP':'112E45', 'SYMBOL':'TSLA', 'QUANTITY (FAILS)':12, 'DESCRIPTION':'RHRH', 'PRICE':4.55}
        test_row5 = {'SETTLEMENT DATE': 20210204, 'CUSIP':'112E45', 'SYMBOL':'TSLA', 'QUANTITY (FAILS)':12, 'DESCRIPTION':'RHRH', 'raise':4.55}
        self.assertEqual(ftdadminmod.process_price(test_row1),44.55)
        self.assertEqual(ftdadminmod.process_price(test_row2),44.55)
        self.assertEqual(ftdadminmod.process_price(test_row3),44.55)
        self.assertNotEqual(ftdadminmod.process_price(test_row4),44.55)
        with self.assertRaises(KeyError):
            ftdadminmod.process_price(test_row5)


class TestTypes(unittest.TestCase):
    def test_process_types(self):
        # happy path
        self.assertEqual(ftdadminmod.process_types(20210204,'112E45','TSLA',12,'RHRH',4.55),(20210204,'112E45','TSLA',12,'RHRH',4.55))
        # settlementdate: test case - string, float, str+float, None
        self.assertEqual(ftdadminmod.process_types('20210204','112E45','TSLA',12,'RHRH',4.55),(20210204,'112E45','TSLA',12,'RHRH',4.55))
        self.assertEqual(ftdadminmod.process_types(20210204.0,'112E45','TSLA',12,'RHRH',4.55),(20210204,'112E45','TSLA',12,'RHRH',4.55))
        with self.assertRaises(ValueError):
            ftdadminmod.process_types('20210204.0','112E45','TSLA',12,'RHRH',4.55)
        with self.assertRaises(TypeError):
            ftdadminmod.process_types(None,'112E45','TSLA',12,'RHRH',4.55)
        # cusip: test case - float, None, list
        # TODO self.assertEqual(ftd.process_types(20210204,112E45,'TSLA',12,'RHRH',4.55),(20210204,'112E45','TSLA',12,'RHRH',4.55))
        # TODO with self.assertRaises(TypeError):
        #    ftd.process_types(20210204,None,'TSLA',12,'RHRH',4.55)
        # TODO with self.assertRaises(ValueError):
        #    ftd.process_types(20210204,['112E45'],'TSLA',12,'RHRH',4.55)

        # symbol:
        # TODO same issue with cusip

        # quantity: test case: string, float, str+float, None
        self.assertEqual(ftdadminmod.process_types(20210204,'112E45','TSLA','12','RHRH',4.55),(20210204,'112E45','TSLA',12,'RHRH',4.55))
        self.assertEqual(ftdadminmod.process_types(20210204,'112E45','TSLA',12.0,'RHRH',4.55),(20210204,'112E45','TSLA',12,'RHRH',4.55))
        with self.assertRaises(ValueError):
            ftdadminmod.process_types(20210204,'112E45','TSLA','12.0','RHRH',4.55),(20210204,'112E45','TSLA',12,'RHRH',4.55)
        with self.assertRaises(TypeError):
            ftdadminmod.process_types(20210204,'112E45','TSLA',None,'RHRH',4.55),(20210204,'112E45','TSLA',12,'RHRH',4.55)
        # TODO description: test case - we only care that it is string
        settlementdate, cusip, symbol, quantity, description1, price = ftdadminmod.process_types(20210204,'112E45','TSLA',12,'RHRH',4.55)
        settlementdate, cusip, symbol, quantity, description2, price = ftdadminmod.process_types(20210204,'112E45','TSLA',12,None,4.55)
        settlementdate, cusip, symbol, quantity, description3, price = ftdadminmod.process_types(20210204,'112E45','TSLA',12,[],4.55)
        self.assertIsInstance(description1,str)
        self.assertIsInstance(description2,str)
        self.assertIsInstance(description3,str)

        # price: test case - int, str, None
        settlementdate, cusip, symbol, quantity, description, price1 = ftdadminmod.process_types(20210204,'112E45','TSLA',12,'RHRH',4)
        settlementdate, cusip, symbol, quantity, description, price2 = ftdadminmod.process_types(20210204,'112E45','TSLA',12,'RHRH','4.55')
        self.assertIsInstance(price1,float)
        self.assertIsInstance(price2,float)
        with self.assertRaises(TypeError):
            ftdadminmod.process_types(20210204,'112E45','TSLA',12,'RHRH',None)

class TestProcess(unittest.TestCase):
    #@patch('ftd.insert_row')
    def test_process(self):
        mock = MagicMock()
        ftdadminmod.process(mock, test_row)
        

if __name__ == '__main__':
    unittest.main()