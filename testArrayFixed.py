import unittest
from arrayFixed import ArrayFixed

class testArrayFixed(unittest.TestCase):

    def testInit(self):
        ary=ArrayFixed()
        self.assertEqual(ary(), [])

    def testInitValues(self):
        ary1=ArrayFixed()
        self.assertEqual(ary1(), [])
        ary=ArrayFixed(maxElements=3,defaultValue=7)
        self.assertEqual(len(ary()), 3)
        self.assertEqual(ary(), [7,7,7])
        for e in ary():
            self.assertEqual(e,7)
    

    def testAdd(self):
        ary=ArrayFixed(maxElements=3)
        ary.add(5)
        ary.add(2)
        self.assertEqual(ary(),[5,2])
        ary.add(7)
        ary.add(9)
        self.assertEqual(ary(),[2,7,9])

    def testArrayTypeAccess(self):
        ary=ArrayFixed()
        ary.add(3)
        ary.add(7)
        ary.add(9)
        ary.add(1)
        self.assertEqual(ary[1],7)   
        self.assertEqual(ary[2],9)   
        self.assertEqual(ary[-1],1)  
        self.assertEqual(ary[-2],9)   
        
    def testMax(self):
        ary=ArrayFixed()
        ary.add(3)
        ary.add(7)
        ary.add(9)
        ary.add(1)
        self.assertEqual(ary.max(),9)

    def testMaxLambda(self):
        ary=ArrayFixed()
        ary.add((2,3))
        ary.add((4,7))
        ary.add((6,9))
        ary.add((8,1))
        self.assertEqual(ary.max(lambda a: a[1]),(6,9))

    
    def testMin(self):
        ary=ArrayFixed()
        ary.add(3)
        ary.add(7)
        ary.add(9)
        ary.add(10)
        self.assertEqual(ary.min(),3)

    def testMinLambda(self):
        ary=ArrayFixed()
        ary.add((2,30))
        ary.add((4,7))
        ary.add((6,9))
        ary.add((8,11))
        self.assertEqual(ary.min(lambda a: a[1]),(4,7))

    def testSum(self):
        ary=ArrayFixed()
        ary.add(3)
        ary.add(7)
        ary.add(9)
        ary.add(10)
        self.assertEqual(ary.sum(),29)

    def testSumLambda(self):
        ary=ArrayFixed()
        ary.add((2,30))
        ary.add((4,7))
        ary.add((6,9))
        ary.add((8,11))
        self.assertEqual(ary.sum(lambda a: a[1]),57)    

    def testMean(self):
        ary=ArrayFixed()
        ary.add(3)
        ary.add(7)
        ary.add(9)
        ary.add(10)
        self.assertEqual(ary.mean(),29/4)

    def testMeanLambda(self):
        ary=ArrayFixed()
        ary.add((2,30))
        ary.add((4,7))
        ary.add((6,9))
        ary.add((8,11))
        self.assertEqual(ary.mean(lambda a: a[1]),57/4)    

if __name__ == '__main__':
    unittest.main()