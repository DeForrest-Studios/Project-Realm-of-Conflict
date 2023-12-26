from sys import exit
from os import remove
from os.path import join
from subprocess import *
from glob import glob


class Launcher:
    def __init__(Self):
        Self.Key = None
        Self.Bot = None
        Self.CommandDictionary = {"start": Self.Start,
                                  "restart": Self.Restart,
                                  "exit": Self.Exit,
                                  "stop": Self.Stop,
                                  "//": Self.Emergency_Stop,
                                  "clear logs": Self.Clear_Logs}
        
        Self.Read_User_Settings()
        Self.Read_Key_File()
        Self.Key_Selection()

        Self.VirtualEnvironmentPath = join(".venv","Scripts","python")

        Self.CallCommand = f"{Self.VirtualEnvironmentPath} -B {join(Self.ProjectFilePath)} {Self.Key} {Self.KeySelection}"

        Self.User_Input()


    def Read_User_Settings(Self):
        with open(join("Launcher", "LauncherSettings.txt"), 'r') as File:
            UserSettings = File.readlines()
            ProjectPath = UserSettings[0].split(":")[1].split("/")
            Self.ProjectFilePath = join(*ProjectPath)
            print(Self.ProjectFilePath)
        

    def Read_Key_File(Self):
        with open("Keys.txt"):
            Self.KeyData = open("Keys.txt", "r").readlines()
            Self.Keys = {Line.split("~")[0].lower():Line.split("~")[1] for Line in Self.KeyData}


    def Key_Selection(Self):
        while Self.Key is None:
            print(f"Please select the key you'd like to run with.\nSelections:{Self.Keys.keys()}")
            Self.KeySelection = input("> ").lower()
            print(Self.KeySelection)
            if Self.KeySelection in Self.Keys.keys():
                Self.Key = Self.Keys[Self.KeySelection.lower()]
            else:
                print("Improper selection.")


    def User_Input(Self):
        while True:
            AdminInput = input()
            print("Input command: ", AdminInput)
            try:
                Self.CommandDictionary[AdminInput.lower()]()
            except KeyError:
                print("Invalid command.")


    def Start(Self):
        Self.Bot = Popen(Self.CallCommand)


    def Restart(Self):
        if Self.Bot is not None:
            print("Discord bot stopped")
            Self.Bot.kill()
            Self.Bot = Popen(Self.CallCommand)
            print("Discord bot restarted")
        else:
            print("There isn't a running bot")

    def Exit(Self):
        if Self.Bot is not None:
            exit()
        else:
            print("There is a running bot")


    def Stop(Self):
        if Self.Bot is not None:
            print("Discord bot stopped")
            Self.Bot = Self.Bot.kill()
        else:
            print("There isn't a running bot")


    def Emergency_Stop(Self):
        if Self.Bot is None:
            print("Bot is not running it seems, stopping altogether though.")
            exit()
        else:
            print("Discord bot stopped")
            Self.Bot = Self.Bot.kill()
            exit()


    def Clear_Logs(Self):
        for File in glob("Source\\Logs\\*.log"):
            try:
                remove(File)
            except OSError:
                print("Error removing log files for some reason")