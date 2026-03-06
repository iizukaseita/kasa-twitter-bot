import os
import random
import requests
from datetime import datetime, timezone, timedelta

try:
    import tweepy
except ImportError:
    tweepy = None

from cities import CITIES
from messages import build_tweet

JST = timezone(timedelta(hours=9))


def get_weather(lat: float, lon: float) -> dict:
    """Open-Meteo APIで今日の天気を取得"""
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": lon,
        "daily": "weather_code,temperature_2m_max,temperature_2m_min,precipitation_sum,precipitation_probability_max",
        "timezone": "Asia/Tokyo",
        "forecast_days": 1,
    }
    resp = requests.get(url, params=params, timeout=10)
    resp.raise_for_status()
    data = resp.json()

    daily = data["daily"]
    return {
        "weather_code": daily["weather_code"][0],
        "temp_max": daily["temperature_2m_max"][0],
        "temp_min": daily["temperature_2m_min"][0],
        "precip_sum": daily["precipitation_sum"][0],
        "precip_prob": daily["precipitation_probability_max"][0],
    }


def classify_weather(weather_code: int, precip_prob: float, precip_sum: float) -> str:
    """
    天気を分類（アプリと同じロジック）
    - 雪: weather_code 71, 73, 75, 77, 85, 86
    - 雨: precip_prob >= 40 or precip_sum >= 0.5 or weather_code 61-67
    - 曇り/微妙: precip_prob >= 20 or precip_sum >= 0.1
    - 晴れ: それ以外
    """
    snow_codes = {71, 73, 75, 77, 85, 86}
    rain_codes = {51, 53, 55, 56, 57, 61, 63, 65, 66, 67, 80, 81, 82}

    if weather_code in snow_codes:
        return "snow"
    if weather_code in rain_codes or precip_prob >= 40 or precip_sum >= 0.5:
        return "rain"
    if precip_prob >= 20 or precip_sum >= 0.1:
        return "cloudy"
    return "sunny"


def post_tweet(text: str):
    """X APIでツイート"""
    if tweepy is None:
        raise ImportError("tweepy is not installed. Run: pip install tweepy")
    client = tweepy.Client(
        consumer_key=os.environ["X_API_KEY"],
        consumer_secret=os.environ["X_API_KEY_SECRET"],
        access_token=os.environ["X_ACCESS_TOKEN"],
        access_token_secret=os.environ["X_ACCESS_TOKEN_SECRET"],
    )
    response = client.create_tweet(text=text)
    return response


def main():
    # ランダムに都市を選択
    city = random.choice(CITIES)
    # 表示名を組み立て（例: "札幌市中央区", "川口市" など）
    area_name = city["city"] + city["name"] if city["name"] not in city["city"] else city["city"]
    print(f"Selected area: {area_name} ({city['pref']})")

    # 天気取得
    weather = get_weather(city["lat"], city["lon"])
    print(f"Weather: code={weather['weather_code']}, "
          f"precip_prob={weather['precip_prob']}%, "
          f"precip_sum={weather['precip_sum']}mm, "
          f"temp={weather['temp_min']}~{weather['temp_max']}℃")

    # 天気分類
    weather_type = classify_weather(
        weather["weather_code"],
        weather["precip_prob"],
        weather["precip_sum"],
    )
    print(f"Classification: {weather_type}")

    # ツイート生成
    tweet_text = build_tweet(
        area_name=area_name,
        city_name=city["city"],
        pref=city["pref"],
        weather_type=weather_type,
        precip_prob=weather["precip_prob"],
        precip_max=weather["precip_sum"],
        temp_max=weather["temp_max"],
        temp_min=weather["temp_min"],
    )
    print(f"Tweet ({len(tweet_text)} chars):\n{tweet_text}")

    # ツイート投稿
    if os.environ.get("DRY_RUN") == "true":
        print("\n[DRY RUN] Tweet not posted.")
    else:
        response = post_tweet(tweet_text)
        print(f"\nTweet posted! ID: {response.data['id']}")


if __name__ == "__main__":
    main()
