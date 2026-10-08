<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="docs/logo/banner-dark.svg">
    <img src="docs/logo/banner-light.svg" width="640" alt="LED Controller · Bilginier">
  </picture>
</p>

# LED Controller — ESP32-C3 LED Şerit Kontrolcüsü

12–24 V LED şeritleri WiFi üzerinden açıp kapatan ve PWM ile dimleyen küçük bir kontrol kartı. Proje KiCad donanım dosyalarını, iki firmware seçeneğini (ESPHome / PlatformIO) ve 3D yazıcıyla basılabilen bir kutuyu içerir.

![Kutu](docs/images/case_assembly.png)

| PCB üst | Şematik |
|---|---|
| ![PCB](docs/images/pcb_top.png) | ![Şematik](docs/images/schematic.png) |

## Özellikler

- **Kontrol:** ESP32-C3-WROOM-02 (WiFi + BLE). Programlama dahili USB üzerinden USB-C ile yapılıyor, ayrı bir USB-UART çipi yok.
- **Giriş:** 12–24 V DC. PTC sigorta ve TVS ile korunuyor. AP63203 buck regülatör 3.3 V üretiyor.
- **Besleme:** D1/D2 diyotlarıyla kart adaptörden **ya da** sadece USB'den beslenebiliyor, yani programlarken adaptör gerekmiyor.
- **LED sürme:** LED şeridini low-side AO3400A MOSFET anahtarlıyor. 20 kHz PWM kullanılıyor, böylece duyulabilir vızıltı olmuyor. Gate'teki pull-down sayesinde LED boot sırasında kapalı kalıyor.
- **Arayüz:** RESET butonu, BOOT/kullanıcı butonu ve durum LED'i var.
- **Kart:** 64 × 38 mm, 2 katman, 4 × M3 montaj deliği.

## Klasör yapısı

```
hardware/          KiCad projesi (şematik, PCB, proje sembol kütüphanesi)
  BOM.md / BOM.csv malzeme listesi (okunabilir tablo / üretici formatı)
  ledctl-gerbers.zip   üreticiye (JLCPCB/PCBWay vb.) doğrudan yüklenebilir
  fabrication/     Gerber, drill, pick-and-place (pos) dosyaları
  scripts/         şematik/PCB'yi üreten Python betikleri (design.py = tek kaynak)
firmware/
  esphome/         Home Assistant için ESPHome konfigürasyonu
  platformio/      bağımsız Arduino firmware'i (web arayüzü + REST API)
    prebuilt/      derlenmiş factory imajı (0x0 adresine yazılır)
enclosure/         OpenSCAD kaynak + basılmaya hazır STL'ler
docs/              şematik PDF, PCB montaj PDF'i, görseller
  logo/            Bilginier logosu (SVG) + üretici betik (PCB, kutu ve banner aynı kaynaktan)
```

## Malzeme listesi (BOM)

Ayrıntılı liste için [`hardware/BOM.md`](hardware/BOM.md), makineli montaj için [`hardware/BOM.csv`](hardware/BOM.csv) dosyasına bak.

