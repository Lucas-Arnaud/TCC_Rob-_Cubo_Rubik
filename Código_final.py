# Autor: Lucas Arnaud de Araújo
# Trabalho de Conclusão de Curso em Engenharia Mecânica
# Universidade Federal de Pernambuco
# Projeto: ROBÔ SOLUCIONADOR DO CUBO DE RUBIK COM USO DE MOTORES DE PASSO E SENSORES DE COR
# Nome do arquivo: Código_final (utilizado no computador)
# Data de atualização: 17/09/2024

# Este código se divide em 3 partes:
# Parte 1: importação das bibliotecas, conexões com as seriais e definição das funções gerais;
# Parte 2: definição da função menu_principal que interege com o usuário e integra as funções gerais;
# Parte 3: execução da função menu_principal e fechamento das conexões seriais.

# Para mais detalhes acesse o arquivo PDF denominado [TCC_Lucas_Arnaud] disponibilizado nesta pasta do github.

#################################### PARTE 1 ####################################

############### IMPORTAÇÃO BIBLIOTECAS ################

# Importando bibliotecas
import serial
import time
import kociemba

############### CONEXÕES SERIAIS ################

# Configura a conexão serial para os sensores (Arduino UNO na porta serial COM 3)
try:  
    porta_serial_SENSORES = serial.Serial("COM3", 9600, timeout=1)  # Tenta abrir a porta serial COM3, com velocidade de 9600 bps e timeout de 1 segundo, para comunicação com o Arduino UNO e sensores
    print("Conectado à porta", porta_serial_SENSORES.portstr)  # Se a conexão acontecer, imprime uma mensagem confirmando a conexão e o nome da porta
except serial.SerialException:  # Caso ocorra um erro (porta não encontrada ou ocupada) na tentativa de conectar à porta serial 
    print("Porta USB não detectada")  # Imprime uma mensagem de erro informando que a porta não foi detectada
    exit()  # Encerra o programa após falha na conexão

# Configura a conexão serial para os motores (Arduino MEGA com a RAMPS 1.4 na porta serial COM 4)
try:
    porta_serial_MOTORES = serial.Serial("COM4", 250000)  # Tenta abrir a porta serial COM4, com velocidade de 250000 bps, usada para comunicação com os motores
    print("Conectado à porta", porta_serial_MOTORES.portstr)  # Se a conexão acontecer, imprime uma mensagem confirmando a conexão e o nome da porta
except serial.SerialException:  # Caso ocorra um erro (porta não encontrada ou ocupada) na tentativa de conectar à porta serial
    print("Porta USB não detectada")  # Imprime uma mensagem de erro informando que a porta não foi detectada
    exit()  # Encerra o programa após falha na conexão

############### DEFINIÇÕES DAS FUNÇÕES E DICIONÁRIO ################

#### DICIONÁRIO DOS COMANDOS G-CODE - FLUXOGRAMAS A, B e C
comandos = {
    "D":  ['G91','G0 X0.625 F300'],
    "D'": ['G91','G0 X-0.625 F300'],
    "D2": ['G91','G0 X1.250 F300'],
    "F":  ['G91','G0 Y-0.625 F300'],
    "F'": ['G91','G0 Y0.625 F300'],
    "F2": ['G91','G0 Y1.250 F300'],
    "R":  ['G91','G0 Z-0.625 F300'],
    "R'": ['G91','G0 Z0.625 F300'],
    "R2": ['G91','G0 Z1.250 F300'],
    "L":  ['M302 P1', 'T0', 'G91','G0 E0.625 F300'],
    "L'": ['M302 P1', 'T0', 'G91','G0 E-0.625 F300'],
    "L2": ['M302 P1', 'T0', 'G91','G0 E-1.250 F300'],
    "B":  ['M302 P1', 'T1', 'G91','G0 E0.625 F300'],
    "B'": ['M302 P1', 'T1', 'G91','G0 E-0.625 F300'],
    "B2": ['M302 P1', 'T1', 'G91','G0 E-1.250 F300'],
    "U":  ['M302 P1', 'T2', 'G91','G0 E2.500 F1500'],
    "U'": ['M302 P1', 'T2', 'G91','G0 E-2.500 F1500'],
    "U2": ['M302 P1', 'T2', 'G91','G0 E-5.000 F1500']
}

