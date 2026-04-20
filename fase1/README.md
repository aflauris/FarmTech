# 🌱 FarmTech Solutions — Sistema de Irrigação Inteligente

## Fase 2 — Coleta de Dados com ESP32

**Aluna:** Ana Flora Lauris  
**Instituição:** FIAP  
**Estado:** São Paulo  
**Culturas trabalhadas:** Soja e Milho  

---

## 📋 Descrição do Projeto

A FarmTech Solutions é uma startup de Agricultura Digital. Nesta segunda fase do projeto, foi desenvolvido um sistema de irrigação automatizado e inteligente utilizando um ESP32 simulado na plataforma [Wokwi](https://wokwi.com).

O sistema monitora em tempo real:
- Níveis de nutrientes NPK (Nitrogênio, Fósforo e Potássio) via botões
- pH do solo via sensor LDR
- Umidade via sensor DHT22

Com base nesses dados, o sistema decide automaticamente se deve acionar ou não a bomba de irrigação (representada por um relé).

---

## 🌾 Culturas Agrícolas

As culturas foram escolhidas por serem as principais do estado de São Paulo.

### Soja
| Parâmetro | Valor ideal | Valor no sistema |
|---|---|---|
| pH do solo | 6.0 – 7.0 | Informativo (limitação do Wokwi) |
| Umidade mínima para irrigar | 60% | 60% |
| NPK necessário | N, P e K | Qualquer um detectado |

### Milho
| Parâmetro | Valor ideal | Valor no sistema |
|---|---|---|
| pH do solo | 5.5 – 7.0 | Informativo (limitação do Wokwi) |
| Umidade mínima para irrigar | 55% | 55% |
| NPK necessário | N, P e K | Qualquer um detectado |

---

## 🔌 Componentes do Circuito

| Componente | Função no projeto | Pino ESP32 |
|---|---|---|
| Botão verde (N) | Simula sensor de Nitrogênio | GPIO 13 |
| Botão verde (P) | Simula sensor de Fósforo | GPIO 12 |
| Botão verde (K) | Simula sensor de Potássio | GPIO 14 |
| LDR | Simula sensor de pH do solo | GPIO 34 (analógico) |
| DHT22 | Simula sensor de umidade do solo | GPIO 15 |
| Relé | Simula bomba d'água | GPIO 26 |
| LED azul | Indicador visual da bomba | GPIO 27 |

---

## 🖼️ Circuito no Wokwi

![Circuito FarmTech no Wokwi](./circuito_wokwi.png)

> O circuito foi montado e simulado na plataforma [Wokwi.com](https://wokwi.com).

---

## ⚙️ Lógica de Irrigação

O sistema funciona da seguinte forma:

1. Ao iniciar, o Serial Monitor solicita que o usuário selecione a cultura (`1` para Soja, `2` para Milho)
2. Com a cultura selecionada, o sistema passa a monitorar os sensores continuamente a cada 2 segundos
3. A bomba de irrigação é acionada quando **duas condições são verdadeiras simultaneamente**:
   - A umidade do solo está **abaixo do mínimo** da cultura selecionada
   - **Pelo menos um** dos nutrientes NPK está presente (botão pressionado)

```
irrigar = (umidade < umidadeMinima) AND (N OR P OR K)
```

### Justificativa das adaptações para simulação

O sensor de pH (LDR) foi mantido apenas como leitura informativa no Serial Monitor. Durante os testes, o LDR no Wokwi retornou valor fixo em 0.0, impossibilitando seu uso confiável na lógica de decisão. Isso é coerente com o próprio enunciado do projeto, que já prevê substituições didáticas dos sensores reais por componentes disponíveis no simulador.

Da mesma forma, os botões NPK simulam sensores que na prática retornariam valores contínuos — aqui funcionam como leitura binária (presente/ausente), conforme especificado no enunciado.

---

## 💻 Como executar

1. Acesse [wokwi.com](https://wokwi.com) e importe o projeto
2. Carregue o arquivo `farmtech_fase2.ino`
3. Inicie a simulação clicando em **Play**
4. No Serial Monitor, digite `1` (Soja) ou `2` (Milho) e clique em **Send**
5. Ajuste a umidade no DHT22 para abaixo do mínimo da cultura
6. Pressione qualquer botão (N, P ou K) — o relé e o LED azul devem acionar

---

## 📁 Estrutura do Repositório

```
farmtech/
├── fase1/
│   ├── farmtech.py         # Aplicação Python - Fase 1
│   ├── analise.R           # Análise estatística em R
│   └── dados_farmtech.csv  # Dados exportados pelo Python
├── fase2/
│   ├── farmtech_fase2.ino  # Código C/C++ do ESP32
│   ├── README.md           # Este arquivo
│   └── circuito_wokwi.png  # Print do circuito no Wokwi
└── link_video.txt          # Link do vídeo no YouTube
```

---

## 🔗 Conexão com a Fase 1

Este projeto é a continuação direta da Fase 1, onde foram desenvolvidos:
- Aplicação Python com cadastro de culturas (Soja e Milho), cálculo de área plantada e manejo de insumos
- Análise estatística em R com média e desvio padrão dos dados coletados

As mesmas culturas — **Soja** e **Milho**, principais do estado de São Paulo — foram utilizadas como base para definir os parâmetros de irrigação desta fase.

> 📺 Vídeo de demonstração da Fase 1: https://youtu.be/eqO-80eAe9I

---

## 🎥 Vídeo de Demonstração

> 📺 Link do vídeo no YouTube: https://youtu.be/r2hCuZzWI8w

O vídeo demonstra o funcionamento completo do sistema: seleção de cultura, variação de umidade, acionamento dos botões NPK e resposta do relé.

---

## 📚 Tecnologias Utilizadas

- **ESP32** — microcontrolador principal
- **C/C++ (Arduino)** — linguagem do firmware
- **Wokwi** — plataforma de simulação de circuitos
- **Python** — aplicação de gestão agrícola (Fase 1)
- **R** — análise estatística (Fase 1)
