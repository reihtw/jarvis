#! /usr/bin/env python 3.6.4
# coding: utf-8

# importando os módulos do chatbot

# from pocketsphinx import pocketsphinx, Jsgf, FsgModel
from chatterbot import ChatBot
from datetime import datetime
from googlesearch import search
# from pocketsphinx import LiveSpeech
from gtts import gTTS

# import os
# import subprocess as s
import speech_recognition as sr
import pyttsx3
import wikipedia
import webbrowser
import pygame

wikipedia.set_lang('pt') # define português como língua
en = pyttsx3.init() # inicia pttsx3
bot = ChatBot('Jarvis', read_only=True) # cria o ChatBot Jarvis
keywords = ['o que é', 'quem é', 'quem foi', 'definição', 'defina'] # chaves de pesquisa
google_keywords = ['pesquisar por', 'pesquise por', 'jarvis pesquise por', 'pesquise para mim sobre', 'jarvis pesquise para mim sobre']

dict_cmds = {} # dicionário de comandos

def load_cmds(): # carrega os comandos
	lines = open('./commands.txt', 'r').readlines() # abre o arquivo commands.txt como leitura
	for line in lines: # separa falas e comandos respectivamente em um dicionario
		line = line.replace('\n', '') # retira todos os "enters"
		parts = line.split('|') # separa em uma lista as partes da fala e comando, utilizando o caractere '|' como divisor
		dict_cmds.update({parts[0] : parts[1]}) # adicona os itens da lista no dicionário, fala[0]:comando[1]

def setVoice(): # carrega o idioma pt-br para a voz
	voices = en.getProperty('voices') # carrega todas as vozes
	for voice in voices: # seleciona a opção da voz brasileira
		if voice.name == 'brazil':
			en.setProperty('voice', voice.id)

def speak(text): # função de fala
	en.say(text) # carrega o texto para falar
	en.runAndWait() # fala e espera uma nova entrada.

def playmusic(soundfile):
    """Stream music with mixer.music module in blocking manner.
       This will stream the sound from disk while playing.
    """
    pygame.init()
    pygame.mixer.init()
    clock = pygame.time.Clock()
    pygame.mixer.music.load(soundfile)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        clock.tick(1000)

def evaluate(text): # avalia se a fala (string) recebida representa um comando
	try:
		result = dict_cmds[text] # assina o result = tipo de comando
	except:
		result = None # caso não seja um comando, retorna None assumindo que seja uma conversa normal
	return result

def def_month(month): # recebe o mês(int) e retorna o nome (string)
	meses = {
        1:'Janeiro',
        2:'Fevereiro',
        3:'Março',
        4:'Abril',
        5:'Maio',
        6:'Junho',
        7:'Julho',
        8:'Agosto',
        9:'Setembro',
        10:'Outubro',
        11:'Novembro',
        12:'Dezembro'
    }

	return meses[month]

def run_cmd(cmd_type): # retorna os comandos
	result = None # resultado inicialmente em None

	if cmd_type == 'asktime': # se o comando for asktime ele retorna a hora
		now = datetime.now()
		result = 'São ' + str(now.hour) + ' horas e ' + str(now.minute) + ' minutos.'
	elif cmd_type == 'askdate': # se o comando for askdate ele retorna a data
		now = datetime.now()
		result = 'Hoje é ' + str(now.day) + ' de ' + def_month(now.month) + ' de ' + str(now.year) + '.'

	return result # retorna o resultado

def get_answer(text):
	result = None # resultados

	for key in keywords: # percorre a lista de chaves para verificar se ele inicia com alguma das chaves
		if text.startswith(key) and text != key and text is not None: # se a fala começa com alguma das chaves e verifica se o texto não é somente a chave
			result = text.replace(key, '') # retira a chave da fala
			result = wikipedia.summary(wikipedia.search(result)[0], sentences=2) # busca na intenet a definição
			break

	return result

def search_web(text):
	result = None
	
	if text is not None:
		for key in google_keywords:
			if text.startswith(key) and text != key:
				result = text.replace(key, '')
		if result is not None:
			c = 0	
			for url in search(text, stop=3):
				webbrowser.open_new_tab(url)
				c+=1
				if c == 3:
					break
			return 'pesquisando por ' + result.rstrip()
	return result
setVoice() # setar a voz
load_cmds() # carregar comandos

# for k,v in dict_cmds.items(): # teste para ver se os comandos estavam sendo recebidos de forma correta
#    print(k,'=============>',v)

# OBSOLETO!
#config = pocketsphinx.Decoder.default_config() # configuração do sphinx trazida para cá para transformar o aúdio em pt
#config.set_string('-hmm', 'model')
#config.set_string('-lm', 'model.lm.bin')
#config.set_string('-dict', 'model.dic')
#config.set_string('logfn', os.devnull)
#decoder = pocketsphinx.Decoder(config)


#def recognize_pt(audio):
#    raw_data = audio.get_raw_data(convert_rate=16000, convert_width=2)
#    decoder.start_utt()
#    decoder.process_raw(raw_data, False, True)
#    decoder.end_utt()
#
#    hypothesis = decoder.hyp()
#    if hypothesis is not None:
#        return hypothesis.hypstr
#    return None

r = sr.Recognizer() # inicia o speech_recognition anteriormente definido como sr

with sr.Microphone() as s: # alias para sr.Microphone() para s
	r.adjust_for_ambient_noise(s) # habilita a opção de reconhecer o que é barulho do ambiente

	# speech = None
	while True: # loop infinito para conversa
		try:
			audio = r.listen(s) # obtem o áudio e o passa para a variavel 'audio'
			# speech = recognize_pt(audio) # usando phoxsphinx
			speech = r.recognize_google(audio, language='pt').lower() # reconhece o áudio coma a api do google
			#response = run_cmd(evaluate(speech)) # obtem a resposta passando por evaluate e run_cmd para verificaçã   o de comandos
			response = bot.get_response(speech)
			print('Você disse: {}'.format(speech))  # mostra o que você disse

            #if speech == 'sair' or speech == 'tchau' or speech == 'até mais': # se receber alguma msg de saída ele saí
            #  break
			
			#if response == None: # se resposta retornar None ele irá tentar verificar se é um comando de pesquisa
			#	response = get_answer(speech) # tenta verificar se é um comando de pesquisa
			#	if response == None:
			#		response = search_web(speech)
			#		if response == None: # se ainda assim não for um comando de pesquisa ele tratará como uma conversa comum
			#			response = bot.get_response(speech) # response recebe a resposta "pensada" pelo ChatBot

			# tentativa de usar o gTTS falha
			voice = gTTS(text=response, lang='pt')
			voice.save('voz.mp3')

			print('Bot: {}'.format(response)) # mostra o que o Bot retornou como resposta
			#print('Tipo de comando: ', evaluate(speech)) # mostra o tipo de comando que ele reconheceu
			speak(response) # Bot fala a resposta
			# s.call(['MPC-HC', 'voz.mp3']) # parte da tentativa de utilizar o gTTS
			playmusic('./voz.mp3')
		except:
			pass # ignorando erros para o programa não encerrar
#print('Você disse: {}'.format(speech))
#print('Bot: {}'.format(speech))
#speak(speech)
