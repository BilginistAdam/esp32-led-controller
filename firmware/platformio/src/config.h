#pragma once

// ---- Pin map (hardware rev A, see hardware/ledctl.kicad_sch) ----
constexpr int PIN_LED_PWM = 4;   // IO4 -> R5 -> Q1 (AO3400A) gate, low-side switch
constexpr int PIN_BUTTON  = 9;   // IO9 BOOT button (SW2), active low, R2 pull-up
constexpr int PIN_STATUS  = 10;  // IO10 -> R7 -> D4 green status LED, active high

// ---- PWM ----
constexpr uint32_t PWM_FREQ_HZ  = 20000;  // above audible range, no coil whine
constexpr uint8_t  PWM_BITS     = 10;     // 0..1023
constexpr uint8_t  PWM_CHANNEL  = 0;

// ---- Behaviour ----
constexpr uint32_t FADE_MS            = 300;    // on/off/brightness transition
constexpr uint32_t BUTTON_DEBOUNCE_MS = 30;
constexpr uint32_t BUTTON_LONG_MS     = 800;    // hold: dim cycle
constexpr uint32_t BUTTON_RESET_MS    = 8000;   // hold 8 s: forget WiFi & reboot
constexpr uint32_t SAVE_DELAY_MS      = 2000;   // debounce NVS writes

constexpr const char* HOSTNAME = "led-ctrl";
constexpr const char* AP_NAME  = "LedCtrl-Setup";   // captive portal SSID
