# ============================================================
# FarmTech Solutions — Fase 2
# Opcional 2: Análise Estatística em R para Decisão de Irrigação
# Autor: Ana Flora Lauris
# Descrição: Lê dados reais exportados do Serial Monitor do ESP32
#            e usa estatística para decidir se deve irrigar.
# ============================================================

# ─── 1. LEITURA DO CSV ───────────────────────────────────────
# Após rodar o Wokwi, copie as linhas que começam com "CSV,"
# do Serial Monitor e salve como "sensores_fase2.csv"
# O arquivo deve ter este formato:
# cultura,n,p,k,ph,umidade,irrigar
# Soja,1,0,1,6.5,58.3,SIM

cat("============================================================\n")
cat("  FARMTECH SOLUTIONS — Análise Estatística de Irrigação\n")
cat("============================================================\n\n")

# Verifica se o arquivo existe
if (!file.exists("sensores_fase2.csv")) {
  cat("[AVISO] Arquivo 'sensores_fase2.csv' não encontrado.\n")
  cat("        Usando dados simulados para demonstração.\n\n")
  
  # Dados simulados como fallback
  set.seed(42)
  n_leituras <- 20
  dados_sensores <- data.frame(
    cultura  = sample(c("Soja", "Milho"), n_leituras, replace = TRUE),
    n        = sample(c(0, 1), n_leituras, replace = TRUE),
    p        = sample(c(0, 1), n_leituras, replace = TRUE),
    k        = sample(c(0, 1), n_leituras, replace = TRUE),
    ph       = round(runif(n_leituras, min = 4.5, max = 8.5), 1),
    umidade  = round(runif(n_leituras, min = 40, max = 85), 1),
    irrigar  = sample(c("SIM", "NAO"), n_leituras, replace = TRUE)
  )
  fonte <- "SIMULADOS"
  
} else {
  dados_sensores <- read.csv("sensores_fase2.csv", stringsAsFactors = FALSE)
  colnames(dados_sensores) <- c("cultura", "n", "p", "k", "ph", "umidade", "irrigar")
  fonte <- "REAIS (ESP32)"
  cat(paste("Arquivo carregado com", nrow(dados_sensores), "leituras.\n\n"))
}

cat(paste("Fonte dos dados:", fonte, "\n\n"))

# ─── 2. PARÂMETROS POR CULTURA ───────────────────────────────
culturas <- list(
  Soja  = list(umidade_min = 60, ph_min = 6.0, ph_max = 7.0),
  Milho = list(umidade_min = 55, ph_min = 5.5, ph_max = 7.0)
)

# ─── 3. ANÁLISE ESTATÍSTICA GERAL ────────────────────────────
cat("--- Estatísticas Gerais das Leituras ---\n\n")

cat("Umidade (%):\n")
cat("  Média        :", round(mean(dados_sensores$umidade), 2), "%\n")
cat("  Desvio padrão:", round(sd(dados_sensores$umidade), 2), "%\n")
cat("  Mínima       :", min(dados_sensores$umidade), "%\n")
cat("  Máxima       :", max(dados_sensores$umidade), "%\n\n")

cat("pH do solo:\n")
cat("  Média        :", round(mean(dados_sensores$ph), 2), "\n")
cat("  Desvio padrão:", round(sd(dados_sensores$ph), 2), "\n")
cat("  Mínimo       :", min(dados_sensores$ph), "\n")
cat("  Máximo       :", max(dados_sensores$ph), "\n\n")

npk_freq <- colMeans(dados_sensores[, c("n", "p", "k")]) * 100
cat("Frequência de detecção dos nutrientes:\n")
cat("  Nitrogênio (N):", round(npk_freq["n"], 1), "% das leituras\n")
cat("  Fósforo    (P):", round(npk_freq["p"], 1), "% das leituras\n")
cat("  Potássio   (K):", round(npk_freq["k"], 1), "% das leituras\n\n")

# ─── 4. DECISÃO DE IRRIGAÇÃO POR CULTURA ─────────────────────
cat("--- Decisão de Irrigação por Cultura ---\n\n")