#### FUNÇÃO PARA ENVIAR COMANDOS PARA OS MOTORES - FLUXOGRAMAS A, B e C
def enviar_comando_motores(comando):
    porta_serial_MOTORES.write(bytes(comando + '\n', 'UTF-8'))  # Envia o comando, convertido em bytes com UTF-8, para a porta serial, adicionando uma nova linha no final
    time.sleep(0.250)  # Pequena pausa para garantir que o comando seja enviado

#### FUNÇÃO PARA MOVIMENTAR MOTORES A PARTIR DE UMA SEQUÊNCIA DE MOVIMENTOS - FLUXOGRAMAS A, B e C
def movimentar_motores(entrada):
    sequencia_movimentos = entrada.strip().upper() # Remove espaços em branco extras e transforma a sequência de movimentos em letras maiúsculas
    if sequencia_movimentos: # Verifica se a sequência de movimentos não está vazia
        movimentos = sequencia_movimentos.split() # Divide a sequência de movimentos em uma lista de comandos, assumindo que estão separados por espaços
        enviar_comando_motores('M302 P1') # Envia o comando 'M302 P1' para permitir a movimentação do extrusor a frio
        enviar_comando_motores('M203 E5') # Define a velocidade máxima do extrusor com o comando 'M203 E5'
        enviar_comando_motores('G91')     # Configura o sistema para modo de movimentação relativa, com o comando 'G91'
        
        for movimento in movimentos: # Para cada movimento na lista de movimentos
            if movimento in comandos: # Verifica se o movimento está na lista de comandos válidos
                gcode = comandos[movimento] # Obtém o comando G-code associado ao movimento a partir do dicionário 'comandos'
                
                # Para cada comando G-code associado ao movimento
                for cmd in gcode:
                    enviar_comando_motores(cmd) # Envia o comando G-code para os motores
            else: # Se o movimento não for reconhecido,
                print(f"Movimento '{movimento}' não reconhecido.")  # Imprime uma mensagem de erro
    else: # Se a sequência de movimentos estiver vazia
        print("Sequência de movimentos vazia.") # Imprime uma mensagem de aviso

#### FUNÇÃO ENVIAR COMANDOS PARA O ARDUINO UNO - FLUXOGRAMA C
def enviar_comando_sensores(comando):
    porta_serial_SENSORES.write(bytes(comando + '\n', 'UTF-8')) # Envia o comando, convertido em bytes com UTF-8, para a porta serial, adicionando uma nova linha no final
    time.sleep(0.1)  # Pequena pausa para garantir que o comando seja enviado

#### FUNÇÃO PARA LER LINHA DA SERIAL IMPRESSOS PELO ARDUINO UNO - FLUXOGRAMA C
def ler_linha_serial_sensores():
    return porta_serial_SENSORES.readline().decode('utf-8').strip()  # Lê uma linha completa da porta serial dos sensores, decodifica de UTF-8 para string, remove espaços em branco ou quebras de linha

