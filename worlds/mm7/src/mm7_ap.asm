; MM7 Archipelago - Test Patch
; Mega Man 7 (USA)

hirom

; ============================================
; AP WRAM layout
; Using $7E1FA1-$7E1FDF.
; $7E1FA0 appears to be cleared during state transitions.
; ============================================

!AP_BOSS_FLAGS     = $7E1FA1
!AP_BOSS_FLAGS_2   = $7E1FA2
!AP_DEBUG_FLAGS    = $7E1FA3
!AP_ITEM_ID_LO     = $7E1FA4
!AP_ITEM_ID_HI     = $7E1FA5
!AP_EXECUTE_FLAG   = $7E1FA6
!AP_RECV_INDEX_LO  = $7E1FA7
!AP_RECV_INDEX_HI  = $7E1FA8
!AP_CONNECTION     = $7E1FA9
!AP_RUNTIME_START  = $7E1FA1
!MM7_PROTO_FLAGS   = $7E0B78

!AP_PROTO_CHECKS   = $7E1FA2 ; already AP_BOSS_FLAGS_2
!AP_PROTO_ITEMS    = $7E1FAA ; AP-owned randomized Proto clues
!AP_TEMP           = $7E1FAB
!AP_GOAL_FLAGS     = $7E1FAC
!AP_PICKUP_FLAGS   = $7E1FB0

; ============================================
; New-game setup
; ============================================

org $C00C22
    LDA #$01
    STA $0B79 ; ???
    STA $0B7A ; Robot Museum Flag
    STA $0B7B ; New stages introduction flag
    STZ $0B7C ; Wily Stage
    JSL AP_SetStartingTanks
    JSL AP_SetStartingItems
    LDA #$82
    STA $0B77
    JSL AP_SetStartingBolts
    JSL AP_ClearRuntime
    NOP
    NOP
    NOP

; ============================================
; Remove Rush Coil as a starting item
; ============================================

org $C00BFC
    LDA #$00 ; Rush Coil Ammo

org $C00C18
    LDA #$00 ; Rush Coil Ammo

; org $C00C54
;     JSR AP_SkipIntroStage
;     BRA $C00C81

; ============================================
; Main loop AP hook
; Replaces:
;   C000AF: JSR $315A
;   C000B2: INC $00D1
; ============================================

org $C000AF
    JSL AP_MainLoopHook
    NOP
    NOP

; ============================================
; Vanilla boss weapon grant left restored but bypassed.
; Boss rewards are AP-only via AP_StageExitAPOnlyBossGate.
; ============================================

org $C00DCB
    LDA #$80
    STA $0B83,X

; ============================================
; Stage select medal hook
; Original:
;   C038CC BD 83 0B    LDA $0B83,X
;   C038CF 10 05       BPL $C038D6
;   C038D1 DA          PHX
;   C038D2 20 02 39    JSR $3902
;   C038D5 FA          PLX
; ============================================

org $C038CC
    JSL AP_StageSelectMedalHook
    NOP
    NOP
    NOP
    NOP
    NOP
    NOP

; ============================================
; Boss spawn defeated-state hook
; ============================================

org $C3035F
    JSL AP_LoadBossDefeatedState

; ============================================
; Proto Man Cloud Man meeting hook
; ============================================

org $C2C4B3
    JML AP_ProtoCloudMeetingGate
    NOP
    NOP
    NOP
    NOP
    NOP
    NOP
    NOP
    NOP

; ============================================
; AP-only boss reward gate.
; Always records the AP boss flag and skips vanilla weapon-get.
; ============================================

org $C00DBC
    JML AP_StageExitAPOnlyBossGate
    NOP

; ============================================
; Wily unlock gate.
; Replaces vanilla all-weapons check with AP boss flags check.
; ============================================

org $C00DE1
    JML AP_WilyUnlockGate
    NOP
    NOP
    NOP
    NOP
    NOP
    NOP
    NOP

; ============================================
; Wily Capsule defeated goal hook
; Original:
;   D8DAB4 EE CA 0B    INC $0BCA
;   D8DAB7 A9 08       LDA #$08
; ============================================

org $D8DAB4
    JSL AP_WilyCapsuleDefeatedHook
    NOP

; ============================================
; Rush Search pickup AP location hook
; Original:
;   D8D128 A9 9C       LDA #$9C
;   D8D12A 8D 97 0B    STA $0B97
;   D8D12D 4C E7 D1    JMP $D1E7
; ============================================

org $D8D128
    JML AP_RushSearchPickupCheck
    NOP
    NOP
    NOP
    NOP

