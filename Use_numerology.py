# Title:        Use_numerology.py
# Author:       Lennox Stampp
# Date:         4/27/2022
# Purpose:      GUI app to run the Numerology class module.

import tkinter as tk
from tkinter import ttk
import numerology
import re


# GUI
class UseNumerologyGUI(numerology.Numerology):

    # Initial GUI object constructor and attributes
    def __init__(self):
        # Set up parent class
        # name = name entry field   dob = dob entry field
        super().__init__()

        # Variables
        self.gifSliceArr = []
        self.iSliceIndx = 0
        self.iGifSliceCnt = 0

        # Main window set up
        self.mainWin = tk.Tk()
        self.mainWin.geometry("500x700")
        self.mainWin.title("Numerology by Lennox Stampp")
        self.mainWin.config(bg="black")

        # Set up ttk theme style
        self.themes = ttk.Style()
        self.themes.theme_use("alt")

        # Set up background gif
        # --Label to hold gif img
        self.lblGifHolder = ttk.Label(self.mainWin, image="", borderwidth=0, background="black")
        
        # --Gif image set up
        # ----Loop through each frame in gif and add it to gifSliceArr
        self.loopNum = 0

        while True:
            # Show gif loading progress
            print(f"Gif img loading {(self.loopNum / 24) * 100:.2f}% ......\n{'*' * self.loopNum * 2}")
            # Get gif frame/slice image according to the frame/slice index
            try:
                self.sGifSlice = f"gif -index {{{self.iSliceIndx}}}"
                self.gifImg = tk.PhotoImage(file="qnumrology500x800.gif", format=self.sGifSlice)

            # ------Get gif frame count and exit loop
            except:
                self.iLastSlice = self.iSliceIndx - 1
                break

            # Add Gif frame image object to array
            self.gifSliceArr.append(self.gifImg)
            self.iSliceIndx += 1
            self.loopNum += 1

        # Create subclass of ttk.Frame theme 'TFrame'
        self.themes.configure('Mainfrm.TFrame', background="black")

        # Frame to hold input and outputs and buttons
        self.frmMain = ttk.Frame(self.mainWin, width=500, height=300, style='Mainfrm.TFrame')
        # Inner frames
        self.btnFrame = ttk.Frame(self.frmMain, style='Mainfrm.TFrame')
        self.entrFrame = ttk.Frame(self.frmMain, style='Mainfrm.TFrame')
        self.outFrame = ttk.Frame(self.frmMain, style='Mainfrm.TFrame')

        # Create subclass ttk.Label theme 'TLabel'
        self.themes.configure('New.TLabel', foreground='white', background="purple")
        # Labelframe for input lbfEntry1
        self.lblForFrame = ttk.Label(text="Enter your first and last name:", style='New.TLabel', width=26)
        self.lblframe1 = ttk.Labelframe(master=self.entrFrame, labelwidget=self.lblForFrame,
                                        style='New.TLabel', borderwidth=5, labelanchor='n')

        # Create subclass ttk.Entry theme 'TEntry'
        self.themes.configure('new.TEntry', fieldbackground="black",
                              highlightwidth=10, insertcolor="white")

        # Name entry
        self.lbfEntry1 = ttk.Entry(self.lblframe1, style='new.TEntry', foreground='grey')
        # --Placeholder text
        self.lbfEntry1.insert(0, "First Last")
        # --Event when inside of entry field is clicked
        self.lbfEntry1.bind('<ButtonPress>', lambda event: self.clrFrEntr1(event))
        # --Event when keyboard focus is not on entry field
        self.lbfEntry1.bind('<FocusOut>', lambda event: self.lvEntr1Blnk(event))
        # --Event to validate name entry and disable/enable btnSubmit
        self.lbfEntry1.bind('<Leave>', lambda event: self.ckNameEntry(event))

        # Labelframe for input lbfEntry2
        self.lblForFrame2 = ttk.Label(text="Date of Birth: (mm/dd/yyyy)", style='New.TLabel', width=26)
        self.lblframe2 = ttk.Labelframe(self.entrFrame, labelwidget=self.lblForFrame2,
                                        style='New.TLabel', borderwidth=5, labelanchor='n')
        # DOB entry
        self.lbfEntry2 = ttk.Entry(self.lblframe2, style='new.TEntry', foreground='grey')
        # --Placeholder text
        self.lbfEntry2.insert(0, "mm/dd/yyyy")
        # --Event when inside of entry field is clicked
        self.lbfEntry2.bind('<ButtonPress>', lambda event: self.clrFrEntr2(event))
        # --Event when keyboard focus is not on entry field
        self.lbfEntry2.bind('<FocusOut>', lambda event: self.lvEntr2Blnk(event))
        # --Event to validate DOB format and disable/enable btnSubmit
        self.lbfEntry2.bind('<Leave>', lambda event: self.ckDateFormt(event))

        # Buttons
        # --Create sublass ttk.Button theme 'TButton'
        self.themes.configure('New.TButton', foreground='white', background="purple",
                              width=20, height=20)
        self.themes.map('New.TButton', background=[('active', 'black')])
        # --Submit button
        self.btnSubmit = ttk.Button(self.btnFrame, text="Submit", style='New.TButton')
        self.btnSubmit.bind('<ButtonPress>', lambda event: [self.setNumerologyData(event),
                                                            self.hideFrames(event),
                                                            self.showOutFrame(event),
                                                            self.dispOutput(event)
                                                            ])

        # --Exit button
        self.btnExit = ttk.Button(self.btnFrame, text="Exit", command=self.mainWin.destroy,
                                  style='New.TButton')

        # --Main button - Return to input screen
        self.btnMain = ttk.Button(self.btnFrame, text="Main", style='New.TButton')
        self.btnMain.bind('<ButtonPress>', lambda event: self.rtnToMain(event))
        self.btnMain.pack_forget()

        # Output screen
        self.dispArea = tk.Text(self.outFrame, background="black", foreground="purple")

        # Build window widgets
        self.lblGifHolder.place(x=0, y=0)
        self.frmMain.pack()
        self.btnFrame.pack(side="right")
        self.btnSubmit.pack(side="top", fill="both", padx=15, pady=15)
        self.btnExit.pack(side="top", fill="both", padx=15, pady=15)
        self.entrFrame.pack()
        self.lblframe1.pack(pady=10)
        self.lbfEntry1.pack(pady=5)
        self.lblframe2.pack(pady=10)
        self.lbfEntry2.pack(pady=5)

        # Run gif animation
        self.animate_gif(0)
        # Run window script
        tk.mainloop()

    # Loop through gif images in gifSliceArr[count] recursively and update gif img
    # after 90 milliseconds
    def animate_gif(self, count):
        # check if last gif frame, if so reset count and start from first gif slice
        if count > self.iLastSlice or self.iLastSlice < 0:
            count = 0
        # load new image slice onto window
        self.lblGifHolder.config(image=self.gifSliceArr[count])
        count += 1
        # refresh window
        self.mainWin.after(90, lambda: self.animate_gif(count))

    # Event functions

    # --Button event to hide buttons and entry fields
    def hideFrames(self, event):
        if event.widget.state()[0] == "active":
            self.btnFrame.pack_forget()
            self.btnSubmit.pack_forget()
            self.entrFrame.pack_forget()

    # ----Show the output display and add button to the bottom to exit
    def showOutFrame(self, event):
        if event.widget.state()[0] == "active":
            self.outFrame.pack()
            self.dispArea.pack()
            self.btnFrame.pack(side="bottom")
            self.btnExit.pack()
            self.btnMain.pack()

    # -- Button to return to main screen
    def rtnToMain(self, event=None):
        # remove output display frames
        self.outFrame.pack_forget()
        self.dispArea.pack_forget()
        self.btnFrame.pack_forget()
        self.btnExit.pack_forget()
        self.btnMain.pack_forget()
        # set up input frame
        self.btnFrame.pack(side="right")
        self.btnSubmit.pack(side="top", fill="both", padx=15, pady=15)
        self.btnExit.pack(side="top", fill="both", padx=15, pady=15)
        self.entrFrame.pack()

    # -- Entry field events
    # ----Used with <ButtonPress> to clear entry field 1 and change font color to white
    def clrFrEntr1(self, event=None):
        self.lbfEntry1.delete(0, tk.END)
        self.lbfEntry1.config(foreground="white")

    # ----Used with <ButtonPress> to clear entry field 2 and change font color to white
    def clrFrEntr2(self, event=None):
        self.lbfEntry2.delete(0, tk.END)
        self.lbfEntry2.config(foreground="white")

    # ----Used with <FocusOut> to add placeholder text to entry field 1 and change font color to grey
    def lvEntr1Blnk(self, event=None):
        if len(self.lbfEntry1.get()) == 0:
            self.lbfEntry1.config(foreground="grey")
            self.lbfEntry1.insert(0, "First Last")

    # ----Used with <FocusOut> to add placeholder text to entry field 2 and change font color to grey
    def lvEntr2Blnk(self, event=None):
        if len(self.lbfEntry2.get()) == 0:
            self.lbfEntry2.config(foreground="grey")
            self.lbfEntry2.insert(0, "mm/dd/yyyy")

    # Validation functions
    # --Validate date is proper format with 8 digits and 2 (- or /)
    # --Used with <ButtonPress> event of btnSubmit
    def ckDateFormt(self, event):
        sDtStr = self.lbfEntry2.get()
        regExPtrn = "[0-1]\d[-/][0-3]\d[-/][0-2]\d\d\d"
        matchReslt = re.match(regExPtrn, sDtStr)
        if not matchReslt:
            event.widget.insert(0, "Re-enter mm/dd/yyyy")
            self.btnSubmit.state(["disabled"])
        else:
            self.btnSubmit.state(["!disabled"])

    # --Validate name field has input A-Z
    def ckNameEntry(self, event):
        sNmStr = self.lbfEntry1.get()
        regExPtrn = "[A-Za-z]+ [A-Za-z]+"
        matchReslt = re.match(regExPtrn, sNmStr)
        if len(sNmStr) == 0 or not matchReslt:
            event.widget.insert(0, "Re-enter fname lname")
            self.btnSubmit.state(["disabled"])
        else:
            pass

    # --Set numerology name and dob
    def setNumerologyData(self, event=None):
        self.setName(self.lbfEntry1.get())
        self.setDOB(self.lbfEntry2.get())

    # --Display output onto dispArea
    def dispOutput(self, event=None):
        # Display heading
        self.dispArea.insert(tk.END, f"\n{'_' * 50:^60}\n")
        self.dispArea.insert(tk.END, f"{'Birth Name:':<21}{'.'* 15:^20}{self.getName():<5}\n")
        self.dispArea.insert(tk.END, f"{'Date of Birth:':<21}{'.'* 15:^20}{self.getDOB():<5}\n")
        self.dispArea.insert(tk.END, f"{'-' * 50:^60}\n")
        self.dispArea.insert(tk.END, f"{'--Numerology results--':^50}\n")
        self.dispArea.insert(tk.END, f"{'-' * 50:^60}\n")
        self.dispArea.insert(tk.END, f"{'-' * 50:^60}\n\n")
        # Display info
        self.dispArea.insert(tk.END, f"{'Life Path Number:':<21}{'.'* 15:^20}{self.getLifePath():<5}\n")
        self.dispArea.insert(tk.END, f"{'Birth Day Number:':<21}{'.' * 15:^20}{self.getBirthDayNum():<5}\n")
        self.dispArea.insert(tk.END, f"{'Attitude Day Number:':<21}{'.' * 15:^20}{self.getAttitude():<5}\n")
        self.dispArea.insert(tk.END, f"{'Soul Number:':<21}{'.' * 15:^20}{self.getSoul():<5}\n")
        self.dispArea.insert(tk.END, f"{'Personality Number:':<21}{'.' * 15:^20}{self.getPersonality():<5}\n")
        self.dispArea.insert(tk.END, f"{'Power Name Number:':<21}{'.' * 15:^20}{self.getPowerName():<5}\n")
        self.dispArea.insert(tk.END, f"{'-' * 50:^60}\n")
        self.dispArea.insert(tk.END, f"{'-' * 50:^60}")
        self.dispArea.insert(tk.END, f"\n{'*** Scroll to view results of multiple entries ***':^}\n\n")



# run app
run = UseNumerologyGUI()