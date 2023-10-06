import wx
import wx.adv
import csv
from datetime import datetime
import matplotlib.pyplot as plt
from collections import Counter
import wx.lib.mixins.listctrl as listmix
from search_section_clause import  SearchSectionClause

class RecordListCtrl(wx.ListCtrl, listmix.ListCtrlAutoWidthMixin):
    def __init__(self, parent):
        wx.ListCtrl.__init__(self, parent, style=wx.LC_REPORT | wx.BORDER_SUNKEN)
        listmix.ListCtrlAutoWidthMixin.__init__(self)


class TryUsFrame(wx.Frame):
    def __init__(self, parent):
        super().__init__(parent, id=wx.ID_ANY, title=u"Try Us Page", pos=wx.DefaultPosition,
                          size=wx.Size(600, 400), style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)

        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)
        self.SetBackgroundColour(wx.Colour(255, 0, 0))

        # Add content to the "Try Us" page here

        # Create a label with large font, centered at the top
        label = wx.StaticText(self, wx.ID_ANY, u"SELECT THE TIME PERIOD", wx.DefaultPosition, wx.DefaultSize,
                              wx.ALIGN_CENTER)
        label.Wrap(-1)
        label_font = wx.Font(18, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False,
                             "Baskerville Old Face")
        label.SetFont(label_font)

        # Create labels and date pickers for "From" and "To" dates
        from_label = wx.StaticText(self, wx.ID_ANY, u"From:", wx.DefaultPosition, wx.DefaultSize, 0)
        self.from_date_picker = wx.adv.DatePickerCtrl(self, wx.ID_ANY, style=wx.adv.DP_DROPDOWN | wx.adv.DP_SHOWCENTURY)
        to_label = wx.StaticText(self, wx.ID_ANY, u"To:", wx.DefaultPosition, wx.DefaultSize, 0)
        self.to_date_picker = wx.adv.DatePickerCtrl(self, wx.ID_ANY, style=wx.adv.DP_DROPDOWN | wx.adv.DP_SHOWCENTURY)

        # Set initial date values (optional)
        initial_date = datetime.today()
        self.from_date_picker.SetValue(initial_date)
        self.to_date_picker.SetValue(initial_date)

        # Create the ComboBox with the specified values
        find_label = wx.StaticText(self, wx.ID_ANY, u"Find:", wx.DefaultPosition, wx.DefaultSize, 0)
        self.find_combo = wx.ComboBox(self, wx.ID_ANY, choices=["penalty cases", "distribution chart", "Radar/Camera", "Mobile Phone Usage"], style=wx.CB_DROPDOWN | wx.CB_READONLY)

        try_us_label = wx.StaticText(self, wx.ID_ANY,
                                     u"Search section clause penalty records, here. 😝😝",
                                     wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTER)
        try_us_label.Wrap(400)  # Adjust the width as needed

        try_us_sizer = wx.BoxSizer(wx.VERTICAL)
        try_us_sizer.Add(label, 0, wx.ALIGN_CENTER | wx.ALL, 8)  # Add the large label at the top

        # Create a sizer for date pickers, labels, and the ComboBox
        date_picker_sizer = wx.GridSizer(3, 2, 10, 10)
        date_picker_sizer.Add(from_label, 0, wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL, 0)
        date_picker_sizer.Add(self.from_date_picker, 0, wx.EXPAND, 0)
        date_picker_sizer.Add(to_label, 0, wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL, 0)
        date_picker_sizer.Add(self.to_date_picker, 0, wx.EXPAND, 0)
        date_picker_sizer.Add(find_label, 0, wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL, 0)
        date_picker_sizer.Add(self.find_combo, 0, wx.EXPAND, 0)

        try_us_sizer.Add(date_picker_sizer, 0, wx.ALL | wx.EXPAND, 10)
        submit_button = wx.Button(self, wx.ID_ANY, u"Submit", wx.DefaultPosition, wx.DefaultSize, 0)
        submit_button.Bind(wx.EVT_BUTTON, self.handle_submit)
        try_us_sizer.Add(submit_button, 0, wx.ALIGN_CENTER | wx.ALL, 8)
         # Add date picker and ComboBox sizer
        try_us_sizer.Add(try_us_label, 0, wx.ALIGN_CENTER | wx.ALL, 8)

        search_section_clause = wx.Button(self, wx.ID_ANY, u"Search Section Clause", wx.DefaultPosition, wx.DefaultSize, 0)
        search_section_clause.Bind(wx.EVT_BUTTON, self.search_section)
        try_us_sizer.Add(search_section_clause, 0, wx.ALIGN_CENTER | wx.ALL, 8)

        self.SetSizerAndFit(try_us_sizer)



    def search_section(self, event):
        # Create a new frame for the "Try Us" page
        next_page = SearchSectionClause(self)
        next_page.Show()





