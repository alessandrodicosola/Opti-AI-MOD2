using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Drawing;
using System.IO;
using System.Linq;
using System.Text;

namespace VerifyPWP
{
    public class CPParser : Parser
    {
        public DataInfo GetInfo(TextReader reader)
        {
            var wh = reader.ReadLine().Trim().Split().Select(x => int.Parse(x)).ToArray();
            var n = int.Parse(reader.ReadLine().Trim());
            var rects = new List<Rectangle>(n);
            String line = null;
            while ((line = reader.ReadLine()) != null)
            {
                var dim = line.Trim().Split().ToArray().Select(x => int.Parse(x)).ToArray();
                var rect = new Rectangle(dim[2], dim[3], dim[0], dim[1]);
                rects.Add(rect);
            }
            
            return new DataInfo(wh[0],wh[1],n,rects);
        }
    }
}
