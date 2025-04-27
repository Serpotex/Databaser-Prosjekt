class Config:
    #SQLALCHEMY_DATABASE_URI = 'sqlite:///db/social_media.db'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///db.sqlite3'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'supersecretkey'  # For forms, sessions, etc.
    