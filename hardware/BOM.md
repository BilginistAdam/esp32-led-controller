# Malzeme Listesi (BOM) — ESP32-C3 LED Kontrolcü rev A

Bir kart için 24 kalem ve toplam 32 parça gerekiyor. Pasifler 0603/0805/1206 SMD boyutunda. Örnek parça numarası "herhangi" olan kalemlerde açıklamadaki değerleri karşılayan her parça olur.

Makinede montaj yaptıracaksan `BOM.csv` ve `fabrication/ledctl-pos.csv` dosyalarını kullan.

## Aktif parçalar

| Adet | Ref | Değer | Açıklama | Kılıf | Örnek parça no |
|---:|---|---|---|---|---|
| 1 | U2 | ESP32-C3-WROOM-02-N4 | WiFi/BLE modül, 4 MB flash, PCB anten | Modül | Espressif ESP32-C3-WROOM-02-N4 |
| 1 | U1 | AP63203WU | Senkron buck, 3.8–32 V giriş → 3.3 V / 2 A | TSOT-23-6 | Diodes Inc. AP63203WU-7 |
| 1 | Q1 | AO3400A | N-MOSFET 30 V / 5.7 A, lojik seviye (LED şerit anahtarı) | SOT-23 | AOS AO3400A |
| 1 | D1 | SS34 | Schottky 40 V / 3 A (adaptör → buck) | SMA | SS34 |
| 1 | D2 | SS14 | Schottky 40 V / 1 A (USB VBUS → buck) | SMA | SS14 |
| 1 | D3 | SMAJ28A | TVS, 28 V, tek yönlü | SMA | SMAJ28A |
| 1 | D4 | Yeşil LED | Durum LED'i | 0603 | herhangi |

## Pasifler

| Adet | Ref | Değer | Açıklama | Kılıf |
|---:|---|---|---|---|
| 1 | L1 | 4.7 µH | Güç bobini, Isat ≥ 3 A, ekranlı | 4×4 mm (örn. Changjiang FNR4030S4R7MT) |
| 1 | F1 | PTC 3 A | Resetlenebilir sigorta, I_hold ≥ 3 A, V_max ≥ 30 V | 1812 |
| 1 | C1 | 10 µF 50 V | Buck giriş, X5R/X7R | 1206 |
| 1 | C2 | 100 nF 50 V | Buck giriş HF dekuplaj, X7R | 0603 |
| 2 | C3, C7 | 100 nF | Bootstrap (C3), modül dekuplaj (C7), ≥16 V | 0603 |
| 2 | C4, C5 | 22 µF 10 V | Buck çıkış, X5R/X7R | 0805 |
| 1 | C6 | 10 µF | Modül besleme, ≥10 V | 0805 |
| 1 | C8 | 1 µF | EN RC gecikmesi, ≥10 V | 0603 |
| 4 | R1–R4 | 10 kΩ | EN pull-up, strapping pull-up'ları (IO9/IO8/IO2) | 0603 |
| 1 | R5 | 100 Ω | MOSFET gate seri direnci | 0603 |
| 1 | R6 | 100 kΩ | Gate pull-down (boot'ta LED kapalı) | 0603 |
| 1 | R7 | 1 kΩ | Durum LED'i direnci | 0603 |
| 2 | R8, R9 | 5.1 kΩ %1 | USB-C CC1/CC2 pull-down | 0603 |

## Elektromekanik

| Adet | Ref | Değer | Açıklama | Örnek parça no |
|---:|---|---|---|---|
| 2 | J1, J2 | 2 pin, 5.08 mm | Vidalı klemens (J1 = 12–24 V giriş, J2 = LED şerit) | Phoenix Contact MKDS 1,5/2-5,08 (1715721) |
| 1 | J3 | USB-C 16P | USB 2.0 Type-C dişi, SMD + THT gövde | HRO TYPE-C-31-M-12 |
| 1 | J4 | 1×4, 2.54 mm | UART/debug pin header (opsiyonel, takılmayabilir) | herhangi |
| 2 | SW1, SW2 | 5.1×5.1 mm | Tact switch, 1.5 mm buton yüksekliği (RESET / BOOT) | XKB TS-1187A-B-A-B |

## Kutu ve montaj

| Adet | Parça | Not |
|---:|---|---|
| 1 | Gövde (`enclosure/ledctl_case_base.stl`) | PETG veya PLA |
| 1 | Kapak (`enclosure/ledctl_case_lid.stl`) | Yüzü aşağı basılır |
| 4 | M3 × 20 vida | Plastiğe yol açan tip, ya da M3 heat-set insert ile makine vidası |
| 2 | Duvar vidası + dübel | Başı en fazla 8 mm, gövdesi en fazla 4 mm (anahtar deliği için) |
| — | Çift taraflı bant | Opsiyonel, düz taban için |

## PCB

| Özellik | Değer |
|---|---|
| Ölçü | 64 × 38 mm |
| Katman | 2 |
| Kalınlık | 1.6 mm |
| Bakır | 1 oz |
| Min. iz / boşluk | 0.2 / 0.2 mm |
| Min. delik | 0.3 mm (via) |
| Üretim dosyası | `ledctl-gerbers.zip` |
