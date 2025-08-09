# GhostMac – MAC Address Changer

GhostMac, Linux əməliyyat sistemlərində şəbəkə interfeyslərinin MAC ünvanını dəyişdirmək, təsadüfi MAC ünvanı generasiya etmək və orijinal MAC ünvanını bərpa etmək üçün hazırlanmış yüngül və funksional alətdir. Layihə həm komanda sətri interfeysi (CLI), həm də mətn əsaslı istifadəçi interfeysi (TUI) təqdim edir.

## Xüsusiyyətlər
- **CLI rejimi** – `main.py` vasitəsilə birbaşa komanda sətrindən idarəetmə
- **TUI rejimi** – `tui.py` vasitəsilə interaktiv menyu
- Orijinal MAC ünvanının avtomatik ehtiyat nüsxələnməsi
- Təsadüfi MAC ünvanı generasiyası
- MAC ünvanı dəyişikliklərinin log faylında saxlanması
- Sadə və təhlükəsiz işləmə prinsipi

---

## Quraşdırma
```bash
# Repository-ni klonlayın
git clone https://github.com/<istifadəçi_adı>/GhostMac.git
cd GhostMac

# Asılılıqları quraşdırın
pip install colorama
```

---

## İstifadə

### 1. CLI versiyası (`main.py`)
```bash
# MAC ünvanını dəyişmək
sudo python3 main.py -i eth0 -m 00:11:22:33:44:55

# Təsadüfi MAC ünvanı təyin etmək
sudo python3 main.py -i eth0 --random

# Orijinal MAC ünvanına qaytarmaq
sudo python3 main.py -i eth0 --reset
```

---

### 2. TUI versiyası (`tui.py`)
```bash
sudo python3 tui.py
```
Menyu vasitəsilə:
1. MAC ünvanını dəyişmək (manual və ya təsadüfi)
2. Cari MAC ünvanını göstərmək
3. Log faylını görüntüləmək
4. Orijinal MAC ünvanını bərpa etmək
0. Proqramdan çıxmaq

---

## Fayl Strukturu
```
GhostMac/
│── main.py           # CLI versiyası
│── tui.py            # Terminal UI versiyası
│── README.md         # Layihə haqqında sənəd
└── requirements.txt  # Asılılıqlar
```

---

## Qeydlər
- Alət yalnız **Linux** mühitində test edilmişdir.
- MAC ünvanını dəyişmək üçün `sudo` icazəsi tələb olunur.
- Dəyişikliklər `~/.ghostmac/macchanger.log` faylında saxlanılır.
- Orijinal MAC ünvanı ehtiyat nüsxə olaraq `~/.ghostmac/<interface>_original_mac.txt` və ya `~/.original_mac.txt` faylında saxlanılır.

