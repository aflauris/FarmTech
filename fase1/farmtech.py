# FarmTech Solutions - Sistema de Gestão Agrícola
# Culturas: Soja e Milho

import csv

# Vetores (listas) para armazenar os dados
culturas = []
areas = []
insumos = []
totais = []

def calcular_area(cultura):
    if cultura == "1":  # Soja - Retângulo
        largura = float(input("Largura do campo (metros): "))
        comprimento = float(input("Comprimento do campo (metros): "))
        return largura * comprimento
    elif cultura == "2":  # Milho - Triângulo
        base = float(input("Base do campo (metros): "))
        altura = float(input("Altura do campo (metros): "))
        return (base * altura) / 2

def calcular_insumo():
    insumo = input("Nome do insumo (ex: Herbicida, Fosfato): ")
    quantidade_por_metro = float(input("Quantidade por metro (mL/metro): "))
    comprimento_rua = float(input("Comprimento de cada rua (metros): "))
    num_ruas = int(input("Número de ruas: "))
    total_ml = quantidade_por_metro * comprimento_rua * num_ruas
    total_litros = total_ml / 1000
    print(f"Total necessário: {total_ml} mL = {total_litros} litros")
    return insumo, total_litros

def inserir_dados():
    print("\n--- INSERIR DADOS ---")
    print("Qual cultura?")
    print("1 - Soja (campo retangular)")
    print("2 - Milho (campo triangular)")
    cultura = input("Escolha: ")

    if cultura == "1":
        culturas.append("Soja")
    elif cultura == "2":
        culturas.append("Milho")
    else:
        print("Opção inválida!")
        return

    area = calcular_area(cultura)
    areas.append(area)
    print(f"Área calculada: {area} m²")

    insumo, total = calcular_insumo()
    insumos.append(insumo)
    totais.append(total)

    print("✅ Dados inseridos com sucesso!")

def ver_dados():
    print("\n--- DADOS CADASTRADOS ---")
    if len(culturas) == 0:
        print("Nenhum dado cadastrado ainda.")
        return
    for i in range(len(culturas)):
        print(f"[{i}] Cultura: {culturas[i]} | Área: {areas[i]} m² | Insumo: {insumos[i]} | Total: {totais[i]} litros")

def atualizar_dados():
    ver_dados()
    if len(culturas) == 0:
        return
    pos = int(input("\nQual posição deseja atualizar? "))
    if pos < 0 or pos >= len(culturas):
        print("Posição inválida!")
        return
    print(f"Atualizando registro [{pos}] - {culturas[pos]}")
    print("1 - Soja | 2 - Milho")
    cultura = input("Nova cultura: ")
    if cultura == "1":
        culturas[pos] = "Soja"
    else:
        culturas[pos] = "Milho"
    areas[pos] = calcular_area(cultura)
    insumo, total = calcular_insumo()
    insumos[pos] = insumo
    totais[pos] = total
    print("✅ Dados atualizados!")

def deletar_dados():
    ver_dados()
    if len(culturas) == 0:
        return
    pos = int(input("\nQual posição deseja deletar? "))
    if pos < 0 or pos >= len(culturas):
        print("Posição inválida!")
        return
    culturas.pop(pos)
    areas.pop(pos)
    insumos.pop(pos)
    totais.pop(pos)
    print("✅ Registro deletado!")

def exportar_csv():
    with open('dados_farmtech.csv', 'w', newline='', encoding='utf-8') as arquivo:
        writer = csv.writer(arquivo)
        writer.writerow(['cultura', 'area', 'insumo', 'total_litros'])
        for i in range(len(culturas)):
            writer.writerow([culturas[i], areas[i], insumos[i], totais[i]])
    print("✅ Dados exportados para dados_farmtech.csv!")

# Menu principal
while True:
    print("\n===== FARMTECH SOLUTIONS =====")
    print("1 - Inserir dados")
    print("2 - Ver dados")
    print("3 - Atualizar dados")
    print("4 - Deletar dados")
    print("5 - Sair")
    opcao = input("Escolha uma opção: ")

    if opcao == "1":
        inserir_dados()
    elif opcao == "2":
        ver_dados()
    elif opcao == "3":
        atualizar_dados()
    elif opcao == "4":
        deletar_dados()
    elif opcao == "5":
        exportar_csv()
        print("Saindo... Até logo!")
        break
    else:
        print("Opção inválida! Tente novamente.")