# ...

    def handle_submit(self, event):
            # Get selected dates and ComboBox option
            from_date_str, to_date_str, selected_item = self.get_selected_dates()

            try:
                # Convert date strings to datetime objects
                from_date = datetime.strptime(from_date_str, "%d\\%m\\%Y")
                to_date = datetime.strptime(to_date_str, "%d\\%m\\%Y")

                # Read the CSV file
                with open('penalty_cases.csv', 'r') as csv_file:
                    csv_reader = csv.DictReader(csv_file)
                    case_dates = []
                    filtered_records = []

                    for row in csv_reader:
                        case_date = datetime.strptime(row['OFFENCE_MONTH'], '%d/%m/%Y')

                        if from_date <= case_date <= to_date:
                            case_dates.append(case_date)

                        if selected_item == "penalty cases":
                            # Filter for penalty cases
                            if from_date <= case_date <= to_date:
                                filtered_records.append(row)

                        elif selected_item == "Radar/Camera":
                            # Filter for Radar/Camera with CAMERA_IND == "Y"
                            if from_date <= case_date <= to_date and row.get("CAMERA_IND") == "Y":
                                filtered_records.append(row)

                        elif selected_item == "Mobile Phone Usage":
                            # Filter for Mobile Phone Usage with MOBILE_PHONE_IND == "Y"
                            if from_date <= case_date <= to_date and row.get("MOBILE_PHONE_IND") == "Y":
                                filtered_records.append(row)

                    if selected_item == "distribution chart":
                        # Generate a line chart showing the frequency of cases over the selected dates
                        plt.figure(figsize=(10, 6))

                        # Use Counter to count the frequency of dates
                        date_counter = Counter(case_dates)
                        dates, frequencies = zip(*sorted(date_counter.items()))

                        plt.plot(dates, frequencies, marker='o', linestyle='-')
                        plt.xlabel("Date")
                        plt.ylabel("Frequency")
                        plt.title("Distribution of Cases Over Time")
                        plt.xticks(rotation=45)
                        plt.grid(True)

                        plt.show()

                        return  # No need to display records for "distribution chart"

                    if filtered_records:
                        result_frame = wx.Frame(self, wx.ID_ANY, selected_item)
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
                        wx.MessageBox("No records found for the selected criteria.", selected_item, wx.OK | wx.ICON_INFORMATION)

            except Exception as e:
                wx.MessageBox("An error occurred: {}".format(str(e)), "Error", wx.OK | wx.ICON_ERROR)




    def get_selected_dates(self):
        from_date = self.from_date_picker.GetValue()
        to_date = self.to_date_picker.GetValue()

        # Format the dates as "dd\mm\yyyy"
        formatted_from_date = from_date.Format("%d\\%m\\%Y")
        formatted_to_date = to_date.Format("%d\\%m\\%Y")

        # Get the selected item from the ComboBox
        selected_item = self.find_combo.GetValue()

        return formatted_from_date, formatted_to_date, selected_item
