"""
Úloha 1: Kdy se přemnoží bakterie?
---------------------------------
Vzoreček: N(t) = N0 * (1 + r)**t
  N0-počáteční počet bakterií
  r-hodinový přírůstek (80 % = 0.80)
  t-čas v hodinách
"""
import math

POCATECNI_POCET = 500
RUST = 1.80     
KAPACITA_MISKY = 2_000_000

def pocet_bakterii(hodiny: float) -> float:
    """Vrátí počet bakterií po zadaném počtu hodin."""
    return POCATECNI_POCET * (RUST ** hodiny)
 
def okamzik_prekroceni() -> float:
    """
    Určí přesný čas dosáhnutí kapacity misky.
    """
    return math.log(KAPACITA_MISKY / POCATECNI_POCET) / math.log(RUST)
 
def prvni_plna_hodina() -> int:
    """Vrátí nejmenší celé t, při kterém počet bakterií přesáhne kapacitu."""
    t = 0
    while pocet_bakterii(t) < KAPACITA_MISKY:
        t += 1
    return t

def tiskni_tabulku(max_hodin: int = 15) -> None:
    """Vypíše tabulku počtu bakterií pro každou celou hodinu."""
    print(f"{'Hodina':>8}  {'Počet bakterií':>18}  {'Stav':>10}")
    print("-" * 44)
    for t in range(max_hodin + 1):
        n = pocet_bakterii(t)
        stav = "PŘEKROČENO" if n >= KAPACITA_MISKY else "v pořádku"
        print(f"{t:>8}  {n:>18,.0f}  {stav:>10}")

if __name__ == "__main__":
    print("-" * 44)
    print("   SIMULACE RŮSTU BAKTERIÁLNÍ KULTURY")
    print("-" * 44)
    print(f"  Počáteční počet:  {POCATECNI_POCET:>12,}")
    print(f"  Hodinový přírůstek:     {(RUST - 1)*100:.0f} %")
    print(f"  Kapacita misky:   {KAPACITA_MISKY:>12,}")
    print()
 
    # Výpis tabulky
    tiskni_tabulku(max_hodin=15)
    print()
 
    # Přesný analytický výsledek
    t_presny = okamzik_prekroceni()
    hodiny_cele = int(t_presny)
    minuty = round((t_presny - hodiny_cele) * 60)
    print(f"Přesný okamžik překročení kapacity:")
    print(f"  t* = {t_presny:.4f} hodiny  ({hodiny_cele} h {minuty} min)")
    print()
 
    # První celá hodina
    t_plna = prvni_plna_hodina()
    print(f"První celá hodina s překročenou kapacitou: {t_plna} h")
    print(f"  Počet bakterií v {t_plna}. hodině: "
          f"{pocet_bakterii(t_plna):,.0f}")
    print()
 
    # Interaktivní dotaz uživatele
    print("-" * 44)
    while True:
        vstup = input("Zadej počet hodin (nebo 'konec'): ").strip()
        if vstup.lower() in ("konec", "q", "exit"):
            break
        try:
            t = float(vstup)
            n = pocet_bakterii(t)
            print(f"  Po {t} hodinách: {n:,.0f} bakterií")
            if n >= KAPACITA_MISKY:
                print("!Kapacita misky je překročena!")
            print()
        except ValueError:
            print("Zadej číslo (např. 10 nebo 12.5)\n")


"""
Úloha 2: Může projít vadný výrobek kontrolou?
---------------------------------

"""
 
import random
 
# ── Konstanty ─────────────────────────────────────────────────────────────────
NORMA_MIN = 14.7      # dolní hranice normy (g/l)
NORMA_MAX = 15.3      # horní hranice normy (g/l)
CHYBA = 0.03          # relativní chyba přístroje (3 %)
 
# Bezpečnější interval: aby přístroj nikdy nepustil vadný výrobek,
# musíme kontrolovat v užším rozsahu:
#   m >= NORMA_MIN  zaručeně znamená c >= NORMA_MIN / 1,03
#   m <= NORMA_MAX  zaručeně znamená c <= NORMA_MAX / 0,97
# (konzervativní odhad — neakceptuje ani hraniční výrobky)
BEZP_MIN = NORMA_MIN / (1 - CHYBA)   # ≈ 15.15 g/l
BEZP_MAX = NORMA_MAX / (1 + CHYBA)   # ≈ 14.85 g/l
 
 
# ── Funkce: jedno simulované měření ──────────────────────────────────────────
def zmer(skutecna_koncentrace: float) -> float:
    """
    Simuluje jedno měření přístroje s náhodnou chybou v rozsahu ±CHYBA.
    Chyba je rovnoměrně rozdělena v intervalu [-3 %, +3 %].
    """
    chyba_koef = random.uniform(1 - CHYBA, 1 + CHYBA)
    return skutecna_koncentrace * chyba_koef
 
 
