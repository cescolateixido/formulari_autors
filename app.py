from flask import Flask, render_template, request, redirect, url_for, jsonify
import pandas as pd
import os

app = Flask(__name__)

# Configuración del archivo Excel de datos
EXCEL_DATOS = "base_dades_formulari.xlsx"
EXCEL_RESPOSTES = "respostes_formulari.xlsx"

def carregar_dades():
    # Cargamos cada hoja según tus especificaciones 
    comercials = pd.read_excel(EXCEL_DATOS, sheet_name='llistat_comercials').to_dict(orient='records')
    centres = pd.read_excel(EXCEL_DATOS, sheet_name='llistat_centres').to_dict(orient='records')
    animacions = pd.read_excel(EXCEL_DATOS, sheet_name='tipus_animacio').to_dict(orient='records')
    llibres = pd.read_excel(EXCEL_DATOS, sheet_name='llibres_disponibles').to_dict(orient='records')
    return comercials, centres, animacions, llibres

@app.route('/')
def formulari():
    comercials, centres, animacions, llibres = carregar_dades()
    return render_template('formulari.html', 
                           comercials=comercials, 
                           centres=centres, 
                           animacions=animacions, 
                           llibres=llibres)

@app.route('/enviar', methods=['POST'])
def enviar():
    dades = request.form.to_dict()
    df_nova = pd.DataFrame([dades])
    
    # Guardar en Excel local [cite: 2]
    if os.path.exists(EXCEL_RESPOSTES):
        df_existent = pd.read_excel(EXCEL_RESPOSTES)
        df_final = pd.concat([df_existent, df_nova], ignore_index=True)
    else:
        df_final = df_nova
        
    df_final.to_excel(EXCEL_RESPOSTES, index=False)
    return "Dades guardades correctament a l'Excel local."

if __name__ == '__main__':
    app.run(debug=True)