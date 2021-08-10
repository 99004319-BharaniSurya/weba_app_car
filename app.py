from logging import debug
from flask import Flask, app,redirect,url_for,render_template,request
import pyodbc
import pandas as pd
import plotly.express as px
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
server = 'sql-car.database.windows.net'
database = 'car_details'
username = 'azure-car'
password = '{India#123}'   
driver= '{ODBC Driver 17 for SQL Server}'
app=Flask(__name__)
analysis_drop1=0
analysis_drop2=0
analytics_drop=0
analytics_year=0

@app.route('/',methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if request.form['action1'] == 'Analysis':
            return redirect(url_for('analysis'))
        elif  request.form['action1'] == 'Analytics':
            return redirect(url_for('analytics'))
        else:
            pass # unknown
    elif request.method == 'GET':
        return render_template('index.html')
    
    return render_template('index.html')

@app.route('/analysis',methods=['GET', 'POST'])
def analysis():

    if request.method == 'POST':
        if request.form['action4'] == 'Submit' and request.form['action2'] != "Choose..." and request.form['action3'] != "Choose...":
            global analysis_drop1,analysis_drop2
            analysis_drop1=request.form['action2']
            analysis_drop2=request.form['action3']
            return redirect(url_for('analysis_results'))
        else:
            pass # unknown
    elif request.method == 'GET':
        return render_template('analysis.html')
    
    return render_template('analysis.html')

@app.route('/analytics',methods=['GET', 'POST'])
def analytics():

    if request.method == 'POST':
        if request.form['action7'] == 'Submit' and request.form['action5'] != "Choose..." and request.form['action6'] !=None and request.form['action6'].isdigit() and int(request.form['action6'])>=2000 and int(request.form['action6'])<=2100 :
            global analytics_drop,analytics_year 
            analytics_drop= request.form['action5']
            analytics_year=request.form['action6']
            return redirect(url_for('analytics_results'))
        else:
            pass # unknown
    elif request.method == 'GET':
        return render_template('analytics.html')
    
    return render_template('analytics.html')

@app.route('/analysis_results')
def analysis_results():
    
    with pyodbc.connect('DRIVER='+driver+';SERVER=tcp:'+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password) as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * from "+analysis_drop1+" ORDER BY year")
            row = cursor.fetchone()
            year_row=[]
            car_mauf_row=[]
            
            while row:
                year_row.append((row[0]))
                car_mauf_row.append((row[2]))
                row = cursor.fetchone()
            data={"Year":year_row,"Cars_Manufactured "+analysis_drop1+" (in millions)":car_mauf_row}
            df=pd.DataFrame(data)
            

    with pyodbc.connect('DRIVER='+driver+';SERVER=tcp:'+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password) as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * from "+analysis_drop2+" ORDER BY year")
            row = cursor.fetchone()
            year_row=[]
            car_mauf_row=[]
            
            while row:
                year_row.append((row[0]))
                car_mauf_row.append((row[2]))
                row = cursor.fetchone()
            data1={"Year":year_row,"Cars_Manufactured "+analysis_drop2+" (in millions)":car_mauf_row}
            df1=pd.DataFrame(data1)
            
    df['Cars_Manufactured '+analysis_drop2+' (in millions)']=df1['Cars_Manufactured '+analysis_drop2+' (in millions)']
    

    fig = px.line(df, x="Year",y=df.columns[1:3])
    fig.show()
    return redirect(url_for('analysis'))


@app.route('/analytics_results',methods=['GET', 'POST'])
def analytics_results():
    with pyodbc.connect('DRIVER='+driver+';SERVER=tcp:'+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password) as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * from "+analytics_drop+" ORDER BY year")
            row = cursor.fetchone()
            year_row=[]
            car_mauf_row=[]
            
            while row:
                year_row.append((row[0]))
                car_mauf_row.append((row[2]))
                row = cursor.fetchone()
            data={"Year":year_row,"Cars_Manufactured "+analytics_drop+" (in millions)":car_mauf_row}
            df=pd.DataFrame(data)
            X=df.iloc[:,:1].values
            y=df.iloc[:,-1].values
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)
            regressor = LinearRegression()
            regressor.fit(X_train, y_train)
            predicted_val=str(round((float(regressor.predict([[analytics_year]]))),2))
            

            return render_template('final_result.html',first_header=predicted_val,p1=analytics_drop,p2=analytics_year)

if __name__ == '__main__':
    app.run(debug=True)


