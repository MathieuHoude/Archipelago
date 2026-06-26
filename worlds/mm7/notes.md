## AP Custom Flags — $7E1800-$7E180F
TODO:
Stage entry / boss intro skip still uses vanilla weapon ownership.
Need to patch stage-entry cleared check to use !AP_BOSS_FLAGS.
Stage exit should check the medals
Stage exit always possible option
Items location should still spawn even if we got the item
Also call AP_UpdateWilyUnlock when returning from the shop/stage-select init,


## Free ROM Space (confirmed)
PRG ROM offsets: $007BA0-$007FFF  
CPU addresses:   $C07BA0-$C07FFF  
Size: ~1114 bytes — all usable


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
C00C0B  C2 20          REP #$20
C00C0D  A2 1C          LDX #$1C
C00C0F  9E 82 0B       STZ $0B82,X
C00C12  CA             DEX
C00C13  CA             DEX
C00C14  10 F9          BPL $C00C0F
C00C16  E2 20          SEP #$20
C00C18  A9 80          LDA #$80
C00C1A  8D 9B 0B       STA $0B9B <--- Rush Coil
C00C1D  60             RTS
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
C00C49  20 68 3D       JSR $3D68
C00C4C  9C B0 0B       STZ $0BB0
C00C4F  AD 79 0B       LDA $0B79
C00C52  F0 05          BEQ $C00C59
C00C54  9C 73 0B       STZ $0B73
C00C57  80 28          BRA $C00C81







Getting a 1up
C25655  20 80 57       JSR $5780
C25658  20 74 57       JSR $5774
C2565B  90 18          BCC $C25675
C2565D  AD 81 0B       LDA $0B81
C25660  C9 09          CMP #$09
C25662  B0 09          BCS $C2566D
C25664  EE 81 0B       INC $0B81 <--- Lives
C25667  A9 12          LDA #$12
C25669  22 05 32 C0    JSL $C03205 <--- Sound Effect Routine
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



-----Stage Selection Routine-----(8 stages?)
--------sub start--------
C034CC  22 17 3C C0    JSL $C03C17
C034D0  20 1C 38       JSR $381C
C034D3  AD A6 00       LDA $00A6
C034D6  29 50          AND #$50
C034D8  F0 17          BEQ $C034F1
C034DA  20 0E 38       JSR $380E
C034DD  F0 12          BEQ $C034F1
C034DF  8D 73 0B       STA $0B73 <--- StageID
C034E2  A9 0A          LDA #$0A
C034E4  85 01          STA $01
C034E6  A0 08          LDY #$08
C034E8  20 AB 31       JSR $31AB

--------sub start--------
C0380E  A5 07          LDA $07
C03810  0A             ASL
C03811  18             CLC
C03812  65 07          ADC $07
C03814  18             CLC
C03815  65 04          ADC $04
C03817  AA             TAX
C03818  BD 24 93       LDA $9324,X
C0381B  60             RTS
----------------
--------sub start--------
C0381C  A5 04          LDA $04
C0381E  85 1F          STA $1F
C03820  A5 07          LDA $07
C03822  85 21          STA $21
C03824  AD A6 00       LDA $00A6
C03827  89 08          BIT #$08
C03829  F0 02          BEQ $C0382D
C0382B  C6 07          DEC $07
C0382D  89 04          BIT #$04
C0382F  F0 02          BEQ $C03833
C03831  E6 07          INC $07
C03833  89 02          BIT #$02
C03835  F0 02          BEQ $C03839
C03837  C6 04          DEC $04
C03839  89 01          BIT #$01
C0383B  F0 02          BEQ $C0383F
C0383D  E6 04          INC $04
C0383F  A5 04          LDA $04
C03841  10 04          BPL $C03847
C03843  A9 00          LDA #$00
C03845  80 06          BRA $C0384D
C03847  C9 03          CMP #$03
C03849  90 04          BCC $C0384F
C0384B  A9 02          LDA #$02
C0384D  85 04          STA $04
C0384F  A5 07          LDA $07
C03851  10 04          BPL $C03857
C03853  A9 00          LDA #$00
C03855  80 06          BRA $C0385D
C03857  C9 03          CMP #$03
C03859  90 04          BCC $C0385F
C0385B  A9 02          LDA #$02
C0385D  85 07          STA $07
C0385F  A5 04          LDA $04
C03861  C5 1F          CMP $1F
C03863  D0 06          BNE $C0386B
C03865  A5 07          LDA $07
C03867  C5 21          CMP $21
C03869  F0 06          BEQ $C03871
C0386B  A9 14          LDA #$14
C0386D  22 05 32 C0    JSL $C03205
C03871  A6 04          LDX $04
C03873  BD 1E 93       LDA $931E,X
C03876  85 05          STA $05
C03878  A6 07          LDX $07
C0387A  BD 21 93       LDA $9321,X
C0387D  85 08          STA $08
C0387F  60             RTS
----------------








Spawn Boss Routine?
                     --------sub start--------
C286E0  22 39 0C C3    JSL $C30C39
C286E4  A5 34          LDA $34
C286E6  04 14          TSB $14
C286E8  A6 01          LDX $01
C286EA  FC B9 87       JSR ($87B9,X)
C286ED  AD 73 0B       LDA $0B73
C286F0  C9 09          CMP #$09
C286F2  B0 08          BCS $C286FC
C286F4  0A             ASL
C286F5  AA             TAX
C286F6  BD 83 0B       LDA $0B83,X
C286F9  10 01          BPL $C286FC
C286FB  60             RTS
                     ----------------
C286FC  A5 01          LDA $01
C286FE  C9 06          CMP #$06
C28700  D0 01          BNE $C28703
C28702  60             RTS
                     ----------------



                     --------sub start--------
C30353  A9 09          LDA #$09
C30355  CD 73 0B       CMP $0B73
C30358  90 16          BCC $C30370
C3035A  AD 73 0B       LDA $0B73
C3035D  0A             ASL
C3035E  AA             TAX
C3035F  BD 83 0B       LDA $0B83,X
C30362  18             CLC
C30363  10 0B          BPL $C30370
C30365  A9 10          LDA #$10
C30367  22 4E 0E C3    JSL $C30E4E
C3036B  22 EF 08 C1    JSL $C108EF
C3036F  38             SEC
C30370  6B             RTL
                     ----------------












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







cp Megaman\ VII\ \(USA\).sfc build/mm7_clean.sfc &&
cp Megaman\ VII\ \(USA\).sfc build/mm7_patched.sfc &&
python src/patch_mm7base.py

zip -r ../mm7.apworld mm7   -x "mm7/__pycache__/*"   -x "mm7/*.pyc"   -x "mm7/build/*"

python Generate.py --player_files Players

python Patch.py output/