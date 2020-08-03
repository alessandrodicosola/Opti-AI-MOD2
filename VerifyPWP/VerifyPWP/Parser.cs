using System;
using System.Collections.Generic;
using System.Drawing;
using System.IO;
using System.Text;

namespace VerifyPWP
{
    interface Parser
    {
        public DataInfo GetInfo(TextReader reader);
    }
    
}