#### FUNÇÃO PARA REALIZAR A LEITURA AUTOMÁTICA INTEGRANDO MOTORES E SENSORES - FLUXOGRAMA C
def leitura_automatica():
    comandos_leitura = [ #Definição da sequência de comandos de movimentos e de leitura para leitura dos 48 rótulos com 60 movimentos
    "L1", "L2", "R", "L'", "L1", "U", "L1", "L2", "U", "L1", "L2", "U", "L1", "L2", "U", 
    "F'", "B", "L2", "L1", "U", "L1", "U", "L1", "L2", "U", "L1", "U", "F2", "B2", "L1", 
    "L2", "U", "L1", "U", "L1", "L2", "U", "L1", "U", "R", "L'", "L1", "U", "L1", "L2", 
    "U", "L1", "U", "L1", "L2", "U", "F", "B'", "L1", "L2", "U", "L1", "U", "L1", "L2", 
    "U", "L1", "U", "R", "L'", "F", "B'", "L2", "U", "L1", "L2", "U", "L1", "L2", "U", 
    "L1", "L2", "U", "R", "L'", "F", "B'", "U", "L2", "U2", "L2", "U", "R", "L'", "F", 
    "B'", "L2", "U", "L2", "U", "L2", "U", "L2", "U", "R", "L'", "U", "L2", "U2", "L2", 
    "U", "F", "B'"]
    
    for comando in comandos_leitura:  # Envio de cada comando de acordo com a sua categoria (sensores ou motores)
    if comando.startswith("L1") or comando.startswith("L2"):  # Verifica se o comando é relacionado aos sensores (L1 ou L2)
        enviar_comando_sensores(comando)  # Envia o comando para os sensores
        while True:  # Loop para ler a resposta dos sensores de forma contínua até que não haja mais resposta
            resposta = ler_linha_serial_sensores()  # Lê uma linha da porta serial dos sensores
            if resposta:        # Se houver uma resposta
                print(resposta) # Imprime a resposta
            else:               # Se não houver resposta (resposta vazia)
                break           # Interrompe o loop
    else:  # Se o comando não for para sensores (é um comando para os motores)
        movimentar_motores(comando)  # Envia o comando para os motores

    print("Leitura do cubo finalizada.") # Imprime que a leitura foi finalizada

#### FUNÇÕES PARA A PARTIR DE UMA SEQUÊNCIA DE EMBARALHAMENTO FORMAR A STRING DE ESTADO DO CUBO (54) - FLUXOGRAMA D

def rotacionar_face_sentido_horario(face):     # Função para rotacionar uma face 90 graus no sentido horário
    return [face[6], face[3], face[0], face[7], face[4], face[1], face[8], face[5], face[2]]

def rotacionar_face_sentido_antihorario(face): # Função para rotacionar uma face 90 graus no anti-horário
    return [face[2], face[5], face[8], face[1], face[4], face[7], face[0], face[3], face[6]]

def rotacionar_face_180(face):                 # Função para rotacionar uma face em 180 graus
    return [face[8], face[7], face[6], face[5], face[4], face[3], face[2], face[1], face[0]]

