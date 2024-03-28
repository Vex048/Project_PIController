from flask import Flask, render_template, request
import plot


app = Flask(__name__,static_url_path='/static')



@app.route('/')
def index():
    return render_template('index.html', title="Automatyka",TSIM=5000,TP=0.1,TI=1000,KP=0.1,
                               TZAD=17,TO=20,TA=19,CI=1005,P=14,Q=0.8,
                               D=0.5,PMAX=2500,X=2,Y=2,Z=2)

@app.route('/', methods=['POST','GET'])
def createChart():
    if request.method == "POST":
        Tsim=request.form['tsim']
        tp=request.form['tp']
        ti=request.form['ti']
        Kp=request.form['Kp']
        Tzad=request.form['Tzad']
        To = request.form['To']
        Ta = request.form['Ta']
        Ci = request.form['Ci']
        p = request.form['p']
        Q = request.form['Q']
        d = request.form['d']
        Pmax = request.form['Pmax']
        x = request.form['x']
        y = request.form['y']
        z = request.form['z']
        parametrs=[float(Tsim),float(tp),float(ti),float(Kp),float(Tzad),float(To),float(Ta),
                   float(Ci),float(p),float(Q),float(d),float(Pmax),float(x),float(y),float(z)]
        graph, graph2, graph3, grpah4 =plot.makeChart(parametrs[0],parametrs[1],parametrs[2],parametrs[3],
                                                       parametrs[4],parametrs[5],parametrs[6],parametrs[7],
                                                        parametrs[8],parametrs[9],parametrs[10],parametrs[11],
                                                        parametrs[12],parametrs[13],parametrs[14])
        return render_template('index.html', plot1=graph, plot2=graph2, plot3=graph3, plot4=grpah4,
                               TSIM=parametrs[0],TP=parametrs[1],TI=parametrs[2],KP=parametrs[3],
                               TZAD=parametrs[4],TO=parametrs[5],TA=parametrs[6],CI=parametrs[7],P=parametrs[8],Q=parametrs[9],
                               D=parametrs[10],PMAX=parametrs[11],X=parametrs[12],Y=parametrs[13],Z=parametrs[14])
        



if __name__ == "__main__":
    app.run(debug=True)