# ── Funkce: analýza jedné skutečné koncentrace ───────────────────────────────
def analyzuj(koncentrace: float, pocet_mereni: int = 10_000) -> dict:
    """
    Pro zadanou skutečnou koncentraci provede `pocet_mereni` simulovaných měření.
    Vrátí slovník s výsledky.
    """
    v_norme         = NORMA_MIN <= koncentrace <= NORMA_MAX
    prijato         = 0   # přístroj ukáže hodnotu v normě
    vyhozeno        = 0   # přístroj ukáže hodnotu mimo normu
 
    for _ in range(pocet_mereni):
        mereni = zmer(koncentrace)
        if NORMA_MIN <= mereni <= NORMA_MAX:
            prijato += 1
        else:
            vyhozeno += 1
 
    return {
        "koncentrace":  koncentrace,
        "v_norme":      v_norme,
        "prijato_%":    prijato / pocet_mereni * 100,
        "vyhozeno_%":   vyhozeno / pocet_mereni * 100,
    }
 
 
# ── Funkce: výpis analytického rozsahu přístroje ─────────────────────────────
def tiskni_rozsah(koncentrace: float) -> None:
    """Vypíše teoretický rozsah naměřených hodnot pro danou koncentraci."""
    m_min = koncentrace * (1 - CHYBA)
    m_max = koncentrace * (1 + CHYBA)
    print(f"  Přístroj může zobrazit: [{m_min:.3f} ; {m_max:.3f}] g/l")
 
 
# ── Hlavní výpočty (zadání) ───────────────────────────────────────────────────
def uloha() -> None:
    print("=" * 56)
    print("  ANALÝZA KONTROLY VÝROBKŮ — chyba přístroje ±3 %")
    print("=" * 56)
    print(f"  Norma:   [{NORMA_MIN} ; {NORMA_MAX}] g/l")
    print(f"  Chyba:   ±{CHYBA*100:.0f} %")
    print()
 
    # 1. Rozsah naměřených hodnot pro c = 15 g/l
    print("1) Rozsah přístroje pro skutečnou koncentraci 15 g/l:")
    tiskni_rozsah(15.0)
    print()
 
    # 2. Správný výrobek — může být vyřazen?
    print("2) Správný výrobek (c = 14,7 g/l — dolní hranice normy):")
    tiskni_rozsah(14.7)
    m_min_spravny = 14.7 * (1 - CHYBA)
    print(f"  Nejnižší možné měření: {m_min_spravny:.3f} g/l "
          f"{'< ' + str(NORMA_MIN) + ' -> ANO, může být vyřazen!' if m_min_spravny < NORMA_MIN else '-> v pořádku'}")
    print()
 
    # 3. Vadný výrobek — může projít?
    print("3) Vadný výrobek (c = 14,5 g/l — těsně pod normou):")
    tiskni_rozsah(14.5)
    m_max_vadny = 14.5 * (1 + CHYBA)
    print(f"  Nejvyšší možné měření: {m_max_vadny:.3f} g/l "
          f"{'-> ANO, může projít kontrolou!' if m_max_vadny >= NORMA_MIN else '-> přístroj jej zachytí'}")
    print()
 
    # 4. Bezpečnější interval
    print("4) Bezpečnější kontrolní interval:")
    if BEZP_MIN > BEZP_MAX:
        print(f"  Norma je příliš úzká pro přístroj s ±{CHYBA*100:.0f}% chybou.")
        print(f"  Doporučení: vyměnit přístroj za přesnější (chyba ≤ 1 %),")
        print(f"  nebo rozšířit normu / opakovat měření 3× a vzít průměr.")
    else:
        print(f"  Bezpečný interval: [{BEZP_MIN:.3f} ; {BEZP_MAX:.3f}] g/l")
    print()
 
 