; ============================================
; Rush plate pickup AP location hooks
; Original plate grant handlers are 11 bytes each:
;   LDA #$xx
;   TSB $0BA4
;   JSR $D1D0
;   JMP $D1E7
; ============================================

org $D8D0D2
    JML AP_RushRPlatePickupCheck
    NOP
    NOP
    NOP
    NOP
    NOP
    NOP
    NOP

org $D8D0E8
    JML AP_RushUPlatePickupCheck
    NOP
    NOP
    NOP
    NOP
    NOP
    NOP
    NOP

org $D8D0FE
    JML AP_RushSPlatePickupCheck
    NOP
    NOP
    NOP
    NOP
    NOP
    NOP
    NOP

org $D8D114
    JML AP_RushHPlatePickupCheck
    NOP
    NOP
    NOP
    NOP
    NOP
    NOP
    NOP

; ============================================
; Rush plate spawn/check AP location hooks
; ============================================

org $D8D0C7
    JML AP_RushRPlateSpawnCheck
    NOP
    NOP
    NOP
    NOP
    NOP
    NOP
    NOP

org $D8D0DD
    JML AP_RushUPlateSpawnCheck
    NOP
    NOP
    NOP
    NOP
    NOP
    NOP
    NOP

org $D8D0F3
    JML AP_RushSPlateSpawnCheck
    NOP
    NOP
    NOP
    NOP
    NOP
    NOP
    NOP

org $D8D109
    JML AP_RushHPlateSpawnCheck
    NOP
    NOP
    NOP
    NOP
    NOP
    NOP
    NOP


; ============================================
; Rush Jet pickup AP location hook
; Original:
;   D8D139 A9 9C       LDA #$9C
;   D8D13B 8D 99 0B    STA $0B99
;   D8D13E 4C E7 D1    JMP $D1E7
; ============================================

org $D8D139
    JML AP_RushJetPickupCheck
    NOP
    NOP
    NOP
    NOP

; ============================================
; Freeze Man presence gate.
; Original block:
;   C286ED AD 73 0B    LDA $0B73
;   C286F0 C9 09       CMP #$09
;   C286F2 B0 08       BCS $C286FC
;   C286F4 0A          ASL
;   C286F5 AA          TAX
;   C286F6 BD 83 0B    LDA $0B83,X
;   C286F9 10 01       BPL $C286FC
;   C286FB 60          RTS
; ============================================

org $C286ED
    JML AP_FreezeManPresenceGate
    NOP
    NOP
    NOP
    NOP
    NOP
    NOP
    NOP
    NOP
    NOP
    NOP
    NOP

; ============================================
; Small C0-bank helper routines
;
; These stay in bank C0 because they call vanilla RTS routines using JSR.
; Do not move them to bank D8 without adding wrappers.
; ============================================

org $C07C00

AP_MainLoopHook:
    JSR $315A
    INC $00D1
    JSL AP_CheckItemReceive
    RTL

org $C07EC0

AP_StageSelectMedalHook:
    PHP
    SEP #$30
    PHX

    ; X is one of $10,$0E,$0C,$0A,$08,$06,$04,$02.
    ; Convert weapon offset into table index: X / 2.
    TXA
    LSR
    TAX

    LDA.l AP_StageSelectBitMaskTable,x
    AND.l !AP_BOSS_FLAGS
    BEQ .not_cleared

.cleared:
    PLX
    PLP

    ; Original cleared behavior:
    ; PHX
    ; JSR $3902
    ; PLX
    PHX
    JSR $3902
    PLX
    RTL

.not_cleared:
    PLX
    PLP
    RTL

; ============================================
; AP custom routines block
;
; Confirmed free space:
;   file offset 0x18EF15
;   CPU address $D8EF15
;   size 0xFEB
;   fill $FF
;
; Keep all general AP routines in this block.
; ============================================

org $D8EF15

AP_SetStartingTanks:
    LDA #$01
    STA $0BA0
    LDA #$00
    STA $0BA1
    LDA #$00
    STA $0BA2
    RTL

AP_SetStartingItems:
    LDA #$00
    STA $0BA4
    RTL

AP_SetStartingBolts:
    LDA #$01
    STA $0BA6
    LDA #$00
    STA $0BA7
    RTL

AP_ClearRuntime:
    PHP
    SEP #$30
    PHX

    LDX #$00
    LDA #$00

.clear_loop:
    STA.l !AP_RUNTIME_START,x
    INX
    CPX #$10
    BNE .clear_loop

    PLX
    PLP
    RTL

