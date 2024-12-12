import pandas as pd
import flask
from flask import Flask, request, jsonify, make_response, render_template, session, Response
import time
import json
import re
import matplotlib
import matplotlib.pyplot as plt
import io
import os
matplotlib.use('Agg')

# https://www.kaggle.com/datasets/octopusteam/imdb-top-1000-movies?resource=download

app = Flask(__name__)
df = pd.read_csv("main.csv")
ratelimit = {}
visitor_ip = []


# @app.route('/')
# def home():
#     with open("index.html") as f:
#         html = f.read()
#     return html

#a and b testing--------------------------------------------------------------------------------
ABcounter = 0
ABclick = {'A':0, 'B':0}
best = None

@app.route('/')
def home():
    global ABcounter
    if ABcounter < 10:
        if ABcounter % 2 == 0:
            version = """
            <head>
    <script src="https://code.jquery.com/jquery-3.4.1.js"></script>
    <script>
      function subscribe() {
        var email = prompt("What is your email?", "????");

        $.post({
          type: "POST",
          url: "email",
          data: email,
          contentType: "application/text; charset=utf-8",
          dataType: "json"
        }).done(function(data) {
          alert(data);
        }).fail(function(data) {
          alert("POST failed");
        });
      }
    </script>
  </head>

            <body>
            
            <div class="header">
            <a href="http://34.72.222.250:5000/">Home</a>
    <a href="/donate.html?from=A">Donate Here!</a>
    <a href="http://34.72.222.250:5000/browse.html">data frame in HTML</a>     
    <a href="http://34.72.222.250:5000/browse.json">data frame in json</a>     
    <a href="http://34.72.222.250:5000/visitors.json">IP of visitors</a>
            </div>
             <button onclick="subscribe()">Subscribe</button>
            
            <h1>Welcome!</h1>
            <p>Enjoy the data.</p>
            <p>Version A</p>
            
            <img src="dashboard1.svg">
            <img src="dashboard1.svg?bins=100">
            <img src="dashboard2.svg">

            </body>
            </html>
            """
        else:
            version = """
            <head>
    <script src="https://code.jquery.com/jquery-3.4.1.js"></script>
    <script>
      function subscribe() {
        var email = prompt("What is your email?", "????");

        $.post({
          type: "POST",
          url: "email",
          data: email,
          contentType: "application/text; charset=utf-8",
          dataType: "json"
        }).done(function(data) {
          alert(data);
        }).fail(function(data) {
          alert("POST failed");
        });
      }
    </script>
  </head>

            <body>
            
            <div class="header">
            <a href="http://34.72.222.250:5000/">Home</a>
    <a href="/donate.html?from=B">Donate Here!</a>
    <a href="/browse.html">data frame in HTML</a>     
    <a href="http://34.72.222.250:5000/browse.json">data frame in json</a>     
    <a href="http://34.72.222.250:5000/visitors.json">IP of visitors</a>
            </div>
             <button onclick="subscribe()">Subscribe</button>

            <h1>Welcome!</h1>
            <p>Enjoy the data.</p>
            <p>Version B</p>
            
            <img src="dashboard1.svg">
            <img src="dashboard1.svg?bins=100">
            <img src="dashboard2.svg">

            </body>
            </html>
            """
        

    
    
    else:
        # selector = request.args.get('from')
        # if selector in ABclick:
        #     ABclick[selector] += 1

        if ABclick['A'] >= ABclick['B']:
            version = """
            <head>
    <script src="https://code.jquery.com/jquery-3.4.1.js"></script>
    <script>
      function subscribe() {
        var email = prompt("What is your email?", "????");

        $.post({
          type: "POST",
          url: "email",
          data: email,
          contentType: "application/text; charset=utf-8",
          dataType: "json"
        }).done(function(data) {
          alert(data);
        }).fail(function(data) {
          alert("POST failed");
        });
      }
    </script>
  </head>

            <body>
            
            <div class="header">
            <a href="http://34.72.222.250:5000/">Home</a>
    <a href="/donate.html?from=A">Donate Here!</a>
    <a href="http://34.72.222.250:5000/browse.html">data frame in HTML</a>     
    <a href="http://34.72.222.250:5000/browse.json">data frame in json</a>     
    <a href="http://34.72.222.250:5000/visitors.json">IP of visitors</a>
            </div>
             <button onclick="subscribe()">Subscribe</button>
            
            <h1>Welcome!</h1>
            <p>Enjoy the data.</p>
            <p>Version A</p>
            
            <img src="dashboard1.svg">
            <img src="dashboard1.svg?bins=100">
            <img src="dashboard2.svg">

            </body>
            </html>
            """
        else:
            version = """
            <head>
    <script src="https://code.jquery.com/jquery-3.4.1.js"></script>
    <script>
      function subscribe() {
        var email = prompt("What is your email?", "????");

        $.post({
          type: "POST",
          url: "email",
          data: email,
          contentType: "application/text; charset=utf-8",
          dataType: "json"
        }).done(function(data) {
          alert(data);
        }).fail(function(data) {
          alert("POST failed");
        });
      }
    </script>
  </head>

            <body>
            
            <div class="header">
            <a href="http://34.72.222.250:5000/">Home</a>
    <a href="/donate.html?from=B">Donate Here!</a>
    <a href="/browse.html">data frame in HTML</a>     
    <a href="http://34.72.222.250:5000/browse.json">data frame in json</a>     
    <a href="http://34.72.222.250:5000/visitors.json">IP of visitors</a>
            </div>
             <button onclick="subscribe()">Subscribe</button>

            <h1>Welcome!</h1>
            <p>Enjoy the data.</p>
            <p>Version B</p>
            
            <img src="dashboard1.svg">
            <img src="dashboard1.svg?bins=100">
            <img src="dashboard2.svg">

            </body>
            </html>
            """


    ABcounter += 1
    return version