for (nome_cultura in names(culturas)) {
  params <- culturas[[nome_cultura]]
  
  # Filtra leituras da cultura
  dados_cultura <- dados_sensores[dados_sensores$cultura == nome_cultura, ]
  
  if (nrow(dados_cultura) == 0) {
    cat(paste0("Cultura: ", nome_cultura, " — sem leituras disponíveis.\n\n"))
    next
  }
  
  # Média da umidade nas últimas 5 leituras (tendência recente)
  ultimas <- tail(dados_cultura, 5)
  umidade_recente <- mean(ultimas$umidade)
  
  # pH médio
  ph_medio <- mean(dados_cultura$ph)
  
  # NPK presente em pelo menos 50% das leituras
  npk_ok <- mean((dados_cultura$n | dados_cultura$p | dados_cultura$k)) >= 0.5
  
  # Condições
  umidade_baixa <- umidade_recente < params$umidade_min
  ph_adequado   <- ph_medio >= params$ph_min & ph_medio <= params$ph_max
  
  irrigar <- umidade_baixa & npk_ok
  
  cat(paste0("Cultura: ", nome_cultura, "\n"))
  cat("  Total de leituras                         :", nrow(dados_cultura), "\n")
  cat("  Umidade média recente (últimas 5 leituras):", round(umidade_recente, 1), "%\n")
  cat("  Umidade mínima necessária                 :", params$umidade_min, "%\n")
  cat("  pH médio                                  :", round(ph_medio, 2), "\n")
  cat("  Faixa de pH ideal                         :", params$ph_min, "–", params$ph_max, "\n")
  cat("  pH adequado?                              :", ifelse(ph_adequado, "SIM", "NÃO"), "\n")
  cat("  NPK presente em ≥50% das leituras?        :", ifelse(npk_ok, "SIM", "NÃO"), "\n")
  cat("  Umidade abaixo do mínimo?                 :", ifelse(umidade_baixa, "SIM", "NÃO"), "\n")
  
  decisao <- ifelse(irrigar, "✅ LIGAR IRRIGAÇÃO", "🚫 MANTER DESLIGADA")
  cat("  >> Decisão                                :", decisao, "\n\n")
}

# ─── 5. GRÁFICOS ─────────────────────────────────────────────
par(mfrow = c(1, 2))

# Gráfico 1: Umidade ao longo das leituras
plot(seq_along(dados_sensores$umidade), dados_sensores$umidade,
     type = "b",
     col  = "steelblue",
     pch  = 16,
     main = paste("Umidade ao Longo das Leituras\n(", fonte, ")"),
     xlab = "Leitura",
     ylab = "Umidade (%)",
     ylim = c(30, 100))

abline(h = 60, col = "green",  lty = 2, lwd = 2)
abline(h = 55, col = "orange", lty = 2, lwd = 2)
abline(h = mean(dados_sensores$umidade), col = "red", lty = 3, lwd = 1)

legend("topright",
       legend = c("Umidade", "Mín. Soja (60%)", "Mín. Milho (55%)", "Média"),
       col    = c("steelblue", "green", "orange", "red"),
       lty    = c(1, 2, 2, 3),
       pch    = c(16, NA, NA, NA),
       cex    = 0.75)

# Gráfico 2: pH ao longo das leituras
plot(seq_along(dados_sensores$ph), dados_sensores$ph,
     type = "b",
     col  = "darkorchid",
     pch  = 16,
     main = paste("pH ao Longo das Leituras\n(", fonte, ")"),
     xlab = "Leitura",
     ylab = "pH",
     ylim = c(3, 10))

abline(h = 6.0, col = "green",  lty = 2, lwd = 2)
abline(h = 5.5, col = "orange", lty = 2, lwd = 2)
abline(h = 7.0, col = "blue",   lty = 2, lwd = 2)
abline(h = mean(dados_sensores$ph), col = "red", lty = 3, lwd = 1)

legend("topright",
       legend = c("pH", "Mín. Soja (6.0)", "Mín. Milho (5.5)", "Máx. (7.0)", "Média"),
       col    = c("darkorchid", "green", "orange", "blue", "red"),
       lty    = c(1, 2, 2, 2, 3),
       pch    = c(16, NA, NA, NA, NA),
       cex    = 0.75)

cat("============================================================\n")
cat("  Gráficos gerados com sucesso!\n")
cat("============================================================\n")
