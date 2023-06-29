from flask import Flask, request

import os

app = Flask(__name__)

@app.get("/")
def index():
   about = '''
      <h1>Home page</h1>
      <p>This is a simply web server created to demonstrate the most commons injection attacks</p>
      <ul>
         <li><a href="/sqli">SQL Injection</a></li>
         <li><a href="/commandinjection">Command Injection</a></li>
         <li>Directory Traversal</li>
         <li>Cross Site Scripting</li>
         <li>Server Side Requests Forgery</li>
      </ul>
   '''
   return about

@app.get('/sqli')
def query():
   form = f"""
   <html>
      <body>
         <form action = "sqli" method = "GET">
            <p><h3>Enter a file to search into server</h3></p>
            <p><input type = 'text' name = 'filename'/></p>
            <p><input type = 'submit' value = 'Search'/></p>
         </form>
      </body>
   </html>
   """
   return form

@app.get('/commandinjection')
def search_files():
   form = f"""
   <html>
      <body>
         <form action = "commandinjection" method = "GET">
            <p><h3>Enter a file to search into server</h3></p>
            <p><input type = 'text' name = 'filename'/></p>
            <p><input type = 'submit' value = 'Search'/></p>
         </form>
      </body>
   </html>
   """
   if request.args.get('filename'):
      filename = request.args.get('filename')
      command = "find / -name " + str(filename)
      output = os.popen(command).read()
      return f"{form}\nRequested file '{filename}' is present at: {output}"
      
   return form

if __name__ == '__main__':
    app.run(port=80, debug=True)