# Função para aplicar movimentos ao cubo virtual e definir a string do cubo após uma sequência de movimentos
def aplicar_movimento(cubo, movimento):
    # Separa as faces do cubo
    U = list(cubo[0:9])
    R = list(cubo[9:18])
    F = list(cubo[18:27])
    D = list(cubo[27:36])
    L = list(cubo[36:45])
    B = list(cubo[45:54])
    # Reorganizando os itens das listas de acordo com cada movimento
    if movimento == "U": # se for o movimento U
        U = rotacionar_face_sentido_horario(U)
        F[0], F[1], F[2], R[0], R[1], R[2], B[0], B[1], B[2], L[0], L[1], L[2] = \
        R[0], R[1], R[2], B[0], B[1], B[2], L[0], L[1], L[2], F[0], F[1], F[2]
    elif movimento == "U'": # se for o movimento U'
        U = rotacionar_face_sentido_antihorario(U)
        F[0], F[1], F[2], R[0], R[1], R[2], B[0], B[1], B[2], L[0], L[1], L[2] = \
        L[0], L[1], L[2], F[0], F[1], F[2], R[0], R[1], R[2], B[0], B[1], B[2]
    elif movimento == "U2": # se for o movimento U2
        U = rotacionar_face_180(U)
        F[0], F[1], F[2], R[0], R[1], R[2], B[0], B[1], B[2], L[0], L[1], L[2] = \
        B[0], B[1], B[2], L[0], L[1], L[2], F[0], F[1], F[2], R[0], R[1], R[2]
    elif movimento == "R": # se for o movimento R
        R = rotacionar_face_sentido_horario(R)
        U[2], U[5], U[8], F[2], F[5], F[8], D[2], D[5], D[8], B[6], B[3], B[0] = \
        F[2], F[5], F[8], D[2], D[5], D[8], B[6], B[3], B[0], U[2], U[5], U[8]
    elif movimento == "R'": # se for o movimento R'
        R = rotacionar_face_sentido_antihorario(R)
        U[2], U[5], U[8], F[2], F[5], F[8], D[2], D[5], D[8], B[6], B[3], B[0] = \
        B[6], B[3], B[0], U[2], U[5], U[8], F[2], F[5], F[8], D[2], D[5], D[8]
    elif movimento == "R2": # se for o movimento R2
        R = rotacionar_face_180(R)
        U[2], U[5], U[8], F[2], F[5], F[8], D[2], D[5], D[8], B[6], B[3], B[0] = \
        D[2], D[5], D[8], B[6], B[3], B[0], U[2], U[5], U[8], F[2], F[5], F[8]
    elif movimento == "F": # se for o movimento F
        F = rotacionar_face_sentido_horario(F)
        U[6], U[7], U[8], R[0], R[3], R[6], D[0], D[1], D[2], L[8], L[5], L[2] = \
        L[8], L[5], L[2], U[6], U[7], U[8], R[6], R[3], R[0], D[2], D[1], D[0]
    elif movimento == "F'": # se for o movimento F'
        F = rotacionar_face_sentido_antihorario(F)
        U[6], U[7], U[8], R[0], R[3], R[6], D[0], D[1], D[2], L[8], L[5], L[2] = \
        R[0], R[3], R[6], D[2], D[1], D[0], L[2], L[5], L[8], U[6], U[7], U[8]
    elif movimento == "F2": # se for o movimento F2
        F = rotacionar_face_180(F)
        U[6], U[7], U[8], R[0], R[3], R[6], D[0], D[1], D[2], L[8], L[5], L[2] = \
        D[2], D[1], D[0], L[8], L[5], L[2], U[8], U[7], U[6], R[0], R[3], R[6]
    elif movimento == "D": # se for o movimento D
        D = rotacionar_face_sentido_horario(D)
        F[6], F[7], F[8], R[6], R[7], R[8], B[6], B[7], B[8], L[6], L[7], L[8] = \
        L[6], L[7], L[8], F[6], F[7], F[8], R[6], R[7], R[8], B[6], B[7], B[8]
    elif movimento == "D'": # se for o movimento D'
        D = rotacionar_face_sentido_antihorario(D)
        F[6], F[7], F[8], R[6], R[7], R[8], B[6], B[7], B[8], L[6], L[7], L[8] = \
        R[6], R[7], R[8], B[6], B[7], B[8], L[6], L[7], L[8], F[6], F[7], F[8]
    elif movimento == "D2": # se for o movimento D2
        D = rotacionar_face_180(D)
        F[6], F[7], F[8], R[6], R[7], R[8], B[6], B[7], B[8], L[6], L[7], L[8] = \
        B[6], B[7], B[8], L[6], L[7], L[8], F[6], F[7], F[8], R[6], R[7], R[8]
    elif movimento == "L": # se for o movimento L
        L = rotacionar_face_sentido_horario(L)
        U[0], U[3], U[6], F[0], F[3], F[6], D[0], D[3], D[6], B[2], B[5], B[8] = \
        B[8], B[5], B[2], U[0], U[3], U[6], F[0], F[3], F[6], D[6], D[3], D[0]
    elif movimento == "L'": # se for o movimento L'
        L = rotacionar_face_sentido_antihorario(L)
        U[0], U[3], U[6], F[0], F[3], F[6], D[0], D[3], D[6], B[2], B[5], B[8] = \
        F[0], F[3], F[6], D[0], D[3], D[6], B[8], B[5], B[2], U[6], U[3], U[0]
    elif movimento == "L2": # se for o movimento L2
        L = rotacionar_face_180(L)
        U[0], U[3], U[6], F[0], F[3], F[6], D[0], D[3], D[6], B[2], B[5], B[8] = \
        D[0], D[3], D[6], B[8], B[5], B[2], U[0], U[3], U[6], F[6], F[3], F[0]
    elif movimento == "B": # se for o movimento B
        B = rotacionar_face_sentido_horario(B)
        U[0], U[1], U[2], R[2], R[5], R[8], D[6], D[7], D[8], L[0], L[3], L[6] = \
        R[2], R[5], R[8], D[8], D[7], D[6], L[0], L[3], L[6], U[2], U[1], U[0]
    elif movimento == "B'": # se for o movimento B'
        B = rotacionar_face_sentido_antihorario(B)
        U[0], U[1], U[2], R[2], R[5], R[8], D[6], D[7], D[8], L[0], L[3], L[6] = \
        L[6], L[3], L[0], U[0], U[1], U[2], R[8], R[5], R[2], D[6], D[7], D[8]
    elif movimento == "B2": # se for o movimento B2
        B = rotacionar_face_180(B)
        U[0], U[1], U[2], R[2], R[5], R[8], D[6], D[7], D[8], L[0], L[3], L[6] = \
        D[8], D[7], D[6], L[6], L[3], L[0], U[2], U[1], U[0], R[8], R[5], R[2]
    
    return ''.join(U) + ''.join(R) + ''.join(F) + ''.join(D) + ''.join(L) + ''.join(B) # Combina todas as faces (U, R, F, D, L, B) em uma única string

