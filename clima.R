install.packages("httr")
install.packages("jsonlite")

# FarmTech Solutions - Dados Climáticos via API Open-Meteo
# Cidade: São Paulo, SP

library(httr)
library(jsonlite)

# Coordenadas de São Paulo
lat <- -23.5505
lon <- -46.6333

# Montando a URL da API
url <- paste0(
  "https://api.open-meteo.com/v1/forecast?",
  "latitude=", lat,
  "&longitude=", lon,
  "&current_weather=true",
  "&hourly=temperature_2m,relativehumidity_2m,windspeed_10m"
)

# Fazendo a requisição
cat("Buscando dados climáticos...\n\n")
resposta <- GET(url)

# Processando a resposta
dados <- fromJSON(content(resposta, "text", encoding = "UTF-8"))
clima <- dados$current_weather

# Exibindo os dados no terminal
cat("===== FARMTECH - DADOS CLIMÁTICOS =====\n")
cat("Local: São Paulo, SP\n")
cat("Temperatura atual:", clima$temperature, "°C\n")
cat("Velocidade do vento:", clima$windspeed, "km/h\n")
cat("Código do tempo:", clima$weathercode, "\n")
cat("Data/Hora:", clima$time, "\n")
cat("========================================\n")