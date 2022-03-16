import logging

import azure.functions as func
import pandas as pd
import pickle

INVALID_REQUEST_MESSSAGE = "This HTTP triggered function needs a valid userId parameter provided in POST as json"

def get_predictions(user_id, n=5):
    user_articles = set(clicks_df[clicks_df["user_id"]==user_id]["click_article_id"].to_list())
    scores = [(article, model.predict(user_id, article).est) for article in left_articles if article not in user_articles]
    scores.sort(key=lambda x: x[1], reverse=True)
    return [x[0] for x in scores[:n]]

clicks_df = pd.read_csv('./clicks_df.csv')
left_articles = set(clicks_df['click_article_id'].to_list())
with open(r"baseline.pickle", "rb") as input_file:
    model = pickle.load(input_file)

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    try:
        user_id = req.get_json()['userId']
        user_id = int(user_id)  
    except:
        return func.HttpResponse(
            INVALID_REQUEST_MESSSAGE,
            status_code=400
    )
    return func.HttpResponse(
        f"{get_predictions(user_id)}",
        status_code=200)
