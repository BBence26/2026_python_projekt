import random
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

ORSZAGOK = {
    "Ausztrália": {"fovaros": "Canberra", "foldresz": "Ausztrália",
        "varosok": ["Canberra", "Sydney", "Melbourne", "Brisbane"],
        "magyarazat": "Canberrát Sydney és Melbourne közötti kompromisszumként építették."},
    "Törökország": {"fovaros": "Ankara", "foldresz": "Európa és Ázsia",
        "varosok": ["Ankara", "Isztambul", "Izmir", "Bursa"],
        "magyarazat": "Ankara belső fekvése miatt lett az új köztársaság központja."},
    "Kanada": {"fovaros": "Ottawa", "foldresz": "Észak-Amerika",
        "varosok": ["Ottawa", "Toronto", "Montreal", "Vancouver"],
        "magyarazat": "Ottawát Viktória királynő jelölte ki kompromisszumként."},
    "Egyesült Államok": {"fovaros": "Washington, D.C.", "foldresz": "Észak-Amerika",
        "varosok": ["Washington, D.C.", "New York", "Los Angeles", "Chicago"],
        "magyarazat": "Washington külön kerület, így nem tartozik egyik államhoz sem."},
    "Brazília": {"fovaros": "Brazíliaváros", "foldresz": "Dél-Amerika",
        "varosok": ["Brazíliaváros", "Rio de Janeiro", "São Paulo", "Salvador"],
        "magyarazat": "Brazíliavárost az ország belső területeinek fejlesztésére tervezték."},
    "Svájc": {"fovaros": "Bern", "foldresz": "Európa",
        "varosok": ["Bern", "Zürich", "Genf", "Bázel"],
        "magyarazat": "Bern központi fekvése miatt lett szövetségi főváros."},
    "Dél-Afrika": {"fovaros": "Pretoria", "foldresz": "Afrika",
        "varosok": ["Pretoria", "Fokváros", "Bloemfontein", "Johannesburg"],
        "kerdes": "Melyik Dél-Afrika közigazgatási fővárosa?",
        "magyarazat": "Pretoria a közigazgatási, Fokváros a törvényhozási, Bloemfontein az igazságszolgáltatási központ."},
    "Marokkó": {"fovaros": "Rabat", "foldresz": "Afrika",
        "varosok": ["Rabat", "Casablanca", "Marrákes", "Fez"],
        "magyarazat": "Rabat tengerparti fekvése miatt könnyen elérhető központ volt."},
    "Új-Zéland": {"fovaros": "Wellington", "foldresz": "Óceánia",
        "varosok": ["Wellington", "Auckland", "Christchurch", "Dunedin"],
        "magyarazat": "Wellington az Északi- és a Déli-sziget között fekszik."},
    "Kína": {"fovaros": "Peking", "foldresz": "Ázsia",
        "varosok": ["Peking", "Sanghaj", "Kanton", "Sencsen"],
        "magyarazat": "Peking történelmi hagyományai miatt maradt főváros."},
    "India": {"fovaros": "Új-Delhi", "foldresz": "Ázsia",
        "varosok": ["Új-Delhi", "Mumbai", "Kolkata", "Chennai"],
        "magyarazat": "A brit kormányzat Kalkuttából Delhibe költöztette központját."},
}

def bb_orszag_lista():
    return list(ORSZAGOK)

def bb_kviz():
    return random.sample(bb_orszag_lista(), 8)

def bb_valaszok(orszag):
    valaszok = ORSZAGOK[orszag]["varosok"].copy()
    random.shuffle(valaszok)
    return valaszok

def bb_eredmeny(nevek, pontok):
    if pontok[0] == pontok[1]:
        gyoztes = "Döntetlen!"
    elif pontok[0] > pontok[1]:
        gyoztes = f"A győztes: {nevek[0]}!"
    else:
        gyoztes = f"A győztes: {nevek[1]}!"
    return f"{nevek[0]}: {pontok[0]}\n{nevek[1]}: {pontok[1]}\n\n{gyoztes}"

