#SingleInstance force
#NoEnv

DisplayNotification("0.5s")

#C::Run, cmd /k "cd /d `%userprofile`%"
#+C::Run, "C:\UtilityShortcuts\Command Prompt"
^!T::
#T::
    Run, C:\Portable_Programs\cygwin\bin\mintty.exe -
    return
#N::Run, "C:\Program Files (x86)\Notepad++\notepad++.exe"
#+Pause::Run, C:\Windows\system32\rundll32.exe sysdm.cpl`,EditEnvironmentVariables
#F4::ControlSend, , !{F4}, ahk_class Progman ;ShutDown, 9
#F5::Run, "C:\ProgramData\Microsoft\Windows\Start Menu\Programs\StartUp\Autorun"

#IfWinActive ahk_class ConsoleWindowClass
^/::SendInput {Raw}C:\DriveMappings\
#IfWinActive

DisplayNotification(timeoutString := -1, text := "AutoHotkey hotkeys are being set up.")
{
    global progressBar
    Gui, +AlwaysOnTop +ToolWindow +Border -SysMenu -Caption
	Gui, Color, afafaf ;changes background color
	Gui, Font, 000000 s16 wbold, Verdana ;changes font color, size and font
	Gui, Add, Text, , %text% ;the text to display
    timeoutMillis := 5000
    If RegExMatch(timeoutString, "Oi)^(\d+)(\.(\d*)s?|s)?", match)
    {
        tStr := match[1] * 1000
        If match[2]
        {
            If match[3]
                tStr += SubStr(match[3] . "00", 1, 3) * 1
        }
        timeoutMillis := tStr
    }
    Gui, Add, Progress, w450 h20 cBlue Range10-%timeoutMillis% vprogressBar ;Start at 10 to compensate
	Gui, Show, NoActivate AutoSize Center ;X0 Y0
    ProgressTimer(timeoutMillis)
	;Gui, Destroy
}

ProgressTimer(fullTimeOut := "", timeout := "20")
{
    global progressBar
    static _step
    static _limit
    If fullTimeOut
    {
        _limit := fullTimeOut
        _step := timeout
        SetTimer, SetProgress, %_step%
    }
    Else
    {
        GuiControlGet, progLevel, , progressBar
        If progLevel >= %_limit%
        {
            SetTimer, SetProgress, Delete
            Gui, Destroy
        }
        Else
            GuiControl,, progressBar, +%_step%
    }
}

SetProgress:
    ProgressTimer()
    return
    