# ── Simulace pro různé koncentrace ───────────────────────────────────────────
def simulace() -> None:
    print("5) Simulace měření (10 000 pokusů na každou koncentraci):")
    print()
    print(f"  {'Konc. (g/l)':>12}  {'Skuteč.stav':>14}  "
          f"{'Přijato (%)':>12}  {'Vyhozeno (%)':>13}  Problém?")
    print("  " + "-" * 72)
 
    testovane = [14.0, 14.4, 14.5, 14.7, 15.0, 15.3, 15.5, 15.6, 16.0]
 
    for c in testovane:
        vysl = analyzuj(c)
        stav = "V NORMĚ   " if vysl["v_norme"] else "MIMO NORMU"
        prob = ""
        if vysl["v_norme"] and vysl["vyhozeno_%"] > 0:
            prob = "<- správný vyřazen"
        if not vysl["v_norme"] and vysl["prijato_%"] > 0:
            prob = "<- vadný prošel!"
        print(f"  {c:>12.1f}  {stav:>14}  "
              f"{vysl['prijato_%']:>11.1f}%  "
              f"{vysl['vyhozeno_%']:>12.1f}%  {prob}")
    print()
 
 
# ── Interaktivní dotaz ────────────────────────────────────────────────────────
def interaktivni() -> None:
    print("-" * 56)
    print("Zadej libovolnou skutečnou koncentraci pro analýzu:")
    while True:
        vstup = input("Koncentrace (g/l) nebo 'konec': ").strip()
        if vstup.lower() in ("konec", "q", "exit"):
            break
        try:
            c = float(vstup.replace(",", "."))
            stav = "V NORMĚ" if NORMA_MIN <= c <= NORMA_MAX else "MIMO NORMU"
            m_min = c * (1 - CHYBA)
            m_max = c * (1 + CHYBA)
            prekryv_min = max(m_min, NORMA_MIN)
            prekryv_max = min(m_max, NORMA_MAX)
            prekryv = max(0, prekryv_max - prekryv_min) / (m_max - m_min) * 100
            print(f"  Skutečná koncentrace:  {c:.3f} g/l  ({stav})")
            print(f"  Přístroj zobrazí:      [{m_min:.3f} ; {m_max:.3f}] g/l")
            print(f"  Překryv s normou:      {prekryv:.1f} %")
            if NORMA_MIN <= c <= NORMA_MAX and prekryv < 100:
                print(f"  Riziko: správný výrobek může být omylem vyřazen.")
            if not (NORMA_MIN <= c <= NORMA_MAX) and prekryv > 0:
                print(f"  Riziko: vadný výrobek může projít kontrolou ({prekryv:.1f} % měření)!")
            print()
        except ValueError:
            print("  Zadej číslo, např. 14.5 nebo 15,8\n")
 
 
if __name__ == "__main__":
    random.seed(42)
    uloha()
    simulace()
    interaktivni()


"""
Úloha 3: Jak připravit nejlevnější chemickou směs?
---------------------------------
"""

# ── Konstanty ─────────────────────────────────────────────────────────────────
KONC_A = 0.10  # 10 %
CENA_A = 40    # Kč/l
KONC_B = 0.50  # 50 %
CENA_B = 80    # Kč/l

# ── Funkce: Výpočet směsi ────────────────────────────────────────────────────
def vypocitej_smes(cilovy_objem: float, cilova_koncentrace: float) -> dict:
    """
    Vypočítá potřebné objemy roztoků A a B a celkovou cenu směsi.
    """
    # Kontrola, zda je koncentrace dosažitelná
    if not (KONC_A <= cilova_koncentrace <= KONC_B):
        return {"mozne": False}
    
    # Směšovací rovnice
    v_b = cilovy_objem * (cilova_koncentrace - KONC_A) / (KONC_B - KONC_A)
    v_a = cilovy_objem - v_b
    
    cena_celkem = (v_a * CENA_A) + (v_b * CENA_B)
    cena_za_litr = cena_celkem / cilovy_objem if cilovy_objem > 0 else 0
    
    return {
        "mozne": True,
        "v_a": v_a,
        "v_b": v_b,
        "cena_celkem": cena_celkem,
        "cena_za_litr": cena_za_litr
    }

