rm -r migrations
flask db init
flask db migrate -m 'Changes to db'
flask db upgrade