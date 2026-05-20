import requests
import math
import time

cidade = "Tupã"

####################################################
# GEOCODING (só uma vez)
####################################################

geo_url = (
    f"https://geocoding-api.open-meteo.com/v1/search?"
    f"name={cidade}&count=1&language=pt&format=json"
)

geo_data = requests.get(geo_url).json()

latitude = geo_data["results"][0]["latitude"]
longitude = geo_data["results"][0]["longitude"]

####################################################
# LOOP INFINITO (atualiza dados)
####################################################

while True:

    weather_url = (
        f"https://api.open-meteo.com/v1/forecast?"
        f"latitude={latitude}"
        f"&longitude={longitude}"
        f"&current="
        f"temperature_2m,"
        f"relative_humidity_2m,"
        f"wind_speed_10m,"
        f"shortwave_radiation,"
        f"surface_pressure"
    )

    weather_data = requests.get(weather_url).json()
    current = weather_data["current"]

    horario_medicao = current["time"]

    # Variáveis
    T = current["temperature_2m"]
    UR = current["relative_humidity_2m"]
    u = current["wind_speed_10m"]
    Rs = current["shortwave_radiation"]
    P_atm = current["surface_pressure"]

    # Radiação líquida
    Rn = 0.77 * Rs

    # Psicrométricos
    es = 0.6108 * math.exp((17.27 * T) / (T + 237.3))
    ea = es * (UR / 100)
    VPD = es - ea

    P_kPa = P_atm / 10
    gamma = 0.000665 * P_kPa

    ####################################################
    # PRINT
    ####################################################

    print("\n===== ATUALIZAÇÃO =====")
    print(f"Cidade: {cidade}")
    print(f"Horário: {horario_medicao}")

    print(f"T: {T:.2f} °C | UR: {UR:.2f}% | Vento: {u:.2f} m/s")
    print(f"Rs: {Rs:.2f} W/m² | Rn: {Rn:.2f} W/m²")
    print(f"VPD: {VPD:.4f} kPa | γ: {gamma:.4f}")

    ####################################################
    # ESPERA (tempo entre atualizações)
    ####################################################

    time.sleep(300)  # 5 minutos