def bb_statisztika_mentes(nevek, pontok):
    datum = datetime.now().strftime("%Y-%m-%d %H:%M")
    with open("statisztika.txt", "a", encoding="utf-8") as fajl:
        fajl.write(f"{datum} | {nevek[0]}: {pontok[0]}/4 | {nevek[1]}: {pontok[1]}/4\n")

def bb_statisztika_olvas():
    try:
        with open("statisztika.txt", "r", encoding="utf-8") as fajl:
            return fajl.read().strip() or "Még nincs elmentett eredmény."
    except FileNotFoundError:
        return "Még nincs elmentett eredmény."

class BBVilagjaro:
    def __init__(self, root):
        self.root = root
        self.root.title("VilágJáró")
        self.root.geometry("560x500")
        self.nevek = []
        self.pontok = [0, 0]
        self.kerdesek = []
        self.sorszam = 0
        self.valasz = tk.StringVar()
        self.oldalak = [ttk.Frame(root, padding=20) for _ in range(5)]
        self.menu, self.nev_frame, self.info_frame, self.stat_frame, self.jatek = self.oldalak

        self.bb_cimke(self.menu, "VilágJáró", font=("Arial", 20, "bold"))
        for szoveg, parancs in [
            ("Verseny indítása", self.bb_nev_megadas),
            ("Országinformációk", self.bb_info_megjelenit),
            ("Statisztika", self.bb_statisztika_megjelenit),
            ("Kilépés", root.destroy),
        ]:
            self.bb_gomb(self.menu, szoveg, parancs)

        self.bb_cimke(self.nev_frame, "Add meg a két játékos nevét")
        self.elso_nev = ttk.Entry(self.nev_frame)
        self.masodik_nev = ttk.Entry(self.nev_frame)
        self.bb_cimke(self.nev_frame, "Első játékos")
        self.elso_nev.pack()
        self.bb_cimke(self.nev_frame, "Második játékos")
        self.masodik_nev.pack()
        self.bb_gomb(self.nev_frame, "Indítás", self.bb_indit)
        self.bb_gomb(self.nev_frame, "Vissza", self.bb_fomenu)

        self.bb_cimke(self.info_frame, "Országinformációk", font=("Arial", 16, "bold"))
        self.info_orszag = tk.StringVar()
        ttk.Combobox(
            self.info_frame, textvariable=self.info_orszag,
            values=bb_orszag_lista(), state="readonly",
        ).pack()
        self.bb_gomb(self.info_frame, "Mutasd", self.bb_orszag_info)
        self.info = self.bb_cimke(self.info_frame, "", wraplength=450)
        self.bb_gomb(self.info_frame, "Vissza", self.bb_fomenu)

        self.bb_cimke(self.stat_frame, "Korábbi eredmények", font=("Arial", 16, "bold"))
        self.stat_label = self.bb_cimke(self.stat_frame, "", justify="left")
        self.bb_gomb(self.stat_frame, "Vissza", self.bb_fomenu)

        self.cim = self.bb_cimke(self.jatek, "", font=("Arial", 14, "bold"))
        self.kerdes = self.bb_cimke(self.jatek, "", wraplength=480, font=("Arial", 13))
        self.valasz_frame = ttk.Frame(self.jatek)
        self.valasz_frame.pack(pady=4)
        self.uzenet = self.bb_cimke(self.jatek, "", wraplength=480)
        self.ellenorzo = ttk.Button(
            self.jatek, text="Válasz ellenőrzése", command=self.bb_ellenoriz
        )
        self.ellenorzo.pack(pady=4)
        self.kovetkezo = ttk.Button(
            self.jatek, text="Következő kérdés", command=self.bb_kovetkezo,
            state="disabled",
        )
        self.kovetkezo.pack(pady=4)
        self.ujra = ttk.Button(self.jatek, text="Főmenü", command=self.bb_fomenu)
        self.bb_fomenu()

    def bb_cimke(self, frame, szoveg, **beallitas):
        cimke = ttk.Label(frame, text=szoveg, **beallitas)
        cimke.pack(pady=5)
        return cimke

    def bb_gomb(self, frame, szoveg, parancs):
        ttk.Button(frame, text=szoveg, command=parancs).pack(pady=4)

    def bb_oldal_valtas(self, oldal):
        for frame in self.oldalak:
            frame.pack_forget()
        oldal.pack(expand=True)

    def bb_fomenu(self):
        self.bb_oldal_valtas(self.menu)

    def bb_nev_megadas(self):
        self.bb_oldal_valtas(self.nev_frame)

    def bb_info_megjelenit(self):
        self.bb_oldal_valtas(self.info_frame)

    def bb_statisztika_megjelenit(self):
        try:
            self.stat_label.config(text=bb_statisztika_olvas())
        except OSError as hiba:
            messagebox.showerror("Fájlhiba", f"A statisztika nem olvasható:\n{hiba}")
        self.bb_oldal_valtas(self.stat_frame)

    def bb_orszag_info(self):
        orszag = self.info_orszag.get()
        if orszag:
            adat = ORSZAGOK[orszag]
            self.info.config(
                text=f"{orszag} fővárosa {adat['fovaros']}, "
                f"és {adat['foldresz']} területén található."
            )

    def bb_indit(self):
        self.nevek = [self.elso_nev.get().strip(), self.masodik_nev.get().strip()]
        if not all(self.nevek) or self.nevek[0].casefold() == self.nevek[1].casefold():
            messagebox.showwarning("Játékosok", "Adj meg két különböző nevet!")
            return
        self.pontok = [0, 0]
        self.kerdesek = bb_kviz()
        self.sorszam = 0
        self.bb_oldal_valtas(self.jatek)
        self.bb_kerdes_megjelenit()

    def bb_kerdes_megjelenit(self):
        orszag = self.kerdesek[self.sorszam]
        jatekos = self.sorszam % 2
        self.valasz.set("")
        self.cim.config(
            text=f"{self.nevek[jatekos]} következik | "
            f"{self.sorszam + 1}/{len(self.kerdesek)} | Pont: {self.pontok[jatekos]}"
        )
        self.kerdes.config(text=ORSZAGOK[orszag].get("kerdes", f"Mi {orszag} fővárosa?"))
        for gomb in self.valasz_frame.winfo_children():
            gomb.destroy()
        for valasz in bb_valaszok(orszag):
            ttk.Radiobutton(
                self.valasz_frame, text=valasz, variable=self.valasz, value=valasz
            ).pack(anchor="w")
        self.uzenet.config(text="")
        self.ellenorzo.config(state="normal")
        self.kovetkezo.config(state="disabled")
        self.valasz_frame.pack(pady=4)
        self.uzenet.pack(pady=8)
        self.ellenorzo.pack(pady=4)
        self.kovetkezo.pack(pady=4)
        self.ujra.pack_forget()

    def bb_ellenoriz(self):
        if not self.valasz.get():
            messagebox.showinfo("Válasz", "Válassz egy várost!")
            return
        orszag = self.kerdesek[self.sorszam]
        jatekos = self.sorszam % 2
        adat = ORSZAGOK[orszag]
        if self.valasz.get() == adat["fovaros"]:
            self.pontok[jatekos] += 1
            uzenet = "Helyes válasz!"
        else:
            uzenet = f"Nem jó, a helyes válasz: {adat['fovaros']}."
        self.uzenet.config(text=f"{uzenet}\n{adat['magyarazat']}")
        for gomb in self.valasz_frame.winfo_children():
            gomb.config(state="disabled")
        self.ellenorzo.config(state="disabled")
        self.kovetkezo.config(state="normal")

    def bb_kovetkezo(self):
        self.sorszam += 1
        if self.sorszam < len(self.kerdesek):
            self.bb_kerdes_megjelenit()
            return
        try:
            bb_statisztika_mentes(self.nevek, self.pontok)
        except OSError as hiba:
            messagebox.showerror("Fájlhiba", f"Az eredmény nem menthető:\n{hiba}")
        self.cim.config(text="Végeredmény")
        self.kerdes.config(text=bb_eredmeny(self.nevek, self.pontok))
        self.valasz_frame.pack_forget()
        self.uzenet.pack_forget()
        self.ellenorzo.pack_forget()
        self.kovetkezo.pack_forget()
        self.ujra.pack(pady=8)