#### FUNÇÃO PARA TRANSFORMAR ESTADO DO CUBO (54) PARA SEQUÊNCIA DE LEITURA (48) - FLUXOGRAMA E
def estado_para_leitura(estado):
    # Verifica se a string de entrada tem exatamente 54 caracteres
    if len(estado) != 54:
        raise ValueError("A string do cubo deve ter exatamente 54 caracteres.")
    
    # Define a ordem de leitura em que as posições serão lidas
    ordem_leitura = [
        6, 1, 24, 26, 21, 20, 7, 18, 23, 10, 15, 17, 11, 16, 9, 42, 37, 44, 38, 43, 36,
        35, 29, 25, 27, 33, 19, 45, 41, 51, 53, 39, 47, 28, 8, 32, 2, 34, 0, 30, 48, 50,
        14, 46, 12, 52, 3, 5
    ]
    # Cria a lista de 48 caracteres para armazenar a sequência correta da leitura a ser feita
    sequencia_a_ser_lida = [''] * 48

    # Organiza as posições reais na sequência da leitura
    for idx, pos in enumerate(ordem_leitura):
        sequencia_a_ser_lida[idx] = estado[pos]

    # Transforma a lista em string
    return ''.join(sequencia_a_ser_lida)

#### FUNÇÃO PARA CÁLCULO DO PERCENTUAL DE ACERTO DA LEITURA - FLUXOGRAMA F
def calcular_percentual_acerto(sequencia_lida, sequencia_correta):
    # Verifica se as duas strings de entrada tem exatamente 48 caracteres
    if len(sequencia_lida) != 48 or len(sequencia_correta) != 48: # se uma delas não tiver 48 caracteres
        raise ValueError("Ambas as sequências devem ter exatamente 48 caracteres.") # imprime mensagem de erro
    
    acertos = 0
    for i in range(48): # Em cada caractere até o 48
        if sequencia_lida[i] == sequencia_correta[i]: # Verifica se em cada caractere há igualdade
            acertos += 1 # Incrementa 1 no número de acertos
    
    percentual_acerto = (acertos / 48) * 100 # Calcula o percentual de acerto 
    return percentual_acerto                 # Retorna o valor do percentual de acerto

#################################### PARTE 2 ####################################

