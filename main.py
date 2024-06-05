from flask import Flask
from flask import render_template
from flask import request
from datetime import datetime, timedelta
from llm_langchain import *

import smtplib
import email.message
import uuid
import json

import psycopg

from configparser import ConfigParser

from database import *
from llm import *

# Para rodar, no terminal digite: 
# flask --app main run --debug
app = Flask(__name__)

@app.route('/resumo_semanal')
def resumo_semanal():  
    config = ConfigParser()
    config.read("config.ini")    
    stakeholder_email = config.get('EMAIL', 'To')

    
    msg = email.message.Message()
    data_atual = datetime.now()
    data_formatada = data_atual.strftime('%d/%m/%Y')
    data_menos_7_dias = data_atual - timedelta(days=7)
    data_formatada_menos_7_dias = data_menos_7_dias.strftime('%d/%m/%Y')
    msg['Subject'] = "Feedbacks da semana: " + data_formatada_menos_7_dias + " - " + data_formatada 
    msg['From'] = config.get('EMAIL', 'From')
    msg['To'] = stakeholder_email
    password = config.get('EMAIL', 'app_password')
    msg.add_header('Content-Type', 'text/html')    
    database = Database()
    vetPorcentagem = database.porcentagenSemanal()       
    
    if (config.get('LLM', 'option') == 'langchain'):
        llm = LLMLangChain() 
    else:
        llm = LLM()

    resp = llm.principais_funcionalidades(database.listFeedbacksDescOrderSemanal())
    msg.set_payload("POSITIVO:"+str(vetPorcentagem['POSITIVO'])+"<br>NEGATIVO:"+str(vetPorcentagem['NEGATIVO'])+"<br><br>"+resp)
    s = smtplib.SMTP('smtp.gmail.com:587')
    s.starttls()
    s.login(msg['From'], password)
    s.sendmail(msg['From'], [msg['To']], msg.as_string().encode('utf-8'))    
    return "Email com sucesso para "+stakeholder_email

# rota/endpoint usado para postman
@app.route("/feedbacks", methods=['POST'])
def feedbacks():
    config = ConfigParser()
    config.read("config.ini")  
    try:
        request_data = request.get_json()
        resposta = dict()        
        resposta["id"] = request_data['id']
        resposta["feedback"] = request_data['feedback']        
        if (config.get('LLM', 'option') == 'langchain'):
            llm = LLMLangChain() 
        else:
            llm = LLM()            
        resp = json.loads(llm.prompt(request_data['feedback']))
        resposta["sentiment"] = resp["sentiment"].upper()        
        request_features = dict()
        request_features['code'] = resp["code"].upper().replace(" ", "_")    
        request_features['reason'] = resp["reason"]
        resposta["request_features"] = request_features   
        database = Database()
        database.insertFeedback(resposta)                          
    except:
        resposta = dict()
        resposta["error"] = "Erro de comunicação ou a LLM ou Feedback (id) já foi previamente analisado! Consulte o relatório!"        
    return resposta


# Quais são as features mais pedidas que conseguimos perceber através de feedbacks?
@app.route('/relatorio')
def relatorio():    
    config = ConfigParser()
    config.read("config.ini")  
    if (config.get('LLM', 'option') == 'langchain'):
        llm = LLMLangChain() 
    else:
        llm = LLM()    
    database = Database()
    vetPorcentagem = database.porcentagens()
    vetFeedbacks = database.listFeedbacksDescOrder()
    return render_template('relatorio.html', vetPorcentagem=vetPorcentagem, vetFeedbacks = vetFeedbacks)

## testes
@app.route("/")
def index():
    id = str(uuid.uuid4())
    return render_template('index.html', id = id)

# # rota de teste realizada com jinja template
@app.route("/feedbacks_template", methods=['POST'])
def feedbacks_template():
    try:
        request_data = request.form
        resposta = dict()        
        resposta["id"] = request_data['id']
        resposta["feedback"] = request_data['feedback']        
        config = ConfigParser()
        config.read("config.ini")  
        if (config.get('LLM', 'option') == 'langchain'):            
            llm = LLMLangChain() 
        else:
            llm = LLM()               
        resp = json.loads(llm.prompt(request_data['feedback']))
        resposta["sentiment"] = resp["sentiment"].upper()        
        request_features = dict()
        request_features['code'] = resp["code"].upper().replace(" ", "_")    
        request_features['reason'] = resp["reason"]
        resposta["request_features"] = request_features    
        database = Database()        
        database.insertFeedback(resposta)                          
    except:
        resposta = dict()
        resposta["error"] = "Erro de comunicação ou a LLM ou Feedback (id) já foi previamente analisado! Consulte o relatório!"        
    return resposta
