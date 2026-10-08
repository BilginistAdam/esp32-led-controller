"""Single source of truth: parts, footprints, nets, schematic positions."""
P = "ledctl"  # project lib nickname

R0603 = "Resistor_SMD:R_0603_1608Metric"
C0603 = "Capacitor_SMD:C_0603_1608Metric"
C0805 = "Capacitor_SMD:C_0805_2012Metric"
C1206 = "Capacitor_SMD:C_1206_3216Metric"
SMA = "Diode_SMD:D_SMA"
TB2 = "TerminalBlock_Phoenix:TerminalBlock_Phoenix_MKDS-1,5-2-5.08_1x02_P5.08mm_Horizontal"
BTN = "Button_Switch_SMD:SW_Push_1P1T_XKB_TS-1187A"

# ref: (lib, symbol, value, footprint, (x, y), {pin: net}, extra_fields)
PARTS = {
    # ---------------- input / protection ----------------
    "J1": ("Connector", "Screw_Terminal_01x02", "DC_IN_12-24V", TB2, (25.4, 40.64), {"1": "VIN_RAW", "2": "GND"}),
    "F1": ("Device", "Polyfuse", "PTC_3A_hold_30V", "Fuse:Fuse_1812_4532Metric", (50.8, 40.64), {"1": "VIN_RAW", "2": "VIN"}),
    "D3": ("Device", "D_Zener", "SMAJ28A", SMA, (71.12, 40.64), {"1": "VIN", "2": "GND"}),
    "J2": ("Connector", "Screw_Terminal_01x02", "LED_STRIP", TB2, (25.4, 66.04), {"1": "VIN", "2": "LED-"}),
    "D1": ("Device", "D_Schottky", "SS34", SMA, (50.8, 66.04), {"1": "VBUCK", "2": "VIN"}),
    "D2": ("Device", "D_Schottky", "SS14", SMA, (81.28, 66.04), {"1": "VBUCK", "2": "VBUS"}),
    # ---------------- USB-C (native USB of ESP32-C3) ----------------
    "J3": ("Connector", "USB_C_Receptacle_USB2.0_16P", "USB-C", "Connector_USB:USB_C_Receptacle_HRO_TYPE-C-31-M-12", (33.02, 129.54),
           {"A1": "GND", "A12": "GND", "B1": "GND", "B12": "GND", "S1": "GND",
            "A4": "VBUS", "A9": "VBUS", "B4": "VBUS", "B9": "VBUS",
            "A5": "CC1", "B5": "CC2", "A6": "USB_D+", "B6": "USB_D+", "A7": "USB_D-", "B7": "USB_D-"}),
    "R8": ("Device", "R", "5.1k", R0603, (71.12, 124.46), {"1": "CC1", "2": "GND"}),
    "R9": ("Device", "R", "5.1k", R0603, (83.82, 124.46), {"1": "CC2", "2": "GND"}),
    # ---------------- buck 12/24V -> 3.3V ----------------
    "U1": ("Regulator_Switching", "AP63203WU", "AP63203WU", "Package_TO_SOT_SMD:TSOT-23-6", (127.0, 45.72),
           {"1": "+3V3", "2": "VBUCK", "3": "VBUCK", "4": "GND", "5": "SW", "6": "BST"}),
    "C1": ("Device", "C", "10uF_50V", C1206, (104.14, 71.12), {"1": "VBUCK", "2": "GND"}),
    "C2": ("Device", "C", "100nF_50V", C0603, (114.3, 71.12), {"1": "VBUCK", "2": "GND"}),
    "C3": ("Device", "C", "100nF", C0603, (157.48, 71.12), {"1": "BST", "2": "SW"}),
    "L1": ("Device", "L", "4.7uH_3A", "Inductor_SMD:L_Changjiang_FNR4030S", (170.18, 71.12), {"1": "SW", "2": "+3V3"}),
    "C4": ("Device", "C", "22uF_10V", C0805, (182.88, 71.12), {"1": "+3V3", "2": "GND"}),
    "C5": ("Device", "C", "22uF_10V", C0805, (195.58, 71.12), {"1": "+3V3", "2": "GND"}),
    "#FLG01": ("power", "PWR_FLAG", "PWR_FLAG", "", (220.98, 33.02), {"1": "VBUCK"}),
    "#FLG02": ("power", "PWR_FLAG", "PWR_FLAG", "", (236.22, 33.02), {"1": "+3V3"}),
    "#FLG03": ("power", "PWR_FLAG", "PWR_FLAG", "", (251.46, 33.02), {"1": "GND"}),
    # ---------------- ESP32-C3 ----------------
    "U2": (P, "ESP32-C3-WROOM-02", "ESP32-C3-WROOM-02", "RF_Module:ESP32-C3-WROOM-02", (160.02, 132.08),
           {"1": "+3V3", "2": "EN", "8": "IO9_BOOT", "7": "IO8", "16": "IO2", "11": "RXD0", "12": "TXD0",
            "13": "USB_D-", "14": "USB_D+", "3": "LED_PWM", "10": "STAT", "9": "GND", "19": "GND"}),
    "C6": ("Device", "C", "10uF", C0805, (106.68, 106.68), {"1": "+3V3", "2": "GND"}),
    "C7": ("Device", "C", "100nF", C0603, (116.84, 106.68), {"1": "+3V3", "2": "GND"}),
    "R1": ("Device", "R", "10k", R0603, (96.52, 167.64), {"1": "+3V3", "2": "EN"}),
    "C8": ("Device", "C", "1uF", C0603, (109.22, 167.64), {"1": "EN", "2": "GND"}),
    "SW1": ("Switch", "SW_Push", "RESET", BTN, (127.0, 187.96), {"1": "EN", "2": "GND"}),
    "R2": ("Device", "R", "10k", R0603, (152.4, 167.64), {"1": "+3V3", "2": "IO9_BOOT"}),
    "SW2": ("Switch", "SW_Push", "BOOT/USER", BTN, (167.64, 187.96), {"1": "IO9_BOOT", "2": "GND"}),
    "R3": ("Device", "R", "10k", R0603, (129.54, 167.64), {"1": "+3V3", "2": "IO8"}),
    "R4": ("Device", "R", "10k", R0603, (139.7, 167.64), {"1": "+3V3", "2": "IO2"}),
    "J4": ("Connector_Generic", "Conn_01x04", "UART", "Connector_PinHeader_2.54mm:PinHeader_1x04_P2.54mm_Vertical", (271.78, 160.02),
           {"1": "GND", "2": "TXD0", "3": "RXD0", "4": "+3V3"}),
    # ---------------- LED strip low-side switch ----------------
    "R5": ("Device", "R", "100R", R0603, (236.22, 114.3), {"1": "LED_PWM", "2": "GATE"}),
    "R6": ("Device", "R", "100k", R0603, (248.92, 114.3), {"1": "GATE", "2": "GND"}),
    "Q1": ("Transistor_FET", "AO3400A", "AO3400A", "Package_TO_SOT_SMD:SOT-23", (264.16, 116.84), {"1": "GATE", "2": "GND", "3": "LED-"}),
    "R7": ("Device", "R", "1k", R0603, (236.22, 144.78), {"1": "STAT", "2": "STAT_A"}),
    "D4": ("Device", "LED", "GREEN", "LED_SMD:LED_0603_1608Metric", (254.0, 144.78), {"1": "GND", "2": "STAT_A"}),
}

NOTES = [
    ((20.32, 25.4), "1) Giris/koruma: PTC + TVS, D1/D2 diode-OR"),
    ((116.84, 25.4), "2) Buck 3.3V (AP63203, FB=VOUT)"),
    ((20.32, 101.6), "3) USB-C: ESP32-C3 dahili USB ile programlama"),
    ((20.32, 167.64), "4) EN RC + RESET, GPIO9 BOOT / kullanici butonu"),
    ((215.9, 99.06), "5) LED serit low-side MOSFET (PWM)"),
]
