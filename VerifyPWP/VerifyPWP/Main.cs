using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Text;
using System.Windows.Forms;

namespace VerifyPWP
{
    public partial class Main : Form
    {

        public Main(DataInfo info)
        {
            InitializeComponent();


            var grid = new CanvasGrid();
            grid.Anchor = AnchorStyles.Top | AnchorStyles.Bottom | AnchorStyles.Left | AnchorStyles.Right;
            grid.Size = new Size(300, 300);
            grid.Location = new Point(0, 0);
            grid.Dock = DockStyle.Fill;

            if (info != null) {
                grid.H = info.H;
                grid.W = info.W;
                grid.Rectangles = info.Rectangles;
                grid.Title = String.Format("{0}X{1} with {2} rectangles", grid.W, grid.H, info.N);
                
            }

            this.Controls.Add(grid);
        }
    }
}
