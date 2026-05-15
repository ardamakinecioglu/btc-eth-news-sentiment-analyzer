import feedparser
import pandas as pd
from datetime import datetime

# BTC & ETH News Sentiment Analyzer
# A beginner-friendly rule-based sentiment analysis project

feeds = {
    "BTC": "https://cointelegraph.com/rss/tag/bitcoin",
    "ETH": "https://cointelegraph.com/rss/tag/ethereum"
}

positive_words = [
    "surge", "surges", "rise", "rises", "gain", "gains", "bullish",
    "optimism", "optimistic", "strong", "growth", "rally", "record",
    "approval", "inflow", "inflows", "upgrade", "recovery"
]

negative_words = [
    "fall", "falls", "drop", "drops", "decline", "declines", "bearish",
    "fear", "risk", "risks", "crash", "loss", "losses", "lawsuit",
    "concern", "concerns", "pressure", "uncertainty", "hack"
]


def classify_sentiment(headline):
    headline = headline.lower()

    positive_score = 0
    negative_score = 0

    for word in positive_words:
        if word in headline:
            positive_score += 1

    for word in negative_words:
        if word in headline:
            negative_score += 1

    if positive_score > negative_score:
        return "Positive"
    elif negative_score > positive_score:
        return "Negative"
    else:
        return "Neutral"


def fetch_news(coin, url):
    feed = feedparser.parse(url)
    news_rows = []

    for entry in feed.entries[:10]:
        headline = entry.title
        sentiment = classify_sentiment(headline)

        news_rows.append({
            "Coin": coin,
            "Headline": headline,
            "Sentiment": sentiment,
            "Source": "Cointelegraph",
            "Date Collected": datetime.now().strftime("%Y-%m-%d")
        })

    return news_rows


def summarize_sentiment(news_rows):
    df = pd.DataFrame(news_rows)

    summary = (
        df.groupby(["Coin", "Sentiment"])
        .size()
        .reset_index(name="Count")
    )

    summary["Percentage"] = summary.groupby("Coin")["Count"].transform(
        lambda x: round((x / x.sum()) * 100, 2)
    )

    return df, summary


all_news = []

for coin, url in feeds.items():
    coin_news = fetch_news(coin, url)
    all_news.extend(coin_news)

df_news, df_summary = summarize_sentiment(all_news)

df_news.to_csv("crypto_news_headlines.csv", index=False)
df_summary.to_csv("crypto_sentiment_summary.csv", index=False)

def print_daily_outlook(summary):
    print("\nBTC & ETH Daily News Sentiment Outlook")
    print("=" * 45)

    for coin in summary["Coin"].unique():
        coin_summary = summary[summary["Coin"] == coin]

        positive_row = coin_summary[coin_summary["Sentiment"] == "Positive"]

        if len(positive_row) > 0:
            positive_score = float(positive_row["Percentage"].iloc[0])
        else:
            positive_score = 0.0

        if positive_score >= 70:
            outlook = "Very Positive"
        elif positive_score >= 55:
            outlook = "Positive"
        elif positive_score >= 45:
            outlook = "Neutral / Positive"
        elif positive_score >= 30:
            outlook = "Neutral / Negative"
        else:
            outlook = "Negative"

        print(f"\n{coin} Market Sentiment Today")
        print("-" * 35)
        print(f"Positive Score: {positive_score:.2f}%")
        print(f"Overall Outlook: {outlook}")


print_daily_outlook(df_summary)

print("\nCSV files created successfully:")
print("- crypto_news_headlines.csv")
print("- crypto_sentiment_summary.csv")