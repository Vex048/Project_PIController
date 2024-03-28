import plotly.express as px
import plotly
import pandas as pd
import json




def makeChart(tsim,tp,ti,Kp,Tzad,To,Ta,Ci,p,Q,d,Pmax,x,y,z):
    k = Q/d
    A = 2*x*y + 2*x*z + 2*y*z 
    Cp = Ci*p*d*A
    N = int(tsim/tp)
    t = [0.0]
    T = [Ta]
    P = [0.0]
    Pstr = [0.0]
    Pzuz = [0.0]
    global Upi, Upi_t
    Upi_t = [0.0]
    Upi = [0.0]
    e = [0.0]
    Umin = -1
    Umax = 1
    sum_e=0

    for _ in range(N):
        t.append(t[-1]+tp)
        e.append(Tzad - T[-1])
        sum_e=sum_e+e[-1]
        Upi_t.append(Kp*(e[-1] + (tp/ti)*sum_e))
        Upi.append(min(max(Upi_t[-1], Umin), Umax))

        P.append(Upi[-1] * Pmax)
        Pstr.append(k*A*(T[-1]-To))  # Tracona moc
        Pzuz.append(Pzuz[-1] + abs((P[-1]) / (1000 * 36000)))  # Przelicznik na kWh dla statystyk

        T.append(T[-1]+(tp*(P[-1] - k*A*(T[-1]-To))/Cp))

    df = pd.DataFrame(dict(
        Czas=t,
        Temperatura=[round(x, 2) for x in T],
        Sterowanie=Upi,
        Moc=[abs(x) for x in P],
        Moc2=Pzuz,
        Zadana=[Tzad]*(N+1),
        Tracona=Pstr
    ))
    newnames = {
        "Temperatura": "Zmiana aktualnej temperatury",
        "Zadana": "Temperatura zadana",
        "Moc": "Moc klimatyzatora",
        "Tracona": "Moc zakłóceń"
    }

    fig1 = px.line(df, x="Czas", y=["Temperatura", "Zadana"], title="Zmiana temperatury pomieszczenia w czasie",
                   labels={"Czas": "Czas [s]", 'value': "Temperatura [°C]"})
    fig1.for_each_trace(lambda v: v.update(name=newnames[v.name]))
    fig1.update_layout(legend=dict(
            title=None, orientation="h", y=1, yanchor="bottom", x=0.5, xanchor="center")
    )

    fig2 = px.line(df, x="Czas", y="Sterowanie", title="Zmiana wartosci sterujacej w czasie",
                   labels={"Czas": "Czas [s]", "Sterowanie": "Wartość sterująca regulatora"})

    fig3 = px.line(df, x="Czas", y=["Moc","Tracona"], title="Moc klimatyzatora a moc zakłóceń",
                   labels={"Czas": "Czas [s]", "value": "Moc [W]"})
    fig3.for_each_trace(lambda v: v.update(name=newnames[v.name]))
    fig3.update_layout(legend=dict(
            title=None, orientation="h", y=1, yanchor="bottom", x=0.5, xanchor="center")
    )

    fig4 = px.line(df, x="Czas", y="Moc2", title="Zużycie mocy w czasie",
                   labels={"Czas": "Czas [s]", "Moc2": "Moc [kWh]"})

    graphJSON1 = json.dumps(fig1, cls=plotly.utils.PlotlyJSONEncoder)
    graphJSON2 = json.dumps(fig2, cls=plotly.utils.PlotlyJSONEncoder)
    graphJSON3 = json.dumps(fig3, cls=plotly.utils.PlotlyJSONEncoder)
    graphJSON4 = json.dumps(fig4, cls=plotly.utils.PlotlyJSONEncoder)

    return graphJSON1, graphJSON2, graphJSON3, graphJSON4


