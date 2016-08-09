/* file        :test.c
 * author      :
 * description :
 * time        : 2016.08.08 17:39:48
 */

// CAN frame initiation
void InitFrame(void)
{
    /* ID       : 0xC69D0D1
       Node     : 0
       Period   : 100ms
       direction: recieve
       function : Unpack_0xC69D0D1
    */
    InitMsg(0xC69D0D1, NODE_0, PRD_100MS, RECI_FLAG, Unpack_0xC69D0D1);

    /* ID       : 0xC68D0D1
       Node     : 0
       Period   : 20ms
       direction: recieve
       function : Unpack_0xC68D0D1
    */
    InitMsg(0xC68D0D1, NODE_0, PRD_20MS, RECI_FLAG, Unpack_0xC68D0D1);

    /* ID       : 0xC71D0D2
       Node     : 0
       Period   : 100ms
       direction: recieve
       function : Unpack_0xC71D0D2
    */
    InitMsg(0xC71D0D2, NODE_0, PRD_100MS, RECI_FLAG, Unpack_0xC71D0D2);
}

// unpack can message: ID = 0xC69D0D1, Trans ECU(s) is(are): TM 
void Unpack_0xC69D0D1(void)
{
    uint32_T tempValue = 0;

    /* value name : Tm.TmVolt
       start bit  : 0
       length     : 16
       factor     : 1
       offset     : 0
     */
    tempValue = data[0];
    tempValue += data[1] * 256;
    Tm.TmVolt = (float)tempValue * 1 + 0;
}

// unpack can message: ID = 0xC68D0D1, Trans ECU(s) is(are): TM 
void Unpack_0xC68D0D1(void)
{
    uint32_T tempValue = 0;

    /* value name : Tm.TmSpd
       start bit  : 24
       length     : 16
       factor     : 1
       offset     : 0
     */
    tempValue = data[3];
    tempValue += data[4] * 256;
    Tm.TmSpd = (float)tempValue * 1 + 0;

    /* value name : Tm.TmTrq
       start bit  : 8
       length     : 16
       factor     : 1
       offset     : -1000
     */
    tempValue = data[1];
    tempValue += data[2] * 256;
    Tm.TmTrq = (float)tempValue * 1 + -1000;
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

    /* value name : Bat.SOC
       start bit  : 32
       length     : 8
       factor     : 0.4
       offset     : 0
     */
    tempValue = data[4];
    Bat.SOC = (float)tempValue * 0.4 + 0;

    /* value name : Bat.BusCurr
       start bit  : 16
       length     : 16
       factor     : 0.05
       offset     : -500
     */
    tempValue = data[2];
    tempValue += data[3] * 256;
    Bat.BusCurr = (float)tempValue * 0.05 + -500;
}