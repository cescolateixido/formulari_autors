from flask import Flask, render_template, request, os
import pandas as pd

app = Flask(__name__)

# Configuració dels arxius Excel
# Nota: Si fas servir Volums a Railway, hauries d'afegir 'data/' davant del nom
EXCEL_DATOS = "base_dades_formulari.xlsx"
EXCEL_RESPOSTES = "respostes_formulari.xlsx"

def carregar_dades():
    # Carreguem cada full segons les teves especificacions
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
    dades = request.form.to_dict()
    df_nova = pd.DataFrame([dades])
    
    # Guardar en Excel local
    if os.path.exists(EXCEL_RESPOSTES):
        df_existent = pd.read_excel(EXCEL_RESPOSTES)
        df_final = pd.concat([df_existent, df_nova], ignore_index=True)
    else:
        df_final = df_nova
        
    df_final.to_excel(EXCEL_RESPOSTES, index=False)
    return "Dades guardades correctament a l'Excel local."

# --- CANVI CRUCIAL PER A RAILWAY ---
if __name__ == '__main__':
    # Railway assigna un port dinàmic a través de la variable d'entorn PORT
    port = int(os.environ.get('PORT', 5000))
    # Hem de posar host='0.0.0.0' per permetre connexions externes
    app.run(host='0.0.0.0', port=port)