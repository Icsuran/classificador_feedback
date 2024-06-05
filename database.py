
import psycopg
from configparser import ConfigParser

class Database:
    def __init__(self):
      self.config = ConfigParser()
      self.config.read("config.ini")

    def buildConnection(self):
      conn = None
      try:
          conn = psycopg.connect("dbname="+self.config.get('DATABASE', 'dbname')+" user="+self.config.get('DATABASE', 'user')+" password="+self.config.get('DATABASE', 'password')+" host="+self.config.get('DATABASE', 'host'))
      except:
          print("Problemas de conexão!")
      return conn

    def porcentagens(self):
      sql = "select sentiment, cast((cast(count(*) as real)/cast((select count(*) from feedbacks) as real))*100 as numeric(8,2)) || '%' from feedbacks group by sentiment;"
      conn = self.buildConnection() 
      cur = conn.cursor()
      cur.execute(sql)                
      vetPorcentagem = dict()
      vetPorcentagem['POSITIVO'] = 0
      vetPorcentagem['NEGATIVO'] = 0
      vetPorcentagem['INCONCLUSIVO'] = 0    
      for record in cur:                        
          vetPorcentagem[record[0]] = record[1]    
      cur.close()
      conn.close()
      return vetPorcentagem
    
    def listFeedbacksDescOrder(self):
        sql = "select * from feedbacks order by data_created desc;"
        conn = self.buildConnection()
        cur = conn.cursor()
        cur.execute(sql)           
        vetFeedbacks = []
        for record in cur:     
            feedback = dict()        
            feedback["id"] = record[0]
            feedback["feedback"] = record[1]
            feedback["sentiment"] = record[2]                
            feedback['code'] = record[3]
            feedback['reason'] = record[4]
            feedback["data_created"] = record[5]
            vetFeedbacks.append(feedback)
        cur.close()
        conn.close()
        return vetFeedbacks
    
    def insertFeedback(self, resposta):
      try:
        conn = self.buildConnection()
        cur = conn.cursor()
        cur.execute("INSERT INTO feedbacks (id, feedback, sentiment, code, reason) VALUES(%s, %s, %s, %s, %s);", [resposta["id"], resposta["feedback"], resposta["sentiment"],  resposta['request_features']['code'],  resposta['request_features']['reason']])
        conn.commit()
        cur.close()
        conn.close() 
        return True  
      except:
        return False           

    def porcentagenSemanal(self):
          sql = "select sentiment, cast((cast(count(*) as real)/cast((select count(*) from feedbacks where data_created >= current_timestamp - interval '7 days') as real))*100 as numeric(8,2)) || '%' from feedbacks where data_created >= current_timestamp - interval '7 days' group by sentiment;"
          conn = self.buildConnection()
          cur = conn.cursor()
          cur.execute(sql)                
          vetPorcentagem = dict()
          vetPorcentagem['POSITIVO'] = 0
          vetPorcentagem['NEGATIVO'] = 0
          vetPorcentagem['INCONCLUSIVO'] = 0    
          for record in cur:                        
              vetPorcentagem[record[0]] = record[1]    
          cur.close()
          conn.close()
          return vetPorcentagem

    def listFeedbacksDescOrderSemanal(self):
            sql = "select * from feedbacks where data_created >= current_timestamp - interval '7 days' order by data_created desc;"
            conn = self.buildConnection()
            cur = conn.cursor()
            cur.execute(sql)           
            vetFeedbacks = []
            for record in cur:     
                feedback = dict()        
                feedback["id"] = record[0]
                feedback["feedback"] = record[1]
                feedback["sentiment"] = record[2]                
                feedback['code'] = record[3]
                feedback['reason'] = record[4]
                feedback["data_created"] = record[5]
                vetFeedbacks.append(feedback)
            cur.close()
            conn.close()
            return vetFeedbacks