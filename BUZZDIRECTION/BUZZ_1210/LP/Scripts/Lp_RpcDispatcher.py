#!/usr/bin/env python

#This class handles RPC callbacks for the Core module functions load, unload,
#burn, and upgrade.  It receives tasking by binding to the RPC_DISPATCH_PORT
#defined in Lp_Defines and waiting for commands.  RPC callbacks are
#registered when the class receives a message containing the string SEND.  When
#this occurs, it parses out any necessary arguments and adds an entry to the
#rpcActions dictionary containing the function to call for this callback as well
#as any necessary arguments.  The key for this dictionary entry is the rpc
#number.  When the class receives a message with the RECV string, it parses out
#the rpc number and executes the function defined for that callback.  The class
#also provides several other useful services by receiving the following
#messages:
#
# !!#TURN_OFF_PRINTING:  This command will prevent the class from printing the
    # RPC RECV confirmation until a !!#TURN_ON_PRINTING is received
# !!#TURN_ON_PRINTING:   This command will cause the class to print the RPC
    # confirmations.
# !!#REG_BLOCK<rpc num>:   This command will register a block for a given rpc
    # number.  This command is used when the LP needs to wait for an rpc to
    # complete before allowing the user to perform any other actions.  When an rpc
    # confirmation for the registered rpc is received, an END message is sent to
    # the LP BLOCKER_PORT.  After registering a block, the LP will listen on the
    # BLOCKER_PORT until the END string arrives.
# !!#QUIT:   This command is used to stop the RPC dispatcher.
#
#****************************************************************************

import threading
import Lp_UserInterface
import socket
import sys

class RpcDispatcher(threading.Thread):
    def __init__(self, processor):
        self.sock=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(('127.0.0.1',Lp_UserInterface.RPC_DISPATCH_PORT))
        self.rpcActions={}
        self.unhandledRpcs={}
        self.proc=processor
        self.enablePrinting=0
        self.lastRpcString=''
        threading.Thread.__init__(self)
        
    def run(self):
        while 1:
            input = self.sock.recv(1024)

            if input.find("SEND")>=0:
                storeRpc=1
                
                #register the rpc action
                id = input[4:input.find(',')]
                
                #see if this send matches an unhandled rpc
                if id in self.unhandledRpcs:
                    storeRpc=0
                    
                function = input[input.find(',')+1:input.find(':')]
                if function == 'Core.load':
                    file = input[input.find(':')+1:]
                    if storeRpc == 1:
                        self.rpcActions[id]=(self.doLoadCallback,[file], id)
                    else:
                        self.doLoadCallback([file],id,self.unhandledRpcs[id])

                elif function == 'Core.unload':
                    iface = input[input.find(':')+1:]
                    if storeRpc == 1:
                        self.rpcActions[id]=(self.doUnloadCallback,[iface], id)
                    else:
                        self.doUnloadCallback(iface,id,self.unhandledRpcs[id])

                elif function == 'Core.uninstallForever':
                    if storeRpc == 1:
                        self.rpcActions[id]=(self.doBurnCallback,[], id)
                    else:
                        self.doBurnCallback([],id,self.unhandledRpcs[id])

                elif function == 'Core.upgrade':
                    if storeRpc == 1:
                        self.rpcActions[id]=(self.doUpgradeCallback,[], id)
                    else:
                        self.doUpgradeCallback([],id,self.unhandledRpcs[id])

            elif input.find("RECV")>=0:
                self.lastRpcString = input
                
                #perform the rpc action, if there is a registered action
                id=input[input.find('#')+1:input.find(',')]
                retCode = input[input.find('rc=')+3:len(input)-1]
                if self.enablePrinting ==1:
                    print input,
                    print '\rLP> ',
                    sys.stdout.flush()

                #we previously got a send with this id and an action was
                #registered
                if id in self.rpcActions and self.rpcActions[id][0] != 0:
                    self.rpcActions[id][0](self.rpcActions[id][1],
                                           self.rpcActions[id][2], retCode)
                    del self.rpcActions[id]
                #we previously got a send with this id but no action was
                #registered
                elif id in self.rpcActions and self.rpcActions[id][0] == 0:
                    del self.rpcActions[id]
                #we have never recevied a send with this id
                else:
                    self.unhandledRpcs[id] = retCode
                    

            elif input.find("!!#QUIT")>=0:
                self.sock.close()
                break
            elif input.find("!!#TURN_ON_PRINTING")>=0:
                self.enablePrinting = 1
            elif input.find("!!#TURN_OFF_PRINTING")>=0:
                self.enablePrinting = 0
            elif input.find('!!#REG_BLOCK')>=0:
                rpcId = input[12:]
                if rpcId in self.unhandledRpcs:
                    self.endBlock([],0,0)
                    del self.unhandledRpcs[rpcId]
                else:
                    self.rpcActions[rpcId] = (self.endBlock,[],rpcId)

    def endBlock(self,emptyList,rpc, retCode):
        self.sock.sendto("END",('127.0.0.1',Lp_UserInterface.BLOCKER_PORT))
            
    def doLoadCallback(self,modfile,rpc, retCode):
        if retCode == '0':
            self.proc.parseXml(modfile[0],1)
        
    def doUnloadCallback(self,iface,rpc, retCode):
        if retCode == '0':
            self.proc.deleteMod(iface,0)
        
    def doBurnCallback(self,emptyList,rpc, retCode):
        self.sock.sendto(self.lastRpcString,('127.0.0.1',Lp_UserInterface.FRONTEND_PORT))
        
    def doUpgradeCallback(self,emptyList,rpc, retCode):
        self.sock.sendto(self.lastRpcString,('127.0.0.1',Lp_UserInterface.FRONTEND_PORT))

