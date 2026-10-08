<p align="center"><img src="../docs/logo/bilginier-logo.svg" width="160" alt="Bilginier"></p>

# Malzeme Listesi (BOM) — LED Controller rev A

Bir kart için 23 kalem ve toplam 32 parça gerekiyor. LCSC numaralarının hepsi Ekim 2026'da lcsc.com'da doğrulandı. Stok durumu sürekli değiştiği için sipariş öncesi yeniden kontrol et.

**Hangi dosyayı kullanmalısın:**

- **Elle sipariş:** `BOM.csv` (üretici parça numarası ve LCSC numarası birlikte).
- **JLCPCB montaj:** `fabrication/ledctl-bom-jlcpcb.csv` ve `fabrication/ledctl-cpl-jlcpcb.csv`. J4 bu listelerde yok, istersen elle lehimlenir.

## Aktif parçalar

| Adet | Ref | Değer | Açıklama | Kılıf | Üretici parça no | LCSC |
|---:|---|---|---|---|---|---|
| 1 | U2 | ESP32-C3-WROOM-02-N4 | WiFi/BLE modül, 4 MB flash, PCB anten | Modül | Espressif ESP32-C3-WROOM-02-N4 | [C2934560](https://www.lcsc.com/product-detail/C2934560.html) |
| 1 | U1 | AP63203WU | Senkron buck, 3.8–32 V → 3.3 V / 2 A | TSOT-23-6 | Diodes AP63203WU-7 | [C780769](https://www.lcsc.com/product-detail/C780769.html) |
| 1 | Q1 | AO3400A | N-MOSFET 30 V / 5.7 A, lojik seviye | SOT-23 | AOS AO3400A | [C20917](https://www.lcsc.com/product-detail/C20917.html) |
| 1 | D1 | SS34 | Schottky 40 V / 3 A (adaptör → buck) | SMA | MDD SS34 | [C8678](https://www.lcsc.com/product-detail/C8678.html) |
| 1 | D2 | SS14 | Schottky 40 V / 1 A (USB → buck) | SMA | MDD SS14 | [C2480](https://www.lcsc.com/product-detail/C2480.html) |
| 1 | D3 | SMAJ28A | TVS 28 V, tek yönlü | SMA | Jingdao SMAJ28A | [C353458](https://www.lcsc.com/product-detail/C353458.html) |
| 1 | D4 | Yeşil LED | Durum LED'i | 0603 | Everlight 19-217/GHC-YR1S2/3T | [C72043](https://www.lcsc.com/product-detail/C72043.html) ¹ |

## Pasifler

| Adet | Ref | Değer | Açıklama | Kılıf | Üretici parça no | LCSC |
|---:|---|---|---|---|---|---|
| 1 | L1 | 4.7 µH | Güç bobini, Isat 3.2 A, ekranlı | 4×4 mm | Changjiang FNR4030S4R7MT | [C167874](https://www.lcsc.com/product-detail/C167874.html) |
| 1 | F1 | PTC | Resetlenebilir sigorta | 1812 | **belirlenecek** ² | — |
| 1 | C1 | 10 µF 50 V | Buck giriş, X5R | 1206 | Samsung CL31A106KBHNNNE | [C13585](https://www.lcsc.com/product-detail/C13585.html) |
| 3 | C2, C3, C7 | 100 nF 50 V | Buck HF (C2), bootstrap (C3), modül (C7), X7R | 0603 | Yageo CC0603KRX7R9BB104 | [C14663](https://www.lcsc.com/product-detail/C14663.html) |
| 2 | C4, C5 | 22 µF 25 V | Buck çıkış, X5R | 0805 | Samsung CL21A226MAQNNNE | [C45783](https://www.lcsc.com/product-detail/C45783.html) |
| 1 | C6 | 10 µF 25 V | Modül besleme, X5R | 0805 | Samsung CL21A106KAYNNNE | [C15850](https://www.lcsc.com/product-detail/C15850.html) |
| 1 | C8 | 1 µF 50 V | EN RC gecikmesi, X5R | 0603 | Samsung CL10A105KB8NNNC | [C15849](https://www.lcsc.com/product-detail/C15849.html) ¹ |
| 4 | R1–R4 | 10 kΩ %1 | EN ve strapping pull-up'ları | 0603 | UNI-ROYAL 0603WAF1002T5E | [C25804](https://www.lcsc.com/product-detail/C25804.html) ¹ |
| 1 | R5 | 100 Ω %1 | Gate seri direnci | 0603 | UNI-ROYAL 0603WAF1000T5E | [C22775](https://www.lcsc.com/product-detail/C22775.html) |
| 1 | R6 | 100 kΩ %1 | Gate pull-down | 0603 | UNI-ROYAL 0603WAF1003T5E | [C25803](https://www.lcsc.com/product-detail/C25803.html) |
| 1 | R7 | 1 kΩ %1 | Durum LED'i direnci | 0603 | UNI-ROYAL 0603WAF1001T5E | [C21190](https://www.lcsc.com/product-detail/C21190.html) |
| 2 | R8, R9 | 5.1 kΩ %1 | USB-C CC pull-down | 0603 | UNI-ROYAL 0603WAF5101T5E | [C23186](https://www.lcsc.com/product-detail/C23186.html) |

## Elektromekanik

| Adet | Ref | Değer | Açıklama | Üretici parça no | LCSC |
|---:|---|---|---|---|---|
| 2 | J1, J2 | 2P, 5.08 mm | Vidalı klemens (J1 = 12–24 V giriş, J2 = LED şerit) | Phoenix Contact 1715721 | [C480516](https://www.lcsc.com/product-detail/C480516.html) |
| 1 | J3 | USB-C 16P | USB 2.0 Type-C dişi | HRO TYPE-C-31-M-12 | [C165948](https://www.lcsc.com/product-detail/C165948.html) |
| 1 | J4 | 1×4, 2.54 mm | UART header (opsiyonel, 1×40 şeritten kesilir) | BOOMELE 2.54-1*40P | [C2337](https://www.lcsc.com/product-detail/C2337.html) |
| 2 | SW1, SW2 | 5.1×5.1×1.5 mm | Tact switch (RESET / BOOT) | XKB TS-1187A-B-A-B | [C318884](https://www.lcsc.com/product-detail/C318884.html) |

## Kutu ve montaj

| Adet | Parça | Not |
|---:|---|---|
| 1 | Gövde (`enclosure/ledctl_case_base.stl`) | PETG veya PLA |
| 1 | Kapak (`enclosure/ledctl_case_lid.stl`) | Yüzü aşağı basılır, logo kazınmış |
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

## Notlar

¹ **Stok:** Bu parçalar kontrol sırasında LCSC mağazasında stokta yoktu ya da azdı. Hepsi yaygın parçalar, JLCPCB montaj stoğu ayrı tutulur. Yoksa aynı değer ve kılıfta başka bir parça kullanılabilir.

² **F1 (PTC sigorta):** 1812 kılıfta 24 V'a dayanıp 3 A taşıyan bir PTC bulunmuyor. 24 V sınıfı 1812 PTC'ler en fazla 1.5 A civarında kalıyor, 3 A olanlar ise 8 V'a kadar dayanıyor (örneğin C21004). Bu yüzden kalem şimdilik boş bırakıldı. Seçenekler:

- **Daha düşük akım:** 1.5 A / 24 V'luk bir 1812 PTC kullan. Şerit akımı da bununla sınırlı kalır.
- **Daha büyük kılıf:** 2920 kılıfta daha yüksek akımlı bir PTC kullan. Bunun için PCB'de footprint değişikliği gerekir.
- **Tek kullanımlık sigorta:** SMD bir eriyen sigorta kullan. Bu da PCB değişikliği gerektirir.

Prototip için F1 yerine 0 Ω köprü ya da kısa bir tel de konabilir, ama bu durumda aşırı akım koruması kalmaz.
