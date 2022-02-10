from flask import Flask, render_template, request, redirect,url_for,jsonify
app = Flask(__name__)


#from spacy.matcher import Matcher 
#from spacy.tokens import Span 
from py2neo import Graph, Subgraph, Node, Relationship
from py2neo import NodeMatcher, RelationshipMatcher
#wordnet = Graph(host='0.0.0.0', port=7687,name="mywordnet")
wordnet = Graph(host='localhost', port=7687,name="neo4j", user="neo4j", password="wnet")

def word_exist(word):
    req= "MATCH (l:LexicalEntry{lemma_form:'"+ str(word) +"'}) RETURN l"
    if(wordnet.run(req).data()):
        return True
    return False

def get_infos(word):      
    req= "MATCH (l:LexicalEntry{lemma_form:'"+ str(word.lower()) +"'})-[*1]->(se:Sense)-[*1]->(s:Synset) RETURN s.definition AS definition, s.pos AS pos, s.examples AS examples"
    data = wordnet.run(req).data()
    if not(data):
        return 'None'
    return data





@app.route('/',methods=['GET'])
def Home():
    return render_template('index.html')


@app.route('/predict',methods=['GET','POST'])
def predict():
    '''
    For rendering results on HTML GUI
    '''
    ## test if no prams passed with predict
    opt_param = request.args.get("type")
    if (opt_param is None) and (request.form.get('word') is None):
        print("Argument not provided")
        return redirect(url_for('Home'))
    if(request.args.get('type')):
        print('got search from get !!!')
        word = request.args.get('type')
        infos = get_infos(word)
    if(request.form.get('word')):
        word = request.form.get('word')
        print('got search from post !!!')
        infos = get_infos(word)
    return render_template('index.html', text=word, infos = infos)


@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('page404.html'), 404



##this is just a comment for testing the pipeline
if __name__=="__main__":
    app.run(host='0.0.0.0',debug=True)

