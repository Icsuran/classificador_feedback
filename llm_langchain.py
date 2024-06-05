from configparser import ConfigParser
from langchain_openai import ChatOpenAI
import os

class LLMLangChain:   
  
  def __init__(self):
    self.config = ConfigParser()
    self.config.read("config.ini")
    os.environ['OPENAI_API_KEY'] = self.config.get("LLM", 'api_key')  
    try:
      self.llm = ChatOpenAI(temperature=0.0)
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

    resp = self.llm.invoke(prompt.format(feedbacks = feedbacks.strip()))
    return resp.content

  
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
    resp = self.llm.invoke(prompt.format(feedback=feedback))
    return resp.content.replace("```", "").replace("json", "")