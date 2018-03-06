import os
import redis
from flask import Flask, render_template, redirect, request, url_for, make_response
from DatabaseModule import *
from ECSModule import *
import json
import random

#credential setup
if os.path.isfile("setenv.py"):
    print "running local"
    import setenv
    #initialize database
    initDBLocal()
else:
    VCAP_SERVICES = json.loads(os.environ['VCAP_SERVICES'])
    CREDENTIALS = VCAP_SERVICES["rediscloud"][0]["credentials"]
    initDB(CREDENTIALS["hostname"],CREDENTIALS["port"], password=CREDENTIALS["password"])
    print "I must be in CF"


initECS()
	
app = Flask(__name__)

def printRadioStationTable():
    table = ""
    stationDict = getListOfStation()
    radioID = 0
    for station in stationDict.keys():
        table = table + """<tr>
              <th scope="row">{}</th>
              <td><a href ="{}">{}</a></td>
              <td><a href ="{}">stream</a></td>
            </tr>""".format(radioID + 1 ,stationDict["ID:"+str(radioID)][2], stationDict["ID:"+str(radioID)][0], stationDict["ID:"+str(radioID)][1])
        radioID = radioID +1
    return table

def printQRTable():
    qrList = getAllImage()
    randQRList = []
    randQRList.append(random.choice(qrList))
    while len(randQRList) < 3:
        newChoice = random.choice(qrList)
        if newChoice not in randQRList:
            randQRList.append(newChoice)
    resp = ""
    for img in randQRList:
        title = img.split(".")[0]
        resp = resp + """
                <div class="col-lg-4">
                    <img src="http://ECSADDRESS{}/{}" alt="{}" width="180" height="180">
                    <br/>
                    <p><h6>{}</h6></p>
                </div><!-- /.col-lg-4 -->
                """.format(os.environ["ecs_bucket"],img, title, title)
    return resp

    

 
  