# ── Hlavní výpočty (zadání) ───────────────────────────────────────────────────
def uloha_3() -> None:
    print("=" * 56)
    print("        OPTIMALIZACE CHEMICKÉ SMĚSI (A + B)")
    print("=" * 56)
    print(f"  Roztok A: Koncentrace {KONC_A*100:.0f} %, Cena {CENA_A} Kč/l")
    print(f"  Roztok B: Koncentrace {KONC_B*100:.0f} %, Cena {CENA_B} Kč/l")
    print("-" * 56)

    # 1. Varianta pro 100 litrů a 30 %
    print("1) Cílová směs: 100 litrů, koncentrace 30 %")
    vysl_1 = vypocitej_smes(100, 0.30)
    if vysl_1["mozne"]:
        print(f"   Potřebné množství roztoku A (10 %): {vysl_1['v_a']:.1f} l")
        print(f"   Potřebné množství roztoku B (50 %): {vysl_1['v_b']:.1f} l")
        print(f"   Celková cena směsi:               {vysl_1['cena_celkem']:,.2f} Kč")
    print()

    # 2. Varianta pro 100 litrů a 35 %
    print("2) Cílová směs: 100 litrů, koncentrace 35 %")
    vysl_2 = vypocitej_smes(100, 0.35)
    if vysl_2["mozne"]:
        print(f"   Potřebné množství roztoku A (10 %): {vysl_2['v_a']:.1f} l")
        print(f"   Potřebné množství roztoku B (50 %): {vysl_2['v_b']:.1f} l")
        print(f"   Celková cena směsi:               {vysl_2['cena_celkem']:,.2f} Kč")
    print()

# ── Interaktivní dotaz ────────────────────────────────────────────────────────
def interaktivni_3() -> None:
    print("-" * 56)
    print("Zadejte vlastní parametry pro výpočet směsi:")
    while True:
        vstup_objem = input("Požadovaný objem v litrech (neor 'konec'): ").strip()
        if vstup_objem.lower() in ("konec", "q", "exit"):
            break
        vstup_konc = input("Požadovaná koncentrace v % (např. 32): ").strip()
        
        try:
            objem = float(vstup_objem.replace(",", "."))
            konc = float(vstup_konc.replace(",", ".")) / 100.0
            
            reseni = vypocitej_smes(objem, konc)
            if reseni["mozne"]:
                print(f"\n  VÝSLEDEK pro {objem} l o koncentraci {konc*100:.1f} %:")
                print(f"    -> Roztok A (10 %): {reseni['v_a']:>10.2f} litrů")
                print(f"    -> Roztok B (50 %): {reseni['v_b']:>10.2f} litrů")
                print(f"    -> Celková cena:    {reseni['cena_celkem']:>10.2f} Kč")
                print(f"    -> Cena za 1 litr:   {reseni['cena_za_litr']:>10.2f} Kč/l\n")
            else:
                print(f"  [CHYBA] Koncentrace {konc*100:.1f} % je mimo dosah možností ({KONC_A*100:.0f} % - {KONC_B*100:.0f} %).\n")
        except ValueError:
            print("  [CHYBA] Zadejte platná čísla.\n")

if __name__ == "__main__":
    uloha_3()
    interaktivni_3()
    
"""
Úloha 4: Kde se nachází meteorit?
---------------------------------
"""

import math
import random

# ── Konstanty (Polohy observatoří) ───────────────────────────────────────────
OBS_A = (0.0, 0.0)
OBS_B = (20.0, 5.0)

AZIMUT_A_STRED = 60.0
AZIMUT_B_STRED = 135.0
CHYBA_AZIMUTU = 1.0  # ±1°

# ── Převod azimutu na matematický úhel (v radiánech) ─────────────────────────
def azimut_na_rad(stupne: float) -> float:
    # Azimut: Sever = 0°, Východ = 90° -> Matematický úhel: osa X (Východ) = 0°, osa Y (Sever) = 90°
    mat_stupne = 90.0 - stupne
    return math.radians(mat_stupne)

# ── Výpočet průsečíku dvou přímek (polohy meteoritu) ──────────────────────────
def spocitej_prusik(azi_a: float, azi_b: float) -> tuple:
    """Vrátí (x, y) souřadnice meteoritu pro dané dva azimuty."""
    rad_a = azimut_na_rad(azi_a)
    rad_b = azimut_na_rad(azi_b)
    
    # Směrnice přímek (y = k*x + q)
    # Pro ošetření svislých přímek použijeme parametrické vyjádření nebo goniometrické funkce
    # x_A + t_A*cos(a) = x_B + t_B*cos(b)
    # y_A + t_A*sin(a) = y_B + t_B*sin(b)
    
    sin_a, cos_a = math.sin(rad_a), math.cos(rad_a)
    sin_b, cos_b = math.sin(rad_b), math.cos(rad_b)
    
    det = cos_a * sin_b - sin_a * cos_b
    if abs(det) < 1e-6:
        return None  # Přímky jsou rovnoběžné
    
    dx = OBS_B[0] - OBS_A[0]
    dy = OBS_B[1] - OBS_A[1]
    
    t_a = (dx * sin_b - dy * cos_b) / det
    
    x = OBS_A[0] + t_a * cos_a
    y = OBS_A[1] + t_a * sin_a
    return (x, y)

