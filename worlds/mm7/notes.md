## AP Custom Flags — $7E1800-$7E180F
Confirmed free: $7E1800-$7E1D8F (verified unused across 2 stages)
Claiming $7E1800-$7E180F for AP integration.

$7E1800 — Boss check flags
  bit 0 = Freeze Man checked
  bit 1 = Burst Man checked
  bit 2 = Cloud Man checked
  bit 3 = Junk Man checked
  bit 4 = Slash Man checked
  bit 5 = Spring Man checked
  bit 6 = Shade Man checked
  bit 7 = Turbo Man checked

$7E1801 — Wily stage check flags
  bit 0 = Wily 1 checked
  bit 1 = Wily 2 checked
  bit 2 = Wily 3 checked
  bit 3 = Wily 4 checked

$7E1802 — Shop check flags
  bit 0-5 = shop slots 1-6

$7E1803 — AP item receive ID (low byte)
$7E1804 — AP item receive ID (high byte)
$7E1805 — AP execute flag (1 = give item, 0 = idle)
$7E1806 — Items received index (low byte)
$7E1807 — Items received index (high byte)
$7E1808 — AP connection state
$7E1809-$7E180F — Reserved for future use


## Free ROM Space (confirmed)
PRG ROM offsets: $007BA0-$007FFF  
CPU addresses:   $C07BA0-$C07FFF  
Size: ~1114 bytes — all usable

Planned layout:
$C07BA0  boss death hook        (~32 bytes)
$C07BC0  item receive routine   (~64 bytes)
$C07C00  shop check routine     (~32 bytes)
$C07C20  item notification      (~48 bytes)
$C07C50  reserved/future        (remaining ~700 bytes)


New game
--------sub start--------
C00BE8  A9 02          LDA #$02
C00BEA  85 DF          STA $DF
C00BEC  9C 78 0B       STZ $0B78 <--- Protoman
C00BEF  9C B1 0B       STZ $0BB1 <--- Mega Items
C00BF2  A9 02          LDA #$02 
C00BF4  8D 81 0B       STA $0B81 <-- Lives
C00BF7  A9 FE          LDA #$FE
C00BF9  1C 77 0B       TRB $0B77 
C00BFC  A9 80          LDA #$80
C00BFE  8D 9B 0B       STA $0B9B <--- Rush Coil
C00C01  AD 76 0B       LDA $0B76
C00C04  F0 05          BEQ $C00C0B
C00C06  A9 04          LDA #$04
C00C08  85 DF          STA $DF
C00C0A  60             RTS
----------------

--------sub start--------
C00C1E  A9 04          LDA #$04
C00C20  85 DF          STA $DF
C00C22  A9 01          LDA #$01
C00C24  8D 79 0B       STA $0B79 <--- ???
C00C27  9C 7A 0B       STZ $0B7A <--- Robot Museum Flag
C00C2A  9C 7B 0B       STZ $0B7B <--- New stages introduction flag
C00C2D  9C 7C 0B       STZ $0B7C <--- Wily flag
C00C30  9C A0 0B       STZ $0BA0 <--- Etanks
C00C33  9C A1 0B       STZ $0BA1 <--- WTanks
C00C36  9C A2 0B       STZ $0BA2 <--- STanks
C00C39  9C A3 0B       STZ $0BA3 <--- Beat
C00C3C  9C A4 0B       STZ $0BA4 <--- Items
C00C3F  9C 77 0B       STZ $0B77 <--- Shop flags
C00C42  9C A6 0B       STZ $0BA6 <--- Bolts
C00C45  9C A7 0B       STZ $0BA7 <--- Bolts x 256
C00C48  60             RTS
----------------


