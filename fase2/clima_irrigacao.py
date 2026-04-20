"""
FarmTech Solutions — Fase 2
Opcional 1: Integração com API OpenWeather
Cidade: Agudos, SP
Autor: Ana Flora Lauris

Este script consulta a API do OpenWeather para verificar a previsão de chuva
e decide se a irrigação deve ser suspensa. O valor da variável `nivel_chuva`
pode ser copiado manualmente para o código C/C++ do ESP32 no Wokwi.
"""

import requests
import json
from datetime import datetime

# ─── CONFIGURAÇÕES ────────────────────────────────────────────────────────────
API_KEY   = "4c43580212655bf7924ab7fc78f9283f"
CIDADE    = "Agudos"
PAIS      = "BR"
UNIDADES  = "metric"   # Celsius
URL_ATUAL = f"https://api.openweathermap.org/data/2.5/weather?q={CIDADE},{PAIS}&appid={API_KEY}&units={UNIDADES}&lang=pt_br"
URL_PREV  = f"https://api.openweathermap.org/data/2.5/forecast?q={CIDADE},{PAIS}&appid={API_KEY}&units={UNIDADES}&lang=pt_br"

# ─── LIMITES AGRÍCOLAS ────────────────────────────────────────────────────────
CULTURAS = {
    "Soja":  {"umidade_min": 60, "chuva_suspende_mm": 5.0},
    "Milho": {"umidade_min": 55, "chuva_suspende_mm": 4.0},
}

# ─── FUNÇÕES ──────────────────────────────────────────────────────────────────

def buscar_clima_atual():
    """Busca temperatura, umidade e chuva atual."""
    try:
        resp = requests.get(URL_ATUAL, timeout=10)
        resp.raise_for_status()
        dados = resp.json()

        temperatura = dados["main"]["temp"]
        umidade     = dados["main"]["humidity"]
        descricao   = dados["weather"][0]["description"]
        chuva_mm    = dados.get("rain", {}).get("1h", 0.0)

        return {
            "temperatura": temperatura,
            "umidade":     umidade,
            "descricao":   descricao,
            "chuva_mm":    chuva_mm,
        }
    except requests.exceptions.RequestException as e:
        print(f"[ERRO] Falha ao buscar clima atual: {e}")
        return None


def buscar_previsao_chuva():
    """Busca previsão de chuva para as próximas 24h (8 períodos de 3h)."""
    try:
        resp = requests.get(URL_PREV, timeout=10)
        resp.raise_for_status()
        dados = resp.json()

        chuva_total = 0.0
        periodos    = dados["list"][:8]  # próximas 24h

        for periodo in periodos:
            chuva_total += periodo.get("rain", {}).get("3h", 0.0)

        return round(chuva_total, 2)

    except requests.exceptions.RequestException as e:
        print(f"[ERRO] Falha ao buscar previsão: {e}")
        return 0.0


def decidir_irrigacao(cultura_nome, clima_atual, chuva_prevista_mm):
    """Decide se deve irrigar com base no clima e na cultura."""
    cultura        = CULTURAS[cultura_nome]
    umidade_atual  = clima_atual["umidade"]
    chuva_agora    = clima_atual["chuva_mm"]
    limite_suspens = cultura["chuva_suspende_mm"]

    motivo = []

    # Condição 1: já está chovendo agora
    if chuva_agora >= limite_suspens:
        motivo.append(f"já está chovendo ({chuva_agora:.1f} mm/h)")
        return False, motivo

    # Condição 2: previsão de chuva nas próximas 24h
    if chuva_prevista_mm >= limite_suspens:
        motivo.append(f"previsão de {chuva_prevista_mm:.1f} mm nas próximas 24h")
        return False, motivo

    # Condição 3: umidade do ar alta (proxy de solo úmido)
    if umidade_atual >= cultura["umidade_min"]:
        motivo.append(f"umidade do ar em {umidade_atual}% (acima do mínimo de {cultura['umidade_min']}%)")
        return False, motivo

    motivo.append("sem chuva prevista e umidade baixa")
    return True, motivo


def imprimir_relatorio(clima_atual, chuva_prevista, cultura_nome, irrigar, motivos):
    """Imprime o relatório completo no terminal."""
    linha = "=" * 55

    print(f"\n{linha}")
    print(f"  🌱 FARMTECH SOLUTIONS — Monitoramento Climático")
    print(f"{linha}")
    print(f"  📍 Cidade      : {CIDADE}, {PAIS}")
    print(f"  🕐 Data/Hora   : {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    print(f"  🌾 Cultura     : {cultura_nome}")
    print(f"{linha}")
    print(f"  🌡️  Temperatura : {clima_atual['temperatura']:.1f} °C")
    print(f"  💧 Umidade ar  : {clima_atual['umidade']}%")
    print(f"  🌧️  Chuva atual : {clima_atual['chuva_mm']:.1f} mm/h")
    print(f"  ☁️  Condição    : {clima_atual['descricao'].capitalize()}")
    print(f"  🔮 Prev. chuva : {chuva_prevista:.1f} mm (próx. 24h)")
    print(f"{linha}")

    status = "✅ LIGAR IRRIGAÇÃO" if irrigar else "🚫 SUSPENDER IRRIGAÇÃO"
    print(f"  Decisão       : {status}")
    print(f"  Motivo        : {'; '.join(motivos)}")
    print(f"{linha}")

    # Valor para copiar no ESP32 (Wokwi)
    nivel_chuva = round(clima_atual["chuva_mm"] + chuva_prevista, 2)
    print(f"\n  ── Para o ESP32 (Wokwi) ──────────────────────────")
    print(f"  Copie esta linha no seu código C/C++:")
    print(f"  float nivel_chuva = {nivel_chuva};  // mm total (atual + prev 24h)")
    print(f"  bool suspender_por_chuva = {str(not irrigar).lower()};")
    print(f"{linha}\n")


# ─── MAIN ─────────────────────────────────────────────────────────────────────

def main():
    print("\nConsultando API OpenWeather...")

    clima_atual     = buscar_clima_atual()
    if not clima_atual:
        print("Não foi possível obter dados climáticos. Verifique a API key e conexão.")
        return

    chuva_prevista  = buscar_previsao_chuva()

    print("\nSelecione a cultura:")
    print("1 - Soja")
    print("2 - Milho")
    opcao = input("Opção: ").strip()

    cultura_nome = "Soja" if opcao == "1" else "Milho"

    irrigar, motivos = decidir_irrigacao(cultura_nome, clima_atual, chuva_prevista)
    imprimir_relatorio(clima_atual, chuva_prevista, cultura_nome, irrigar, motivos)


if __name__ == "__main__":
    main()