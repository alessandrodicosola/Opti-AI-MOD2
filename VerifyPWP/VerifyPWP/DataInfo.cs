using System;
using System.Collections.Generic;
using System.Drawing;
using System.Text;

namespace VerifyPWP
{
    public class DataInfo
    {
        public DataInfo(int W, int H, int N, List<Rectangle> rectangles)
        {
            this.W = W;
            this.H = H;
            this.N = N;
            Rectangles = rectangles;
        }

        public int W { get; }
        public int H { get; }
        public int N { get; }
        public List<Rectangle> Rectangles { get; }
    }

}
