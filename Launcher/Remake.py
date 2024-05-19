from tkinter import Tk, Frame, Button, Listbox, Entry


class Application:
    def __init__(Self) -> None:
        Self.Tk = Tk()
        Self.Tk.geometry("640x600")
        Self.Tk.rowconfigure(0, weight=0)
        Self.Tk.rowconfigure(1, weight=2)
        Self.Tk.rowconfigure(2, weight=2)
        Self.Tk.columnconfigure(0, weight=1)

        Self.ToolbarFrame = Frame(Self.Tk)
        Self.ToolbarFrame.columnconfigure(0, weight=1)
        Self.ToolbarFrame.columnconfigure(1, weight=1)
        Self.ToolbarFrame.columnconfigure(2, weight=1)
        Self.ToolbarFrame.rowconfigure(0, weight=1)
        Self.ToolbarFrame.grid(row=0, column=0, sticky="nw")

        Self.StartButton = Button(Self.ToolbarFrame, text="Start")
        Self.StartButton.grid(row=0, column=0,sticky="nw")

        Self.StartButton = Button(Self.ToolbarFrame, text="Restart")
        Self.StartButton.grid(row=0, column=1,sticky="nw")

        Self.StartButton = Button(Self.ToolbarFrame, text="Stop")
        Self.StartButton.grid(row=0, column=2,sticky="nw")

        Self.ContentFrame = Frame(Self.Tk)
        Self.ContentFrame.columnconfigure(0, weight=0)
        Self.ContentFrame.columnconfigure(1, weight=1)
        Self.ContentFrame.rowconfigure(0, weight=1)
        Self.ContentFrame.grid(row=1, column=0, sticky="nsew")

        Self.PlayersList = Listbox(Self.ContentFrame)
        Self.PlayersList.grid(row=0, column=0, sticky="nsew")
        
        Self.DataList = Listbox(Self.ContentFrame)
        Self.DataList.grid(row=0, column=1, sticky="nsew")

        Self.TerminalFrame = Frame(Self.Tk)
        Self.TerminalFrame.columnconfigure(0, weight=1)
        Self.TerminalFrame.rowconfigure(0, weight=1)
        Self.TerminalFrame.rowconfigure(1, weight=0)
        Self.TerminalFrame.grid(row=2, column=0, sticky="nsew")

        Self.TerminalLog = Listbox(Self.TerminalFrame)
        Self.TerminalLog.grid(row=0, column=0, sticky="nsew")

        


    def Run(Self):
        Self.Tk.mainloop()


Application().Run()