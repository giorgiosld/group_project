'''
@uthor: Giorgio Saldana @email: giorgio.saldana@studenti.unicam.it

Questo file contiene il core del web server con la definizione delle varie routes
e della logica di ciascun componente. Richiama al suo interno altri file quali sono
necessari per poter avviare il DB e il web server in generale

'''
from flask import Flask, request, send_file
from src.db import result_query
from src.schema import create_db
import os
import requests

# richiama il framework Flask
app = Flask(__name__)

# route principale del web server, da qui si può navigare verso le varie challenge
@app.get("/")
def index():
   about = '''
      <h1>Home page</h1>
      <p>This is a simply web server created to demonstrate the most commons injection attacks</p>
      <ul>
         <li><a href="/sql">SQL Injection</a></li>
         <li><a href="/injection">Command Injection</a></li>
         <li><a href="/traversal">Directory Traversal</a></li>
         <li><a href="/ssrf">Server Side Requests Forgery</a></li>
      </ul>
   '''
   return about

# route riguardante l'SQLi, vi è presente un form dalla quale si può interrogare il DB
@app.get('/sql')
def sql():
   form = f"""
   <form action = "sqli" method = "GET">
      <p><h3>Enter an input to see the magic!</h3></p>
      <p><input type = 'text' name = 'query'/></p>
      <p><input type = 'submit' value = 'Search'/></p>
   </form>
   """
   return form

# route "vulnerabile" all'SQLi, dopo aver elaborato la query manda in output il risultato di essa
@app.get('/sqli/<name>')
def sqli(name):
   print("-" * 50)
   print(f"Passing input: {name}")

   exams = result_query(name)
   output = [f"<li>{title}: grade {grade}</li>" for title, grade in exams]

   disclaimer = f"""
      <p>Here are the result of exams I got for student:
         <pre><blockquote>{name}</blockquote></pre>
      </p>
   """
   return f"{disclaimer}<br/><h3>Results</h3><ol>{''.join(output)}</ol>"

# route relativa al command injection, permette di eseguire un comando non desiderato una volta exploitato
@app.get('/injection')
def command_injection():
   form = f"""
   <form action = "injection" method = "GET">
      <p><h3>Enter an input to see the magic!</h3></p>
      <p><input type = 'text' name = 'filename'/></p>
      <p><input type = 'submit' value = 'Search'/></p>
   </form>
   """
   if request.args.get('filename'):
      filename = request.args.get('filename')
      command = "find / -name " + str(filename)
      output = os.popen(command).read()
      return f"{form}\nRequested file '{filename}' is present at: {output}"
      
   return form

# route relativa al Directional Path Attack, vi è incluso l'utilizzo di una funzione "non sicura", quale permette di navigare all'interno del file system del server
@app.get('/traversal')
def traversal():
   form = f"""
   <form action = "traversal" method = "GET">
      <p><h3>Enter an image's name to see the magic![eg. master_degree.jpeg]</h3></p>
      <p><input type = 'text' name = 'filename'/></p>
      <p><input type = 'submit' value = 'Search'/></p>
   </form>
   """
   if request.args.get('filename'):
      filename = request.args.get('filename')
      return send_file(filename)
   return form

# route relativa all'SSRF attack permette l'esecuzione dell'attacco SSRF dovuto ad una mancata "pulizia" dell'output
@app.get('/ssrf')
def ssrf():
   form = f"""
   <form action = "ssrf" method = "GET">
      <p><h3>Do you wanna see the magic?</h3></p>
      <p><input type = 'text' name = 'url'/></p>
      <p><input type = 'submit' value = 'Search'/></p>
   </form>
   """
   if request.args.get('url'):
      url = request.args.get('url')
      return requests.get(url).text
   return form

# funzione principale che inizializza il database per poi eseguire l'applicazione in Flask
if __name__ == '__main__':
   create_db()
   app.run(port=80, debug=True)