Getting a 1up
C25655  20 80 57       JSR $5780
C25658  20 74 57       JSR $5774
C2565B  90 18          BCC $C25675
C2565D  AD 81 0B       LDA $0B81
C25660  C9 09          CMP #$09
C25662  B0 09          BCS $C2566D
C25664  EE 81 0B       INC $0B81
C25667  A9 12          LDA #$12
C25669  22 05 32 C0    JSL $C03205
C2566D  20 E5 56       JSR $56E5
C25670  22 EF 08 C1    JSL $C108EF
C25674  60             RTS
----------------
--------sub start--------
C25780  22 01 03 C1    JSL $C10301
C25784  A5 25          LDA $25
C25786  29 02          AND #$02
C25788  D0 06          BNE $C25790
C2578A  A9 02          LDA #$02
C2578C  85 02          STA $02
C2578E  85 29          STA $29
C25790  60             RTS
----------------
--------sub start--------
C25774  C2 10          REP #$10
C25776  A2 00 0C       LDX #$0C00
C25779  22 71 03 C3    JSL $C30371
C2577D  E2 10          SEP #$10
C2577F  60             RTS
----------------




Hitting a boss
C304E4  A9 18          LDA #$18
C304E6  22 DA 31 C0    JSL $C031DA
C304EA  A5 2E          LDA $2E
C304EC  38             SEC
C304ED  ED 1C 00       SBC $001C
C304F0  85 2E          STA $2E
C304F2  F0 04          BEQ $C304F8
C304F4  10 09          BPL $C304FF
C304F6  64 2E          STZ $2E
C304F8  FE 36 00       INC $0036,X
C304FB  A9 FF          LDA #$FF
C304FD  18             CLC
C304FE  60             RTS
                     ----------------








Stage clear/Getting a weapon
C00D08  20 40 0E       JSR $0E40
C00D0B  AD CB 0B       LDA $0BCB
C00D0E  F0 0B          BEQ $C00D1B
C00D10  A9 06          LDA #$06
C00D12  85 E1          STA $E1
C00D14  64 E2          STZ $E2
C00D16  A9 3C          LDA #$3C
C00D18  85 E3          STA $E3
C00D1A  60             RTS
                     ----------------
C00D1B  AD DB 0B       LDA $0BDB
C00D1E  F0 06          BEQ $C00D26
C00D20  A9 04          LDA #$04
C00D22  85 E1          STA $E1
C00D24  64 E2          STZ $E2
C00D26  60             RTS
                     ----------------
C00D27  20 40 0E       JSR $0E40
C00D2A  A5 E2          LDA $E2
C00D2C  D0 14          BNE $C00D42
C00D2E  AD DB 0B       LDA $0BDB
C00D31  10 0E          BPL $C00D41
C00D33  E6 E2          INC $E2
C00D35  A2 02          LDX #$02
C00D37  A0 01          LDY #$01
C00D39  20 69 39       JSR $3969
C00D3C  A0 08          LDY #$08
C00D3E  20 AB 31       JSR $31AB
C00D41  60             RTS
                     ----------------
C00D42  AD AD 00       LDA $00AD
C00D45  29 0F          AND #$0F
C00D47  D0 0F          BNE $C00D58
C00D49  22 9D 07 C0    JSL $C0079D
C00D4D  20 70 01       JSR $0170
C00D50  A9 04          LDA #$04
C00D52  85 E0          STA $E0
C00D54  64 E1          STZ $E1
C00D56  64 E2          STZ $E2
C00D58  60             RTS
                     ----------------
C00D59  A5 E3          LDA $E3
C00D5B  F0 03          BEQ $C00D60
C00D5D  C6 E3          DEC $E3
C00D5F  60             RTS
                     ----------------
C00D60  20 40 0E       JSR $0E40
C00D63  A5 E2          LDA $E2
C00D65  D0 14          BNE $C00D7B
C00D67  AD CB 0B       LDA $0BCB
C00D6A  10 22          BPL $C00D8E
C00D6C  A2 02          LDX #$02
C00D6E  A0 01          LDY #$01
C00D70  20 69 39       JSR $3969
C00D73  E6 E2          INC $E2
C00D75  A0 08          LDY #$08
C00D77  20 AB 31       JSR $31AB
C00D7A  60             RTS
                     ----------------