AP_SkipIntroStage:
    LDA #$01
    STA $0B73
    RTS

; ============================================
; AP item receive dispatcher
;
; !AP_ITEM_ID_LO     = item id low byte
; !AP_ITEM_ID_HI     = item id high byte
; !AP_EXECUTE_FLAG   = 1 when an item is waiting
; !AP_RECV_INDEX_LO  = received index low byte
; !AP_RECV_INDEX_HI  = received index high byte
; ============================================

AP_CheckItemReceive:
    PHP
    SEP #$30
    PHX

    LDA.l !AP_EXECUTE_FLAG
    BNE +
    JMP .done
+

    ; For now only support IDs $0001-$00FF.
    ; If high byte is nonzero, consume safely.
    LDA.l !AP_ITEM_ID_HI
    BEQ +
    JMP .finish
+

    LDA.l !AP_ITEM_ID_LO

    ; $01-$0B = weapon/Rush table
    CMP #$01
    BCS +
    JMP .finish
+

    CMP #$0C
    BCS +
    JMP .give_weapon_table
+

    ; $0C-$13 = unique item bitfield at $0BA4
    CMP #$14
    BCS +
    JMP .give_unique_bitfield
+

    ; $14 = Proto Shield
    CMP #$14
    BNE +
    JMP .give_proto_shield
+

    ; $15 = Beat
    CMP #$15
    BNE +
    JMP .give_beat
+

    ; $16 = 1-Up
    CMP #$16
    BNE +
    JMP .give_one_up
+

    ; $17 = Small Bolt
    CMP #$17
    BNE +
    JMP .give_small_bolt
+

    ; $18 = Large Bolt
    CMP #$18
    BNE +
    JMP .give_large_bolt
+

    ; $19 = E-Tank
    CMP #$19
    BNE +
    JMP .give_e_tank
+

    ; $1A = W-Tank
    CMP #$1A
    BNE +
    JMP .give_w_tank
+

    ; $1B = S-Tank
    CMP #$1B
    BNE +
    JMP .give_s_tank
+

    ; $1C = Beat Whistle
    CMP #$1C
    BNE +
    JMP .give_beat_whistle
+

    ; $1D = Proto Man Cloud Man clue
    CMP #$1D
    BNE +
    JMP .give_proto_cloud_clue
+

    ; $1E = Proto Man Turbo Man clue
    CMP #$1E
    BNE +
    JMP .give_proto_turbo_clue
+

    JMP .finish

.give_weapon_table:
    SEC
    SBC #$01
    ASL
    TAX

    ; Save direct-page scratch pointer $00/$01 before using it.
    REP #$20
    LDA $00
    PHA

    LDA.l AP_WeaponAddressTable,x
    STA $00

    SEP #$20
    LDA #$9C
    STA ($00)

    REP #$20
    PLA
    STA $00
    SEP #$20

    JMP .finish

.give_unique_bitfield:
    ; item_id - $0C gives bit index 0-7
    SEC
    SBC #$0C
    TAX

    LDA.l AP_BitMaskTable,x
    ORA.l $7E0BA4
    STA.l $7E0BA4

    ; If all four plates are owned, grant Super Adapter.
    LDA.l $7E0BA4
    AND #$0F
    CMP #$0F
    BNE .finish

    LDA #$9C
    STA.l $7E0B9F

    JMP .finish

.give_proto_shield:
    LDA #$9C
    STA.l $7E0B95
    JMP .finish

.give_beat:
    LDA #$84
    STA.l $7E0BA3
    JMP .finish

.give_one_up:
    INC $0B81
    JMP .finish

.give_small_bolt:
    JSR AP_AddSmallBolts
    JMP .finish

.give_large_bolt:
    JSR AP_AddLargeBolts
    JMP .finish

.give_e_tank:
    INC $0BA0
    JMP .finish

.give_w_tank:
    INC $0BA1
    JMP .finish

.give_s_tank:
    INC $0BA2
    JMP .finish

.give_beat_whistle:
    LDA #$84
    STA.l $7E0BA3
    JMP .finish

.give_proto_cloud_clue:
    ; AP owns Proto clue bit 0.
    LDA.l !AP_PROTO_ITEMS
    ORA #$01
    STA.l !AP_PROTO_ITEMS

    ; Also set the vanilla clue bit so the game can use it.
    LDA.l !MM7_PROTO_FLAGS
    ORA #$01
    STA.l !MM7_PROTO_FLAGS

    JMP .finish

