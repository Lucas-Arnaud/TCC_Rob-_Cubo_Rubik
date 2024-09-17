#define PinS2_1  4 //Definição do Pino S2_1 na entrada digital 3
#define PinS3_1 3 //Definição do Pino S3_1 na entrada digital 4
#define PinOUT_1 5 //Definição do Pino OUT_1 na entrada digital 5

#define PinS2_2  9 //Definição do Pino S2_2 na entrada digital 8
#define PinS3_2 8 //Definição do Pino S3_2 na entrada digital 9
#define PinOUT_2 10 //Definição do Pino OUT_2 na entrada digital 10

int red[2]; //Declaração da variável que representará a cor vermelha
int green[2]; //Declaração da variável que representará a cor verde
int blue[2]; // Declaração da variável que representará a cor azul
bool fazer_Leitura = false;
String sequencia_cores = ""; // String para armazenar a sequência de cores lidas
int sensorAtual = -1; // Variável para armazenar qual sensor usar

void classificar_cor_1(int red, int green, int blue); // Inicialização da nova função de classificação
void classificar_cor_2(int red, int green, int blue); // Inicialização da nova função de classificação

void setup() {
  pinMode(PinOUT_1, INPUT); //Definição do PinOUT como sendo um pino de entrada
  pinMode(PinS2_1, OUTPUT); //Definição do Pino S2 como sendo um pino de saída
  pinMode(PinS3_1, OUTPUT); //Definição do Pino S3 como sendo um pino de saída
  
  pinMode(PinOUT_2, INPUT); //Definição do PinOUT como sendo um pino de entrada
  pinMode(PinS2_2, OUTPUT); //Definição do Pino S2 como sendo um pino de saída
  pinMode(PinS3_2, OUTPUT); //Definição do Pino S3 como sendo um pino de saída

  Serial.begin(9600); //Inicia o monitor Serial com velocidade de 9600
}

