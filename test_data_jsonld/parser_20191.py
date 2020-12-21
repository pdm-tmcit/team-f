import os
import re
import json
import pyld
import rdflib
import requests

# グローバル変数
g = rdflib.Graph()

def removeExtra(data):
    array = data.split('\r\n')
    array.remove('o')
    array.remove('')

    return array

# JSON-LDの読み込み,
# JSON-LDをRDFに変換しグラフを作成
def loadJsonld(fileName):
    # Setting HTTP Request URL 
    host = 'http://127.0.0.1:8080/'
    requestUrl = host + fileName

    # Load JSON-LD
    expanded = pyld.jsonld.expand(requestUrl)
    jsonData = json.dumps(expanded, indent=2, ensure_ascii=False)
    jsonld = json.loads(jsonData)[0]
    normalized = pyld.jsonld.normalize(jsonld, {'algorithm': 'URDNA2015', 'format': 'application/nquads'})

    # Display JSON-LD
    # print(jsonData)
    # Display RDF converted from JSON-LD
    # print(normalized)

    g.parse(data=normalized, format='n3')

def getPhase():
    sparql = """
        prefix ns1: <https://werewolf.world/resource/0.3/>
        prefix ns2: <https://licos.online/state/0.3/village#3/>
        SELECT * WHERE {
            ns2:systemMessage ns1:phase ?o.
        }
        """
    phase = g.query(sparql).serialize(format='csv').decode('utf-8')
    phase = removeExtra(phase)

    return phase

##
# 各値取得関数
# getCharacterData()                 :キャラクターデータ取得(SPARQLに必要)
# getCharacterId(characterData)      :キャラクターID取得(人数)
# getCharacterName(characterData)    :キャラクター名取得
# getCharacterStatus(characterData)  :キャラクターステータス取得
# isMineCharacter(characterData)     :自身判定
# getRoleData()                      :全役職データ取得
# getRoleName(roleData)              :役職名取得
# isMineRole(roleData)               :自身の役職判定
# getChatMessage()                   :チャットメッセージ取得
##

def getCharacterData():
    sparql = """
        prefix ns1: <https://werewolf.world/resource/0.3/>
        prefix ns2: <https://licos.online/state/0.3/village#3/>
        select ?o where {
            ns2:systemMessage ns1:character ?o.
        }
        """
    q = g.query(sparql).serialize(format='csv').decode('utf-8')
    characterData = removeExtra(q)

    return characterData

def getCharacterId(characterData):
    sparql = """
        prefix ns1: <https://werewolf.world/resource/0.3/>
        select ?o where { 
            ?class ns1:characterId ?o
        }"""
    q = g.query(sparql, initBindings={'class': rdflib.URIRef(characterData)}).serialize(format='csv').decode('utf-8')
    characterId = removeExtra(q)

    return characterId

def getCharacterName(characterData):
    pattern = re.compile('[a-zA-Z]+')
    sparql = """
        prefix ns1: <https://werewolf.world/resource/0.3/>
        select ?o where { 
            ?class ns1:characterName ?o
        }"""
    q = g.query(sparql, initBindings={'class': rdflib.URIRef(characterData)}).serialize(format='csv').decode('utf-8')
    characterName = removeExtra(q)
    if not pattern.fullmatch(characterName[0]):
        characterName[0], characterName[1] = characterName[1], characterName[0]

    return characterName
    
def getCharacterStatus(characterData):
    sparql = """
        prefix ns1: <https://werewolf.world/resource/0.3/>
        select ?o where { 
            ?class ns1:characterStatus ?o
        }"""
    q = g.query(sparql, initBindings={'class': rdflib.URIRef(characterData)}).serialize(format='csv').decode('utf-8')
    characterStatus = removeExtra(q)

    return characterStatus

def isMineCharacter(characterData):
    sparql = """
        prefix ns1: <https://werewolf.world/resource/0.3/>
        select ?o where { 
            ?class ns1:characterIsMine ?o
        }"""
    q = g.query(sparql, initBindings={'class': rdflib.URIRef(characterData)}).serialize(format='csv').decode('utf-8')
    isMineCharacter = removeExtra(q)
    if isMineCharacter[0] == "true":
        return True
    else:
        return False

def getRoleData():
    sparql = """
        prefix ns1: <https://werewolf.world/resource/0.3/>
        prefix ns2: <https://licos.online/state/0.3/village#3/>
        select ?o where {
            ns2:systemMessage ns1:role ?o.
        }
        """
    q = g.query(sparql).serialize(format='csv').decode('utf-8')
    roleData = removeExtra(q)

    return roleData

def getRoleName(roleData):
    pattern = re.compile('[a-zA-Z]+')
    sparql = """
        prefix ns1: <https://werewolf.world/resource/0.3/>
        select ?o where { 
            ?class ns1:roleName ?o
        }"""
    q = g.query(sparql, initBindings={'class': rdflib.URIRef(roleData)}).serialize(format='csv').decode('utf-8')
    roleName = removeExtra(q)
    if not pattern.fullmatch(roleName[0]):
        roleName[0], roleName[1] = roleName[1], roleName[0]

    return roleName

def isMineRole(roleData):
    sparql = """
        prefix ns1: <https://werewolf.world/resource/0.3/>
        select ?o where { 
            ?class ns1:roleIsMine ?o
        }"""
    q = g.query(sparql, initBindings={'class': rdflib.URIRef(roleData)}).serialize(format='csv').decode('utf-8')
    isMineRole = removeExtra(q)
    if isMineRole[0] == "true":
        return True
    else:
        return False

def getChatMessage():
    sparql = """
        prefix ns1: <https://werewolf.world/resource/0.3/>
        prefix ns2: <https://licos.online/state/0.3/village#3/>
        select ?o where {
            ns2:chatMessage ns1:chatText ?o.
        }
        """
    q = g.query(sparql).serialize(format='csv').decode('utf-8')
    chatMessage = removeExtra(q)
    
    return chatMessage[0][1:len(chatMessage[0])-1]
