# FarmTech Solutions - Análise Estatística
# Dados de área e insumos das culturas

# Dados de exemplo (baseados no que o Python coletaria)
areas <- c(20000, 15000, 8000, 12000, 5000)
totais_litros <- c(20, 15, 10, 18, 8)
culturas <- c("Soja", "Milho", "Soja", "Milho", "Soja")

# ===== ANÁLISE DE ÁREAS =====
cat("===== FARMTECH - ANÁLISE ESTATÍSTICA =====\n\n")

cat("--- Análise de Áreas (m²) ---\n")
cat("Média das áreas:", mean(areas), "m²\n")
cat("Desvio padrão das áreas:", sd(areas), "m²\n")
cat("Área mínima:", min(areas), "m²\n")
cat("Área máxima:", max(areas), "m²\n")

# ===== ANÁLISE DE INSUMOS =====
cat("\n--- Análise de Insumos (litros) ---\n")
cat("Média de insumos:", mean(totais_litros), "litros\n")
cat("Desvio padrão de insumos:", sd(totais_litros), "litros\n")
cat("Mínimo de insumos:", min(totais_litros), "litros\n")
cat("Máximo de insumos:", max(totais_litros), "litros\n")

# ===== ANÁLISE POR CULTURA =====
cat("\n--- Análise por Cultura ---\n")

areas_soja <- areas[culturas == "Soja"]
areas_milho <- areas[culturas == "Milho"]

cat("Média de área - Soja:", mean(areas_soja), "m²\n")
cat("Média de área - Milho:", mean(areas_milho), "m²\n")

# ===== GRÁFICO SIMPLES =====
cores <- ifelse(culturas == "Soja", "green", "yellow")
nomes <- paste(culturas, seq_along(culturas), sep = " ")

barplot(areas,
        names.arg = nomes,
        main = "Áreas por Cultura",
        ylab = "Área (m²)",
        col = cores,
        las = 2)

legend("topright",
       legend = c("Soja", "Milho"),
       fill = c("green", "yellow"))