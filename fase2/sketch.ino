#include <DHT.h>

#define PINO_N 13
#define PINO_P 12
#define PINO_K 14
#define PINO_LDR 34
#define PINO_DHT 15
#define PINO_RELE 26
#define PINO_LED 27

#define TIPO_DHT DHT22
DHT dht(PINO_DHT, TIPO_DHT);

int culturaSelecionada = 0;

void setup() {
  Serial.begin(115200);
  dht.begin();

  pinMode(PINO_N, INPUT_PULLUP);
  pinMode(PINO_P, INPUT_PULLUP);
  pinMode(PINO_K, INPUT_PULLUP);
  pinMode(PINO_RELE, OUTPUT);
  pinMode(PINO_LED, OUTPUT);

  digitalWrite(PINO_RELE, LOW);
  digitalWrite(PINO_LED, LOW);

  Serial.println("===== FARMTECH SOLUTIONS =====");
  Serial.println("Selecione a cultura:");
  Serial.println("1 - Soja");
  Serial.println("2 - Milho");
}

void loop() {
  // Leitura da cultura via Serial
  if (culturaSelecionada == 0 && Serial.available() > 0) {
    char opcao = Serial.read();
    if (opcao == '1') {
      culturaSelecionada = 1;
      Serial.println("Cultura selecionada: SOJA");
      Serial.println("Parametros: Umidade minima 60% | NPK (qualquer um) | pH informativo");
    } else if (opcao == '2') {
      culturaSelecionada = 2;
      Serial.println("Cultura selecionada: MILHO");
      Serial.println("Parametros: Umidade minima 55% | NPK (qualquer um) | pH informativo");
    } else {
      Serial.println("Opcao invalida! Digite 1 para Soja ou 2 para Milho.");
    }
    return;
  }

  if (culturaSelecionada == 0) return;

  // Leitura dos sensores
  bool n = !digitalRead(PINO_N);
  bool p = !digitalRead(PINO_P);
  bool k = !digitalRead(PINO_K);

  int ldrValor = analogRead(PINO_LDR);
  float ph = map(ldrValor, 0, 4095, 0, 14);

  float umidade = dht.readHumidity();

  if (isnan(umidade)) {
    Serial.println("Erro na leitura do DHT22!");
    delay(2000);
    return;
  }

  // Limites por cultura
  float umidadeMinima = (culturaSelecionada == 1) ? 60.0 : 55.0;

  // Lógica de decisão (pH apenas informativo — LDR instável no Wokwi)
  bool umidadeBaixa = umidade < umidadeMinima;
  bool npkPresente = n || p || k;

  bool irrigar = umidadeBaixa && npkPresente;

  // Serial Monitor
  Serial.print("Cultura: ");
  Serial.print(culturaSelecionada == 1 ? "Soja" : "Milho");
  Serial.print(" | N:"); Serial.print(n);
  Serial.print(" P:"); Serial.print(p);
  Serial.print(" K:"); Serial.print(k);
  Serial.print(" | pH:"); Serial.print(ph, 1);
  Serial.print(" (informativo)");
  Serial.print(" | Umidade:"); Serial.print(umidade, 1);
  Serial.print("% (min:"); Serial.print(umidadeMinima, 0); Serial.print("%)");
  Serial.print(" | Irrigar:"); Serial.println(irrigar ? "SIM" : "NAO");

  digitalWrite(PINO_RELE, irrigar ? HIGH : LOW);
  digitalWrite(PINO_LED, irrigar ? HIGH : LOW);

  delay(2000);
}