| Adet | Ref | Parça | LCSC |
|---:|---|---|---|
| 1 | U2 | ESP32-C3-WROOM-02-N4 | C2934560 |
| 1 | U1 | AP63203WU-7 (3.3 V buck) | C780769 |
| 1 | Q1 | AO3400A | C20917 |
| 1 | L1 | FNR4030S4R7MT, 4.7 µH | C167874 |
| 1 / 1 / 1 | D1 / D2 / D3 | SS34 / SS14 / SMAJ28A | C8678 / C2480 / C353458 |
| 1 | D4 | Yeşil LED 0603 | C72043 |
| 1 | F1 | PTC 1812 (bkz. BOM.md notu) | — |
| 1 | C1 | 10 µF 50 V 1206 | C13585 |
| 3 | C2, C3, C7 | 100 nF 50 V 0603 | C14663 |
| 2 | C4, C5 | 22 µF 25 V 0805 | C45783 |
| 1 / 1 | C6 / C8 | 10 µF 0805 / 1 µF 0603 | C15850 / C15849 |
| 4 | R1–R4 | 10 kΩ 0603 | C25804 |
| 1 / 1 / 1 | R5 / R6 / R7 | 100 Ω / 100 kΩ / 1 kΩ 0603 | C22775 / C25803 / C21190 |
| 2 | R8, R9 | 5.1 kΩ 0603 | C23186 |
| 2 | J1, J2 | Phoenix 1715721, 2P 5.08 mm | C480516 |
| 1 | J3 | USB-C HRO TYPE-C-31-M-12 | C165948 |
| 1 | J4 | 1×4 pin header (opsiyonel) | C2337 |
| 2 | SW1, SW2 | TS-1187A-B-A-B | C318884 |
| 4 | — | M3 × 20 vida (kutu) | — |

JLCPCB montaj için hazır dosyalar: `hardware/fabrication/ledctl-bom-jlcpcb.csv` ve `ledctl-cpl-jlcpcb.csv`.

## Pin haritası

| GPIO | İşlev |
|---|---|
| IO4 | LED PWM → R5 → Q1 gate |
| IO9 | BOOT / kullanıcı butonu (aktif düşük) |
| IO10 | Durum LED'i (aktif yüksek) |
| IO18 / IO19 | USB D− / D+ (USB-C) |
| IO20 / IO21 | UART RX / TX (J4, opsiyonel) |

## Firmware

### Seçenek A: ESPHome (Home Assistant)

```bash
cd firmware/esphome
cp secrets.yaml.example secrets.yaml   # WiFi bilgilerini gir
esphome run ledctl.yaml                # ilk yükleme USB-C üzerinden
```

Bu seçenek Home Assistant'a "LED Serit" adlı, dimlenebilir bir ışık olarak eklenir. Butona basınca LED açılıp kapanır, durum LED'i WiFi bağlantısını gösterir.

### Seçenek B: PlatformIO (bağımsız)

```bash
cd firmware/platformio
pio run -t upload        # USB-C
pio device monitor
```

1. **WiFi kurulumu:** İlk açılışta kart `LedCtrl-Setup` adında bir WiFi ağı açar. Bu ağa bağlanıp açılan sayfadan kendi WiFi bilgilerini gir.
2. **Web arayüzü:** Kurulumdan sonra `http://led-ctrl.local` adresinden aç/kapat ve parlaklık ayarı yapılabilir.
3. **REST API:**
   ```bash
   curl http://led-ctrl.local/api/state
   curl -X POST http://led-ctrl.local/api/state -d '{"on":true,"brightness":60}'
   curl -X POST http://led-ctrl.local/api/toggle
   ```
4. **Buton:**
   - Kısa basış: aç/kapat
   - Basılı tutma: parlaklığı 100 → 75 → 50 → 25 → 10 sırasıyla değiştirir
   - 8 saniye basılı tutma: WiFi ayarlarını siler
5. **Durum LED'i:**
   - Sürekli yanık: bağlı
   - Yavaş yanıp sönme: bağlanıyor
   - Hızlı yanıp sönme: kurulum modunda
6. **Diğer:** Son durum NVS'e kaydedilir, elektrik kesilip gelince geri yüklenir. Ayrıca OTA güncelleme (ArduinoOTA) destekleniyor.

Hazır imajı yazmak için:

```bash
esptool.py --chip esp32c3 write_flash 0x0 firmware/platformio/prebuilt/ledctl-factory.bin
```

> **Yükleme başlamazsa:** **BOOT**'a basılı tutarken **RESET**'e bas ve bırak. Kart indirme moduna geçer. Normalde USB üzerinden otomatik reset yeterli olur.

## Kutu (3D baskı)

