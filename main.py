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


