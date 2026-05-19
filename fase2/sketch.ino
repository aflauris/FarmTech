#include <DHT.h>

#define PINO_N    13
#define PINO_P    12
#define PINO_K    14
#define PINO_LDR  34
#define PINO_DHT  15
#define PINO_RELE 26
#define PINO_LED  27

#define TIPO_DHT DHT22
DHT dht(PINO_DHT, TIPO_DHT);

// ── Média móvel do pH ─────────────────────────────────────
#define JANELA_PH 10
float leiturasPH[JANELA_PH];
int indicePH       = 0;
bool bufferCheio   = false;

float calcularMediaPH() {
  int total = bufferCheio ? JANELA_PH : indicePH;
  if (total == 0) return 0.0;
  float soma = 0.0;
  for (int i = 0; i < total; i++) soma += leiturasPH[i];
  return soma / total;
}

// ── Variáveis gerais ──────────────────────────────────────
int  culturaSelecionada = 0;
bool cabecalhoImpresso  = false;

void setup() {
  Serial.begin(115200);
  dht.begin();

  pinMode(PINO_N, INPUT_PULLUP);
  pinMode(PINO_P, INPUT_PULLUP);
  pinMode(PINO_K, INPUT_PULLUP);
  pinMode(PINO_RELE, OUTPUT);
  pinMode(PINO_LED,  OUTPUT);

  digitalWrite(PINO_RELE, LOW);
  digitalWrite(PINO_LED,  LOW);

  // Inicializa buffer de pH com zero
  for (int i = 0; i < JANELA_PH; i++) leiturasPH[i] = 0.0;

  Serial.println("===== FARMTECH SOLUTIONS =====");
  Serial.println("Selecione a cultura:");
  Serial.println("1 - Soja");
  Serial.println("2 - Milho");
}

void loop() {
  // ── Seleção de cultura via Serial ────────────────────────
  if (culturaSelecionada == 0 && Serial.available() > 0) {
    char opcao = Serial.read();
    if (opcao == '1') {
      culturaSelecionada = 1;
      Serial.println("Cultura selecionada: SOJA");
      Serial.println("Parametros: Umidade min 60% | pH ideal 6.0-7.0 | NPK (qualquer um)");
    } else if (opcao == '2') {
      culturaSelecionada = 2;
      Serial.println("Cultura selecionada: MILHO");
      Serial.println("Parametros: Umidade min 55% | pH ideal 5.5-7.0 | NPK (qualquer um)");
    } else {
      Serial.println("Opcao invalida! Digite 1 para Soja ou 2 para Milho.");
    }
    return;
  }

  if (culturaSelecionada == 0) return;

  // ── Cabeçalho CSV (imprime uma vez) ──────────────────────
  if (!cabecalhoImpresso) {
    Serial.println("---CSV---");
    Serial.println("cultura,n,p,k,ph,ph_medio,umidade,irrigar");
    cabecalhoImpresso = true;
  }

  // ── Leitura dos sensores ──────────────────────────────────
  bool n = !digitalRead(PINO_N);
  bool p = !digitalRead(PINO_P);
  bool k = !digitalRead(PINO_K);

  // pH via LDR com média móvel
  int   ldrValor = analogRead(PINO_LDR);
  float phAtual  = (float)map(ldrValor, 0, 4095, 0, 14);

  leiturasPH[indicePH] = phAtual;
  indicePH = (indicePH + 1) % JANELA_PH;
  if (indicePH == 0) bufferCheio = true;

  float phMedio = calcularMediaPH();

  // Umidade via DHT22
  float umidade = dht.readHumidity();
  if (isnan(umidade)) {
    Serial.println("Erro na leitura do DHT22!");
    delay(2000);
    return;
  }

  // ── Parâmetros por cultura ────────────────────────────────
  float umidadeMinima = (culturaSelecionada == 1) ? 60.0 : 55.0;
  float phMin         = (culturaSelecionada == 1) ? 6.0  : 5.5;
  float phMax         = 7.0;
  String cultura      = (culturaSelecionada == 1) ? "Soja" : "Milho";

  // ── Lógica de decisão (agora inclui pH médio) ─────────────
  bool umidadeBaixa = umidade < umidadeMinima;
  bool npkPresente  = n || p || k;
  bool phAdequado   = phMedio >= phMin && phMedio <= phMax;
  bool irrigar      = umidadeBaixa && npkPresente && phAdequado;

  // ── Linha legível no Serial Monitor ──────────────────────
  Serial.print("Cultura: ");      Serial.print(cultura);
  Serial.print(" | N:");          Serial.print(n);
  Serial.print(" P:");            Serial.print(p);
  Serial.print(" K:");            Serial.print(k);
  Serial.print(" | pH atual:");   Serial.print(phAtual, 1);
  Serial.print(" pH medio:");     Serial.print(phMedio, 1);
  Serial.print(" (");             Serial.print(phMin, 1);
  Serial.print("-");              Serial.print(phMax, 1);
  Serial.print(")");
  Serial.print(" | Umidade:");    Serial.print(umidade, 1);
  Serial.print("% (min:");        Serial.print(umidadeMinima, 0);
  Serial.print("%)");
  Serial.print(" | pH ok:");      Serial.print(phAdequado ? "SIM" : "NAO");
  Serial.print(" | Irrigar:");    Serial.println(irrigar ? "SIM" : "NAO");

  // ── Linha CSV para exportar ao R ─────────────────────────
  Serial.print("CSV,");
  Serial.print(cultura);    Serial.print(",");
  Serial.print(n);          Serial.print(",");
  Serial.print(p);          Serial.print(",");
  Serial.print(k);          Serial.print(",");
  Serial.print(phAtual, 1); Serial.print(",");
  Serial.print(phMedio, 1); Serial.print(",");
  Serial.print(umidade, 1); Serial.print(",");
  Serial.println(irrigar ? "SIM" : "NAO");

  digitalWrite(PINO_RELE, irrigar ? HIGH : LOW);
  digitalWrite(PINO_LED,  irrigar ? HIGH : LOW);

  delay(2000);
}