| Parça | Dosya | Baskı yönü |
|---|---|---|
| Gövde | `enclosure/ledctl_case_base.stl` | taban aşağıda |
| Kapak | `enclosure/ledctl_case_lid.stl` | yüzü aşağıda (dosya zaten bu yönde) |

- **Önerilen baskı ayarları:** PETG veya PLA, 0.2 mm katman, %20–30 doluluk. Destek gerekmiyor.
- **Montaj:** 4 adet **M3 × 20** vida kapaktan girer, PCB'yi sıkıştırır ve gövdedeki direklere tutunur. Vidalar plastiğe kendi yolunu açabilir; isteğe bağlı olarak `pilot_d = 4.0` ile heat-set insert de kullanılabilir.
- **Duvara montaj:** Tabanda 20 mm aralıklı iki anahtar deliği var, en fazla 8 mm başlı vida uygun. USB-C aşağı bakacak şekilde asılır.
- **Bantla montaj:** Taban tamamen düz olduğu için çift taraflı bantla da yapıştırılabilir.
- **Butonlar:** RESET ve BOOT butonları kapaktaki esnek dillerle basılır. Durum LED'inin ışığı kapaktaki tüpten görünür.
- **Terminaller:** Vidalarına kapaktaki deliklerden tornavidayla erişilir.
- **Ölçüler:** `enclosure/ledctl_case.scad` içindeki parametrelerden (tolerans, duvar kalınlığı, yükseklik) değiştirilebilir.

```bash
openscad -D 'part="base"' -o enclosure/ledctl_case_base.stl enclosure/ledctl_case.scad
openscad -D 'part="lid"'  -o enclosure/ledctl_case_lid.stl  enclosure/ledctl_case.scad
```

## Üretim

1. `hardware/ledctl-gerbers.zip` dosyasını PCB üreticisine yükle. Ayarlar: 2 katman, 1.6 mm, 1 oz bakır.
2. Montaj için `hardware/BOM.csv` (okunabilir hali: `hardware/BOM.md`) ve `hardware/fabrication/ledctl-pos.csv` dosyalarını kullan.
3. ESP modülünün anteni kartın sağ kenarından yaklaşık 6 mm dışarı taşar. Bu bilinçli bir tercih: antenin altında bakır olmaması gerekiyor. Kutu bu taşmaya göre tasarlandı.

## Tasarım notları ve sınırlar

- **Akım:** AO3400A ile kart yaklaşık **3 A** LED akımı için uygun. 24 V'ta bu yaklaşık 70 W, 12 V'ta yaklaşık 36 W eder. Daha yüksek akım için daha güçlü bir MOSFET kullanılmalı ve LED izleri genişletilmeli.
- **Gerilim:** AP63203 en fazla 32 V girişe dayanır. 24 V adaptörlerde sorun yok. TVS (SMAJ28A) kısa süreli darbelere karşı korur, ama sürekli aşırı gerilimden korumaz.
- **F1 sigorta:** 3 A / 24 V için 1812 kılıfta uygun bir PTC yok. Seçenekler [`hardware/BOM.md`](hardware/BOM.md) notunda anlatılıyor.
- **Routing:** İzler Freerouting ile otomatik çizildi. DRC'de elektriksel hata yok, sadece kozmetik silkscreen uyarıları var. Sipariş vermeden önce KiCad 8/9'da ERC ve DRC'yi kendin de çalıştır.
- **Yeniden üretme:** `hardware/scripts/` içindeki betikler şematik ve PCB'yi `design.py` ve `placement.py` dosyalarından üretir. Logo ve isim en son `add_branding.py` ile silkscreen'e eklenir. Bunun için KiCad 7+ Python (`pcbnew`) ve otomatik routing için Freerouting gerekir (`FREEROUTING_JAR` ortam değişkeni).

## Lisans

[MIT](LICENSE). Donanım dosyaları, firmware ve kutu dahil projenin tamamı bu lisansla yayınlanır.
