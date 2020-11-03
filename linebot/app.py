import json
# schema imports
from awsSchema.apigateway import Response, Event

# line bot imports
from linebot import LineBotApi
from linebot.models import TextSendMessage
from linebot.exceptions import LineBotApiError
# chatterbot imports
import chatterbot
from chatterbot import ChatBot
# import s3bz
from s3bz.s3bz import S3

ACCESSTOKEN = 'TQ393qRcgP5+onjGEJQmmuwxpvelLdBGh5+5hA8haI6Jmn2i+KXyDmg8vASWWNJh3Jl22x/w0tRx8E+LqespD7qQS5VZtmCL1OLbrlrp4YNllymiJhGuGaQgH1zy2UlNnWR5+zQ86fwRXc/x3zsX3gdB04t89/1O/w1cDnyilFU='

## crate chatbot object
bot = ChatBot(
    'robot',
    storage_adapter='chatterbot.storage.SQLStorageAdapter',
    preprocessors=[
        'chatterbot.preprocessors.clean_whitespace',
    ],
    database_uri='sqlite:////tmp/database.db',
    read_only=True
)
## download chatbot file
key = 'chatterbotdb.db'
path = '/tmp/database.db'
bucket = 'chatterbot-data'
S3.loadFile(key=key, path=path, bucket = bucket)


def getReplyToken(body):
    return body["events"][0]['replyToken']
def sendReply(replyToken, accessToken):
    '''send line reply message'''
    line_bot_api = LineBotApi(accessToken)
    line_bot_api.reply_message(replyToken, TextSendMessage(text='Hello World!'))
def chatterbotResponse(inputText):
    response = bot.get_response(inputText)
    return response.text
    
    
def lineBot(event, *args):
    e = Event.from_dict(event)
    body = e.getBody()
    try:
        replyToken = getReplyToken(body)
    except:
        return Response.getReturn(statusCode = 400, body = {'error': 'cant get reply token'})
    try:
        sendReply(replyToken, ACCESSTOKEN)
    except:
        return Response.getReturn(statusCode = 400, body = {'error': 'response token not valid'})
    response = {'replyToken': replyToken}
    
    return Response.getReturn( body = response, statusCode= 200, headers = {'hello':'hello'} )