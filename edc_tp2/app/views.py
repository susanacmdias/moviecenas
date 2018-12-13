import json
from s4api.graphdb_api import GraphDBApi
from s4api.swagger import ApiClient
from django.shortcuts import render, redirect
from django.http import HttpResponse

endpoint = "http://localhost:8000"
repo_name = "movies"

client = ApiClient(endpoint=endpoint)
accessor = GraphDBApi(client)

# Create your views here.

def home(request):
    to_be_searched = None

    try:
        if 'search-keyword' in request.POST:
            to_be_searched = request.POST.get("search-keyword")

            query = '''
                PREFIX movPred:<http://movies.org/pred/>
                SELECT ?mov
                WHERE{
                ?film movPred:name ?name .
                FILTER regex(?name, "''' + str(to_be_searched) + '''", "i") .
                ?film movPred:name ?mov .
                }
            '''

            payload_query = {"query" : query}
            res = accessor.sparql_select(body=payload_query, repo_name=repo_name)
            res = json.loads(res)
    
            for e in res['results']['bindings']:
                print(e['mov']['value'])
            
            if not res['results']['bindings']:
                return render(request, '404.html', {})
    finally:
        pass
            
    return render(request, 'index.html', {})

def celebrity(request):
    return render(request, 'celebrity-detail.html', {})

def movie(request):
    return render(request, 'movie-detail.html', {})