@app.route('/', methods=['GET', 'POST'])
def home():
    #if its post
    if request.method == 'POST':
        stationName = request.form['inputStationName']
        stationStream = request.form['inputStationStream']
        stationSite = request.form['inputStationWebsite']
        print(stationName)
        
        #add station
        addRadioStation(stationName, stationStream, stationSite)

    tableResult = ""
  
    resp = """
            <!DOCTYPE html>
            <html lang="en">

          <head>

            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
            <meta name="description" content="">
            <meta name="author" content="">

            <title>Dell EMC Piper Radio</title>

            <!-- Bootstrap core CSS -->
            <link href="./static/vendor/bootstrap/css/bootstrap.min.css" rel="stylesheet">

            <!-- Custom fonts for this template -->
            <link href="./static/vendor/font-awesome/css/font-awesome.min.css" rel="stylesheet" type="text/css">
            <link href="https://fonts.googleapis.com/css?family=Lora:400,700,400italic,700italic" rel="stylesheet" type="text/css">
            <link href='https://fonts.googleapis.com/css?family=Cabin:700' rel='stylesheet' type='text/css'>

            <!-- Custom styles for this template -->
            <link href="./static/css/grayscale.min.css" rel="stylesheet">

          </head>

          <body id="page-top">

            <!-- Navigation -->
            <nav class="navbar navbar-expand-lg navbar-light fixed-top" id="mainNav">
              <div class="container">
                <a class="navbar-brand js-scroll-trigger" href="#page-top">Dell EMC - Piper Radio</a>
                <button class="navbar-toggler navbar-toggler-right" type="button" data-toggle="collapse" data-target="#navbarResponsive" aria-controls="navbarResponsive" aria-expanded="false" aria-label="Toggle navigation">
                  Menu
                  <i class="fa fa-bars"></i>
                </button>
                <div class="collapse navbar-collapse" id="navbarResponsive">
                  <ul class="navbar-nav ml-auto">
                    <li class="nav-item">
                      <a class="nav-link js-scroll-trigger" href="#AvailableStation">Available Stations </a>
                    </li>
                    <li class="nav-item">
                      <a class="nav-link js-scroll-trigger" href="#AddStation">Add Station</a>
                    </li>
                    <li class="nav-item">
                      <a class="nav-link js-scroll-trigger" href="#QRList">Random 3</a>
                    </li>
                  </ul>
                </div>
              </div>
            </nav>

            <!-- Intro Header -->
            <header class="masthead">
              <div class="intro-body">
                <div class="container">
                  <div class="row">
                    <div class="col-lg-8 mx-auto">
                    <p>
                    <!-- Twitter Embed -->
                     <a class="twitter-timeline"  href="sometweet" data-widget-id="970272434929655808">#sometweetr Tweets</a>
                     <script>!function(d,s,id){var js,fjs=d.getElementsByTagName(s)[0],p=/^http:/.test(d.location)?'http':'https';if(!d.getElementById(id)){js=d.createElement(s);js.id=id;js.src=p+"://platform.twitter.com/widgets.js";fjs.parentNode.insertBefore(js,fjs);}}(document,"script","twitter-wjs");</script>
                    </p>
                      <a href="#AvailableStation" class="btn btn-circle js-scroll-trigger">
                        <i class="fa fa-angle-double-down animated"></i>
                      </a>
                    </div>
                  </div>
                </div>
              </div>
            </header>

            <!-- Available Station Section -->
            <section id="AvailableStation" class="content-section text-center">
              <div class="container">
                <div class="row">
                  <div class="col-lg-8 mx-auto">
                    <h2>Availble Station</h2>
                    <p>
                    <table class="table table-striped table-dark">
                      <thead>
                          <tr>
                              <th scope="col">#</th>
                              <th scope="col">Radio Station</th>
                              <th scope="col">Stream URL</th>
                        </tr>
                      </thead>
                      <tbody>
          """
    #get table data from database
    resp = resp + printRadioStationTable()
    resp = resp + """
          </tbody>
        </table>
                    </p>
                    <a href="#AddStation" class="btn btn-circle js-scroll-trigger">
                        <i class="fa fa-angle-double-down animated"></i>
                      </a>
                  </div>
                </div>
              </div>
            </section>

            <!-- Add Station -->
            <section id="AddStation" class="download-section content-section text-center">
              <div class="container">                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  
                <div class="col-lg-8 mx-auto">
                  <h2>Add Station</h2>
                  <form method="post" action="/#AvailableStation">
                      <div class="form-group">
                        <label for="StationName">Station Name</label>
                        <input type="text" class="form-control" id="inputStationName" name="inputStationName" aria-describedby="stationHelp" placeholder="Station Name">
                        <small id="stationHelp" class="form-text text-muted">Place the station name.</small>
                      </div>
                      <div class="form-group">
                        <label for="StreamURL">Stream URL</label>
                        <input type="text" class="form-control" id="inputStationStream" name="inputStationStream" aria-describedby="stationStreamHelp" placeholder="Stream Address">
                        <small id="stationStreamHelp" class="form-text text-muted">Place the station stream URL.</small>
                      </div>
                      <div class="form-group">
                        <label for="StationSite">Station Website</label>
                        <input type="text" class="form-control" id="inputStationWebsite" name="inputStationWebsite" aria-describedby="stationWebsiteHelp" placeholder="Station Website">
                        <small id="stationWebsiteHelp" class="form-text text-muted">Place the station website.</small>
                      </div>

                      <button type="submit" class="btn btn-primary">Submit</button>
                    </form>
                    <a href="#QRList" class="btn btn-circle js-scroll-trigger">
                        <i class="fa fa-angle-double-down animated"></i>
                      </a>
                </div>
              </div>
            </section>

            <!-- QR List -->
            <section id="QRList" class="content-section text-center">
              <div class="container">                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  
                <div class="col-lg-8 mx-auto">
                  <h2>Random 3</h2>
                  <div class="row">
                     """
    resp = resp + printQRTable()+ """
                </div>
              </div>
            </section>


            <!-- Footer -->
            <footer>
              <div class="container text-center">
                <p>Copyright &copy; Li Jwee 2018</p>
              </div>
            </footer>

            <!-- Bootstrap core JavaScript -->
            <script src="static/vendor/jquery/jquery.min.js"></script>
            <script src="static/vendor/bootstrap/js/bootstrap.bundle.min.js"></script>

            <!-- Plugin JavaScript -->
            <script src="static/vendor/jquery-easing/jquery.easing.min.js"></script>

            <!-- Google Maps API Key - Use your own API key to enable the map feature. More information on the Google Maps API can be found at https://developers.google.com/maps/ -->
            <script src="https://maps.googleapis.com/maps/api/js?key=AIzaSyCRngKslUGJTlibkQ3FkfTxj3Xss1UlZDA&sensor=false"></script>

            <!-- Custom scripts for this template -->
            <script src="static/js/grayscale.min.js"></script>

          </body>

        </html>
        """
    return resp


    
	
if __name__ == "__main__":
	app.run(debug=False, host='0.0.0.0', \
                port=int(os.getenv('PORT', '5000')), threaded=True)
