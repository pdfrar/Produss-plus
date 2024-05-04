import PySimpleGUI as sg #Importa a bilbioteca PySimpleGUI, onde pode foi definido que pode ser chamada como "sg".
global sites #Define-se a variável sites como global, para ser usada em qualquer função e classe
sites = ['site1.com', 'site2.com', 'site3.com'] #Define-se valores iniciais para os elementos da variável sites do tipo lista

class FrontEnd: #Cria-se a classe para o FrontEnd, a parte visual do programa que irá interagir com o usuário. 
    def LayoutDaJanelaParaInserirOsSites(self): #Dentro da classe FrontEnd, define-se a tarefa ao lado, com 
        global layoutinsercaodesites #Define-se a variável sites como global, para ser usada em qualquer função e classe
        layoutinsercaodesites = [ #Cria uma lista de elementos visuais, oriundos da biblioteca PySimpleGui, para servir como o layout da janela
            [sg.Text('Insira aqui o URL do site que deseja bloquear: ', font=("Arial", 11))], #Elemento de texto, com fonte Arial 11
            [sg.Input(size=(45,20),key='siteinserido')], #Elemento de Input (onde o usuário pode digitar), com o tamanho de 45x20 pixeis, com o input sendo salvo na key (que é tipo uma variável) siteinserido
            [sg.Button('OK',key='-OK-')] #Elemento de botão, com o botão "OK", guardado na key "-OK-"
        ]
        self.janelainsercaodesites = sg.Window('Insira seus sites', layoutinsercaodesites, resizable=True) #O "self" chama a própria função, executando e abrindo a janela com o layout criado
    
    def AbrirELerJanelaParaInserirOsSites(self): #Cria-se a tarefa para ler os valores inseridos pelo usuário
        self.event, self.values = self.janelainsercaodesites.read() #A janela pode retornar dois tipos de entrada, eventos (ex: botões) ou valores (ex: input de texto)
        print(f'{self.event} {self.values}') #Essa linha printa os valores resgatados da leitura da janela anteriormente criada.
        sites.append(self.values['siteinserido'])

class BackEnd: #Cria-se uma classe de tarefas para o BackEnd, onde ocorre o processamento dos dados e o usuário não tem acesso
    def InputNoArquivoDeTexto(self): #Cria-se a tarefa para ler o input do site e salvar em um arquivo de texto
        try: #A estrutura "try" tenta uma sequência de comandos, esperando um erro.
            with open('hosts.txt', 'w') as h: #Aqui é o comando para abrir o arquivo em modo de escrita sobre um arquivo já existente, representado pelo 'w'
                for i in range(len(sites)): #Este for repete pela qtd igual ao tamanho da lista de sites inseridos
                    h.write('127.0.0.1    {}\n'.format(sites[i])) #Aqui, escreve-se cada linha com o site já no formato do arquivo hosts, com o ip do PC antes do endereço do site.
        except FileNotFoundError: #Aqui é o erro esperado pela estrutura try. Esse erro ocorre quando tenta-se manipular um arquivo e o mesmo ainda não existe, portanto, utiliza-se essa estrutura para criar o arquivo quando ainda não houver o mesmo
            with open('hosts.txt', 'x') as h: #Aqui, cria-se o arquivo e depois o abre em modo de escrita.
                for i in range(len(sites)): #Essas linhas aqui são a mesma lógica da estrutura try acima.
                    h.write('127.0.0.1    {}}\n'.format(sites[i])) #''

#Aqui é onde são executadas as tarefas anteriormente criadas

front_end = FrontEnd() #Cria-se uma instância da classe FrontEnd, passando-a todos os atributos e tarefas da classe.
back_end = BackEnd()
front_end.LayoutDaJanelaParaInserirOsSites() #Chama a função da classe FrontEnd, executando-a.

while True:
    front_end.AbrirELerJanelaParaInserirOsSites() #Enquanto o usuário não parar o programa de alguma forma, o programa lerá os sites inseridos infinitamente.
    back_end.InputNoArquivoDeTexto()
