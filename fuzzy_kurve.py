def kurva_linier_naik(a, b, x):
    if x <= a:
        return 0
    elif a < x <= b:
        return (x - a) / (b - a)
    else:
        return 1
    
def kurva_linier_turun(a, b, x):
    if x <= a:
        return 0
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
        return (c - b) / (c - x)
    
def fDA(x):
    return {
        "surut": kurva_linier_turun(40, 60, x),
        "sedang": segitiga(40, 60, 70, x),
        "penuh": kurva_linier_naik(60, 80, x)
    }
    
def fIH(x):
    return {
        "rendah": kurva_linier_turun(40, 60, x),
        "sedang": segitiga(40, 60, 70, x),
        "tinggi": kurva_linier_naik(60, 80, x)
    }
    
def fK(x):
    return {
        "kering": kurva_linier_turun(40, 60, x),
        "agak lembab": segitiga(40, 60, 70, x),
        "lembab": kurva_linier_naik(60, 80, x)
    }
    
def naik(a, b, x):
    return b - (x * (b - a))

def turun(a, b, x):
    return (x * (b - a)) + a

def defuzzify(alpha, z):
    alpha_values = [a["alpha"] for a in alpha]
    pembilang = sum(alpha_values[i] * z[i] for i in range(len(alpha)))
    penyebut = sum(alpha_values)
    return pembilang / penyebut

def indferensi(DA_val, IH_val, K_val):
    DA = fDA(DA_val)
    IH = fIH(IH_val)
    K = fK(K_val)
    
    alphaDam = [
        {"alpha": min(DA["surut"], IH["rendah"]), "out": "lebar"},
        {"alpha": min(DA["surut"], IH["sedang"]), "out": "lebar"},
        {"alpha": min(DA["surut"], IH["tinggi"]), "out": "sempit"},
        {"alpha": min(DA["sedang"], IH["rendah"]), "out": "lebar"},
        {"alpha": min(DA["sedang"], IH["sedang"]), "out": "lebar"},
        {"alpha": min(DA["sedang"], IH["tinggi"]), "out": "sempit"},
        {"alpha": min(DA["penuh"], IH["rendah"]), "out": "sempit"},
        {"alpha": min(DA["penuh"], IH["sedang"]), "out": "sempit"},
        {"alpha": min(DA["penuh"], IH["tinggi"]), "out": "sempit"}
    ]
    
    alphaDurasi = [
        {"alpha": min(DA["surut"], K["kering"]), "out": "lama"},
        {"alpha": min(DA["surut"], K["agak lembab"]), "out": "lama"},
        {"alpha": min(DA["surut"], K["lembab"]), "out": "singkat"},
        {"alpha": min(DA["sedang"], K["kering"]), "out": "lama"},
        {"alpha": min(DA["sedang"], K["agak lembab"]), "out": "singkat"},
        {"alpha": min(DA["sedang"], K["lembab"]), "out": "singkat"},
        {"alpha": min(DA["penuh"], K["kering"]), "out": "singkat"},
        {"alpha": min(DA["penuh"], K["agak lembab"]), "out": "singkat"},
        {"alpha": min(DA["penuh"], K["lembab"]), "out": "singkat"}
    ]
    
    zDam = [turun(0, 100, rule["alpha"]) if rule["out"] == "sempit" else naik(0, 100, rule["alpha"]) for rule in alphaDam]
    zDurasi = [turun(0, 60, rule["alpha"]) if rule["out"] == "singkat" else naik(0, 60, rule["alpha"]) for rule in alphaDurasi]
    
    Dam = defuzzify(alphaDam, zDam)
    Durasi = defuzzify(alphaDurasi, zDurasi)
    
    return Dam, Durasi

DA_val = float(input("Masukkan nilai debit air (1-100)       : "))
IH_val = float(input("Masukkan nilai intesitas hujan (1-100) : "))
K_val = float(input("Masukkan nilai kelembaban(1-100)       : "))

Dam, Durasi = indferensi(DA_val, IH_val, K_val)

print("tingkat bukaan pintu air : ", Dam, "%")
print("Durasi irigasi : ", Durasi, "Menit/n")
    