using System;
using System.Collections.Generic;
using System.Drawing;
using System.Linq;
using System.Security.Cryptography.X509Certificates;
using System.Text;
using System.Windows.Forms;

namespace VerifyPWP
{
    public class CanvasGrid : PictureBox
    {
        public CanvasGrid() { }

        private Size internalSize;

        private int sep_i;
        private int sep_j;

        private int _w = 1;
        public int W { get => _w; set { _w = value; sep_i = (int)Math.Floor((float)internalSize.Width / _w); ; Invalidate(); } }

        private int _h = 1;
        public int H { get => _h; set { _h = value; sep_j = (int)Math.Floor((float)internalSize.Height / _h); Invalidate(); } }

        private int _padding = 30;
        public List<Rectangle> Rectangles { get; set; } = new List<Rectangle>();
        public string Title { get => _title; set { _title = value; Invalidate(new Rectangle(0, 0, Width, _padding + 1)); } }

        private string _title = "";
        protected override void OnResize(EventArgs e)
        {
            base.OnResize(e);
            internalSize = new Size(Width - _padding * 2, Height - _padding * 2);
            sep_i = internalSize.Width / W;
            sep_j = internalSize.Height / H;
            Invalidate();
        }
        protected override void OnSizeChanged(EventArgs e)
        {
            base.OnSizeChanged(e);
            internalSize = new Size(Width - _padding * 2, Height - _padding * 2);
            sep_i = internalSize.Width / W;
            sep_j = internalSize.Height / H;
            Invalidate();
        }

        protected override void OnPaint(PaintEventArgs e)
        {

            // + 1 for allowing the drawing of borders line

            using (var bitmap = new Bitmap(internalSize.Width + 1, internalSize.Height + 1))
            using (var g = Graphics.FromImage(bitmap))
            {
                // Background
                g.FillRectangle(Brushes.White, new Rectangle(0, 0, W * sep_i, H * sep_j));

                // Draw the grid
                //// Draw vertical lines 
                ///
                using (var p = new Pen(Color.FromArgb(100, Color.Black)))
                {
                    for (int i = 0; i <= W; i++)
                    {
                        g.DrawLine(p, i * sep_i, 0, i * sep_i, sep_j * H);
                    }
                    //// Draw horizontal lines
                    for (int j = 0; j <= H; j++)
                    {
                        g.DrawLine(p, 0, j * sep_j, sep_i * W - 1, j * sep_j);
                    }
                }

                //Rectangles
                if (Rectangles.Count > 0)
                {
                    foreach (var rect in Rectangles)
                    {
                        var r = new Rectangle(rect.X * sep_i, rect.Y * sep_j, rect.Width * sep_i, rect.Height * sep_j);
                        
                        var bottomleft_rect = new Rectangle(r.X, r.Y, sep_i, sep_j);
                        var s = Math.Min(sep_i / 4, sep_j / 4);
                        var rect_center = new Rectangle(bottomleft_rect.X + sep_i / 2 - s / 2, bottomleft_rect.Y + sep_j / 2 - s / 2, s, s);

                        using (var b = new SolidBrush(Color.FromArgb(100, getRandomColor())))
                        using (var b_p = new SolidBrush(ControlPaint.Dark(b.Color)))
                        using (var p = new Pen(ControlPaint.Dark(b.Color), 1))
                        {
                            g.FillRectangle(b, r);
                            g.DrawRectangle(p, r);
                            g.FillPie(b_p, rect_center, 0, 360);
                        }


                    }
                }



                bitmap.RotateFlip(RotateFlipType.RotateNoneFlipY);

                e.Graphics.DrawImage(bitmap, _padding, _padding);

            }

            // Number of x and y axies
            for (int i = 0; i < W; i++)
            {
                var s_f = e.Graphics.MeasureString(i.ToString(), DefaultFont);
                //e.Graphics.DrawString(i.ToString(), DefaultFont, Brushes.Black, new PointF(i * sep_i + sep_i / 2 + _padding + this.Left, Height - _padding / 2));
                e.Graphics.DrawString(i.ToString(), DefaultFont, Brushes.Black, new PointF(i * sep_i + sep_i / 2 + _padding + Left - s_f.Width / 2, Height - _padding / 2 - s_f.Height/2));

            }
            for (int j = 0; j < H; j++)
            {
                var s_f = e.Graphics.MeasureString(j.ToString(), DefaultFont);
                e.Graphics.DrawString(j.ToString(), DefaultFont, Brushes.Black, new PointF(_padding/2 - s_f.Width/2, Math.Abs(sep_j * j - Height) - sep_j / 2 - _padding - s_f.Height /2));
            }

            var h_f = e.Graphics.MeasureString(Title, DefaultFont).Height;
            e.Graphics.DrawString(Title, DefaultFont, Brushes.Black, _padding, _padding - h_f);
        }
        private static Random _random = new Random(System.Environment.TickCount);

        private Color getRandomColor() => Color.FromArgb(100, _random.Next(255), _random.Next(255), _random.Next(255));
    }
}
