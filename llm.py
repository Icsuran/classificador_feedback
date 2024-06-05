# import openai
from openai import OpenAI
from configparser import ConfigParser

class LLM:    
  
  def __init__(self):
    self.config = ConfigParser()
    self.config.read("config.ini")
    try:
      self.client = OpenAI(api_key = self.config.get("LLM", 'api_key'))        
    except:
      print("Não foi possível conectar a OpenAI")
          
  def principais_funcionalidades(self, vetFeedback):  

    prompt = """
    Dada a lista de feedbacks de clientes abaixo em português, identifique os principais problemas relatados:   
    {feedbacks}
    """    
    feedbacks = ""
    for f in vetFeedback:
      feedbacks = feedbacks + f["feedback"] + "\n"    
      
    messages = [{"role": "system", "content": "Assistente virtual"}]    
    messages.append({"role": "user", "content": prompt.format(feedbacks = feedbacks.strip())})
    
    resposta = self.client.chat.completions.create(
        model = "gpt-3.5-turbo",
        messages = messages,
        temperature = 1,
        max_tokens = 100
    )    
    resp = resposta.choices[0].message.content.strip()    
    return resp

  
  def prompt(self, feedback):    
    prompt = """
    Dada uma conversa: "{feedback}", em português, que se trata do feedback de um cliente, 
    faça uma análise do sentimento expresso pelo cliente. Os sentimentos podem ser: positivo, negativo, inconclusivo. 
    Retorne em uma linha somente um sentimento (palavra), conforme descrito acima. 
    Numa segunda linha retorne a itenção da mensagem, como por exemplo: 
    "editar perfil do usuário", "melhorar o atendimento", "criar exemplos de dados".
    Abaixo, numa terceira linha apresente em uma frase  o objetivo da mensagem enviada pelo cliente. 
    Como por exemplo: "O usuário gostaria de realizar a edição do próprio perfil" 
    Transforme o retorno no formato json sendo: "sentiment" para o sentimento (positivo, negativo ou inconclusivo) , "code" para a intenção e 
    "reason" para o objetivo.
    """           
    messages = [{"role": "system", "content": "Assistente virtual"}]    
    messages.append({"role": "user", "content": prompt.format(feedback = feedback)})
    
    resposta = self.client.chat.completions.create(
        model = "gpt-3.5-turbo",
        messages = messages,
        temperature = 1,
        max_tokens = 60
    )    
    resp = resposta.choices[0].message.content.strip().replace("```", "").replace("json", "")    
    return resp