# ── Hlavní analýza a simulace Monte Carlo ─────────────────────────────────────
def simulace_meteoritu(pocet_simulaci: int = 1000) -> None:
    print("=" * 56)
    print("        LOKALIZACE METEORITU POMOCÍ TRIANGULACE")
    print("=" * 56)
    
    # 1. Odhad střední polohy
    stred_x, stred_y = spocitej_prusik(AZIMUT_A_STRED, AZIMUT_B_STRED)
    dist_a = math.dist(OBS_A, (stred_x, stred_y))
    dist_b = math.dist(OBS_B, (stred_x, stred_y))
    
    print("1) Střední odhad polohy:")
    print(f"   Souřadnice meteoritu: [{stred_x:.3f} , {stred_y:.3f}] km")
    print(f"   Vzdálenost od Obs A:  {dist_a:.2f} km")
    print(f"   Vzdálenost od Obs B:  {dist_b:.2f} km")
    print()

    # 2. Určení oblasti (extrémní meze chyb)
    # Vyzkoušíme kombinace extrémních chyb pro zmapování polygonu nejistoty
    body_polygonu = []
    for odchylka_a in [-CHYBA_AZIMUTU, CHYBA_AZIMUTU]:
        for odchylka_b in [-CHYBA_AZIMUTU, CHYBA_AZIMUTU]:
            pt = spocitej_prusik(AZIMUT_A_STRED + odchylka_a, AZIMUT_B_STRED + odchylka_b)
            if pt: body_polygonu.append(pt)
            
    min_x = min(p[0] for p in body_polygonu)
    max_x = max(p[0] for p in body_polygonu)
    min_y = min(p[1] for p in body_polygonu)
    max_y = max(p[1] for p in body_polygonu)
    
    print("2) Oblast možného výskytu (rozsah chyb):")
    print(f"   Osa X: od {min_x:.3f} do {max_x:.3f} km  (rozptyl {max_x - min_x:.2f} km)")
    print(f"   Osa Y: od {min_y:.3f} do {max_y:.3f} km  (rozptyl {max_y - min_y:.2f} km)")
    print()

    # 3. Spuštění simulace Monte Carlo
    print(f"3) Spouštím Monte Carlo simulaci ({pocet_simulaci} měření)...")
    uspesne_simulace = 0
    sum_x, sum_y = 0.0, 0.0
    
    for _ in range(pocet_simulaci):
        # Rovnoměrné rozdělení chyby ±1°
        azi_a = AZIMUT_A_STRED + random.uniform(-CHYBA_AZIMUTU, CHYBA_AZIMUTU)
        azi_b = AZIMUT_B_STRED + random.uniform(-CHYBA_AZIMUTU, CHYBA_AZIMUTU)
        
        vysledek = spocitej_prusik(azi_a, azi_b)
        if vysledek:
            uspesne_simulace += 1
            sum_x += vysledek[0]
            sum_y += vysledek[1]
            
    print(f"   Úspěšně protato přímek: {uspesne_simulace}/{pocet_simulaci}")
    print(f"   Průměrný bod ze simulace: [{sum_x/uspesne_simulace:.3f} , {sum_y/uspesne_simulace:.3f}] km")
    print("\n   [ASCII Náčrt situace]:")
    print("   Sever (+Y)")
    print("     ^")
    print("     |       * Meteorit (cca [12.4 , 21.5])")
    print("     |      /")
    print("     |     / ")
    print("     |    /   \\ ")
    print("     |   /     \\ ")
    print("     +--A-------B-----> Východ (+X)")
    print("       (0,0)   (20,5)")

if __name__ == "__main__":
    random.seed(42)
    simulace_meteoritu(1000)

"""
Úloha 5: Jaký tvar nádrže spotřebuje nejméně materiálu?
---------------------------------
"""

