import os
from flask import Flask, jsonify, request
from flask_cors import CORS 

app = Flask(__name__)

cors = CORS(app, resource={r"/*":{"origins": "*"}})

@app.route("/", methods=["GET"])
def index():
    return "<h1>Hello World!</h1>"
  
  
def pop_dic(dic, pos=0):
    ids = list(dic.keys())
    dados = list(dic.values())

    dic_final = {}
    for verificador in range(len(ids)):
        if verificador != pos:
            id = ids[verificador]
            dado = dados[verificador]
            dic_final[id] = dado

    return dic_final



site = ''
Xphaths = {
    'Play':'',
    'Play2':'',
    'Player':'',
    'Player2':'',
    'Minutagem':'',
    'Minutagem2':'',
    'Anterior':'',
    'Proximo':'',
    'Mute':'',
    'MinutoAtual':'',
    'MinutosTotais':'',
}
users = {} # Lista dos usuarios da sessão.
lista_comando = {} # ['comando',execuções, {id:0 ou 1, id:indica se já executou}]







@app.route('/Register/<id_user>',methods=['GET']) # Registra um novo usuario.
def Registrar_user_chamada(id_user):

    num_user_resgistrados = len(users) 
    for user in range(num_user_resgistrados):
        user = user + 1
        id_user_registrado = users[str(user)]
        if str(id_user_registrado) == str(id_user):
            return jsonify(f'O usuario {id_user} não foi registrado pois já está registrado.')


    id_de_registro = num_user_resgistrados + 1
    users[str(id_de_registro)] = id_user

    return jsonify(f'Usuario {id_user} registrado.')



@app.route('/send_comand/<comand>',methods=['GET']) # Api recebe o comando e adiciona na lista.
def Enviar_comando(comand, comando_valido=False):
    global lista_comando

    if comand == 'play':
        comando = 'play'
        comando_valido=True

    elif comand == 'retroceder':
        comando = 'retroceder'
        comando_valido=True

    elif comand == 'avancar':
        comando = 'avancar'
        comando_valido=True

    elif comand == 'minutagem':
        comando = 'minutagem'
        comando_valido=True

    else:
        try:
            comand = comand.split('-')
            comand = comand[0]
            porcentagem = comand[1]
        except:
            pass
        if comand == 'porcentagem':
            comando = {'0':'porcentagem','1':porcentagem}
            comando_valido = True

    if comando_valido == True:
        users_executados = {}
        num_users_registrados = len(users)
        for id_registro in  range(num_users_registrados):
            id_registro = id_registro + 1
            user = users[str(id_registro)]
            users_executados[user] = 0

        num_comando_solicitados = len(lista_comando)
        id_de_chamada = num_comando_solicitados + 1
        
        id_utilizado = False
        id_anterior = 0
        id_usados = list(lista_comando.keys())
        for vrfcdr in range(len(id_usados)):
            id_usaado = id_usados[vrfcdr]
            if str(id_usaado) == str(id_de_chamada):
                id_utilizado = True
            
            if int(vrfcdr) > int(id_anterior):
                possivel_id = vrfcdr + 1

            id_anterior = vrfcdr

            if id_utilizado == True:
                id_de_chamada = possivel_id
            
            elif id_utilizado == False:
                id_de_chamada = id_de_chamada

        lista_comando[str(id_de_chamada)] = [comando,0,users_executados]

        return jsonify(f'O comando >{comando}< foi encamiado e sera executado.')
    
    return jsonify('Falha encamiamento do comando. Comando ivalido ou Erro no código.')



@app.route('/comand/<user_id>',methods=['GET']) # Retorna os comandos
def Receber_comando(user_id):

    try:
        comando = list(lista_comando.values())[0]
    except:
        return jsonify('Não existem comandos ainda!')

    if comando[2][str(user_id)] == 1:
        return jsonify('Comando em execução no momento já foi executado por você.')
    
    comando_executavel = comando[0]
    return jsonify(comando_executavel)



@app.route('/comand_executed/<id_user>',methods=['GET']) # Indica que o comando foi executado
def Finalizar_comando(id_user):
    global lista_comando
    lista_users = list(users.values())
    for IDs_registrados in lista_users:
        if str(id_user) != str(IDs_registrados):
            return jsonify(f'''Acesso negado!
Usuario não registrado!''')

    
    comando = list(lista_comando.values())
    if comando[0][2][id_user] == 1:
        return jsonify('Acesso negado você já finalizou esse comando!')


    execucoes = comando[0][1]
    execucoes = execucoes + 1


    id = list(lista_comando.keys())[0]
    lista_comando[str(id)][1] = execucoes
    lista_comando[str(id)][2][str(id_user)] = 1



    if comando[0][1] == len(lista_users):
        lista_comando = pop_dic(lista_comando, 0)

    return jsonify('Comando finalizado com sucesso!')








@app.route('/xphath/<item>/<xphath>',methods=['GET']) # Envia os xphaths das funções
def Enviar_xphaths(item, xphath):
    Xphaths[str(item)] = xphath
    return jsonify(Xphaths)


@app.route('/xphaths',methods=['GET']) # Retorna os Xphaths para o usuario
def Receber_xphaths():
    return jsonify(Xphaths)








@app.route('/send_site/<url>',methods=['GET']) # Envia o link do site para a API
def Recebe_link_site(url):
    global site
    site = url
    return jsonify(f'O site selecionado foi: {url} ')


@app.route('/site',methods=['GET']) # retorna o link do site para o user
def Enviar_link_site():
    return jsonify(site)





@app.route('/data/adm/<comand>/<dado>',methods=['GET']) 
def painel_adm(comand, dado):
    global lista_comando

    if comand == 'dados':
        dados = (f'''
{site}
{Xphaths}
{users}
{lista_comando}
''')

    elif comand == 'reset_list_comand':
        lista_comando = {}
        return jsonify('Comandos resetados!')

    elif comand == 'site':
        dados = dado

    return jsonify(dados)







def main():
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

if __name__ == "__main__":
    main()
