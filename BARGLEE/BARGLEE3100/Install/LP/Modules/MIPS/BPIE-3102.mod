File: BPIE-3102.exe
Name: ProfilerIpv4
Version: 0x03010002
Priority: 20
ID: 0x30301
Install: installHandler
Activate: activateHandler
Deactivate: deactivateHandler
Uninstall: uninstallHandler
Chain: 0x30000000
Entry: packetHandler
getconfig: getconfigHandler
reconfigure: reconfigureHandler
persistence: full
Command: startCmdHandler
Command: statusCmdHandler
Command: stopCmdHandler
Command: resetCmdHandler
Command: getIpCmdHandler
Command: getIpIpCmdHandler
Command: getTimeSlotCmdHandler

<interface>
<menu>

  <menuItem>
    <itemText>Start Profiler</itemText>
    <queryList>
      <query>Interface number (def=0xffffffff => any)</query>
      <query>BPF file or string (def=no filter)</query>
      <query>BPF description (def=no description)</query>
      <query>Time limit (seconds; def=0 => no limit)</query>
      <query>Maximum IP entries to store</query>
      <query>Maximum percent of memory for IP entries</query>
      <query>Maximum IP-to-IP entries to store</query>
      <query>Maximum percent of memory for IP-to-IP entries</query>
      <query>Condense IP ports (0 => no; def=1 => yes)</query>
      <query>Do Time Slot scan (0 => no; def=1 => yes)</query>
    </queryList>

    <miniProg>
      <progName>profilerIpv4</progName>
      <handler>startCmdHandler</handler>
      <argList>
        <arg>--interface</arg>
        <arg>--filterFile</arg>
        <arg>--filterDesc</arg>
        <arg>--timeLimit</arg>
        <arg>--maxIp</arg>
        <arg>--maxIpPercent</arg>
        <arg>--maxIpToIp</arg>
        <arg>--maxIpToIpPercent</arg>
        <arg>--portCondense</arg>
        <arg>--timeSlotScan</arg>
        <arg>--name start</arg>
      </argList>
    </miniProg>
  </menuItem>

  <menuItem>
    <itemText>Get Profiler Status</itemText>

    <miniProg>
      <progName>profilerIpv4</progName>
      <handler>statusCmdHandler</handler>
      <argList>
        <arg>--name status</arg>
      </argList>
    </miniProg>
  </menuItem>

  <menuItem>
    <itemText>Stop Profiler</itemText>

    <miniProg>
      <progName>profilerIpv4</progName>
      <handler>stopCmdHandler</handler>
      <argList>
        <arg>--name stop</arg>
      </argList>
    </miniProg>
  </menuItem>

  <menuItem>
    <itemText>Reset Profiler</itemText>

    <miniProg>
      <progName>profilerIpv4</progName>
      <handler>resetCmdHandler</handler>
      <argList>
        <arg>--name reset</arg>
      </argList>
    </miniProg>
  </menuItem>

  <menuItem>
    <itemText>Get IP Profiler Information</itemText>
    <queryList>
        <query>Enter the name of the local file in which to store the read data:</query>
    </queryList>

    <miniProg>
      <progName>profilerIpv4</progName>
      <handler>getIpCmdHandler</handler>
      <argList>
        <arg>--outfile</arg>
        <arg>--name getip</arg>
      </argList>
    </miniProg>
  </menuItem>

  <menuItem>
    <itemText>Get IP-to-IP Profiler Information</itemText>
    <queryList>
        <query>Enter the name of the local file in which to store the read data:</query>
    </queryList>

    <miniProg>
      <progName>profilerIpv4</progName>
      <handler>getIpIpCmdHandler</handler>
      <argList>
        <arg>--outfile</arg>
        <arg>--name getipip</arg>
      </argList>
    </miniProg>
  </menuItem>

  <menuItem>
    <itemText>Get Time Slot Information</itemText>
    <queryList>
        <query>Enter the name of the local file in which to store the read data:</query>
    </queryList>

    <miniProg>
      <progName>profilerIpv4</progName>
      <handler>getTimeSlotCmdHandler</handler>
      <argList>
        <arg>--outfile</arg>
        <arg>--name gettimeslot</arg>
      </argList>
    </miniProg>
  </menuItem>

</menu>
</interface>