C00D7B  A5 AD          LDA $AD
C00D7D  10 0F          BPL $C00D8E
C00D7F  22 9D 07 C0    JSL $C0079D
C00D83  20 70 01       JSR $0170
C00D86  A9 06          LDA #$06
C00D88  85 E0          STA $E0
C00D8A  64 E1          STZ $E1
C00D8C  64 E2          STZ $E2
C00D8E  60             RTS
                     ----------------
C00D8F  AD 3F 21       LDA $213F
C00D92  29 10          AND #$10
C00D94  F0 07          BEQ $C00D9D
C00D96  9C 00 42       STZ $4200
C00D99  5C 06 00 C0    JML $C00006
C00D9D  64 E0          STZ $E0
C00D9F  64 E1          STZ $E1
C00DA1  64 E2          STZ $E2
C00DA3  AD 73 0B       LDA $0B73
C00DA6  D0 0A          BNE $C00DB2
C00DA8  9C 79 0B       STZ $0B79
C00DAB  A9 04          LDA #$04
C00DAD  85 DF          STA $DF
C00DAF  4C 39 67       JMP $6739
C00DB2  C9 09          CMP #$09
C00DB4  F0 1C          BEQ $C00DD2
C00DB6  C9 0A          CMP #$0A
C00DB8  B0 3E          BCS $C00DF8
C00DBA  0A             ASL
C00DBB  AA             TAX
C00DBC  BD 83 0B       LDA $0B83,X
C00DBF  30 1B          BMI $C00DDC
C00DC1  A9 00          LDA #$00
C00DC3  20 30 5B       JSR $5B30
C00DC6  AD 73 0B       LDA $0B73
C00DC9  0A             ASL        
C00DCA  AA             TAX
C00DCB  A9 80          LDA #$80
C00DCD  9D 83 0B       STA $0B83,X  <------
C00DD0  80 0A          BRA $C00DDC






000BB1
bits
1 = junk man mega bolt
2 = turbo man mega bolt
3 = shade man mega bolt
4 = cloud man mega bolt
5 = mega health capsule
6 = spring man mega bolt
7 = ?
8 = ?






--Rules--
rush_r_plate_loc: burst_man_access
rush_u_plate_loc: cloud_man_access && (Rush Coil || Rush Jet || Super Adapter)
rush_s_plate_loc: junk_man_access && freeze_cracker
rush_h_plate_loc: freeze_man_access && (rush_coil || rush_jet || super_adapter)
hyper_bolt_loc: spring_man_access
exit_unit_loc: (freeze_man_access && rush_search) || shop_access
hyper_rocket_buster_loc: (turbo_man_access && super_adapter && rush_search) || (shop_access && hyper_bolt)
energy_balancer_loc: (shade_man_access && rush_search) || (shop_access && hyper_bolt)
beat_loc: slash_man_access && scorch_wheel
proto_man_cloud_man: cloud_man_access && (rush_coil || rush_jet || super_adapter)
proto_man_turbo_man: turbo_man_access
proto_shield_loc: shade_man_access && proto_man_cloud_man && proto_man_turbo_man

rush_search_loc: freeze_man_access || (shop_access && hyper_bolt)
rush_jet_loc: (junk_man_access && (thunder_bolt || rush_coil || rush_jet || super_adapter)) || (shop_access && hyper_bolt)

mega_bolt_cloud_man_loc: cloud_man_access && rush_search
mega_bolt_spring_man_loc: spring_man_access && rush_search
mega_bolt_shade_man_loc: shade_man_access && rush_search
mega_bolt_turbo_man_loc: turbo_man_access && rush_search
mega_bolt_junk_man_loc: junk_man_access && freeze_cracker && rush_search
mega_health_capsule_loc: spring_man_access && rush_search
