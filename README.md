# Robô Solucionador do Cubo de Rubik com uso de motores de passo e sensores de cor
Trabalho de Conclusão de Curso desenvolvido por Lucas Arnaud de Araújo e orientação do professor Dr. José Rodrigues de Oliveira Neto  submetido ao Departamento de Engenharia Mecânica da Universidade Federal de Pernambuco como requisito parcial para obtenção do título de Bacharel em Engenharia Mecânica.
## Resumo
Este projeto apresenta o desenvolvimento de um robô solucionador do cubo de Rubik, focando em velocidade de resolução e simplicidade da leitura das cores do cubo. Sendo assim, o robô foi projetado com o objetivo de identificar as cores das peças do cubo usando sensores de cor e, com base nesses dados, aplicar um algoritmo eficiente para calcular e executar a sequência de movimentos necessária, com uso de motores de passo, para solucionar o quebra-cabeça. Para esse fim, foram abordados aspectos específicos de projeto mecânico, eletrônica, programação e algoritmos. Com isso, o robô desenvolvido utiliza de seis motores de passo conectados aos eixos centrais do cubo, permitindo a rotação ordenada das faces, para realização da leitura e da resolução do cubo. 

Por outro lado, a leitura das cores é realizada com dois sensores de cor, a partir de um método próprio que realiza a leitura dos 48 quadrados com 60 movimentos das faces. Além disso, se implementou o algoritmo k-ésimo vizinho mais próximo (KNN, do inglês K-nearest neighbors) para classificar em cores os valores capturados pelos sensores e também um código para calcular a precisão das leituras automaticamente a partir de um embaralhamento aleatório empregado no robô. Ademais, utilizou-se uma implementação em código do algoritmo de Kociemba para encontrar a solução do cubo com no máximo 20 movimentos. Além da construção do robô, foram explorados conceitos importantes no uso de microcontroladores e de transferências de dados para integrar sensores e motores com um computador e viabilizar a leitura e a resolução do cubo. 

O projeto foi validado em testes para diferentes padrões do cubo e demonstrou sua capacidade de operar de forma eficaz. Nessas avaliações, o robô alcançou uma mediana de 39 leituras corretas e acertou 1375 das 1776 leituras (77,42\%) de cores. Acerca da velocidade, foi alcançado um tempo mínimo de resolução de 3,3 segundos, um desempenho comparável a projetos de referência na área.
## Imagens
![image](https://github.com/user-attachments/assets/33190a0c-9096-4076-8430-f4bd501f8b46)
## Extra
Para mais informações consultar o PDF nomeado TCC_Lucas_Arnaud.


