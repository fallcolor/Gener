{
    "map": [
        [
            "Bat.BusVolt", 
            "float", 
            "BAT_Volt (0/16)", 
            "BMS_Voltage (0xC71D0D2)", 
            "CAN signal", 
            false
        ], 
        [
            "Bat.BusVolt", 
            "float", 
            "BAT_Volt (0/16)", 
            "BMS_Voltage (0xC71D0D2)", 
            "CAN signal", 
            false
        ], 
        [
            "Bat.SOC", 
            "float", 
            "BAT_SOC (32/8)", 
            "BMS_Voltage (0xC71D0D2)", 
            "CAN signal", 
            false
        ], 
        [
            "Bat.BusCurr", 
            "float", 
            "BAT_SOC (32/8)", 
            "BMS_Voltage (0xC71D0D2)", 
            "CAN signal", 
            false
        ]
    ], 
    "hwver": "", 
    "ecu": {
        "BMS": true, 
        "TM": false, 
        "VCU": false,
        "DCDC": false
    }, 
    "canconfig": {}, 
    "project": "test", 
    "appver": 0.121, 
    "time": "", 
    "msgconfig": [
        {
            "node": "2", 
            "prd": "100", 
            "enable": 0, 
            "checked": false, 
            "name": "BMS_CellTemperature", 
            "trans": "0", 
            "DLC": 0, 
            "ID": "0x1874D0D2"
        }, 
        {
            "node": "2", 
            "prd": "100", 
            "enable": 0, 
            "checked": false, 
            "name": "BMS_CellVoltage", 
            "trans": "0", 
            "DLC": 0, 
            "ID": "0x1873D0D2"
        }, 
        {
            "node": "2", 
            "prd": "100", 
            "enable": 0, 
            "checked": false, 
            "name": "BMS_Limit1", 
            "trans": "0", 
            "DLC": 0, 
            "ID": "0x1875D0D2"
        }, 
        {
            "node": "2", 
            "prd": "100", 
            "enable": 0, 
            "checked": false, 
            "name": "BMS_Limit2", 
            "trans": "0", 
            "DLC": 0, 
            "ID": "0x1876D0D2"
        }, 
        {
            "node": "2", 
            "prd": "100", 
            "enable": 0, 
            "checked": false, 
            "name": "BMS_State", 
            "trans": "0", 
            "DLC": 0, 
            "ID": "0xC72D0D2"
        }, 
        {
            "node": "2", 
            "prd": "100", 
            "enable": 1, 
            "checked": false, 
            "name": "BMS_Voltage", 
            "trans": "1", 
            "DLC": 1, 
            "ID": "0xC71D0D2"
        }, 
        {
            "node": "2", 
            "prd": "100", 
            "enable": 0, 
            "checked": false, 
            "name": "DCDC_Failure", 
            "trans": "0", 
            "DLC": 0, 
            "ID": "0x1368"
        }, 
        {
            "node": "2", 
            "prd": "100", 
            "enable": 0, 
            "checked": false, 
            "name": "DCDC_General", 
            "trans": "0", 
            "DLC": 0, 
            "ID": "0x1379"
        }, 
        {
            "node": "2", 
            "prd": "100", 
            "enable": 0, 
            "checked": false, 
            "name": "DCDC_Limits", 
            "trans": "0", 
            "DLC": 0, 
            "ID": "0x1381"
        }, 
        {
            "node": "2", 
            "prd": "100", 
            "enable": 0, 
            "checked": false, 
            "name": "IPU_DCDC_Ctrl", 
            "trans": "0", 
            "DLC": 0, 
            "ID": "0x12A8"
        }, 
        {
            "node": "2", 
            "prd": "100", 
            "enable": 1, 
            "checked": false, 
            "name": "TM_State1", 
            "trans": "1", 
            "DLC": 1, 
            "ID": "0xC68D0D1"
        }, 
        {
            "node": "2", 
            "prd": "100", 
            "enable": 1, 
            "checked": false, 
            "name": "TM_State2", 
            "trans": "1", 
            "DLC": 1, 
            "ID": "0xC69D0D1"
        }, 
        {
            "node": "2", 
            "prd": "100", 
            "enable": 1, 
            "checked": false, 
            "name": "TM_State3", 
            "trans": "1", 
            "DLC": 1, 
            "ID": "0xC6AD0D1"
        }, 
        {
            "node": "2", 
            "prd": "100", 
            "enable": 0, 
            "checked": false, 
            "name": "VCU2IPK3", 
            "trans": "0", 
            "DLC": 0, 
            "ID": "0x8F200A0"
        }, 
        {
            "node": "2", 
            "prd": "100", 
            "enable": 0, 
            "checked": false, 
            "name": "VCU_HVEnable", 
            "trans": "0", 
            "DLC": 0, 
            "ID": "0xC77D2D0"
        }, 
        {
            "node": "2", 
            "prd": "100", 
            "enable": 1, 
            "checked": false, 
            "name": "VCU_TM", 
            "trans": "1", 
            "DLC": 1, 
            "ID": "0xC6BD1D0"
        }
    ]
}