#a and b testing---------------------------------------------------------------------------------
 
@app.route('/browse.html')
def browse_handler():
    data = df.to_html()
    display = f"<h1>Browse in HTML</h1>{data}"
    return display


@app.route('/browse.json')
def browse_json():
    user_ip = request.remote_addr  
    current_time = time.time()
    
    if user_ip not in visitor_ip:
        visitor_ip.append(user_ip)
    
    if user_ip in ratelimit:
        last_access_time = ratelimit[user_ip]
        time_since_last_access = current_time - last_access_time

        if time_since_last_access < 60: 
            retry_after = 60 - time_since_last_access
            response = make_response(jsonify({'error': 'Too many requests'}), 429)
            response.headers['Retry-After'] = str(int(retry_after))
            return response
    
    ratelimit[user_ip] = current_time
    
    dict_browse = df.to_dict()
    datajson = jsonify(dict_browse)
    
    return datajson


@app.route('/visitors.json')
def visitors_json():
    visitors = visitor_ip
    # test = type(visitors)
    visitors_tojson = json.dumps(visitors)
    return visitors_tojson
    # return test



@app.route('/donate.html')
def donate():
    version = request.args.get('from')
    if version in ABclick:
        ABclick[version] += 1 
        
    return f"""
    <html>
    <body>
    
    <nav>
    <a href="http://34.72.222.250:5000/">Home</a>
    <a href="/donate.html">Donate Here!</a>
    <a href="/browse.html">data frame in HTML</a>     
    <a href="/browse.json">data frame in json</a>     
    <a href="/visitors.json">IP of visitors</a>
    </nav>
    
    <h1>Donate Here!</h1>

    <p>You should donate to my project, so I can use the funds towards my virtual machine, so I may keep it longer in order to create better projects!</p>
    
    <p>Venmo: @sample123</p>
    
    <p>Zelle: (123)456-7890</p>
    
    <p>Visits from Version A: {ABclick['A']}</p>
    <p>Visits from Version B: {ABclick['B']}</p>
    
    </body>
    </html>
    """

@app.route('/email', methods=["POST"])
def email():
    email = str(request.data, "utf-8")
    if len(re.findall(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{3}$", email)) > 0:  # 1
        with open("emails.txt", "a") as f:  # open file in append mode
            f.write(email + "\n")  # 2
        with open("emails.txt", "r") as f:
            num_subscribed = sum(1 for line in f) 
        return jsonify(f"thanks, your subscriber number is {num_subscribed}!")
    return jsonify("error - add a valid email")  # 3


# testing---------------------------------------------------------------------------------------
ratings = df['averageRating']
year = df['releaseYear']
votes = df['numVotes']
genres = df['genres']

@app.route("/dashboard1.svg")
def dashboard1():    
    fig, ax = plt.subplots(figsize=(3, 2))
    average_ratings = df.groupby('releaseYear')['averageRating'].mean().reset_index()
    
    if flask.request.args.get("bins"):
        color = "yellow"
        file_name = 'dashboard1-query.svg'
    else:
        color = "blue"
        file_name = 'dashboard1.svg'
    
    # color = "yellow" if flask.request.args.get("bins") else "blue"
    plt.plot(average_ratings['releaseYear'], average_ratings['averageRating'], color = color)
    
    ax.set_ylabel("Average Ratings")
    ax.set_xlabel("Year")
    plt.tight_layout()
    
    f = io.StringIO() 
    fig.savefig(f, format="svg")
    plt.savefig(file_name, format = 'svg')
    # plt.savefig('dashboard1.svg', format = 'svg')
    plt.close()
    
    return flask.Response(f.getvalue(), headers={"Content-type": "image/svg+xml"})

@app.route("/dashboard1bin.svg")
def dashboard1bin():
    return """
    <html>
    <body>
    <img src="dashboard1.svg?bins=100">
    </body>
    </html>
    """


@app.route("/dashboard2.svg")
def dashboard2():    
    fig, ax = plt.subplots(figsize=(3, 2))
    average_votes = df.groupby('genres')['numVotes'].mean().reset_index()
    plt.bar(average_votes['genres'], average_votes['numVotes'])
    
    # Assuming 'df' is already defined somewhere in the code
    #df.plot(x='releaseYear', y='averageRating', ax=ax)
    
    ax.set_ylabel("Votes")
    ax.set_xlabel("Genres")
    plt.tight_layout()
    
    f = io.StringIO() 
    fig.savefig(f, format="svg")
    plt.savefig('dashboard2.svg', format = 'svg')
    plt.close()
    
    return flask.Response(f.getvalue(), headers={"Content-type": "image/svg+xml"})

# @app.route("/dashboard1_100.svg")
# def dashboardtest():    
#     fig, ax = plt.subplots(figsize=(3, 2))
#     pd.Series(ratings).plot.hist(ax=ax, bins=100)
    
#     ax.set_ylabel("Temperatures")
#     plt.tight_layout()
    
#     f = io.StringIO() 
#     fig.savefig(f, format="svg")
#     plt.close()
    
#     return flask.Response(f.getvalue(), headers={"Content-type": "image/svg+xml"})

# testing---------------------------------------------------------------------------------------

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True, threaded=False) # don't change this line!

# NOTE: app.run never returns (it runs for ever, unless you kill the process)
# Thus, don't define any functions after the app.run call, because it will
# never get that far.

# @app.route('/hi.html')
# def hi_handler():
#     return "howdy!"
        



    