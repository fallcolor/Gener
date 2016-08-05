

// unpack can message: ID = 0xC6AD0D1, Trans ECU(s) is(are): TM 
void Unpack_0xC6AD0D1(void)
{
    uint32_T tempValue = 0;

    /* value name : TM.InvTemp
       start bit  : 48
       length     : 16
       factor     : 1
       offset     : -40
     */
    tempValue = data[6];
    tempValue += data[7] * 256;
    TM.InvTemp = (int16_T)tempValue * 1 + -40;

    /* value name : TM.EneAct
       start bit  : 16
       length     : 16
       factor     : 0.01
       offset     : -300
     */
    tempValue = data[2];
    tempValue += data[3] * 256;
    TM.EneAct = (bool_T)tempValue * 0.01 + -300;
}

// unpack can message: ID = 0xC69D0D1, Trans ECU(s) is(are): TM 
void Unpack_0xC69D0D1(void)
{
    uint32_T tempValue = 0;

    /* value name : TM.Eff
       start bit  : 16
       length     : 8
       factor     : 1
       offset     : 0
     */
    tempValue = data[2];
    TM.Eff = (float)tempValue * 1 + 0;

    /* value name : TM.VoltC
       start bit  : 0
       length     : 16
       factor     : 1
       offset     : 0
     */
    tempValue = data[0];
    tempValue += data[1] * 256;
    TM.VoltC = (float)tempValue * 1 + 0;
}

// unpack can message: ID = 0xC68D0D1, Trans ECU(s) is(are): TM 
void Unpack_0xC68D0D1(void)
{
    uint32_T tempValue = 0;

    /* value name : TM.CM
       start bit  : 4
       length     : 2
       factor     : 1
       offset     : 0
     */
    tempValue = (data[0] & 63) >> 4;
    TM.CM = (avd)tempValue * 1 + 0;
}

// unpack can message: ID = 0xC71D0D2, Trans ECU(s) is(are): BMS 
void Unpack_0xC71D0D2(void)
{
    uint32_T tempValue = 0;

    /* value name : Bat.BusVolt
       start bit  : 0
       length     : 16
       factor     : 0.015
       offset     : 0
     */
    tempValue = data[0];
    tempValue += data[1] * 256;
    Bat.BusVolt = (float)tempValue * 0.015 + 0;
}