import PySimpleGUI as sg #Importa a bilbioteca PySimpleGUI, onde pode foi definido que pode ser chamada como "sg".
global sites #Define-se a variável sites como global, para ser usada em qualquer função e classe
import socket
import ctypes
global ip
soma = 0
global num_linhas
num_linhas = 0
sites = [] #Define-se valores iniciais para os elementos da variável sites do tipo lista

class FrontEnd: #Cria-se a classe para o FrontEnd, a parte visual do programa que irá interagir com o usuário. 
    def LayoutDaJanelaParaInserirOsSites(self): #Dentro da classe FrontEnd, define-se a tarefa ao lado, com 
        global layoutinsercaodesites #Define-se a variável sites como global, para ser usada em qualquer função e classe
        layoutinsercaodesites = [ #Cria uma lista de elementos visuais, oriundos da biblioteca PySimpleGui, para servir como o layout da janela
            [sg.Text('Insira aqui o URL do site que deseja bloquear: ', font=("Arial", 11))], #Elemento de texto, com fonte Arial 11
            [sg.Input(size=(45,20),key='siteinserido')], #Elemento de Input (onde o usuário pode digitar), com o tamanho de 45x20 pixeis, com o input sendo salvo na key (que é tipo uma variável) siteinserido
            [sg.Button('ADICIONAR',key='add')],
            [sg.Button('BLOQUEAR SITES ADICIONADOS',key='block')],
            [sg.Button('DESATIVAR',key='des')]
        ]
        self.janelainsercaodesites = sg.Window('Insira seus sites', layoutinsercaodesites, resizable=True) #O "self" chama a própria função, executando e abrindo a janela com o layout criado
    
    def AbrirELerJanelaParaInserirOsSites(self): #Cria-se a tarefa para ler os valores inseridos pelo usuário
        self.event, self.values = self.janelainsercaodesites.read() #A janela pode retornar dois tipos de entrada, eventos (ex: botões) ou valores (ex: input de texto)
        print(f'{self.event} {self.values}') #Essa linha printa os valores resgatados da leitura da janela anteriormente criada.
        if self.event == 'add':
            sites.append(self.values['siteinserido'])
        return self.event

class BackEnd: #Cria-se uma classe de tarefas para o BackEnd, onde ocorre o processamento dos dados e o usuário não tem acesso
    
    def contar_linhas():
        global num_linhas
        with open('sitesparabloquear.txt', 'r') as arquivo:
            for linha in arquivo:
                num_linhas += 1
        return num_linhas
    
    def sitesiniciais():
        with open('sitesparabloquear.txt', 'r') as arquivo:
            for linha in arquivo:
                sites.append(linha)
    
    def InputNoArquivoDeTexto(self): #Cria-se a tarefa para ler o input do site e salvar em um arquivo de texto
        #try: #A estrutura "try" tenta uma sequência de comandos, esperando um erro.
        
        retorninho = front_end.AbrirELerJanelaParaInserirOsSites()

        if retorninho == 'add':
            with open('sitesparabloquear.txt', 'a+') as h: #Aqui é o comando para abrir o arquivo em modo de escrita sobre um arquivo já existente, representado pelo 'w'
                h.write(f'{sites[-1]}\n') #Aqui, escreve-se cada linha com o site já no formato do arquivo hosts, com o ip do PC antes do endereço do site.
        elif retorninho == 'block': 
            with open('C:\Windows\System32\drivers\etc\hosts', 'a+') as h:
                for i in range(BackEnd.contar_linhas()): #Essas linhas aqui são a mesma lógica da estrutura try acima.
                    h.write('127.0.0.1    {}\n'.format(sites[i])) #''
#Aqui é onde são executadas as tarefas anteriormente criadas

front_end = FrontEnd() #Cria-se uma instância da classe FrontEnd, passando-a todos os atributos e tarefas da classe.
back_end = BackEnd()
front_end.LayoutDaJanelaParaInserirOsSites() #Chama a função da classe FrontEnd, executando-a.
BackEnd.sitesiniciais()

while ctypes.windll.shell32.IsUserAnAdmin() != 0:
    back_end.InputNoArquivoDeTexto()

sg.popup("Você deve executar o programa como administrador.")