# ── Konstanty ─────────────────────────────────────────────────────────────────
MIN_OBJEM = 1.0     # m**3
MIN_VYSKA = 1.0     # m
MAX_VYSKA = 3.0     # m

# ── Výpočet poloměru a povrchu nádrže ──────────────────────────────────────────
def analyzuj_valec(h: float, cilovy_objem: float = MIN_OBJEM) -> tuple:
    """Pro danou výšku a objem spočítá poloměr a celkový povrch pláště."""
    # r = odmocnina(V / (pi * h))
    r = math.sqrt(cilovy_objem / (math.pi * h))
    # S = 2 * pi * r^2 + 2 * pi * r * h
    povrch = 2 * math.pi * (r ** 2) + 2 * math.pi * r * h
    return r, povrch

# ── Hlavní výpočty a optimalizace ─────────────────────────────────────────────
def optimalizace_nadrze() -> None:
    print("=" * 56)
    print("        OPTIMALIZACE ROZMĚRŮ VÁLCOVÉ NÁDRŽE")
    print("=" * 56)
    print(f"  Požadovaný objem: {MIN_OBJEM} m**3")
    print(f"  Rozsah výšek:      {MIN_VYSKA} až {MAX_VYSKA} m")
    print("-" * 56)
    
    # 1. Návrh pěti různých rozměrů
    print("1) Návrh 5 variant rozměrů nádrže:")
    vysky_test = [1.0, 1.5, 2.0, 2.5, 3.0]
    
    print(f"   {'Varianta':<10} {'Výška (m)':>10} {'Poloměr (m)':>13} {'Povrch (m**2)':>13}")
    print("   " + "-" * 48)
    
    nejlepsi_povrch = float('inf')
    nejlepsi_h = 0.0
    nejlepsi_r = 0.0
    
    for i, h in enumerate(vysky_test, 1):
        r, s = analyzuj_valec(h)
        print(f"   {i:<10} {h:>10.2f} {r:>13.4f} {s:>13.4f}")
        if s < nejlepsi_povrch:
            nejlepsi_povrch = s
            nejlepsi_h = h
            nejlepsi_r = r
            
    print()
    print(f"  Z těchto 5 variant je nejúspornější Varianta s h = {nejlepsi_h} m ")
    print(f"  (Spotřeba materiálu: {nejlepsi_povrch:.4f} m**2)")
    print()

    # 2. Jemné vyhledání nejúspornější varianty (Brute force s krokem 0.01 m)
    print("2) Jemné hledání minima (krok 0.01 m):")
    
    opt_povrch = float('inf')
    opt_h = 0.0
    opt_r = 0.0
    
    krok = 0.01
    aktualni_h = MIN_VYSKA
    
    # Pro grafické znázornění v konzoli
    graf_data = []
    
    while aktualni_h <= MAX_VYSKA:
        r, s = analyzuj_valec(aktualni_h)
        if s < opt_povrch:
            opt_povrch = s
            opt_h = aktualni_h
            opt_r = r
        
        # Uložíme si vybrané body pro zjednodušený graf
        if abs(aktualni_h - round(aktualni_h, 1)) < 1e-5 and round(aktualni_h, 1) in [1.0, 1.2, 1.4, 1.6, 1.8, 2.0, 2.4, 3.0]:
            graf_data.append((aktualni_h, s))
            
        aktualni_h += krok
        
    print(f"   Absolutně nejúspornější rozměr v zadaném rozsahu:")
    print(f"   Optimální výška:   {opt_h:.2f} m")
    print(f"   Optimální poloměr: {opt_r:.4f} m")
    print(f"   Minimální povrch:  {opt_povrch:.4f} m**2")
    print(f"   Poznámka: Teoretické optimum pro 1 m**3 je h = 2r (h ≈ 1.084 m, S ≈ 5.54 m**2).")
    print()
    
    # 3. Grafické znázornění závislosti v textové podobě
    print("3) Graf závislosti spotřeby materiálu (S) na výšce (h):")
    print("   h (m) | S (m**2)")
    print("   ----------------------------------------")
    for h_g, s_g in graf_data:
        # Vytvoření řádku grafu pomocí hvězdiček
        sirka_grafu = int((s_g - 5.4) * 20)  # škálování pro vizualizaci
        bar = "*" * max(1, sirka_grafu)
        print(f"   {h_g:.1f}   | {s_g:.2f} {bar}")

if __name__ == "__main__":
    optimalizace_nadrze()