import PySimpleGUI as sg #Importa a bilbioteca PySimpleGUI, onde pode foi definido que pode ser chamada como "sg".
global sites #Define-se a variável sites como global, para ser usada em qualquer função e classe
import socket
import ctypes
global ip
soma = 0
global num_linhas
num_linhas = 0
sites = [] #Define-se valores iniciais para os elementos da variável sites do tipo lista
linhasparaapagar = []
sitesparamostrar = []
class FrontEnd: #Cria-se a classe para o FrontEnd, a parte visual do programa que irá interagir com o usuário. 
    def LayoutDaJanelaParaInserirOsSites(self): #Dentro da classe FrontEnd, define-se a tarefa ao lado, com 
        global layoutinsercaodesites #Define-se a variável sites como global, para ser usada em qualquer função e classe
        layoutinsercaodesites = [ #Cria uma lista de elementos visuais, oriundos da biblioteca PySimpleGui, para servir como o layout da janela
            [sg.Text('Insira aqui o URL do site que deseja bloquear: ', font=("Arial", 11))], #Elemento de texto, com fonte Arial 11
            [sg.Input(size=(45,20),key='siteinserido')], #Elemento de Input (onde o usuário pode digitar), com o tamanho de 45x20 pixeis, com o input sendo salvo na key (que é tipo uma variável) siteinserido
            [sg.Button('ADICIONAR SITE',key='add')],
            [sg.Button('REMOVER ALGUNS SITES',key='removeralguns')],
            [sg.Button('BLOQUEAR SITES ADICIONADOS',key='block')],
            [sg.Button('DESATIVAR BLOQUEIO',key='des')]
        ]
        self.janelainsercaodesites = sg.Window('Insira seus sites', layoutinsercaodesites, resizable=True) #O "self" chama a própria função, executando e abrindo a janela com o layout criado

    def LayoutDaJanelaParaApagarAlgunsSites(self): #Dentro da classe FrontEnd, define-se a tarefa ao lado, com 
        global sitesparamostrar
        linhasparaapagar.clear() #ATÉ A LINHA 35 ADICIONEI AGORA PQ ELE NÃO EXCLUÍA SE NÃO TIVESSE NO HOST AINDA
        for i in range(0, len(sites)):
            linhasparaapagar.append(sites[i])
        sitesparamostrar.clear()
        for element in linhasparaapagar:
            sitesparamostrar.append([sg.Checkbox(f'{element}',key=f'{element}',size=(45,1))])
        global layoutexclusaodesites #Define-se a variável sites como global, para ser usada em qualquer função e classe
        layoutexclusaodesites = [ #Cria uma lista de elementos visuais, oriundos da biblioteca PySimpleGui, para servir como o layout da janela
            [sg.Text('Selecione os sites que deseja excluir da lista de bloqueio: ', font=("Arial", 11))], #Elemento de texto, com fonte Arial 11
            *[[site] for site in sitesparamostrar],
            [sg.Button('OK',key='-OK-')]
        ]
        self.janelaexclusaodesites = sg.Window('Insira seus sites', layoutexclusaodesites, resizable=True) #O "self" chama a própria função, executando e abrindo a janela com o layout criado

        return self.janelaexclusaodesites
    
    def AbrirELerJanelaParaInserirOsSites(self): #Cria-se a tarefa para ler os valores inseridos pelo usuário
        self.event, self.values = self.janelainsercaodesites.read() #A janela pode retornar dois tipos de entrada, eventos (ex: botões) ou valores (ex: input de texto)
        if self.event == 'add':
            spb = open('sitesparabloquear.txt', 'r')
            print(list(spb))
            if f'{self.values['siteinserido']}\n' not in spb and self.values['siteinserido'] not in spb and self.values['siteinserido'] != '\n':
                sites.append(self.values['siteinserido'])
        return self.event
        
    
