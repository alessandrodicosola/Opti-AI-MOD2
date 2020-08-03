using Microsoft.VisualStudio.TestTools.UnitTesting;
using VerifyPWP;
using System;
using System.Collections.Generic;
using System.Text;
using System.Drawing;
using System.IO;

namespace VerifyPWP.Tests
{
    [TestClass()]
    public class CPParserTests
    {
        [TestMethod()]
        public void GetInfoTest()
        {
            string input = @"9 12
            5
            3 3 0 9
            2 4 7 0";

            var parser = new CPParser();
            var result = parser.GetInfo(new StringReader(input));


            Assert.IsTrue(result.W == 9);
            Assert.IsTrue(result.H == 12);
            Assert.IsTrue(result.N == 5);
            Assert.IsTrue(result.Rectangles.Count == 2);
            Assert.IsTrue(result.Rectangles.Contains(new Rectangle(0, 9, 3, 3)));
            Assert.IsTrue(result.Rectangles.Contains(new Rectangle(7, 0, 2, 4)));
            
        }
    }
}