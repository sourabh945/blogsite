API documentation for easy use
------------------------------

These apis are use for the accessing the GET and CRETAE options of the database using wrapper 

It is REST framework apis 

------------------------------

LIST OF APIS : 

1. Getting access token: 

    DESC: it is use for making the access token for api access it use your login credential to make the token

    URL : '/api/create-token/'

    METHOD : POST

    STRUCTURE : --HEAD 'Content-Type: application/json' --data {"username": <your username> , "password": <your password>}

    RESPONSE : {"username": <your username> , "token": <access token>}

2. Getting the blog by id: 

    DESC : it is use for getting the blog by id

    URL : '/api/posts/<str:id>/'

    METHOD : POST 

    STRUCTURE : --HEAD 'Content-Type: application/json' --HEAD 'Authorization: Token <your access token>'

    RESPONSE : {
        "id" : <int: id>,
        "title" : <str: title>,
        "date_of_pub": <date: date of publication>,
        "author" : <str: author usename>,
        "content": <str: content>
    }

3. Creating the blog:

    DESC : it is use for creating the blog

    URL : '/api/posts/'

    METHOD : POST   

    STRUCTURE : --HEAD 'Content-Type: application/json' --HEAD 'Authorization: Token <your access token>' --data {"title":<blog title> , "content": <content> }

    RESPONSE : {
        "id": <int: id of create blog>
    }

4. Get all blogs: 

    DESC : it is return the blog pages with page size define by you but with max_page_size of 100 

    URL : '/api/posts/?page_size=<int: page_size>&page=<int: page number>'

    METHOD : GET

    STRUCTURE : --HEAD 'Content-Type: application/json' --HEAD 'Authorization: Token <your access token>'

    RESPONSE : {
        "count": <int: total number of blogs>,
        "next": <url: url for access next page>,
        "previous": <url: url for access previous page>,
        "results": [
            {
                "id" : <int: id>,
                "title" : <str: title>,
                "date_of_pub": <date: date of publication>,
                "author" : <str: author usename>,
                "content": <str: content>
            }
        ]
    }

5. hello message: 

    DESC : it is testing url for checking the authencite of your token 

    URL : 'api/hello/'

    METHOD : GET

    STRUCTURE : --HEAD 'Content-Type: application/json' --HEAD 'Authorization: Token <your access token>'

    RESPONSE : {
        "message" : "Hello {username}"
    }