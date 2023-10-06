import wx
import os
import pandas as pd
from try_us_frame import TryUsFrame

class frameMain(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title=u"TRAFFIC DATA NSW", pos=wx.DefaultPosition,
                          size=wx.Size(857, 598), style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)

        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)

        # Set the frame's background color to red
        self.SetBackgroundColour(wx.Colour(255, 0, 0))

        bSizerFrameMain = wx.BoxSizer(wx.VERTICAL)

        bSizerMainFrame = wx.BoxSizer(wx.VERTICAL)

        self.m_staticText2 = wx.StaticText(self, wx.ID_ANY, u"NSW Traffic Penalty Insights", wx.DefaultPosition,
                                          wx.DefaultSize, 0)
        self.m_staticText2.Wrap(-1)
        self.m_staticText2.SetFont(wx.Font(18, 72, 90, 92, False, "Baskerville Old Face"))

        bSizerMainFrame.Add(self.m_staticText2, 0, wx.ALIGN_CENTER | wx.ALIGN_TOP | wx.ALL, 5)

        self.m_staticText3 = wx.StaticText(self, wx.ID_ANY,
                                          u"Welcome to the ultimate source that will satisfy your traffic penalty analysis cravings! Dive into the data, expose trends, and explore the colorful world of NSW traffic offenses.",
                                          wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTER)
        self.m_staticText3.Wrap(400)  # Adjust the width as needed
        bSizerMainFrame.Add(self.m_staticText3, 0, wx.ALIGN_CENTER | wx.ALL, 8)

        # Create a horizontal sizer for images and labels
        image_sizer = wx.BoxSizer(wx.HORIZONTAL)

        # Directory path where your images are located
        image_dir = "images"

        # List of image file names
        image_files = ["legal.jpg", "contact.jpg", "faq.jpg"]

        for image_file in image_files:
            image_path = os.path.join(image_dir, image_file)

            # Load the image, get its original size, and then calculate the new size while maintaining the aspect ratio
            image = wx.Image(image_path, wx.BITMAP_TYPE_ANY)
            width, height = image.GetWidth(), image.GetHeight()
            max_size = 300
            if width > height:
                new_width = max_size
                new_height = int(height * (max_size / width))
            else:
                new_height = max_size
                new_width = int(width * (max_size / height))

            # Resize the image
            image.Rescale(new_width, new_height)
            image_bitmap = image.ConvertToBitmap()

            label_text = image_file.split('.')[0]

            # Create a panel to hold the image and label
            image_panel = wx.Panel(self, wx.ID_ANY)
            image_sizer_item = wx.BoxSizer(wx.VERTICAL)
            image_panel.SetSizer(image_sizer_item)

            static_bitmap = wx.StaticBitmap(image_panel, wx.ID_ANY, image_bitmap)
            image_sizer_item.Add(static_bitmap, 0, wx.ALIGN_CENTER)

            label = wx.StaticText(image_panel, wx.ID_ANY, label_text, wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTER)
            label.Wrap(-1)
            image_sizer_item.Add(label, 0, wx.ALIGN_CENTER)

            image_sizer.Add(image_panel, 0, wx.ALL | wx.EXPAND, 5)

        bSizerMainFrame.Add(image_sizer, 0, wx.ALIGN_CENTER)

        # Create a centered "Try Us" button with black label, lighter shade of blue background, and font same as the first label's font
        button_font = self.m_staticText2.GetFont()  # Get the font from the first label
        self.m_button1 = wx.Button(self, wx.ID_ANY, u"Try us", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_button1.SetForegroundColour(wx.Colour(0, 0, 0))  # Set the button label color to black
        self.m_button1.SetBackgroundColour(wx.Colour(100, 100, 255))  # Set the button background color to a lighter shade of blue
        self.m_button1.SetFont(button_font)  # Set the button font
        self.m_button1.Bind(wx.EVT_BUTTON, self.on_try_us_click)

        bSizerMainFrame.Add(self.m_button1, 0, wx.ALIGN_CENTER | wx.ALL, 5)

        bSizerFrameMain.Add(bSizerMainFrame, 1, wx.ALL | wx.EXPAND, 0)

        self.SetSizer(bSizerFrameMain)
        self.Layout()

        self.Centre(wx.BOTH)

    def on_try_us_click(self, event):
        # Create a new frame for the "Try Us" page
        try_us_frame = TryUsFrame(self)
        try_us_frame.Show()


app = wx.App(False)
frame = frameMain(None)
frame.Show()
app.MainLoop()
