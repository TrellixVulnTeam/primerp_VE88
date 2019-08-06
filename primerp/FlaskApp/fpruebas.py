import time
import pygal
from pygal.style import LightStyle
from pymongo import MongoClient
import pprint
#import cairosvg

client = MongoClient('mongodb://172.16.11.20:27017/')

db = client.registros
def functQuery(titulo,result,graph,nombre):
    result = list(result)
    for element in result:
        if element['_id'] == None:
            result.remove(element)
        if element['_id'] == 'DNS':
            result.remove(element)
    for element in result:
        element['total'] = element['total'] / 2**20
        element['total'] = round(element['total'],2)

    if (len(result)>1):
        host = ['app', []]
        conteomb = ['mb', []]
        for i in range(len(result)):
            host[1].append(result[i]['_id'])
            conteomb[1].append(int(result[i]['total']))
        graph.title = titulo
        for i in range(len(result)):
            graph.add(host[1][i], conteomb[1][i])
        graph_data = graph.render_to_png('C:/Users/asalinas/Documents/PycharmProjects/flask/proyecto/primerp/primerp/FlaskApp/templates/salidaReporte/archivos/tablas/'+nombre+'.png')
    pprint.pprint(result)

    return result

def functQueryApp(titulo,result,graph,nombre):
    result = list(result)

    for element in result:
        if element['_id']['Categoria'] == 'unscanned' or element['_id']['Categoria'] == 'unknown':
            result.remove(element)

    for element in result:
        element['total'] = element['total'] / 2**20
        element['total'] = round(element['total'],2)

    if (len(result)>1):
        host = ['host', []]
        conteomb = ['mb', []]
        for i in range(len(result)):
            #print(result[i]['_id']['App'])
            host[1].append(result[i]['_id']['App'])
            conteomb[1].append(int(result[i]['total']))
        graph.title = titulo
        for i in range(len(result)):
            graph.add(host[1][i], conteomb[1][i])
        graph_data = graph.render_to_png('C:/Users/asalinas/Documents/PycharmProjects/flask/proyecto/primerp/primerp/FlaskApp/templates/salidaReporte/archivos/tablas/'+nombre+'.png')
    return result

def functQueryUsuarios(titulo,result,graph,nombre):
    result = list(result)
    for element in result:
        if element['_id'] == None:
            result.remove(element)
        if element['_id'] == 'DNS':
            result.remove(element)

    for element in result:
        element['total'] = element['total'] / 2**20
        element['total'] = round(element['total'],2)

    if (len(result)>1):
        host = ['app', []]
        conteomb = ['mb', []]
        for i in range(len(result)):
            host[1].append(result[i]['_id']['ip'])
            conteomb[1].append(int(result[i]['total']))
        graph.title = titulo
        for i in range(len(result)):
            graph.add(host[1][i], conteomb[1][i])
        graph_data = graph.render_to_png('C:/Users/asalinas/Documents/PycharmProjects/flask/proyecto/primerp/primerp/FlaskApp/templates/salidaReporte/archivos/tablas/'+nombre+'.png')
    pprint.pprint(result)

    return result

############## FUNCIONES REPORTES #############################



def rep1(fechai,fechaf,empresa): #Top 10 categorias web
    graph = pygal.Pie(height=420)
    nombre = "rep1"
    result = db.web.aggregate([
        {"$match": {"$and": [{"_id.Fecha": {"$gte":fechai, "$lte":fechaf}},{"_id.Empresa":empresa}]}},
        {"$addFields":{"Total": {"$sum":"$_id.Bytes"}}},
        {"$group": {"_id": "$_id.categoria","total":{"$sum":"$Total"}}},
        {"$sort": {"total": -1}},
        {"$limit":12}
    ])
    result = list(result)
    graph_data=functQuery("Sitios web",result,graph,nombre)
    pprint.pprint(graph_data)
    return graph_data

def rep2(fechai,fechaf,empresa): #Top usuarios categorias web
    graph = pygal.Bar(height=420)
    nombre = "rep2"
    result = db.web.aggregate([
        {"$match": {"$and": [{"_id.Fecha": {"$gte":fechai, "$lte":fechaf}},{"_id.Empresa":empresa}]}},
        {"$addFields":{"Total": {"$sum":"$_id.Bytes"}}},
        {"$group": {"_id": {"usuario":"$_id.usuario","ip":"$_id.ip","hostname":"$_id.hostname",'categoria':'$_id.categoria',},"total":{"$sum":"$Total"}}},
        {"$sort": {"total": -1}},
        {"$limit":12}
    ])
    result = list(result)
    graph_data=functQueryUsuarios("Usuarios",result,graph,nombre)
    pprint.pprint(graph_data)
    return result



