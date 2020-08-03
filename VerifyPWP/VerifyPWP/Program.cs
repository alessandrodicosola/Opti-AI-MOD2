using System;
using System.Collections.Generic;
using System.Linq;
using System.Runtime.CompilerServices;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace VerifyPWP
{
    static class Program
    {
        /// <summary>
        ///  The main entry point for the application.
        /// </summary>
        [STAThread]
        static void Main()
        {
            Application.SetHighDpiMode(HighDpiMode.SystemAware);
            Application.EnableVisualStyles();
            Application.SetCompatibleTextRenderingDefault(false);

            var parsers = new Dictionary<String, Parser>() 
            {
                {"CP",new CPParser() }
            };

            var args = Environment.GetCommandLineArgs();
            DataInfo info = null;
            if (args.Length > 1)
            {
                var type = args[1].ToUpper();
                var output_cp_path = args[2];

                var parser = parsers[type];
                info = parser.GetInfo(new System.IO.StreamReader(output_cp_path));
            }
            else
            {
                MessageBox.Show("[ERROR] Expected: VerifyPWP.exe (CP|SAT|SMT) out_file_path");
                Environment.Exit(1);
            }

            Application.Run(new Main(info));
        }
    }
}
