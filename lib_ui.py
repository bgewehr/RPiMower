#!/usr/bin/env python
import npyscreen, curses

class MyTestApp(npyscreen.NPSAppManaged):
    def onStart(self):
	self.keypress_timeout_default = 1
        self.addForm("MAIN",       MainForm, name="Screen 1", color="IMPORTANT",)
        self.addForm("SECOND",     MainForm, name="Screen 2", color="WARNING",  )
	self.currentform = None

    def onCleanExit(self):
        npyscreen.notify_wait("Goodbye!")
        
    def change_form(self, name):
        self.switchForm(name)
        self.resetHistory()
    
class MainForm(npyscreen.ActionForm):
    def create(self):
	self.keypress_timeout_default = 1
        self.add(npyscreen.TitleText, name = "Text:", value= "Press ^T to change screens" )
        self.sentfield = self.add(npyscreen.TitleText, name = "Sent:", value="", editable=False )
        self.receivedfield = self.add(npyscreen.TitleText, name = "Received:", value="", editable=False )
        
        self.add_handlers({"^T": self.change_forms})


    def on_ok(self):
        # Exit the application if the OK button is pressed.
        self.parentApp.switchForm(None)

    def change_forms(self, *args, **keywords):
        if self.name == "Screen 1":
            change_to = "SECOND"
        else:
            change_to = "MAIN"

        # Tell the MyTestApp object to change forms.
        self.parentApp.change_form(change_to)

def init():
    TA = MyTestApp()
    TA.run()


if __name__ == '__main__':
    main()


