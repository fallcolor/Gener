{
  "map": [
    [
      "Bat.BusVolt", 
      "float", 
      "BAT_VOLT(0/16)", 
      "Bat_Volt(0x14AA03F2)", 
      "CAN Message", 
      false
    ], 
    [
      "Bat.SOC", 
      "float", 
      "BAT_VOLT(32/8)", 
      "Bat_Volt(0x14AA03F2)", 
      "CAN Message", 
      false
    ]
  ], 
  "hwver": "v1.0", 
  "ecu": {
    "BMS": false, 
    "TM": false, 
    "VCU": true
  }, 
  "canconfig": {
    "baudrate": {
      "n0": 500
    }, 
    "sampoint": {
      "n1": 75
    }, 
    "timeoutprd": 15
  }, 
  "project": "test", 
  "appver": "v0.1", 
  "time": "2016-8-12 16:40:40", 
  "msgconfig": [
    {
      "node": 3, 
      "prd": 50, 
      "enable": true, 
      "checked": true, 
      "name": "BMS_VCU", 
      "trans": true, 
      "DLC": 8, 
      "ID": "0x14FF00A0"
    }, 
    {
      "node": 4, 
      "prd": 50, 
      "enable": true, 
      "checked": false, 
      "name": "BMS_TM", 
      "trans": true, 
      "DLC": 8, 
      "ID": "0x14FF01A0"
    }
  ]
}