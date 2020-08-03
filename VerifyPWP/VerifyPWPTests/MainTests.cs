using Microsoft.VisualStudio.TestTools.UnitTesting;
using VerifyPWP;
using System;
using System.Collections.Generic;
using System.Text;

namespace VerifyPWP.Tests
{
    [TestClass()]
    public class MainTests
    {
        [TestMethod()]
        public void MainTest()
        {
            string input = @"9 12
            5
            3 3 0 9
            2 4 7 0";

            var parser = new CPParser();
            
            var result = parser.GetInfo(new System.IO.StringReader(input));
            Assert.IsNotNull(result);

            var main = new Main(result);

           

            main.ShowDialog();

        }
    }
}