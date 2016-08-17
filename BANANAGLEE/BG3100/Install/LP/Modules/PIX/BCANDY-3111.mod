Entry: EntryPoint
Name: Console
File: BCANDY-3111.exe
Version: 0x03010101
Priority: 1
ID: 0x60101
chain: 0x10000000
activate: cm_activate
deactivate: cm_deactivate 
install: cm_install
uninstall: cm_uninstall
MUNGE
Command: cm_add_to_buffer_handler
Command: cm_init_handler
Command: cm_close_handler


<interface>
<menu>

  <menuItem>    
    <itemText>Start console session</itemText>
    <miniProg>
      <progName>Console</progName>
      <handler>cm_add_to_buffer_handler</handler>
      <argList>
        <arg>--infile Cmds</arg>
      </argList>
      
    </miniProg>
  </menuItem>
  
 
</menu>
</interface>
