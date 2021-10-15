import os


def handle_uploaded_file(p, f):
    with open(p, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

def handle_uploaded_file_str(p, f):
    with open(p, 'w+') as destination:
        destination.write(f)

if __name__ == "__main__":
    print(os.getcwd())
    handle_uploaded_file_str("asd.txt", 'fsjalsdf'
                                        'sdfasd'
                                        'fdsa'
                                        '123'
                                        '中文'
                                        'a')