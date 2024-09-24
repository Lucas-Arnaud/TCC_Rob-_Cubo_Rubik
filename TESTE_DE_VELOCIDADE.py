# Autor: Lucas Arnaud de Araújo
# Trabalho de Conclusão de Curso em Engenharia Mecânica
# Universidade Federal de Pernambuco
# Projeto: ROBÔ SOLUCIONADOR DO CUBO DE RUBIK COM USO DE MOTORES DE PASSO E SENSORES DE COR
# Nome do arquivo: TESTE_DE_VELOCIDADE (utilizado no computador)
# Data de atualização: 24/09/2024

# Este código utiliza do arquivo "Código_Final" apenas as etapas necessárias para movimentar os motores de acordo com os padrões para realização dos testes de velocidade.
# Deve-se escolher a sequência de movimentos e o intervalo entre comandos que estão comentados para realizar os testes desejados.
# Para mais detalhes acesse o arquivo PDF denominado [TCC_Lucas_Arnaud] disponibilizado nesta pasta do github.

############### IMPORTAÇÃO BIBLIOTECAS ################
import serial
import time

# Dicionário de comandos G-code
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

############### CONEXÃO SERIAL ################
# Configura a conexão serial para os motores (Arduino MEGA com a RAMPS 1.4 na porta serial COM 4)
try:
    porta_serial_MOTORES = serial.Serial("COM4", 250000)  # Tenta abrir a porta serial COM4, com velocidade de 250000 bps, usada para comunicação com os motores
    print("Conectado à porta", porta_serial_MOTORES.portstr)  # Se a conexão acontecer, imprime uma mensagem confirmando a conexão e o nome da porta
except serial.SerialException:  # Caso ocorra um erro (porta não encontrada ou ocupada) na tentativa de conectar à porta serial
    print("Porta USB não detectada")  # Imprime uma mensagem de erro informando que a porta não foi detectada
    exit()  # Encerra o programa após falha na conexão

############### DEFINIÇÃO DOS PADRÕES PARA REALIZAÇÃO DOS TESTES ################
###### PADRÃO 1 #######
#sequencia_movimentos =  "R' F2 U R L D F2 R' U2 F2 D' R2 F2 B2 D R2 D' L2 U2 F2"    #exemplo de solução
#sequencia_movimentos = "F2 U2 L2 D R2 D' B2 F2 R2 D F2 U2 R F2 D' L' R' U' F2 R "   #embaralhamento
###### PADRÃO 2 #######
#sequencia_movimentos =  "F2 U B2 L' D' F2 R U B2 U2 F2 R2 F2 U R2 D F2 R2 U2 F2 "    #exemplo de solução
#sequencia_movimentos = "F2 U2 R2 F2 D' R2 U' F2 R2 F2 U2 B2 U' R' F2 D L B2 U' F2"   #embaralhamento
###### PADRÃO 3 #######
#sequencia_movimentos =  "U2 D F' R D2 F2 D2 B2 D' R2 U R L2 F' L2 F2 R2 F2 D2 B2"    #exemplo de solução
#sequencia_movimentos = "B2 D2 F2 R2 F2 L2 F L2 R' U' R2 D B2 D2 F2 D2 R' F D' U2"    #embaralhamento
###### PADRÃO 4 #######
#sequencia_movimentos =  "L2 F2 B2 D2 F2 U' L D F' B' U' L2 D R2 D' F2 U R2 L2 U"    #exemplo de solução
#sequencia_movimentos = "U' L2 R2 U' F2 D R2 D' L2 U B F D' L' U F2 D2 B2 F2 L2"     #embaralhamento
###### PADRÃO 5 #######
#sequencia_movimentos =  "U F2 B2 R F D R2 F2 L' B' R' B2 R F' U2 F2 D' L2 D R2"     #exemplo de solução
#sequencia_movimentos = "R2 D' L2 D F2 U2 F R' B2 R B L F2 R2 D' F' R' B2 F2 U'"     #embaralhamento
###### PADRÃO 6 #######
#sequencia_movimentos =  "U F' L' F L2 B' L' D' B2 R' D' L' U B R2 U' R2 U B2 U "    #exemplo de solução
#sequencia_movimentos = "U' B2 U' R2 U R2 B' U' L D R B2 D L B L2 F' L F U' "        #embaralhamento
###### PADRÃO 7 #######
#sequencia_movimentos =  "L U' D2 L D2 B R L' B' R2 U2 B' U L2 F2 U F2 B2 U D "      #exemplo de solução
#sequencia_movimentos = "D' U' B2 F2 U' F2 L2 U' B U2 R2 B L R' B' D2 L' D2 U L'"    #embaralhamento
###### PADRÃO 8  #######
#sequencia_movimentos =  "B' L' F' U F B U D2 B' R F' R2 U2 L2 D' L2 D2 R2 F2 D"     #exemplo de solução
#sequencia_movimentos = "D' F2 R2 D2 L2 D L2 U2 R2 F R' B D2 U' B' F' U' F L B"      #embaralhamento
###### PADRÃO 9 #######
#sequencia_movimentos =  "R' F2 R B' U B D2 R' B R2 F' U2 R U2 F2 R2 D L2 F2 U2"     #exemplo de solução
#sequencia_movimentos = "U2 F2 L2 D' R2 F2 U2 R' U2 F R2 B' R D2 B' U' B R' F2 R"    #embaralhamento
###### PADRÃO 10 #######   
#sequencia_movimentos =  "R' D B' R' F B L B R2 D2 B2 D' L U2 F2 U' R2 U2 F2"        #exemplo de solução
#sequencia_movimentos = "F2 U2 R2 U F2 U2 L' D B2 D2 R2 B' L' B' F' R B D' R"        #embaralhamento

sequencia_movimentos = entrada.strip().upper() # Remove espaços em branco extras e transforma a sequência de movimentos em letras maiúsculas
if sequencia_movimentos: # Verifica se a sequência de movimentos não está vazia
   movimentos = sequencia_movimentos.split() # Divide a sequência de movimentos em uma lista de comandos, assumindo que estão separados por espaços
   for movimento in movimentos: # Para cada movimento na lista de movimentos
       if movimento in comandos: # Verifica se o movimento está na lista de comandos válidos
          gcode = comandos[movimento] # Obtém o comando G-code associado ao movimento a partir do dicionário 'comandos'  
          # Para cada comando G-code associado ao movimento
          for cmd in gcode:
          porta_serial.write(bytes(cmd + '\n', 'UTF-8')) # Envia o comando G-code para os motores
          ##INTERVALOS DE ENVIO ENTRE OS COMANDOS PARA ESCOLHER E REALIZAR OS TESTES##
          #time.sleep (0.500)
          #time.sleep (0.1) 
          #time.sleep (0.0500)
          #time.sleep (0.0450)
# Fecha as conexões seriais
porta_serial.close()
print("Conexão fechada")