class BackEnd: #Cria-se uma classe de tarefas para o BackEnd, onde ocorre o processamento dos dados e o usuário não tem acesso
    
    def limparHost():
        linhasparaapagar.clear()
        with open('C:\Windows\System32\drivers\etc\hosts', 'r') as arqhost:
            linhashost = arqhost.readlines()
        for i, linha in enumerate(linhashost):
            if linha[0] != '#':
                linhasparaapagar.append(i)
        with open('C:\Windows\System32\drivers\etc\hosts', 'w') as arqhost:
            for i, linha in enumerate(linhashost):
                if i not in linhasparaapagar:
                    arqhost.write(linha)

    def contar_linhas(arq):
        global num_linhas
        num_linhas = 0
        with open(f'{arq}', 'r') as arquivo:
            for linha in arquivo:
                num_linhas += 1
        return num_linhas
    
    def sitesiniciais():
        with open('sitesparabloquear.txt', 'r') as arquivo:
            for linha in arquivo:
                sites.append(linha)
    
    def ControleDeOcorrencias(self): #Cria-se a tarefa para ler o input do site e salvar em um arquivo de texto
        global sites
        #try: #A estrutura "try" tenta uma sequência de comandos, esperando um erro.
        
        retorninho = front_end.AbrirELerJanelaParaInserirOsSites()

        if retorninho == 'add':
            spb = open('sitesparabloquear.txt', 'r')
            if f'{sites[-1]}\n' not in spb and sites[-1] not in spb:
                with open('sitesparabloquear.txt', 'a+') as h: #Aqui é o comando para abrir o arquivo em modo de escrita sobre um arquivo já existente, representado pelo 'w'
                    h.write(f'{sites[-1]}\n') #Aqui, escreve-se cada linha com o site já no formato do arquivo hosts, com o ip do PC antes do endereço do site.
        elif retorninho == 'block':
            BackEnd.limparHost()
            with open('C:\Windows\System32\drivers\etc\hosts', 'a+') as h:
                for i in range(0, BackEnd.contar_linhas('sitesparabloquear.txt')): #Essas linhas aqui são a mesma lógica da estrutura try acima.
                    if i == 0:
                        h.write('\n127.0.0.1    {}'.format(sites[i]))
                    else: 
                        h.write('\n127.0.0.1    {}'.format(sites[i]))
        elif retorninho == 'des':
            BackEnd.limparHost()
            open ('sitesparabloquear.txt', 'w').close()
        elif retorninho == 'removeralguns':
            listadesitesparaapagar = []
            front_end.LayoutDaJanelaParaApagarAlgunsSites()  # Captura a janela retornada
            self.event, self.values = front_end.janelaexclusaodesites.read()
            while self.event != sg.WINDOW_CLOSED and self.event != '-OK-':
                self.event, self.values = front_end.janelaexclusaodesites.read()
            for i in range(0, len(sites)):
                if self.values[sites[i]] == True:
                    listadesitesparaapagar.append(sites[i])
            with open ('sitesparabloquear.txt', 'r') as b:
                linhas = b.readlines()
            linhas_modificadas = [linha for linha in linhas if linha not in listadesitesparaapagar]
            with open ('sitesparabloquear.txt', 'w') as b:
                b.writelines(linhas_modificadas)
            BackEnd.limparHost()
            sites.clear()
            BackEnd.sitesiniciais()
            with open('C:\Windows\System32\drivers\etc\hosts', 'a+') as h:
                for i in range(0, BackEnd.contar_linhas('sitesparabloquear.txt')): #Essas linhas aqui são a mesma lógica da estrutura try acima.
                    if i == 0:
                        h.write('\n127.0.0.1    {}'.format(sites[i]))
                    else:
                        h.write('\n127.0.0.1    {}'.format(sites[i]))
            front_end.janelaexclusaodesites.close()

#Aqui é onde são executadas as tarefas anteriormente criadas
front_end = FrontEnd() #Cria-se uma instância da classe FrontEnd, passando-a todos os atributos e tarefas da classe.
back_end = BackEnd()
BackEnd.sitesiniciais()
front_end.LayoutDaJanelaParaInserirOsSites() #Chama a função da classe FrontEnd, executando-a.

while ctypes.windll.shell32.IsUserAnAdmin() != 0:
    back_end.ControleDeOcorrencias()

sg.popup("Você deve executar o programa como administrador.")
