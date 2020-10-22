import datetime
from bs4 import *
import requests
from tkinter import *
import ast

file = open('moedas.txt', 'r', encoding='UTF-8')
moedas = file.read().replace('\n',', ')
file.close()
moedas = ast.literal_eval(moedas)

dataAtual = str(datetime.datetime.now())
dataAtual = dataAtual[:dataAtual.index(' ')]
dataAtual = dataAtual[:dataAtual.rindex('-')]+str(int(dataAtual[dataAtual.rindex('-'):])+1)

def conversao():
    valorOriginal = valor1.get()
    moedaOriginal = moedas[moeda1.get()]
    moedaDestino = moedas[moeda2.get()]
    url = f'https://www3.bcb.gov.br/bc_moeda/rest/converter/{valorOriginal}/1/{moedaOriginal}/{moedaDestino}/{dataAtual}'
    req = requests.get(url)
    soup = BeautifulSoup(req.text, 'html.parser')

    valor = soup.find('valor-convertido').text

    print(valor)
    valor2.set(valor)

def inversao():
    temp = moeda1.get()
    moeda1.set(moeda2.get())
    moeda2.set(temp)

if __name__ == "__main__":    
    window = Tk()
    window.title('Conversor de moedas')
    window.resizable(False,False)

    De = Label(window, text= 'De:')
    De.grid(row=0, column=0)

    Para = Label(window, text= 'Para:')
    Para.grid(row=1, column=0)

    valor1 = StringVar()
    valor1.set(1.00)
    v1 = Entry(window, textvariable=valor1)
    v1.grid(row=0, column=1)

    valor2 = StringVar()
    v2 = Entry(window, textvariable=valor2)
    v2.grid(row=1, column=1)

    moeda1 = StringVar(window)
    moeda1.set('Dólar dos Estados Unidos (USD)')
    moeda1dropdown = OptionMenu(window,moeda1, *moedas)
    moeda1dropdown.grid(row=0, column=3)

    moeda2 = StringVar(window)
    moeda2.set('Real Brasileiro (BRL)')
    moeda2dropdown = OptionMenu(window,moeda2, *moedas)
    moeda2dropdown.grid(row=1, column=3)

    conversao()
    botaoConverter = Button(window, text='Converter',command=conversao)
    botaoConverter.grid(row=3,column=1)

    botaoInverter = Button(window, text='Inverter Moedas', command=inversao)
    botaoInverter.grid(row=3,column=3)

    window.mainloop()