void loop() {
  if (Serial.available() > 0) { // Verifica se há dados disponíveis na porta serial
    String input = Serial.readStringUntil('\n'); // Lê a linha recebida

    if (input == "L1") { // Se o caractere recebido for 'L1'
      sensorAtual = 1; // Define sensorAtual como 1
      fazer_Leitura = true; // Define fazer_Leitura como verdadeiro
    } else if (input == "L2") { // Se o caractere recebido for 'L2'
      sensorAtual = 2; // Define sensorAtual como 2
      fazer_Leitura = true; // Define fazer_Leitura como verdadeiro
    } else if (input == "P") { // Se o caractere recebido for 'P'
      Serial.println(sequencia_cores); // Imprime a sequência de cores armazenada
    }
  }

  if (fazer_Leitura) { // Se fazer_Leitura for verdadeiro
    if (sensorAtual == 1) {
      // Leitura das cores do sensor 1
      digitalWrite(PinS2_1, LOW); // Aciona um valor LOW ao Pino S2
      digitalWrite(PinS3_1, LOW); // Aciona um valor LOW ao Pino S3
      red[0] = pulseIn(PinOUT_1, LOW); // define red como sendo responsável por ler a informação de pulso LOW do pino out
      red[0] = map (red[0], 13, 55, 255, 0);
      delay(15); // delay de 15 milissegundos até o próximo comando
      digitalWrite(PinS2_1, HIGH); // Aciona um valor HIGH ao Pino S2
      digitalWrite(PinS3_1, HIGH); // Aciona um valor HIGH ao Pino S3
      green[0] = pulseIn(PinOUT_1, LOW); // define green como sendo responsável por ler a informação de pulso LOW do pino out
      green[0] = map (green[0], 11, 60, 255, 0); //era 40 no lugar de 50
      delay(15); // delay de 15 milissegundos até o próximo comando
      digitalWrite(PinS2_1, LOW); // Aciona um valor LOW ao Pino S2
      digitalWrite(PinS3_1, HIGH); // Aciona um valor HIGH ao Pino S3
      blue[0] = pulseIn(PinOUT_1, LOW); // define blue como sendo responsável por ler a informação de pulso LOW do pino out
      blue[0] = map (blue[0], 13, 47, 255, 0);
      delay(15); // delay de 15 milissegundos até o próximo comando

      // Imprimindo valores e definindo as cores do SENSOR 1
      Serial.print("Sensor 1: ");
      //delay(100);
      Serial.print(red[0]);
      //delay(100);
      Serial.print("\t| ");
      //delay(100);
      Serial.print(green[0]);
      //delay(100);
      Serial.print("\t| ");
      //delay(100);
      Serial.print(blue[0]);
      //delay(100);
      Serial.print("\t| ");
      //delay(100);
      //Serial.println("TESTE_1");
      //delay(100);
      classificar_cor_1(red[0], green[0], blue[0]);
      
       // Chamada da função classificar_cor para o SENSOR 1
    } else if (sensorAtual == 2) {
      // Leitura das cores do sensor 2
      digitalWrite(PinS2_2, LOW); // Aciona um valor LOW ao Pino S2
      digitalWrite(PinS3_2, LOW); // Aciona um valor LOW ao Pino S3
      red[1] = pulseIn(PinOUT_2, LOW); // define red como sendo responsável por ler a informação de pulso LOW do pino out
      red[1] = map (red[1], 17, 111, 255, 0); //era 71 no lugar de 75
      delay(15); // delay de 15 milissegundos até o próximo comando
      digitalWrite(PinS2_2, HIGH); // Aciona um valor HIGH ao Pino S2
      digitalWrite(PinS3_2, HIGH); // Aciona um valor HIGH ao Pino S3
      green[1] = pulseIn(PinOUT_2, LOW); // define green como sendo responsável por ler a informação de pulso LOW do pino out
      green[1] = map (green[1], 19, 96, 255, 0);
      delay(15); // delay de 15 milissegundos até o próximo comando
      digitalWrite(PinS2_2, LOW); // Aciona um valor LOW ao Pino S2
      digitalWrite(PinS3_2, HIGH); // Aciona um valor HIGH ao Pino S3
      blue[1] = pulseIn(PinOUT_2, LOW); // define blue como sendo responsável por ler a informação de pulso LOW do pino out
      blue[1] = map (blue[1], 14, 75, 255, 0);
      delay(15); // delay de 15 milissegundos até o próximo comando

      // Imprimindo valores e definindo as cores do SENSOR 2
      Serial.print("Sensor 2: ");
      Serial.print(red[1]);
      Serial.print("\t| ");
      Serial.print(green[1]);
      Serial.print("\t| ");
      Serial.print(blue[1]);
      Serial.print("\t| ");
      classificar_cor_2(red[1], green[1], blue[1]); // Chamada da função classificar_cor para o SENSOR 2
    }
    fazer_Leitura = false;
  }
}

