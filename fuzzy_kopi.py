def kurva_linier_naik(a, b, x):
    if x <= a:
        return 0
    elif a < x <= b:
        return (x - a) / (b - a)
    else:
        return 1
    
def kurva_linier_turun(a, b, x):
    if x <= a:
        return 1
    elif a < x <= b:
        return (b - x) / (b - a)
    else:
        return 0
    
def segitiga(a, b, c, x):
    if x <= a or x >= c:
        return 0
    elif a < x <= b:
        return (x - a) / (b - a)
    elif b < x < c:
        return (c - x) / (c - b)
    
def fuzzy_kekentalan(x):
    return {
        "encer": kurva_linier_turun(40, 60, x),
        "sedang": segitiga(40, 60, 80, x),
        "kental": kurva_linier_naik(60, 80, x)
    }

def fuzzy_asam(x):
    return {
        "rendah": kurva_linier_turun(30, 50, x),
        "sedang": segitiga(30, 50, 70, x),
        "tinggi": kurva_linier_naik(50, 70, x)
    }

def fuzzy_manis(x):
    return {
        "kurang": kurva_linier_turun(20, 50, x),
        "cukup": segitiga(20, 50, 80, x),
        "manis": kurva_linier_naik(50, 80, x)
    }

def fuzzy_aroma(x):
    return {
        "lemah": kurva_linier_turun(30, 50, x),
        "sedang": segitiga(30, 50, 70, x),
        "kuat": kurva_linier_naik(50, 70, x)
    }

def fuzzy_aftertaste(x):
    return {
        "singkat": kurva_linier_turun(30, 50, x),
        "cukup lama": segitiga(30, 50, 70, x),
        "panjang": kurva_linier_naik(50, 70, x)
    }

def defuzzify(alpha, z):
    alpha_values = [a["alpha"] for a in alpha]
    pembilang = sum(alpha_values[i] * z[i] for i in range(len(alpha)))
    penyebut = sum(alpha_values)
    return pembilang / penyebut

def inferensi(kekentalan, asam, manis, aroma, aftertaste):
    Kekentalan = fuzzy_kekentalan(kekentalan)
    Asam = fuzzy_asam(asam)
    Manis = fuzzy_manis(manis)
    Aroma = fuzzy_aroma(aroma)
    Aftertaste = fuzzy_aftertaste(aftertaste)
    
    rules = [
        {"alpha": min(Kekentalan["encer"], Asam["rendah"], Manis["kurang"], Aroma["lemah"], Aftertaste["singkat"]), "out": "rendah"},
        {"alpha": min(Kekentalan["encer"], Asam["sedang"], Manis["cukup"], Aroma["sedang"], Aftertaste["cukup lama"]), "out": "sedang"},
        {"alpha": min(Kekentalan["sedang"], Asam["sedang"], Manis["cukup"], Aroma["kuat"], Aftertaste["panjang"]), "out": "tinggi"},
        {"alpha": min(Kekentalan["kental"], Asam["tinggi"], Manis["manis"], Aroma["kuat"], Aftertaste["panjang"]), "out": "sangat tinggi"}
    ]
    
    z = [
        20 + (rule["alpha"] * 30) if rule["out"] == "rendah" else
        50 + (rule["alpha"] * 70) if rule["out"] == "sedang" else
        85 + (rule["alpha"] * 15) if rule["out"] == "tinggi" else
        100 for rule in rules
    ]
    
    kualitas = defuzzify(rules, z)
    return kualitas

kekentalan = float(input("Masukkan tingkat kekentalan kopi (1-100): "))
asam = float(input("Masukkan tingkat rasa asam (1-100): "))
manis = float(input("Masukkan tingkat kadar manis (1-100): "))
aroma = float(input("Masukkan tingkat aroma kopi (1-100): "))
aftertaste = float(input("Masukkan tingkat aftertaste kopi (1-100): "))

kualitas = inferensi(kekentalan, asam, manis, aroma, aftertaste)

print(f"\nTingkat kualitas kopi: {kualitas:.2f}%")
