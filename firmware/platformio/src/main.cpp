// ESP32-C3 LED Strip Controller - standalone firmware
// Features: WiFi captive-portal setup, web UI, REST API, physical button,
//           smooth PWM dimming, state persistence, mDNS, ArduinoOTA.
#include <Arduino.h>
#include <WiFi.h>
#include <WebServer.h>
#include <ESPmDNS.h>
#include <ArduinoOTA.h>
#include <Preferences.h>
#include <WiFiManager.h>
#include <ArduinoJson.h>
#include "config.h"
#include "web_ui.h"

WebServer server(80);
Preferences prefs;

// ------------------------------------------------------------------ state
struct State {
  bool on = false;
  uint8_t brightness = 100;  // percent, 1..100
} state;

static float currentDuty = 0;  // 0..1, what is on the pin now
static float startDuty = 0, targetDuty = 0;
static uint32_t fadeStart = 0;
static bool dirty = false;
static uint32_t dirtySince = 0;

// perceptual (gamma 2.2) brightness -> duty
static float pctToDuty(uint8_t pct) { return powf(pct / 100.0f, 2.2f); }

static void writeDuty(float d) {
  const uint32_t maxv = (1u << PWM_BITS) - 1;
  ledcWrite(PWM_CHANNEL, (uint32_t)lroundf(constrain(d, 0.0f, 1.0f) * maxv));
}

static void applyState() {
  startDuty = currentDuty;
  targetDuty = state.on ? pctToDuty(state.brightness) : 0.0f;
  fadeStart = millis();
  dirty = true;
  dirtySince = millis();
}

static void fadeLoop() {
  if (currentDuty == targetDuty) return;
  float t = (millis() - fadeStart) / (float)FADE_MS;
  currentDuty = t >= 1.0f ? targetDuty : startDuty + (targetDuty - startDuty) * t;
  writeDuty(currentDuty);
}

static void saveLoop() {
  if (dirty && millis() - dirtySince > SAVE_DELAY_MS) {
    prefs.putBool("on", state.on);
    prefs.putUChar("bri", state.brightness);
    dirty = false;
  }
}

static void setOn(bool on) { state.on = on; applyState(); }
static void toggle() { setOn(!state.on); }
static void setBrightness(int pct) {
  state.brightness = (uint8_t)constrain(pct, 1, 100);
  applyState();
}

// ------------------------------------------------------------------ button
// short press: toggle | hold: cycle brightness 100->75->50->25->10 | 8 s: WiFi reset
static void buttonLoop() {
  static bool lastRaw = true, stable = true;
  static uint32_t changedAt = 0, pressedAt = 0;
  static bool longFired = false;
  bool raw = digitalRead(PIN_BUTTON);  // HIGH = released
  uint32_t now = millis();
  if (raw != lastRaw) { lastRaw = raw; changedAt = now; }
  if (now - changedAt < BUTTON_DEBOUNCE_MS || raw == stable) {
    if (!stable && !longFired && now - pressedAt > BUTTON_LONG_MS) {
      static const uint8_t steps[] = {100, 75, 50, 25, 10};
      size_t i = 0;
      while (i < sizeof(steps) && steps[i] > state.brightness) i++;
      state.brightness = steps[(i + 1) % sizeof(steps)];
      state.on = true;
      applyState();
      longFired = true;
    }
    if (!stable && now - pressedAt > BUTTON_RESET_MS) {
      Serial.println("[btn] WiFi reset");
      for (int i = 0; i < 10; i++) { digitalWrite(PIN_STATUS, i & 1); delay(100); }
      WiFiManager wm;
      wm.resetSettings();
      ESP.restart();
    }
    return;
  }
  stable = raw;
  if (!stable) { pressedAt = now; longFired = false; }
  else if (!longFired) toggle();  // released before long-press
}

// ------------------------------------------------------------------ status LED
// solid = connected, slow blink = connecting, fast blink = setup portal
enum class Net { Connecting, Portal, Online } net = Net::Connecting;
static void statusLoop() {
  uint32_t ms = millis();
  bool v = net == Net::Online ? true : net == Net::Portal ? (ms / 150) & 1 : (ms / 600) & 1;
  digitalWrite(PIN_STATUS, v);
}

// ------------------------------------------------------------------ web
static void sendState() {
  JsonDocument doc;
  doc["on"] = state.on;
  doc["brightness"] = state.brightness;
  doc["rssi"] = WiFi.RSSI();
  doc["ip"] = WiFi.localIP().toString();
  doc["uptime_s"] = millis() / 1000;
  String out;
  serializeJson(doc, out);
  server.send(200, "application/json", out);
}

static void handlePost() {
  JsonDocument doc;
  if (deserializeJson(doc, server.arg("plain"))) {
    server.send(400, "application/json", "{\"error\":\"invalid json\"}");
    return;
  }
  if (doc["brightness"].is<int>()) state.brightness = constrain((int)doc["brightness"], 1, 100);
  if (doc["on"].is<bool>()) state.on = doc["on"];
  if (doc["toggle"] | false) state.on = !state.on;
  applyState();
  sendState();
}

static void setupWeb() {
  server.on("/", HTTP_GET, [] { server.send_P(200, "text/html", INDEX_HTML); });
  server.on("/api/state", HTTP_GET, sendState);
  server.on("/api/state", HTTP_POST, handlePost);
  server.on("/api/toggle", HTTP_POST, [] { toggle(); sendState(); });
  server.onNotFound([] { server.send(404, "text/plain", "not found"); });
  server.begin();
}

// ------------------------------------------------------------------ setup/loop
void setup() {
  // LED off as early as possible (gate also has a 100k pull-down)
  ledcSetup(PWM_CHANNEL, PWM_FREQ_HZ, PWM_BITS);
  ledcAttachPin(PIN_LED_PWM, PWM_CHANNEL);
  writeDuty(0);
  pinMode(PIN_BUTTON, INPUT_PULLUP);
  pinMode(PIN_STATUS, OUTPUT);

  Serial.begin(115200);
  prefs.begin("ledctl", false);
  state.on = prefs.getBool("on", false);
  state.brightness = prefs.getUChar("bri", 100);
  applyState();
  dirty = false;

  WiFi.setHostname(HOSTNAME);
  WiFiManager wm;
  wm.setConfigPortalBlocking(false);
  wm.setAPCallback([](WiFiManager*) { net = Net::Portal; });
  if (!wm.autoConnect(AP_NAME)) {
    // portal running: keep LED + button working until configured
    while (WiFi.status() != WL_CONNECTED) {
      wm.process();
      buttonLoop(); fadeLoop(); saveLoop(); statusLoop();
      delay(2);
    }
  }
  net = Net::Online;
  Serial.printf("[wifi] %s  http://%s.local\n", WiFi.localIP().toString().c_str(), HOSTNAME);

  MDNS.begin(HOSTNAME);
  MDNS.addService("http", "tcp", 80);
  ArduinoOTA.setHostname(HOSTNAME);
  ArduinoOTA.begin();
  setupWeb();
}

void loop() {
  server.handleClient();
  ArduinoOTA.handle();
  buttonLoop();
  fadeLoop();
  saveLoop();
  net = WiFi.status() == WL_CONNECTED ? Net::Online : Net::Connecting;
  statusLoop();
  delay(1);
}