void classificar_cor_1(int red, int green, int blue) {

  //delay(100);
  //Serial.println("TESTE_2");
  //delay(100);

  // 60 amostras de cada cor (red, green, blue)
  int amostras[60][3] = {
    {219, 203, 210}, {213, 203, 218}, {225, 203, 218}, {219, 203, 218}, {219, 229, 218}, {213, 208, 218}, {213, 193, 203}, 
    {206, 187, 195}, {206, 193, 203}, {200, 187, 195}, //BRANCO
    {158, 114, 38}, {158, 146, 38}, {134, 104, 45}, {152, 114, 53}, {152, 125, 53}, {140, 130, 68}, {188, 120, 60},
    {164, 125, 60}, {176, 135, 75}, {170, 135, 75}, // AMARELO
    {170, 99, 105}, {176, 135, 150}, {152, 99, 98}, {140, 104, 38}, {109, 26, 45}, {164, 104, 90}, {128, 62, 45}, 
    {146, 52, 60}, {134, 62, 45}, {158, 104, 90}, //VERMELHO
    {170, 78, 45}, {176, 114, 68}, {170, 109, 90}, {164, 88, 75}, {188, 141, 135}, {164, 83, 68}, {152, 83, 113},
    {188, 130, 120}, {146, 78, 83}, {158, 83, 83}, //LARANJA
    {61, 104, 68}, {79, 99, 68}, {73, 99, 60}, {73, 114, 90}, {115, 135, 128}, {55, 78, 68}, {30, 78, 68}, 
    {97, 99, 75}, {85, 109, 98}, {109, 104, 60}, //VERDE
    {55, 99, 105}, {55, 52, 83}, {43, 73, 90}, {61, 62, 98}, {67, 83, 98}, {67, 52, 90}, {67, 83, 120}, {103, 94, 113}, 
    {79, 73, 105}, {91, 73, 113} // AZUL
};


  // Nome das cores
  String cores[6] = {"U - Branco", "D - Amarelo", "F - Vermelho", "B - Laranja",  "L - Verde", "R - Azul"};

  // Armazenar distâncias e índice de cores correspondentes
  float distancias[60];
  int indices_cor[60];

  //delay(100);
  //Serial.println("TESTE_3");
 // delay(100);

  // Calcular a distância euclidiana para cada amostra
  for (int i = 0; i < 60; i++) {
    int amostraRed = amostras[i][0];
    int amostraGreen = amostras[i][1];
    int amostraBlue = amostras[i][2];

    distancias[i] = sqrt(
      pow((red - amostraRed), 2) +
      pow((green - amostraGreen), 2) +
      pow((blue - amostraBlue), 2)
    );

    // Classificar as amostras em cores (divisão por blocos de 10)
    if (i < 10) {
      indices_cor[i] = 0; // Branco
    } else if (i < 20) {
      indices_cor[i] = 1; // Amarelo
    } else if (i < 30) {
      indices_cor[i] = 2; // Vermelho
    } else if (i < 40) {
      indices_cor[i] = 3; // Laranja
    } else if (i < 50) {
      indices_cor[i] = 4; // Verde
    } else {
      indices_cor[i] = 5; // Azul
    }
  }

  // Ordenar as distâncias (com bubble sort por simplicidade)
  for (int i = 0; i < 59; i++) {
    for (int j = 0; j < 59 - i; j++) {
      if (distancias[j] > distancias[j + 1]) {
        // Troca de distâncias
        float tempDist = distancias[j];
        distancias[j] = distancias[j + 1];
        distancias[j + 1] = tempDist;

        // Troca de índices de cor correspondente
        int tempIndex = indices_cor[j];
        indices_cor[j] = indices_cor[j + 1];
        indices_cor[j + 1] = tempIndex;
      }
    }
  }

  // Agora, fazemos a votação com os 3 vizinhos mais próximos (K=3)
  int votos[6] = {0, 0, 0, 0, 0, 0};  // Corrigido para 6 posições, uma para cada cor

  for (int i = 0; i < 3; i++) {
    votos[indices_cor[i]]++;  // Adiciona um voto para a cor correspondente
  }

  // Encontrar a cor com o maior número de votos
  int maiorVoto = 0;
  int indiceCor = -1;
  for (int i = 0; i < 6; i++) {
    if (votos[i] > maiorVoto) {
      maiorVoto = votos[i];
      indiceCor = i;
    }
  }

  // Exibe a cor identificada
  if (indiceCor != -1) {
    //delay(15);
    Serial.println(cores[indiceCor]);
    sequencia_cores += cores[indiceCor].charAt(0);  // Armazena a primeira letra da cor
  } else {
    Serial.println("Desconhecida");
    sequencia_cores += 'X';
  }

  //Serial.println(sequencia_cores);  // Exibe a sequência de cores
}

