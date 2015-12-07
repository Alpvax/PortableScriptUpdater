class GuiWindow
{
    static nextID := 1
    displayed := false
    currentFunctionText := "Initialising"
    __new(){
        global currentFunctionText
        this.id := GuiWindow.nextID++
        MsgBox % this.id
        Gui, % this.id . ": New", +AlwaysOnTop +ToolWindow +Border -SysMenu -Caption
        Gui, % this.id . ": Color", afafaf ;changes background color
        Gui, % this.id . ": Font", 000000 s16 wbold, Verdana ;changes font color, size and font
        Gui, % this.id . ": Add", Text, vcurrentFunctionText, % this.currentFunctionText ;the text to display
        ;Gui, Add, Text, vcurrentFunctionText, Initialising ;the text to display
        this.setText("Checking scripts")
	}
    
    setText(text)
    {
        this.currentFunctionText := text
        GuiControl, Text, currentFunctionText, % this.currentFunctionText
        this.display()
    }
    
    add(frames)
    {
        
    }
    
    display()
    {
        Gui, % this.id . ": Show", AutoSize Center
    }
    
    close()
    {
        Gui, % this.id . ": Destroy"
    }
}

guiWin := new GuiWindow()
guiWin.display()
SetTimer, guiDone, -2000
return

guiDone:
    guiWin.close()
    return