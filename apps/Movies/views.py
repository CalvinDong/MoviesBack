# Create your views here.
import json

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from conda_build.api import render
from apps import globalvar as gl

def index(request):
    return HttpResponse( "Hello World" )


def recommendation(request):
    print('recommendation')
    dataset = gl.get_value( 'dataset' )
    knn_model = gl.get_value( 'knn_model' )
    movie_list = list( dataset.index )

    if request.method == 'POST':
        concat = request.POST
        postBody = request.body
        print( concat )
        print( type( postBody ) )
        print( postBody )
        json_result = json.loads( postBody )
        print( json_result )
        name = json_result['name']
        print(name)
        return_data = {}
        if name not in movie_list:
            return_data['movies'] = ['Movie [' + str(name) + '] is not in our dataset, So we cannot recommendation']
            return JsonResponse(return_data, json_dumps_params={"ensure_ascii":False})
        query_index = dataset.index.get_loc( name )
        distances, indices = knn_model.kneighbors( dataset.loc[name, :].values.reshape( 1, -1 ),
                                                   n_neighbors=11 )

        recommendations = list()
        for i in range( 0, len( distances.flatten() ) ):
            if i == 0:
                print( 'Recommendations for {0}:\n'.format( dataset.index[query_index] ) )
            else:
                print( '{0}: {1}, with distance of {2}:'.format( i, dataset.index[indices.flatten()[i]],
                                                                 distances.flatten()[i] ) )
                recommendations.append( dataset.index[indices.flatten()[i]] )
        return_data['movies'] = recommendations
        return JsonResponse(return_data, json_dumps_params={"ensure_ascii":False})
    else:
        return HttpResponse( 'it is not a POST request' )
