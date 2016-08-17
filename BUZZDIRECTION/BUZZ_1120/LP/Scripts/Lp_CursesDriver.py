import curses , traceback , os

class textBox:
    def __init__(self,text,row,col,maxC):
        self.dispText=text
        self.dispRow=row
        self.dispCol=col
        self.maxChars=maxC
        self.strPos=0

class CursesDriver:

    def __init__(self,variables,numVars,sT):
        try:    
            
            #Workaround for python curses library bug
            #Necessary to force curses to properly respond to SIGWINCH
            os.environ['LINES']=""
            del os.environ['LINES']
            os.environ['COLUMNS']=""
            del os.environ['COLUMNS']
        
            self.padPos=0
            self.padPosX=0
            
            #The variableValues list is used to keep track of variable names and current values that
            #have been entered.
            self.variableValues=[]
            
            #Second value list used to store arguments for second tunnel. 
            self.variableValues2=[]
            
            #List of textBox objects which keep track of cursor positions for each variable
            self.textBoxes=[]
            
            self.screen=curses.initscr()
            
            self.numVars=numVars
            self.longestVar=0
            (self.maxY,self.maxX)=self.screen.getmaxyx()
            self.neededRows=0
            self.neededCols=0
            self.padScreen=curses.newpad(1,1)
            self.screenType=sT
            if self.screenType=='default':
                self.__initDefaultScreen(variables,numVars)
            elif self.screenType=='redir':
                self.__initRedirScreen(variables,numVars)
            elif self.screenType=='out':
                self.__initOutScreen(variables,numVars)
            
            curses.cbreak()
            curses.noecho()
            self.screen.keypad(1)
            self.padScreen.keypad(1)
            self.rawVars=variables
            
        except AttributeError:
            self.screen.keypad(0)
            curses.echo()
            curses.nocbreak()
            curses.endwin()
            traceback.print_exc()    
    
    def __initRedirScreen(self,variables,numVars):    
        
        self.numVars=(self.numVars*2)+3
        self.textBoxes=["","","","","","","","","","","","","","","","","","","","",""]
        self.variableValues=["","","","","","","","","","",""]
        self.variableValues2=["","","","","","","","","","",""]
                  
        #The order dictionaries are used to synchronize the order of varibles in textBoxes and 
        #variableValues
             
                        #Position in 
                        #variableValues
                            #|
                            #V
        order1={'transprot':(0,3),'osrcip':(3,15),'odstip':(4,15),'osrcport':(5,5),
                'odstport':(6,5),'nsrcip':(7,15),'ndstip':(8,15),'nsrcport':(9,5),
                'ndstport':(10,5)}
                              #^
                              #|
                         #Max number of 
                         #chars for this
                         #variable
        
        order2={'nsrcip':(13,15),'ndstip':(14,15),'nsrcport':(15,5),'ndstport':(16,5),
                'osrcip':(17,15),'odstip':(18,15),'osrcport':(19,5),'odstport':(20,5)}
         
        self.textBoxes[1]=textBox('Create this Tunnel(Y/N)',2,25,1)
        self.variableValues[1]=('enable','Y')
        
        self.textBoxes[2]=textBox('Enable Persistence(Y/N)',3,25,1)
        self.variableValues[2]=('persist','N')
        
        self.textBoxes[11]=textBox('Create this Tunnel(Y/N)',2,67,1)
        self.variableValues2[1]=('enable','Y')
        
        self.textBoxes[12]=textBox('Enable Persistence(Y/N)',3,67,1)
        self.variableValues2[2]=('persist','N')

        for el in variables:
            try:
                index=order1[el[0]]
                if index[0]==0:
                    self.textBoxes[index[0]]=textBox(el[1],0,25,index[1])
                    self.variableValues[index[0]]=(el[0],"")
                elif index[0]>6:
                    self.textBoxes[index[0]]=textBox(el[1],index[0]+10,18,index[1])
                    self.variableValues[index[0]]=(el[0],"")
                else:
                    self.textBoxes[index[0]]=textBox(el[1],index[0]+4,18,index[1])
                    self.variableValues[index[0]]=(el[0],"")
            except KeyError:
                continue
        
        for el in variables:
            try:
                index=order2[el[0]]
                if index[0]>16:
                    self.textBoxes[index[0]]=textBox(el[1],(index[0]-10)+10,61,index[1])
                    self.variableValues2[index[0]-10]=(el[0],"")
                else:
                    self.textBoxes[index[0]]=textBox(el[1],(index[0]-10)+4,61,index[1])
                    self.variableValues2[index[0]-10]=(el[0],"")
            
            except KeyError:
                continue
        
        self.neededRows=25
        self.neededCols=80
        
        self.padScreen.resize(self.neededRows,self.neededCols)
        
        self.__drawRedirScreen(variables)
        
    def __drawRedirScreen(self,variables):
        try:
            self.padScreen.addstr(2,25,"Y")
            self.padScreen.addstr(3,25,"N")
            self.padScreen.addstr(2,67,"Y")
            self.padScreen.addstr(3,67,"N")
            self.padScreen.addstr(1,8,"----------------------------Attacker------------------------------")
            self.padScreen.addstr(4,19,"|")
            self.padScreen.addstr(5,19,"V")
            self.padScreen.addstr(4,62,"^")
            self.padScreen.addstr(5,62,"|")
            self.padScreen.addstr(6,5,"Attacker to Firewall Packet")
            self.padScreen.addstr(6,48,"Firewall to Attacker Packet")
            self.padScreen.addstr(11,19,"|")
            self.padScreen.addstr(12,19,"V")
            self.padScreen.addstr(11,62,"^")
            self.padScreen.addstr(12,62,"|")
            self.padScreen.addstr(13,8,"-----------------------------Firewall-----------------------------")
            self.padScreen.addstr(14,19,"|")
            self.padScreen.addstr(15,19,"V")
            self.padScreen.addstr(14,62,"^")
            self.padScreen.addstr(15,62,"|")
            self.padScreen.addstr(16,5,"Firewall to Target Packet")
            self.padScreen.addstr(16,48,"Target to Firewall Packet")
            for box in self.textBoxes:
                self.padScreen.addstr(box.dispRow,box.dispCol-(len(box.dispText)+2),(box.dispText+": "))

            self.padScreen.addstr(21,8,"-----------------------------Target------------------------------")
            self.padScreen.addstr(22,(self.neededCols/4),"Ctrl-G: Go    Ctrl-N: Clear Form")
            self.padScreen.addstr(23,(self.neededCols/4),"Ctrl-B: Back")
        
        except:
            self.screen.keypad(0)
            curses.echo()
            curses.nocbreak()
            curses.endwin()
            traceback.print_exc()    
            return []
        
    def __initOutScreen(self,variables,numVars):
        self.numVars=7
        self.textBoxes=["","","","","","",""]
        self.variableValues=["","","","","","",""]
    
                       #Position in 
                       #variableValues
                           #|
                           #| Row to draw this variable on.
                           #| | 
                           #V V    
        order={'transprot':(0,0,3),'odstip':(2,3,15),'odstport':(3,4,5),
               'nsrcip':(4,7,15), 'nsrcportstart':(5,8,5),'nsrcportend':(6,8,5)}
                               #^
                               #|
                          #Max number of 
                          #chars for this
                          #variable
        
        self.textBoxes[1]=textBox('Enable Persistence(Y/N)',1,25,1)
        self.variableValues[1]=('persist','N')
        
        for el in variables:
            try:
                index=order[el[0]]
                if index[0]==0:
                    self.textBoxes[index[0]]=textBox(el[1],index[1],25,index[2])
                    self.variableValues[index[0]]=(el[0],"")
                elif index[0]==5:
                    self.textBoxes[index[0]]=textBox(el[1],index[1],35,index[2])
                    self.variableValues[index[0]]=(el[0],"")
                elif index[0]==6:
                    self.textBoxes[index[0]]=textBox(el[1],index[1],45,index[2])
                    self.variableValues[index[0]]=(el[0],"")
                else:
                    self.textBoxes[index[0]]=textBox(el[1],index[1],24,index[2])
                    self.variableValues[index[0]]=(el[0],"")
            except KeyError:
                continue
        
        self.neededRows=22
        self.neededCols=80
        
        self.padScreen.resize(self.neededRows,self.neededCols)
        
        self.__drawOutScreen(variables)
        
    def __drawOutScreen(self,variables):
        try:
            
            self.padScreen.addstr(1,25,"N")
            self.padScreen.addstr(2,8,"-----------------------------------------------Server")
            self.padScreen.addstr(5,19,"^")
            self.padScreen.addstr(6,19,"|")
            self.padScreen.addstr(9,8,"----------------------------------------------Firewall")
            self.padScreen.addstr(11,10,"Dest IP  : IP address of interest.  Entered above.")
            self.padScreen.addstr(12,10,"Dest Port: Port of interest.  Entered above.")
            self.padScreen.addstr(13,19,"^")
            self.padScreen.addstr(14,19,"|")
            self.padScreen.addstr(15,10,"Src IP  : Any")
            self.padScreen.addstr(16,10,"Src Port: Any")
            for box in self.textBoxes:
                self.padScreen.addstr(box.dispRow,box.dispCol-(len(box.dispText)+2),(box.dispText+": "))
                 
            self.padScreen.addstr(18,8,"----------------------------------------------Client")
            self.padScreen.addstr(19,(self.neededCols/4),"Ctrl-G: Go    Ctrl-N: Clear Form")
            self.padScreen.addstr(20,(self.neededCols/4),"Ctrl-B: Back")
        
        except:
            self.screen.keypad(0)
            curses.echo()
            curses.nocbreak()
            curses.endwin()
            traceback.print_exc()    
            return []
        
    def __initDefaultScreen(self,variables,numVars):
    
        for el in variables:
            self.variableValues.append((el[0],""))
            if self.longestVar<len(el[1]):
                self.longestVar=len(el[1])
            
        currentRow=5
        for el in variables:
            self.textBoxes.append(textBox(el[1],currentRow,self.longestVar+8,22))
            currentRow+=1
                
        self.neededRows=numVars+6
        self.neededCols=self.longestVar+50
        
        self.padScreen.resize(self.neededRows,self.neededCols)
        
        self.__drawDefaultScreen(variables)
    
    def __drawDefaultScreen(self,variables):
        try:
            currentRow=5
                
            for el in variables:
                dots=""
                for i in range(0,self.longestVar-len(el[1])+5,1):
                    dots=dots+"."
                self.padScreen.addstr(currentRow,2,(el[1]+dots+"["))
                self.padScreen.addstr(currentRow,self.longestVar+30,("]"))
                currentRow+=1
                
            self.padScreen.addstr(2,(self.neededCols/4),"Ctrl-G: Go    Ctrl-N: Clear Form")
            self.padScreen.addstr(3,(self.neededCols/4),"Ctrl-B: Back")
        except:
            self.screen.keypad(0)
            curses.echo()
            curses.nocbreak()
            curses.endwin()
            traceback.print_exc()    
            return []
            
    def runCurses(self):
        try:
            activeIndex=0
                
            self.padScreen.move(self.textBoxes[0].dispRow,
                                self.textBoxes[0].dispCol+len(self.variableValues[0][1]))
              
            self.screen.refresh()                 
            self.padScreen.refresh(0,0,0,0,self.maxY-1,self.maxX-1)
            
            while 1:
                x=self.screen.getch()
                #self.padScreen.addstr(0,50,str(x))
                
                if x==curses.KEY_DOWN or x==9 or x==10:
                    if activeIndex<self.numVars-1:
                        activeIndex+=1
                    
                    #Scroll vertical if necessary
                    if self.textBoxes[activeIndex].dispRow>((self.padPos+self.maxY)-3):
                        self.padPos=self.padPos+((self.textBoxes[activeIndex].dispRow-(self.padPos+self.maxY))+3)
                    
                    elif self.textBoxes[activeIndex].dispRow<self.padPos:
                        if self.textBoxes[activeIndex].dispRow-3<0:
                            self.padPos=0
                        else:
                            self.padPos=self.textBoxes[activeIndex].dispRow-3
                    
                    if activeIndex<=10 or self.screenType=='default':
                        self.padScreen.move(self.textBoxes[activeIndex].dispRow,
                                            self.textBoxes[activeIndex].dispCol+len(self.variableValues[activeIndex][1]))

                        neededSpace=2+len(self.textBoxes[activeIndex].dispText)+len(self.variableValues[activeIndex][1])

                        self.textBoxes[activeIndex].strPos=len(self.variableValues[activeIndex][1])
                    else:
                        self.padScreen.move(self.textBoxes[activeIndex].dispRow,
                                            self.textBoxes[activeIndex].dispCol+len(self.variableValues2[activeIndex-10][1]))    

                        neededSpace=2+len(self.textBoxes[activeIndex].dispText)+len(self.variableValues2[activeIndex-10][1])

                        self.textBoxes[activeIndex].strPos=len(self.variableValues2[activeIndex-10][1])
                    
                    #Scroll horizontal if necessary
                    (y,xc)=self.padScreen.getyx()    
                    if xc>self.maxX-2:
                        if neededSpace>=self.maxX:
                            self.padPosX=(xc-self.maxX)+2
                        else:
                            self.padPosX=(xc-neededSpace)
                    else:
                        self.padPosX=0
                    
                    self.screen.redrawwin()
                    self.screen.refresh()
                    self.padScreen.refresh(self.padPos,self.padPosX,0,0,self.maxY-1,self.maxX-1)
                
                elif x==curses.KEY_UP:
                    if activeIndex>0:
                        activeIndex-=1
                    elif activeIndex==0:
                        if self.padPos>0:
                            self.padPos-=1
                            self.padScreen.refresh(self.padPos,0,0,0,self.maxY-1,self.maxX-1)
                    
                    #Scroll vertical if necessary
                    if self.textBoxes[activeIndex].dispRow<self.padPos:
                        if self.textBoxes[activeIndex].dispRow-3<0:
                            self.padPos=0
                        else:
                            self.padPos=self.textBoxes[activeIndex].dispRow-3
                    elif self.textBoxes[activeIndex].dispRow>((self.padPos+self.maxY)-3):
                        self.padPos=self.padPos+((self.textBoxes[activeIndex].dispRow-(self.padPos+self.maxY))+3)
                    
                    if activeIndex<=10 or self.screenType=='default':
                        self.padScreen.move(self.textBoxes[activeIndex].dispRow,
                                            self.textBoxes[activeIndex].dispCol+len(self.variableValues[activeIndex][1]))

                        neededSpace=2+len(self.textBoxes[activeIndex].dispText)+len(self.variableValues[activeIndex][1])
                        self.textBoxes[activeIndex].strPos=len(self.variableValues[activeIndex][1])
                    else:
                        self.padScreen.move(self.textBoxes[activeIndex].dispRow,
                                            self.textBoxes[activeIndex].dispCol+len(self.variableValues2[activeIndex-10][1]))
                        
                        neededSpace=2+len(self.textBoxes[activeIndex].dispText)+len(self.variableValues2[activeIndex-10][1])
                        self.textBoxes[activeIndex].strPos=len(self.variableValues2[activeIndex-10][1])
                    
                    #Scroll horizontal if necessary
                    (y,xc)=self.padScreen.getyx()    
                    if xc>self.maxX-2:    
                        if neededSpace>=self.maxX:
                            self.padPosX=(xc-self.maxX)+2
                        else:
                            self.padPosX=(xc-neededSpace)
                    else:
                        self.padPosX=0
                    
                    self.screen.redrawwin()
                    self.screen.refresh()
                    self.padScreen.refresh(self.padPos,self.padPosX,0,0,self.maxY-1,self.maxX-1)
                
                #Left arrow key
                elif x==curses.KEY_LEFT:
                    curY,curX=self.padScreen.getyx()
                    if curX>self.textBoxes[activeIndex].dispCol:
                        self.textBoxes[activeIndex].strPos-=1
                        self.padScreen.move(self.textBoxes[activeIndex].dispRow,curX-1)
                        self.padScreen.refresh(self.padPos,self.padPosX,0,0,self.maxY-1,self.maxX-1)
                    
                #Right arrow key
                elif x==curses.KEY_RIGHT:
                    curY,curX=self.padScreen.getyx()
                    
                    if activeIndex<=10 or self.screenType=='default':
                        varLength=len(self.variableValues[activeIndex][1])
                    else:
                        varLength=len(self.variableValues2[activeIndex-10][1])
                    
                    if curX<self.textBoxes[activeIndex].dispCol+varLength:
                        self.textBoxes[activeIndex].strPos+=1        
                        self.padScreen.move(self.textBoxes[activeIndex].dispRow,curX+1)
                        self.padScreen.refresh(self.padPos,self.padPosX,0,0,self.maxY-1,self.maxX-1)
                
                elif x==8 or x==263 or x==curses.KEY_BACKSPACE or x==127:
                    curY,curX=self.padScreen.getyx()
                    
                    if curX==self.padPosX:
                        self.padPosX-=1
                    
                    if activeIndex<=10 or self.screenType=='default':
                        varLength=len(self.variableValues[activeIndex][1])
                    else:
                        varLength=len(self.variableValues2[activeIndex-10][1])
                    
                    if varLength>0 and curX>self.textBoxes[activeIndex].dispCol:
                        self.padScreen.move(curY,curX-1)
                        self.padScreen.delch()
                        
                        self.textBoxes[activeIndex].strPos-=1
                        strPos=self.textBoxes[activeIndex].strPos
                        if activeIndex<=10 or self.screenType=='default':
                            newStr=self.variableValues[activeIndex][1]
                            newElement=(self.variableValues[activeIndex][0],(newStr[:strPos]+newStr[strPos+1:]))
                            self.variableValues[activeIndex]=newElement
                        else:
                            newStr=self.variableValues2[activeIndex-10][1]
                            newElement=(self.variableValues2[activeIndex-10][0],(newStr[:strPos]+newStr[strPos+1:]))
                            self.variableValues2[activeIndex-10]=newElement
                        
                        self.padScreen.move(curY,self.textBoxes[activeIndex].dispCol+self.textBoxes[activeIndex].maxChars)
                        self.padScreen.insch(" ")
                        self.padScreen.move(curY,curX-1)
                        self.padScreen.refresh(self.padPos,self.padPosX,0,0,self.maxY-1,self.maxX-1)
                
                elif x==10 or x==curses.KEY_ENTER:
                    continue
                
                #ctrl-g
                elif x==7:
                    toReturn1=[]
                    toReturn2=[]
                    
                    self.screen.keypad(0)
                    self.padScreen.clear()
                    self.screen.clear()
                    curses.echo()
                    curses.nocbreak()
                    curses.endwin()
                    
                    if self.screenType=='redir':
                        #Check if the left tunnel should be created
                        if self.variableValues[1][1]=='y' or self.variableValues[1][1]=='Y':
                            toReturn1=self.variableValues[3:]
                            toReturn1.append(self.variableValues[0])
                        
                            if self.variableValues[2][1]=='y' or self.variableValues[2][1]=='Y':
                                toReturn1.append(('persist','1'))
                            elif self.variableValues[2][1]=='n' or self.variableValues[2][1]=='N':
                                toReturn1.append(('persist','0'))
                                
                        #Check if the right tunnel should be created
                        if self.variableValues2[1][1]=='y' or self.variableValues2[1][1]=='Y':
                            toReturn2=self.variableValues2[3:]
                            toReturn2.append(self.variableValues[0])
                            
                            if self.variableValues2[2][1]=='y' or self.variableValues2[2][1]=='Y':
                                toReturn2.append(('persist','1'))
                            elif self.variableValues2[2][1]=='n' or self.variableValues2[2][1]=='N':
                                toReturn2.append(('persist','0'))
                    
                        return (toReturn1,toReturn2)    
                        
                    elif self.screenType=='out':
                        toReturn=self.variableValues[2:]
                        toReturn.append(self.variableValues[0])
                        
                        if self.variableValues[1][1]=='y' or self.variableValues[1][1]=='Y':
                            toReturn.append(('persist','1'))
                        elif self.variableValues[1][1]=='n' or self.variableValues[1][1]=='N':
                            toReturn.append(('persist','0'))

                        return (toReturn,[])
                    
                    else:
                        return (self.variableValues,[])
                
                #crtl-b
                elif x==2:
                    self.screen.keypad(0)
                    self.padScreen.clear()
                    self.screen.clear()
                    curses.echo()
                    curses.nocbreak()
                    curses.endwin()
                    return ([],[])
                
                #crtl-n
                elif x==14:
                    for i in range(0,len(self.variableValues),1):
                        self.variableValues[i]=(self.variableValues[i][0],"")
                        
                    if self.screenType=='redir':
                        for i in range(1,len(self.variableValues2),1):
                            self.variableValues2[i]=(self.variableValues2[i][0],"")
                            
                        self.variableValues[1]=('enable','Y')        
                        self.variableValues[2]=('persist','N')
        
                        self.variableValues2[1]=('enable','Y')    
                        self.variableValues2[2]=('persist','N')
                        
                    elif self.screenType=='out':
                        self.variableValues[1]=('persist','N')        
                        self.variableValues[5]=('nsrcportstart','')        
                        self.variableValues[6]=('nsrcportend','')
                    
                    activeIndex=0
                    self.padScreen.erase()
                    self.__screenReset()
                    
                #window resized
                elif x==curses.KEY_RESIZE or x<0:    
                    (self.maxY,self.maxX)=self.screen.getmaxyx()
                    activeIndex=0
                    self.padScreen.move(self.textBoxes[0].dispRow,
                                        self.textBoxes[0].dispCol+len(self.variableValues[0][1]))
                    self.padScreen.refresh(self.padPos,self.padPosX,0,0,self.maxY-1,self.maxX-1)
                            
                else:
                    
                    self.padScreen.refresh(self.padPos,self.padPosX,0,0,self.maxY-1,self.maxX-1)
                    if activeIndex<=10 or self.screenType=='default':
                        varLength=len(self.variableValues[activeIndex][1])
                    else:
                        varLength=len(self.variableValues2[activeIndex-10][1])
                    
                    if varLength<self.textBoxes[activeIndex].maxChars and x<256 and x>0:
                        
                        curY,curX=self.padScreen.getyx()
                        if curX-self.textBoxes[activeIndex].dispCol<varLength:
                            self.padScreen.move(curY,self.textBoxes[activeIndex].dispCol+self.textBoxes[activeIndex].maxChars)
                            self.padScreen.delch()
                            self.padScreen.move(curY,curX)
                            self.padScreen.insch(chr(x))
                            self.padScreen.move(curY,curX+1)
                        else:
                            self.padScreen.addch(chr(x))
                        
                        curPos=self.textBoxes[activeIndex].strPos
                        self.textBoxes[activeIndex].strPos+=1
                        
                        
                        if activeIndex<=10 or self.screenType=='default':
                            newElement=(self.variableValues[activeIndex][0],
                                       (self.variableValues[activeIndex][1][:curPos]+chr(x)+
                                         self.variableValues[activeIndex][1][curPos:])
                                       )
                            self.variableValues[activeIndex]=newElement
                        else:
                            newElement=(self.variableValues2[activeIndex-10][0],
                                       (self.variableValues2[activeIndex-10][1][:curPos]+
                                        chr(x)+self.variableValues2[activeIndex-10][1][curPos:])
                                       )

                            self.variableValues2[activeIndex-10]=newElement
                        
                        (y,xc)=self.padScreen.getyx()    
                        if xc>=self.padPosX+self.maxX:
                            self.padPosX+=1
                        
                        self.padScreen.refresh(self.padPos,self.padPosX,0,0,self.maxY-1,self.maxX-1)
                    
            self.screen.keypad(0)
            self.padScreen.clear()
            self.screen.clear()
            curses.echo()
            curses.nocbreak()
            curses.endwin()
            return self.variableValues
        except:
            self.screen.keypad(0)
            curses.echo()
            curses.nocbreak()
            curses.endwin()
            traceback.print_exc()
            return ([],[])
            
            
    def __screenReset(self):
        
        if self.screenType=='default':
            self.__drawDefaultScreen(self.rawVars)
        elif self.screenType=='redir':
            self.__drawRedirScreen(self.rawVars)
        elif self.screenType=='out':
            self.__drawOutScreen(self.rawVars)
            
        self.padScreen.move(self.textBoxes[0].dispRow,
                            self.textBoxes[0].dispCol+len(self.variableValues[0][1]))
        
        self.padScreen.refresh(self.padPos,self.padPosX,0,0,self.maxY-1,self.maxX-1)
