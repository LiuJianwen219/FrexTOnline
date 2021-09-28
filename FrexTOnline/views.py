from django.http import HttpResponse
from django.shortcuts import render, redirect


# Create your views here.
def test(request):
    freeExperiment = {
        'expItems': [
            {
                'expId': "0001",
                'expName': "exp01",
                'fileList': [
                    {
                        'fileId': "fid0001",
                        'fileName': "wenjian01"
                    },
                    {
                        'fileId': "fid0002",
                        'fileName': "wenjian02"
                    },
                ]
            },
            {
                'expId': "0002",
                'expName': "exp02",
                'fileList': [
                    {
                        'fileId': "fid0002",
                        'fileName': "wenjian02"
                    },
                    {
                        'fileId': "fid0003",
                        'fileName': "wenjian03"
                    },
                ]
            },
        ]

    }
    return render(request, 'Home/P1.html', {'freeExperiment': freeExperiment, 'text': "text"})


def favicon(request):
    return HttpResponse("favicon.ico")


def home(request):
    return redirect('/home/')
