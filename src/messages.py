import random

# くもすけの挨拶パターン
GREETINGS = [
    "おはよう〜くも！",
    "おはようだくも〜！",
    "もーにんぐ〜くも！",
    "おはよ〜くも☁",
    "くもすけだくも〜！おはよう！",
    "おはようございますだくも〜！",
    "今日もいい朝だくも〜！",
]

# 傘いる（雨）パターン
RAIN_MESSAGES = [
    "今日の{city}は🌧雨だくも〜！傘を忘れずにだくも☂",
    "{city}は雨が降りそうだくも🌧 傘、いるよ〜くも！",
    "あめあめ〜くも🌧 {city}は今日傘がいるくも☂ 気をつけてね〜くも！",
    "{city}のみんな〜！今日は傘いるくも🌧 濡れないようにね〜くも☂",
    "今日の{city}は☂傘いるよ〜くも！雨に気をつけてね〜くも🌧",
    "{city}は雨模様だくも🌧 お出かけには傘を持ってね〜くも！",
]

# 傘いらない（晴れ）パターン
SUNNY_MESSAGES = [
    "今日の{city}は☀️晴れだくも〜！傘はいらないくも！いってらっしゃい〜くも✨",
    "{city}は☀️いいお天気だくも！傘いらないよ〜くも！",
    "ぴっかぴか〜くも☀️ {city}は今日傘いらないくも！気持ちいい一日になりそうだくも✨",
    "{city}のみんな〜！今日は☀️傘いらないくも〜！サングラスの方がいいかもだくも😎",
    "今日の{city}は傘いらないくも☀️ お出かけ日和だくも〜！",
    "{city}は晴れだくも〜☀️ 傘はお家でお留守番だくも！",
]

# 曇り・微妙パターン
CLOUDY_MESSAGES = [
    "今日の{city}は☁️くもりだくも〜。念のため折りたたみ傘があると安心だくも！",
    "{city}は☁️くもりだくも〜。傘は…微妙なところだくも。一応持っていくのがおすすめだくも！",
    "くもすけの仲間がいっぱいだくも☁️ {city}は今日くもり。折りたたみ傘があるといいかもだくも〜",
    "{city}は☁️くもりだくも。降るかどうか微妙だくも〜。心配なら傘持っていってね〜くも！",
]

# 雪パターン
SNOW_MESSAGES = [
    "今日の{city}は❄️雪だくも〜！傘いるよ〜くも！あったかくしてね〜くも⛄",
    "{city}は❄️雪が降りそうだくも〜！傘もマフラーもいるくも⛄",
    "さむさむ〜くも❄️ {city}は今日雪だくも！傘いるよ〜くも。すべらないように気をつけてね〜くも⛄",
    "{city}のみんな〜！❄️雪だくも〜！傘もいるし、あったかくしてお出かけしてね〜くも⛄",
]

# 締めの一言
CLOSINGS = [
    "\n\n#傘いるくん #天気 #{pref}",
    "\n\n#傘いるくん #今日の天気 #{city}",
    "\n\n#傘いるくん #{city}の天気",
]

# 天気詳細の追加文
def detail_text(precip_prob, precip_max, temp_max, temp_min):
    parts = []
    if temp_max is not None and temp_min is not None:
        parts.append(f"🌡{temp_min:.0f}℃〜{temp_max:.0f}℃")
    if precip_prob is not None:
        parts.append(f"☔{precip_prob:.0f}%")
    if parts:
        return "（" + "・".join(parts) + "）"
    return ""


def build_tweet(area_name, city_name, pref, weather_type, precip_prob=None, precip_max=None, temp_max=None, temp_min=None):
    """
    area_name: 表示名（例: "札幌市中央区"）
    city_name: 市名（例: "札幌市"）
    weather_type: "rain", "snow", "cloudy", "sunny"
    """
    greeting = random.choice(GREETINGS)
    
    if weather_type == "rain":
        body = random.choice(RAIN_MESSAGES).format(city=area_name)
    elif weather_type == "snow":
        body = random.choice(SNOW_MESSAGES).format(city=area_name)
    elif weather_type == "cloudy":
        body = random.choice(CLOUDY_MESSAGES).format(city=area_name)
    else:
        body = random.choice(SUNNY_MESSAGES).format(city=area_name)
    
    detail = detail_text(precip_prob, precip_max, temp_max, temp_min)
    
    # Clean pref name for hashtag (remove 県/府/都)
    pref_tag = pref.replace("県", "").replace("府", "").replace("都", "")
    # Clean city name for hashtag (remove 市/町/村)
    city_tag = city_name.replace("市", "").replace("町", "").replace("村", "")
    closing = random.choice(CLOSINGS).format(city=city_tag, pref=pref_tag)
    
    tweet = f"{greeting}\n{body}\n{detail}{closing}"
    
    # Ensure within 280 char limit (Japanese chars count as 2 in X's counting)
    return tweet