void classificar_cor_2(int red, int green, int blue) {

  //delay(100);
  //Serial.println("TESTE_2");
  //delay(100);

  // 60 amostras de cada cor (red, green, blue)
  int amostras[30][3] = {
    {228, 238, 230}, {231, 238, 230}, {231, 235, 230}, {231, 238, 234}, {225, 232, 230},// BRANCO
    {184, 162, 79}, {190, 169, 92}, {187, 166, 88}, {184, 162, 84}, {193, 176, 96}, // AMARELO
    {152, 33, 63}, {155, 30, 42}, {152, 43, 54}, {155, 36, 42}, {152, 33, 46}, // VERMELHO
    {184, 93, 54}, {187, 93, 84}, {182, 106, 63}, {171, 86, 75}, {187, 96, 59},  // LARANJA
    {35, 93, 50}, {33, 89, 54}, {30, 89, 50}, {27, 86, 46}, {33, 89, 46},  // VERDE
    {22, 46, 92}, {22, 40, 88}, {19, 46, 121}, {27, 50, 100}, {35, 56, 100},  // AZUL
};


  // Nome das cores
  String cores[6] = {"U - Branco", "D - Amarelo", "F - Vermelho", "B - Laranja", "L - Verde", "R - Azul"};

  // Armazenar distâncias e índice de cores correspondentes
  float distancias[30];
  int indices_cor[30];

  //delay(100);
  //Serial.println("TESTE_3");
  //delay(100);

  // Calcular a distância euclidiana para cada amostra
  for (int i = 0; i < 30; i++) {
    int amostraRed = amostras[i][0];
    int amostraGreen = amostras[i][1];
    int amostraBlue = amostras[i][2];

    distancias[i] = sqrt(
      pow((red - amostraRed), 2) +
      pow((green - amostraGreen), 2) +
      pow((blue - amostraBlue), 2)
    );

    // Classificar as amostras em cores (divisão por blocos de 10)
    if (i < 5) {
      indices_cor[i] = 0; // Branco
    } else if (i < 10) {
      indices_cor[i] = 1; // Amarelo
    } else if (i < 15) {
      indices_cor[i] = 2; // Vermelho
    } else if (i < 20) {
      indices_cor[i] = 3; // Laranja
    } else if (i < 25) {
      indices_cor[i] = 4; // Verde
    } else {
      indices_cor[i] = 5; // Azul
    }
  }

  // Ordenar as distâncias (com bubble sort por simplicidade)
  for (int i = 0; i < 29; i++) {
    for (int j = 0; j < 29 - i; j++) {
      if (distancias[j] > distancias[j + 1]) {
        // Troca de distâncias
        float tempDist = distancias[j];
        distancias[j] = distancias[j + 1];
        distancias[j + 1] = tempDist;

        // Troca de índices de cor correspondente
        int tempIndex = indices_cor[j];
        indices_cor[j] = indices_cor[j + 1];
        indices_cor[j + 1] = tempIndex;
      }
    }
  }

  // Agora, fazemos a votação com os 3 vizinhos mais próximos (K=3)
  int votos[6] = {0, 0, 0, 0, 0, 0};  // Corrigido para 6 posições, uma para cada cor

  for (int i = 0; i < 3; i++) {
    votos[indices_cor[i]]++;  // Adiciona um voto para a cor correspondente
  }

  // Encontrar a cor com o maior número de votos
  int maiorVoto = 0;
  int indiceCor = -1;
  for (int i = 0; i < 6; i++) {
    if (votos[i] > maiorVoto) {
      maiorVoto = votos[i];
      indiceCor = i;
    }
  }
   //delay(5000);
  // Exibe a cor identificada
  if (indiceCor != -1) {
    //delay(15);
    Serial.println(cores[indiceCor]);
    sequencia_cores += cores[indiceCor].charAt(0);  // Armazena a primeira letra da cor
  } else {
    Serial.println("Desconhecida");
    sequencia_cores += 'X';
  }

  //Serial.println(sequencia_cores);  // Exibe a sequência de cores
}