def rep3(fechai,fechaf,empresa): #Usuarios Wifi
    graph = pygal.Bar(height=420)
    nombre = "rep3"
    result = db.appwifi.aggregate([
        {"$match": {"$and": [{"_id.Fecha": {"$gte": fechai, "$lte": fechaf}},{"_id.Empresa": empresa}]}},
        {"$addFields":{"Total": {"$sum":"$_id.Bytes"}}},
        {"$group": {"_id": {'usuario':'$_id.usuario',"ip":"$_id.ip","hostname":"$_id.hostname","SSID":"$_id.SSID"},"total":{"$sum":"$Total"}}},
        {"$sort": {"total": -1}},
        {"$limit":12}
    ])
    result = list(result)
    for element in result:
        element['total'] = element['total'] / 2**20
        element['total'] = round(element['total'],2)

    pprint.pprint(result)
    return result

def rep4(fechai,fechaf,empresa): #Top 10 aplicaciones
    graph = pygal.Bar(height=420)
    nombre = "rep4"
    result = db.aplicacion.aggregate([
        {"$match": {"$and": [{"_id.Fecha": {"$gte": fechai, "$lte": fechaf}},{"_id.Empresa": empresa}]}},
        {"$addFields":{"Total": {"$sum":"$_id.Bytes"}}},
        {"$group": {"_id": {"App":"$_id.Aplicacion","Categoria":"$_id.categoria"}, "total":{"$sum":"$Total"}}},
        {"$sort": {"total": -1}},
        {"$limit":12}
    ])
    print("Resultado")
    result = list(result)
    #pprint.pprint(result)
    graph_data = functQueryApp("Aplicaciones",result,graph,nombre)

    return graph_data

def rep5(fechai,fechaf,empresa): #Top 10 Audio/Video
    graph = pygal.Bar(height=420)
    nombre = "rep5"
    result = db.aplicacion.aggregate([
        {"$match": {"$and": [{"_id.Fecha": {"$gte": fechai, "$lte": fechaf}},{"_id.Empresa": empresa},{"_id.uid":7}]}},
        {"$addFields":{"Total": {"$sum":"$_id.Bytes"}}},
        {"$group": {"_id": {"App":"$_id.Aplicacion","Categoria":"$_id.categoria"}, "total":{"$sum":"$Total"}}},
        {"$sort": {"total": -1}},
        {"$limit":12}
        ])
    result = list(result)
    graph_data=functQueryApp("Audio y video",result,graph,nombre)
    return graph_data

def rep6(fechai,fechaf,empresa): #Top 10 Audio/Video por usuario
    graph = pygal.Bar(height=420)
    nombre = "rep6"
    result = db.aplicacion.aggregate([
        {"$match": {"$and": [{"_id.Fecha": {"$gte": fechai, "$lte": fechaf}},{"_id.Empresa": empresa},{"_id.uid":7}]}},
        {"$addFields":{"Total": {"$sum":"$_id.Bytes"}}},
        {"$group": {"_id": {"App":"$_id.Aplicacion","Usuario":"$_id.usuario","ip":"$_id.ip","Categoria":"$_id.categoria"}, "total":{"$sum":"$Total"}}},
        {"$sort": {"total": -1}},
        {"$limit":12}
    ])
    graph_data=functQueryUsuarios("Audio y video por usuario",result,graph,nombre)
    return graph_data

def rep7(fechai,fechaf,empresa): #Top 10 Audio/Video WIFI por usuario
    graph = pygal.Bar(height=420)
    nombre = "rep7"
    result = db.appwifi.aggregate([
        {"$match": {"$and": [{"_id.Fecha": {"$gte": fechai, "$lte": fechaf}},{"_id.Empresa": empresa},{"_id.uid":7}]}},
        {"$addFields":{"Total": {"$sum":"$_id.Bytes"}}},
        {"$group": {"_id": {"Usuario":"$_id.usuario","ip":"$_id.ip","Categoria":"$_id.categoria","SSID":"$_id.SSID"}, "total":{"$sum":"$Total"}}},
        {"$sort": {"total": -1}},
        {"$limit":12}
    ])
    result = list(result)
    graph_data=functQueryUsuarios("Audio y video por WIFI",result,graph,nombre)
