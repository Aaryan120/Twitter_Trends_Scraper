import os


class Config:
    DB_CONNECTION_STRING = os.getenv('DB_CONNECTION_STRING')
    DB_NAME = "TwitterTrends"
    COLLECTION_NAME = "TRENDS"
    DRIVER_PATH = "D:\Selenium Drivers\chromedriver-win64"
    PROXY_USERNAME = os.getenv('PROXY_USERNAME')
    PROXY_PASSWORD = os.getenv('PROXY_PASSWORD')
    PROXY_PORT = os.getenv('PROXY_PORT')
    PROXY_HOST = os.getenv('PROXY_HOST')
    TWITTER_USERNAME = os.getenv('TWITTER_USERNAME')
    TWITTER_PASSWORD = os.getenv('TWITTER_PASSWORD')
    TWITTER_EMAIL = os.getenv('TWITTER_EMAIL')