.give_proto_turbo_clue:
    ; AP owns Proto clue bit 1.
    LDA.l !AP_PROTO_ITEMS
    ORA #$02
    STA.l !AP_PROTO_ITEMS

    ; Also set the vanilla clue bit so the game can use it.
    LDA.l !MM7_PROTO_FLAGS
    ORA #$02
    STA.l !MM7_PROTO_FLAGS

    JMP .finish

.finish:
    ; Increment 16-bit received index stored as two bytes.
    LDA.l !AP_RECV_INDEX_LO
    INC
    STA.l !AP_RECV_INDEX_LO
    BNE .clear_flag

    LDA.l !AP_RECV_INDEX_HI
    INC
    STA.l !AP_RECV_INDEX_HI

.clear_flag:
    LDA #$00
    STA.l !AP_EXECUTE_FLAG

.done:
    PLX
    PLP
    RTL

AP_BitMaskTable:
    db $01, $02, $04, $08, $10, $20, $40, $80

AP_WeaponAddressTable:
    dw $0B85 ; $01 Freeze Cracker
    dw $0B91 ; $02 Danger Wrap
    dw $0B87 ; $03 Thunder Bolt
    dw $0B89 ; $04 Junk Shield
    dw $0B8D ; $05 Slash Claw
    dw $0B93 ; $06 Wild Coil
    dw $0B8F ; $07 Noise Crush
    dw $0B8B ; $08 Scorch Wheel
    dw $0B9B ; $09 Rush Coil
    dw $0B97 ; $0A Rush Search
    dw $0B99 ; $0B Rush Jet

AP_AddSmallBolts:
    CLC
    LDA.l $7E0BA6
    ADC #$05
    STA.l $7E0BA6
    LDA.l $7E0BA7
    ADC #$00
    STA.l $7E0BA7
    RTS

AP_AddLargeBolts:
    CLC
    LDA.l $7E0BA6
    ADC #$32
    STA.l $7E0BA6
    LDA.l $7E0BA7
    ADC #$00
    STA.l $7E0BA7
    RTS

; ============================================
; Boss defeated/check flag tables and hooks
; ============================================

AP_BossBitMaskTable:
    db $00 ; index 0 unused / unknown
    db $01 ; index 1 = Freeze Man
    db $02 ; index 2 = Cloud Man
    db $04 ; index 3 = Junk Man
    db $08 ; index 4 = Turbo Man
    db $10 ; index 5 = Slash Man
    db $20 ; index 6 = Shade Man
    db $40 ; index 7 = Burst Man
    db $80 ; index 8 = Spring Man

AP_StageSelectBitMaskTable:
    db $00 ; index 0 unused
    db $01 ; X=$02
    db $02 ; X=$04
    db $04 ; X=$06
    db $08 ; X=$08
    db $10 ; X=$0A
    db $20 ; X=$0C
    db $40 ; X=$0E
    db $80 ; X=$10

AP_LoadBossDefeatedState:
    PHP
    SEP #$30
    PHX

    ; X is stage_id * 2 here.
    TXA
    LSR
    TAX

    LDA.l AP_BossBitMaskTable,x
    AND.l !AP_BOSS_FLAGS
    BEQ .not_defeated

.defeated:
    PLX
    PLP
    SEC
    LDA #$80
    RTL

.not_defeated:
    PLX
    PLP
    CLC
    LDA #$00
    RTL

AP_ProtoCloudMeetingGate:
    PHP
    SEP #$20

    ; If AP already recorded this Proto Man meeting check, skip it.
    LDA.l !AP_PROTO_CHECKS
    AND #$01
    BNE .Skip

    ; Otherwise record the AP check and continue to vanilla meeting/event path.
    LDA.l !AP_PROTO_CHECKS
    ORA #$01
    STA.l !AP_PROTO_CHECKS

    PLP
    JML $C2C4ED

.Skip:
    PLP
    JML $C2C4BF

AP_StageExitAPOnlyBossGate:
    PHP
    SEP #$30
    PHX

    ; X is stage_id * 2 here.
    ; Record the boss as defeated for AP.
    TXA
    LSR
    TAX

    LDA.l AP_BossBitMaskTable,x
    ORA.l !AP_BOSS_FLAGS
    STA.l !AP_BOSS_FLAGS

    PLX
    PLP

    ; Skip vanilla weapon-get / boss weapon grant.
    JML $C00DDC

AP_WilyUnlockGate:
    PHP
    SEP #$20

    LDA.l !AP_BOSS_FLAGS
    CMP #$FF
    BEQ .all_defeated

