import wx
import math
from fractions import Fraction

DISP_COLOR = wx.Colour(243, 248, 205) # Yellowish
STACK4 = 0
STACK3 = 0
STACK2 = 0
STACK1 = 0

class MainFrame(wx.Frame):
    '''Main calculator frame'''
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('title', "Feet-Inch Calculator")
        wx.Frame.__init__(self, *args, **kwargs)
        self.calcPanel = CalcPanel(self)
        fsizer = wx.BoxSizer(wx.VERTICAL)
        fsizer.Add(self.calcPanel, 1, wx.EXPAND, 10)
        self.CenterOnScreen()
        self.SetSizerAndFit(fsizer)

        
class CalcPanel(wx.Panel):
    '''Panel containing display, conversion radiobox and buttons'''
    def __init__(self, *args, **kwargs):
        wx.Panel.__init__(self, *args, **kwargs)
        sizer = wx.GridBagSizer(3,2)

        #-------------Display------------------
        self.display4 = wx.StaticText(self, -1, str(STACK4),
                                      style=wx.ALIGN_RIGHT|wx.ST_NO_AUTORESIZE)
        self.display3 = wx.StaticText(self, -1, str(STACK3), 
                                      style=wx.ALIGN_RIGHT|wx.ST_NO_AUTORESIZE)
        self.display2 = wx.StaticText(self, -1, str(STACK2),
                                      style=wx.ALIGN_RIGHT|wx.ST_NO_AUTORESIZE)
        self.display1 = wx.StaticText(self, -1, str(STACK1),
                                      style=wx.ALIGN_RIGHT|wx.ST_NO_AUTORESIZE)
        self.display = wx.TextCtrl(self, -1, style=wx.TE_RIGHT)
        self.text4 = wx.StaticText(self, -1, "4:")
        self.text3 = wx.StaticText(self, -1, "3:")
        self.text2 = wx.StaticText(self, -1, "2:")
        self.text1 = wx.StaticText(self, -1, "1:")
        sizer.Add(self.text4, (0,0), (1,1), wx.EXPAND|wx.LEFT|wx.TOP, 10)
        sizer.Add(self.text3, (1,0), (1,1), wx.EXPAND|wx.LEFT, 10)
        sizer.Add(self.text2, (2,0), (1,1), wx.EXPAND|wx.LEFT, 10)
        sizer.Add(self.text1, (3,0), (1,1), wx.EXPAND|wx.LEFT, 10)
        sizer.Add(self.display4, (0,1), (1,1), wx.EXPAND|wx.RIGHT|wx.TOP, 10)
        sizer.Add(self.display3, (1,1), (1,1), wx.EXPAND|wx.RIGHT, 10)
        sizer.Add(self.display2, (2,1), (1,1), wx.EXPAND|wx.RIGHT, 10)
        sizer.Add(self.display1, (3,1), (1,1), wx.EXPAND|wx.RIGHT, 10)
        sizer.Add(self.display, (4,0), (1,2), wx.EXPAND|wx.RIGHT|wx.LEFT, 10)

        #-------------Conversion RadioBox --------------
        self.rbox = wx.RadioBox(self, label= "Conversion",
                           choices=["Feet", "Inches", "Decimal"],
                           majorDimension=3, style=wx.RA_SPECIFY_COLS)
        self.rbox.SetSelection(0)
        sizer.Add(self.rbox, (5,0), (1,2), wx.ALIGN_LEFT|wx.EXPAND|wx.RIGHT|wx.LEFT, 10)
        self.rbox.Bind(wx.EVT_RADIOBOX, self.conversion)

        #--------------Buttons-----------------
        gsizer1 = wx.GridSizer(5,3,2,2)
        buttons1 = (('7', '8', '9'),
                    ('4', '5', '6'),
                    ('3', '2', '1'),
                    ('C', '0', '.'))
        gsizer2 = wx.GridSizer(5,2,2,2)
        buttons2 = (("Swap", "Del"),
                    ("/", "'"),
                    ("*", "^"),
                    ("-", "sqrt"),
                    ("+", "Enter"))
        gsizer1.Add((1,1), 1, wx.EXPAND)
        gsizer1.Add((1,1), 1, wx.EXPAND)
        gsizer1.Add((1,1), 1, wx.EXPAND)
        for row in buttons1:
            for label in row:
                b = wx.Button(self, label=label, size=(40,-1))
                gsizer1.Add(b)
                b.Bind(wx.EVT_BUTTON, self.OnButton)                
        sizer.Add(gsizer1, (6,0),(1,1), wx.EXPAND|wx.LEFT|wx.BOTTOM|wx.ALIGN_BOTTOM, 10)

        for row in buttons2:
            for label in row:
                b = wx.Button(self, label=label, size=(60,-1))
                gsizer2.Add(b)
                b.Bind(wx.EVT_BUTTON, self.OnButton)
                b.Bind(wx.EVT_KEY_DOWN, self.OnKeyPress)
        sizer.Add(gsizer2, (6,1),(1,1), wx.EXPAND|wx.LEFT|wx.RIGHT|wx.BOTTOM, 10)
        self.SetSizerAndFit(sizer)

    def OnKeyPress(self, event):
        keycode = event.GetKeyCode()
        if keycode == wx.WXK_RETURN or wx.WXK_NUMPAD_ENTER:
            self.enter()

        elif keycode == wx.WXK_ADD or wx.WXK_NUMPAD_ADD:
            self.add()

        
    def OnButton(self, event):
        #Get title of clicked button
        global STACK1, STACK2, STACK3, STACK4, STATE, TEMP_NUM
        label = event.GetEventObject().GetLabel()

        if label == 'Enter':
            self.enter()

        elif label == '+':
            self.add()

        elif label == '-':
            self.sub()

        elif label == '/':
            self.div()

        elif label == '*':
            self.mult()

        elif label == 'sqrt':
            self.sqrt()

        elif label == '^':
            self.power()

        elif label == 'Swap':
            self.swap()

        elif label == 'Del':
            self.delete()

        elif label == 'C':
            self.display.SetValue('')

        else:
            self.display.SetValue(self.display.GetValue() + label)
            
    def enter(self):
        """ enter a new number to the stack"""
        global STACK1, STACK2, STACK3, STACK4
        if self.display.GetValue() != "":
            STACK4 = STACK3
            STACK3 = STACK2
            STACK2 = STACK1
            STACK1 = self.frac_to_decimal()
            self.updateDisplay()
        else:
            STACK4 = STACK3
            STACK3 = STACK2
            STACK2 = STACK1
            STACK1 = 0
            self.updateDisplay()
                        
    def swap(self):
        """ swap contents of stack1 and stack2"""
        global STACK1, STACK2
        STACK1, STACK2 = STACK2, STACK1
        self.updateDisplay()

    def delete(self):
        """ delete number from stack1 display and shift remaining results down stack"""
        global STACK1, STACK2, STACK3, STACK4
        STACK1 = STACK2
        STACK2 = STACK3
        STACK3 = STACK4
        STACK4 = 0
        self.updateDisplay()
        
    def add(self):
        """ add stack1 and display or contents of stack"""
        global STACK1, STACK2, STACK3, STACK4
        if self.display.GetValue() != "":
            STACK1 = STACK1 + self.frac_to_decimal()
            self.updateDisplay()
        else:
            STACK1 = STACK2 + STACK1
            STACK2 = STACK3
            STACK3 = STACK4
            STACK4 = 0
            self.updateDisplay()
                            
    def sub(self):
        """ subtract stack1 and display or contents of stack"""
        global STACK1, STACK2, STACK3, STACK4
        if self.display.GetValue() != "":
            STACK1 = STACK1 - self.frac_to_decimal()
            self.updateDisplay()
        else:
            STACK1 = STACK2 - STACK1
            STACK2 = STACK3
            STACK3 = STACK4
            STACK4 = 0
            self.updateDisplay()
   
    def mult(self):
        """ multiply stack1 and display or contents of stack"""
        global STACK1, STACK2, STACK3, STACK4
        if self.display.GetValue() != "":
            STACK1 = STACK1 * self.frac_to_decimal()
            self.updateDisplay()
        else:
            STACK1 = STACK2 * STACK1
            STACK2 = STACK3
            STACK3 = STACK4
            STACK4 = 0
            self.updateDisplay()

    def div(self):
        """ divide stack1 and display or contents of stack"""
        global STACK1, STACK2, STACK3, STACK4
        if self.display.GetValue() != "":
            STACK1 = STACK1 / self.frac_to_decimal()
            self.updateDisplay()
        else:
            STACK1 = STACK2 / STACK1
            STACK2 = STACK3
            STACK3 = STACK4
            STACK4 = 0
            self.updateDisplay()

    def sqrt(self):
        """ take the square root of display or stack1"""
        global STACK1, STACK2, STACK3, STACK4
        if self.display.GetValue() != "":
            if self.display.GetValue() >= 0:
                STACK4 = STACK3
                STACK3 = STACK2
                STACK2 = STACK1
                STACK1 = math.sqrt(self.frac_to_decimal())
                self.updateDisplay()
            else:
                dlg = wx.MessageDialog(self, "Neg numbers not valid",
                                       wx.OK|wx.CANCEL)
                dlg.ShowModal()
                dlg.Destroy()
        else:
            if STACK1 >= 0:
                STACK1 = math.sqrt(STACK1)
                self.updateDisplay()
            else:
                dlg = wx.MessageDialog(self, "Neg numbers not valid",
                                       wx.OK|wx.CANCEL)
                dlg.ShowModal()
                dlg.Destroy()

    def power(self):
        """ raise to the power"""
        global STACK1, STACK2, STACK3, STACK4
        if self.display.GetValue() != "":
            STACK1 = STACK1 ** self.frac_to_decimal()
            self.updateDisplay()
        else:
            STACK1 = STACK2 ** STACK1
            STACK2 = STACK3
            STACK3 = STACK4
            STACK4 = 0
            self.updateDisplay()            
            
    def updateDisplay(self):
        """ update display """
        global STACK1, STACK2, STACK3, STACK4
        if self.rbox.GetSelection() == 0:
            S4 = self.fraction_str(STACK4)
            S3 = self.fraction_str(STACK3)
            S2 = self.fraction_str(STACK2)
            S1 = self.fraction_str(STACK1)
        elif self.rbox.GetSelection() == 1:
            S4 = str(STACK4 * 12)
            S3 = str(STACK3 * 12)
            S2 = str(STACK2 * 12)
            S1 = str(STACK1 * 12)
        else:
            S4 = str(STACK4)
            S3 = str(STACK3)
            S2 = str(STACK2)
            S1 = str(STACK1)
            
        self.display4.SetLabel(S4)
        self.display3.SetLabel(S3)
        self.display2.SetLabel(S2)
        self.display1.SetLabel(S1)
        self.display.SetValue('')
        self.display.SetFocus()

    def frac_to_decimal(self):
        """ convert feet-inch input to decimal feet"""
        s = self.display.GetValue()
        s.strip()
        if s.find("'") == -1:
            dec_ft = float(s)
        else:
            if s.find('/') == -1:
                ft_index = s.find("'")
                ft = int(s[:ft_index])
                inch = int(s[(ft_index+1):])
                dec_ft = ft + inch/12.0
            else:
                ft_index = s.find("'")
                in_index = s.find(' ')
                ft = int(s[:ft_index])
                inch = int(s[(ft_index+1):in_index])
                frac = float(Fraction(s[(in_index+1):]))
                dec_ft = ft + (inch + frac)/12
        return dec_ft

    def fraction_str(self, num):
        """ convert decimal ft to ft-in string"""
        ft_int = int(num)
        inch = (num - int(num))* 12
        inch_int = int(inch)
        frac = (inch - inch_int) * 16
        numerator = int(frac)
        if numerator == 0:
            frac_text = ""
        elif inch >= (11 + (15.4999/16)):
            ft_int = ft_int + 1
            inch_int = 0
            frac_text = ""
        elif numerator == 16:
            inch_int = inch_int + 1
            frac_text = ""
        else:
            denominator = 16
            while numerator % 2 == 0:
                numerator = numerator / 2
                denominator = denominator / 2
            frac_text = str(numerator) + '/' + str(denominator)
        frac_str = str(ft_int) + "' " + str(inch_int) + " " + frac_text
        return frac_str

    def conversion(self, event):
        self.updateDisplay()
                
        
        
                    
if __name__ == '__main__':
    calculator = wx.App(False)
    calc = MainFrame(None)
    calc.Show(True)
    calculator.MainLoop()
