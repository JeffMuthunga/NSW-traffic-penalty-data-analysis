import wx
import wx.adv
import csv
from datetime import datetime
import wx.lib.mixins.listctrl as listmix

class RecordListCtrl(wx.ListCtrl, listmix.ListCtrlAutoWidthMixin):
    def __init__(self, parent):
        wx.ListCtrl.__init__(self, parent, style=wx.LC_REPORT | wx.BORDER_SUNKEN)
        listmix.ListCtrlAutoWidthMixin.__init__(self)

class SearchSectionClause(wx.Frame):
    def __init__(self, parent):
        super().__init__(parent, id=wx.ID_ANY, title=u"Search Section Clauses", pos=wx.DefaultPosition,
                          size=wx.Size(600, 400), style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)

        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)
        self.SetBackgroundColour(wx.Colour(255, 0, 0))

        # Create labels and date pickers for "From" and "To" dates
        from_label = wx.StaticText(self, wx.ID_ANY, u"From:", wx.DefaultPosition, wx.DefaultSize, 0)
        self.from_date_picker = wx.adv.DatePickerCtrl(self, wx.ID_ANY, style=wx.adv.DP_DROPDOWN | wx.adv.DP_SHOWCENTURY)
        to_label = wx.StaticText(self, wx.ID_ANY, u"To:", wx.DefaultPosition, wx.DefaultSize, 0)
        self.to_date_picker = wx.adv.DatePickerCtrl(self, wx.ID_ANY, style=wx.adv.DP_DROPDOWN | wx.adv.DP_SHOWCENTURY)

        # Create labels and text control for section clauses
        section_label = wx.StaticText(self, wx.ID_ANY, u"Search based on section clauses", wx.DefaultPosition, wx.DefaultSize, 0)
        section_label_font = wx.Font(18, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False,
                             "Baskerville Old Face")
        section_label.SetFont(section_label_font)

        self.section_input = wx.TextCtrl(self, wx.ID_ANY, "", wx.DefaultPosition, wx.DefaultSize, 0)

        # Set initial date values (optional)
        initial_date = datetime.today()
        self.from_date_picker.SetValue(initial_date)
        self.to_date_picker.SetValue(initial_date)

        try_us_sizer = wx.BoxSizer(wx.VERTICAL)

        # Create a sizer for date pickers
        date_picker_sizer = wx.GridSizer(2, 2, 10, 10)
        date_picker_sizer.Add(from_label, 0, wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL, 0)
        date_picker_sizer.Add(self.from_date_picker, 0, wx.EXPAND, 0)
        date_picker_sizer.Add(to_label, 0, wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL, 0)
        date_picker_sizer.Add(self.to_date_picker, 0, wx.EXPAND, 0)

        try_us_sizer.Add(date_picker_sizer, 0, wx.ALL | wx.EXPAND, 10)

        # Add section label and input box
        try_us_sizer.Add(section_label, 0, wx.ALIGN_LEFT | wx.ALL, 8)
        try_us_sizer.Add(self.section_input, 0, wx.EXPAND | wx.ALL, 8)

        submit_button = wx.Button(self, wx.ID_ANY, u"Submit", wx.DefaultPosition, wx.DefaultSize, 0)
        submit_button.Bind(wx.EVT_BUTTON, self.handle_submit)
        try_us_sizer.Add(submit_button, 0, wx.ALIGN_CENTER | wx.ALL, 8)

        self.SetSizerAndFit(try_us_sizer)

    def handle_submit(self, event):
        from_date_str = self.from_date_picker.GetValue().Format("%d\\%m\\%Y")
        to_date_str = self.to_date_picker.GetValue().Format("%d\\%m\\%Y")
        section_clauses = self.section_input.GetValue().split()  # Get section clauses from input

        try:
            from_date = datetime.strptime(from_date_str, "%d\\%m\\%Y")
            to_date = datetime.strptime(to_date_str, "%d\\%m\\%Y")

            # Read the CSV file
            with open('penalty_cases.csv', 'r') as csv_file:
                csv_reader = csv.DictReader(csv_file)
                case_dates = []
                filtered_records = []

                for row in csv_reader:
                    case_date = datetime.strptime(row['OFFENCE_MONTH'], '%d/%m/%Y')

                    if from_date <= case_date <= to_date and row['SECTION_CLAUSE'] in section_clauses:
                        case_dates.append(case_date)
                        filtered_records.append(row)

                if filtered_records:
                    # Display filtered records in a list
                    result_frame = wx.Frame(self, wx.ID_ANY, "Search Results")
                    record_list_ctrl = RecordListCtrl(result_frame)

                    # Insert column headers with bold font
                    headers = ["OFFENCE_FINYEAR", "OFFENCE_MONTH", "OFFENCE_CODE", "OFFENCE_DESC", "LEGISLATION", "SECTION_CLAUSE", "FACE_VALUE"]
                    for col, header in enumerate(headers):
                        record_list_ctrl.InsertColumn(col, header)
                        record_list_ctrl.SetColumnWidth(col, wx.LIST_AUTOSIZE_USEHEADER)

                    # Insert records into the table
                    for record in filtered_records:
                        index = record_list_ctrl.InsertItem(record_list_ctrl.GetItemCount(), record['OFFENCE_FINYEAR'])
                        for col, header in enumerate(headers[1:], 1):  # Skip the first column
                            record_list_ctrl.SetItem(index, col, record[header])

                    result_frame.Show()
                else:
                    wx.MessageBox("No records found for the selected criteria.", "Search Results", wx.OK | wx.ICON_INFORMATION)

        except Exception as e:
            wx.MessageBox("An error occurred: {}".format(str(e)), "Error", wx.OK | wx.ICON_ERROR)