.not_all_defeated:
    PLP
    JML $C00E08

.all_defeated:
    PLP
    JML $C00DEC

AP_WilyCapsuleDefeatedHook:
    PHP
    SEP #$20

    ; Preserve replaced vanilla behavior: INC $0BCA
    LDA.l $7E0BCA
    INC
    STA.l $7E0BCA

    ; Mark AP goal complete.
    LDA.l !AP_GOAL_FLAGS
    ORA #$01
    STA.l !AP_GOAL_FLAGS

    ; Preserve replaced vanilla behavior: LDA #$08
    LDA #$08

    PLP
    RTL

AP_RushSearchPickupCheck:
    PHP
    SEP #$20

    ; Mark Rush Search pickup location checked.
    ; Bit 0 of AP_PICKUP_FLAGS.
    LDA.l !AP_PICKUP_FLAGS
    ORA #$01
    STA.l !AP_PICKUP_FLAGS

    PLP

    ; Skip vanilla Rush Search grant and continue normal pickup cleanup.
    JML $D8D1E7

AP_RushJetPickupCheck:
    PHP
    SEP #$20

    ; Mark Rush Jet pickup location checked.
    ; Bit 5 of AP_PICKUP_FLAGS.
    LDA.l !AP_PICKUP_FLAGS
    ORA #$20
    STA.l !AP_PICKUP_FLAGS

    PLP

    ; Skip vanilla Rush Jet grant and continue normal pickup cleanup.
    JML $D8D1E7

AP_FreezeManPresenceGate:
    PHP
    SEP #$30
    PHX

    LDA.l $7E0B73
    CMP #$09
    BCS .continue

    TAX

    LDA.l AP_BossBitMaskTable,x
    AND.l !AP_BOSS_FLAGS
    BNE .skip_object

.continue:
    PLX
    PLP
    JML $C286FC

.skip_object:
    PLX
    PLP
    JML $C286FB

AP_RushRPlatePickupCheck:
    PHP
    SEP #$20

    LDA.l !AP_PICKUP_FLAGS
    ORA #$02
    STA.l !AP_PICKUP_FLAGS

    PLP

    ; Preserve vanilla plate pickup side effect.
    JSR $D1D0

    ; Skip vanilla plate grant and continue normal pickup cleanup.
    JML $D8D1E7

AP_RushUPlatePickupCheck:
    PHP
    SEP #$20

    LDA.l !AP_PICKUP_FLAGS
    ORA #$04
    STA.l !AP_PICKUP_FLAGS

    PLP

    ; Preserve vanilla plate pickup side effect.
    JSR $D1D0

    ; Skip vanilla plate grant and continue normal pickup cleanup.
    JML $D8D1E7

AP_RushSPlatePickupCheck:
    PHP
    SEP #$20

    LDA.l !AP_PICKUP_FLAGS
    ORA #$08
    STA.l !AP_PICKUP_FLAGS

    PLP

    ; Preserve vanilla plate pickup side effect.
    JSR $D1D0

    ; Skip vanilla plate grant and continue normal pickup cleanup.
    JML $D8D1E7

AP_RushHPlatePickupCheck:
    PHP
    SEP #$20

    LDA.l !AP_PICKUP_FLAGS
    ORA #$10
    STA.l !AP_PICKUP_FLAGS

    PLP

    ; Preserve vanilla plate pickup side effect.
    JSR $D1D0

    ; Skip vanilla plate grant and continue normal pickup cleanup.
    JML $D8D1E7

AP_RushRPlateSpawnCheck:
    PHP
    SEP #$20

    LDA.l !AP_PICKUP_FLAGS
    AND #$02
    BNE .already_checked

    PLP
    RTS

.already_checked:
    PLP
    JML $D8D1DF


AP_RushUPlateSpawnCheck:
    PHP
    SEP #$20

    LDA.l !AP_PICKUP_FLAGS
    AND #$04
    BNE .already_checked

    PLP
    RTS

.already_checked:
    PLP
    JML $D8D1DF


AP_RushSPlateSpawnCheck:
    PHP
    SEP #$20

    LDA.l !AP_PICKUP_FLAGS
    AND #$08
    BNE .already_checked

    PLP
    RTS

.already_checked:
    PLP
    JML $D8D1DF


AP_RushHPlateSpawnCheck:
    PHP
    SEP #$20

    LDA.l !AP_PICKUP_FLAGS
    AND #$10
    BNE .already_checked

    PLP
    RTS

.already_checked:
    PLP
    JML $D8D1DF

assert pc() <= $D8FF00