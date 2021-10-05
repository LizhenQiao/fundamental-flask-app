from app import webapp
webapp.secret_key = "you-will-never-know-lol"
webapp.run('0.0.0.0', 5000, debug=False)
