import os
from flask import Flask, render_template, request, send_file
import pandas as pd

app = Flask(__name__)

# Configuració dels arxius Excel
EXCEL_DATOS = "base_dades_formulari.xlsx"

# RUTA DEL VOLUM (Corregida amb la barra inicial /)
DIRECTORI_DADES = "/app/data"

# Creem la carpeta si no existeix (necessari perquè funcioni el volum)
if not os.path.exists(DIRECTORI_DADES):
    os.makedirs(DIRECTORI_DADES, exist_ok=True)

# Arxiu de respostes (Afegit el parèntesi que faltava)
EXCEL_RESPOSTES = os.path.join(DIRECTORI_DADES, "respostes_formulari.xlsx")

def carregar_dades():
    try:
        comercials = pd.read_excel(EXCEL_DATOS, sheet_name='llistat_comercials').to_dict(orient='records')
        centres = pd.read_excel(EXCEL_DATOS, sheet_name='llistat_centres').to_dict(orient='records')
        animacions = pd.read_excel(EXCEL_DATOS, sheet_name='tipus_animacio').to_dict(orient='records')
        llibres = pd.read_excel(EXCEL_DATOS, sheet_name='llibres_disponibles').to_dict(orient='records')
        return comercials, centres, animacions, llibres
    except Exception as e:
        print(f"Error carregant l'Excel de dades: {e}")
        return [], [], [], []

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
    try:
        dades = request.form.to_dict()
        df_nova = pd.DataFrame([dades])
        
        if os.path.exists(EXCEL_RESPOSTES):
            df_existent = pd.read_excel(EXCEL_RESPOSTES)
            df_final = pd.concat([df_existent, df_nova], ignore_index=True)
        else:
            df_final = df_nova
            
        df_final.to_excel(EXCEL_RESPOSTES, index=False)
        return "Dades guardades correctament al Volum de Railway!"
    except Exception as e:
        return f"Error en guardar les dades: {e}"

# RUTA EXTRA: Per descarregar l'Excel fàcilment
@app.route('/descarregar')
def descarregar():
    if os.path.exists(EXCEL_RESPOSTES):
        return send_file(EXCEL_RESPOSTES, as_attachment=True)
    return "Encara no hi ha cap resposta guardada."

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)