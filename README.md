# Last Christmas

## Dev Setup

### Backend

- start db with `docker-compose -f docker-compose-dev up`
- run the `init.sql`file on the database
- start the api by running `app.py`
- the crawler can be manually started by calling the endpoint `curl 127.0.0.1:5000/api/crawler/www.youtube.de`

### Frontend

- check required installations with `node -v` and `npm -v`
- inside `frontend` folder run `npm install` to install project dependencies
- start react dev server by running `npm start`

## API Endpoints

- '/api/search/<string:search_term>'
- /api/crawler/<string:url>

## Implementation einer Suchmaschine