#    print(graph_data)
    return graph_data

def rep8(fechai,fechaf,empresa): #Sitios web permitidos
    graph = pygal.Bar(height=420)
    nombre = "rep8"
    result = db.web.aggregate([
        {"$match": {"$and": [{"_id.Fecha": {"$gte": fechai, "$lte": fechaf}},{"_id.Empresa": empresa},{"_id.Accion":"passthrough"}]}},
        {"$addFields":{"Total": {"$sum":"$_id.Bytes"}}},
        {"$group": {"_id": "$_id.hostname","total":{"$sum":"$Total"}}},
        {"$sort": {"total": -1}},
        {"$limit":12}
    ])
    graph_data=functQuery("Sitios permitidos",result,graph,nombre)
    return graph_data


def rep9(fechai,fechaf,empresa): #Categorias web bloqueadas
    graph = pygal.Pie(height=420)
    nombre = "rep9"
    result = db.web.aggregate([
        {"$match": {"$and": [{"_id.Fecha": {"$gte":fechai, "$lte":fechaf}},{"_id.Empresa":empresa},{"_id.Accion":"blocked"}]}},
        {"$group": {"_id": "$_id.categoria","total":{"$sum":1}}},
        {"$sort": {"total": -1}},
        {"$limit":12}
    ])
    result = list(result)
    for element in result:
        if element['_id'] == None:
            result.remove(element)

    pprint.pprint(result)
    #graph_data=functQuery("Categorias bloqueadas",result,graph,nombre)
    #pprint.pprint(graph_data)
    return result

def rep10(fechai,fechaf,empresa): #Sitios web bloqueados
    graph = pygal.Bar(height=420)
    nombre = "rep10"
    result = db.web.aggregate([
        {"$match": {"$and": [{"_id.Fecha": {"$gte": fechai, "$lte": fechaf}},{"_id.Empresa": empresa},{"_id.Accion":"blocked"}]}},
        {"$addFields":{"Total": {"$sum":"$_id.Bytes"}}},
        {"$group": {"_id": {'hostname':"$_id.hostname",'categoria':"$_id.categoria"},"total":{"$sum":"$Total"}}},
        {"$sort": {"total": -1}},
        {"$limit":12}
    ])
    result = list(result)
    for element in result:
        if element['_id'] == None:
            result.remove(element)

    pprint.pprint(result)

    #graph_data=functQuery("Sitios web bloqueados",result,graph,nombre)
    return result

def rep11(fechai,fechaf,empresa): #Top usuarios categorias web bloqueados
    graph = pygal.Pie(height=420)
    nombre = "rep11"
    result = db.web.aggregate([
        {"$match": {"$and": [{"_id.Fecha": {"$gte":fechai, "$lte":fechaf}},{"_id.Empresa":empresa},{"_id.Accion":"blocked"}]}},
        {"$addFields":{"Total": {"$sum":"$_id.Bytes"}}},
        {"$group": {"_id": {"usuario":"$_id.usuario","ip":"$_id.ip","categoria":"$_id.categoria"},"total":{"$sum":"$Total"}}},
        {"$sort": {"total": -1}},
        {"$limit":12}
    ])
    result = list(result)
    for element in result:
        element['total'] = element['total'] / 2**20
        element['total'] = round(element['total'],2)
    pprint.pprint(result)

    #graph_data=functQuery("Usuarios",result,graph,nombre)
    #pprint.pprint(graph_data)
    return result

def rep12(fechai,fechaf,empresa):
    graph = pygal.Bar(height=420)
    nombre = "rep12"
    result = db.virus.aggregate([
        {"$match": {"$and": [{"_id.Fecha": {"$gte": fechai, "$lte": fechaf}},{"_id.Empresa": empresa}]}},
        {"$group":{"_id":{"fecha":"$_id.Fecha","usuario":"$_id.usuario","ip":"$_id.ip","virus":"$_id.Virus","Accion":"$_id.Accion","count":"$count"}}}
    ])
    result = list(result)
    pprint.pprint(result)
    return result

start =time.time()

initialDate = '2019-06-01'
finalDate = '2019-08-01'
empresa = "Cidexsa-Aeropuerto FWF30D"

#consulta = rep5(initialDate,finalDate,empresa)
#pprint.pprint(consulta)
consulta = rep12(initialDate,finalDate,empresa)

print(time.time()-start)