#### FUNÇÃO MENU PRINCIPAL QUE INTEGRA TODAS AS FUNÇÕES ANTERIORES E INTERAGE COM O USUÁRIO - FLUXOGRAMA DETALHADO
def menu_principal():
    # Define e imprime o Cubo inicial resolvido
    cubo_inicial = "UUUUUUUUURRRRRRRRRFFFFFFFFFDDDDDDDDDLLLLLLLLLBBBBBBBBB"
    print("Cubo inicial:               ", cubo_inicial)

    # Pede a sequência de movimentos de EMBARALHAMENTO para o usuário e armazena numa varíavel removendo espaços em branco no início e no final da string e convertendo todos os caracteres para letras maiúsculas
    sequencia_embaralhamento = input("1 - Digite a sequência de movimentos desejada para EMBARALHAR O CUBO: ").strip().upper()

    # Define o cubo virtual que será modificado (inicialmente resolvido)
    cubo = "UUUUUUUUURRRRRRRRRFFFFFFFFFDDDDDDDDDLLLLLLLLLBBBBBBBBB"

    # Aplica cada movimento do EMBARALHAMENTO no cubo virtual para definir como será o estado do cubo
    for movimento in sequencia_embaralhamento.split():
        cubo = aplicar_movimento(cubo, movimento)

    # Exibe os movimentos solicitados
    print("Sequência de embaralhamento:", sequencia_embaralhamento)

    # Imprime que o embaralhamento será realizado
    print("Realizando embaralhamento.....")
    time.sleep(2.0)

    # Executar os movimentos do EMBARALHAMENTO no cubo físico
    movimentar_motores(sequencia_embaralhamento)
    # Imprime que o embaralhamento foi finalizado
    print("Embaralhamento finalizado")
    
    # Exibe o estado final do cubo
    print("Cubo embaralhado (54):      ", cubo)

    # Armazena a sequência correta de estado do cubo na variável sequencia_correta aplicando a função estado_para_leitura no cubo virtual
    sequencia_correta = estado_para_leitura(cubo)
    # Exibe como deverá ser a sequência de leitura do cubo
    print("Sequência de leitura (48):  ", sequencia_correta)
    time.sleep(2.0)

    # Pede se o usuário deve deseja realizar a leitura e armazena a escolha numa variável
    escolha = input("2 - Deseja realizar a leitura do cubo? ('S'/'N')")
    if escolha == 'S': # se a escolha for "Sim"
        print(f"Com leitura.") # Imprime que haverá leitura
        time.sleep(1.0)
        leitura_automatica() # Implementa a leitura automática
        enviar_comando_sensores("P") # Envia o comando "P" ao Arduino UNO para que a sequência lida seja impressa na serial
        sequencia_lida = ler_linha_serial_sensores() # Lê a sequência impressa na serial e armazena na variável sequência lida
        print(f"Essa é a sequência lida (48): {sequencia_lida}") # Imprime a sequência lida
        print(f"Essa é a sequência correta (48): {sequencia_correta}") # Imprime a sequência correta
        percentual_acerto = calcular_percentual_acerto(sequencia_lida, sequencia_correta) # Calcula o percentual de acerto e armazena numa variável
        acertos_aux = (percentual_acerto/100)*48 # Calcula o número de acertos
        print(f"Número de acertos: {acertos_aux} de 48") # Imprime o número de acertos
        print(f"Percentual de acerto: {percentual_acerto:.2f}%") # Imprime o percentual de acertos
        time.sleep(3.0)
    elif escolha == 'N': # se a escolha for "Não"
        print(f"Sem leitura.") # Imprime que não haverá leitura
        time.sleep(1.0)
    else: # se a escolha não for "Sim" ou "Não"
        print("Opção inválida. Tente novamente.") # Imprime que a opção é inválida

    time.sleep(3.0)
    # Armazena na variável solution a sequência de movimentos de solução para o cubo embaralhado a partir da função solve da biblioteca kociemba
    solution = kociemba.solve(cubo)
    print("Calculando solução.....") # Imprime que está calculando a solução
    time.sleep(2.0)
    print("Por Kociemba, a solução é:  ", solution) # Imprime a solução
    time.sleep(2.0)
    print("Aplicando a solução.....") # Imprime que a solução está sendo aplicada
    movimentar_motores(solution) # Implementa a sequência de movimentos da solução no cubo físico
    print("Resolução finalizada") # Imprime que a resolução foi finalizada
    for movimento in solution.split(): # Aplica os movimentos da solução no cubo virtual que está embaralhado
        cubo = aplicar_movimento(cubo, movimento)
    print("Cubo restaurado (54):       ", cubo) # Imprime o cubo restaurado

#################################### PARTE 3 ####################################

# Inicia o menu principal
menu_principal()

# Fechar conexões seriais
porta_serial_SENSORES.close()
porta_serial_MOTORES.close()
print("Conexões fechadas")
