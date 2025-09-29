# My Financial Market Mood Ring - Data Fetcher with News
import praw
import os
import datetime
import json
import feedparser
from textblob import TextBlob

print("🔮 Financial Market Mood Ring Starting...")
print(f"Analysis started at: {datetime.datetime.now()}")

# Reddit API connection - use environment variables in production
reddit = praw.Reddit(
    client_id=os.environ.get('REDDIT_CLIENT_ID', 'wqtWJt88WTOZzVHesMGuCQ'),
    client_secret=os.environ.get('REDDIT_CLIENT_SECRET', 'NfIXpUfZHmJ4UIyak0dzVspEVTfPTg'),
    user_agent="FinancialMoodRing/1.0 by /u/YourUsername"
)

print("🔗 Connected to Reddit API")

# Define subreddits to analyze
subreddits_to_analyze = [
    {'name': 'stocks', 'weight': 1.0, 'posts': 10},
    {'name': 'investing', 'weight': 1.2, 'posts': 8},
    {'name': 'options', 'weight': 0.8, 'posts': 6},
    {'name': 'ValueInvesting', 'weight': 1.1, 'posts': 5}
]

# Define RSS news sources
news_sources = [
    {'name': 'Reuters Business', 'url': 'https://feeds.reuters.com/reuters/businessNews', 'weight': 1.3},
    {'name': 'MarketWatch', 'url': 'https://feeds.marketwatch.com/marketwatch/marketpulse/', 'weight': 1.1},
    {'name': 'Yahoo Finance', 'url': 'https://feeds.finance.yahoo.com/rss/2.0/headline', 'weight': 1.0}
]

# Track sentiment across all sources
total_bullish_score = 0
total_bearish_score = 0
total_neutral_score = 0
total_posts_analyzed = 0
source_breakdown = {}

print("📊 Analyzing market sentiment across Reddit subreddits...")

# Analyze Reddit subreddits (your existing code)
for sub_config in subreddits_to_analyze:
    sub_name = sub_config['name']
    weight = sub_config['weight']
    post_limit = sub_config['posts']
    
    print(f"\n📈 Analyzing r/{sub_name} (weight: {weight})...")
    
    bullish_count = 0
    bearish_count = 0
    neutral_count = 0
    
    try:
        subreddit = reddit.subreddit(sub_name)
        
        for post in subreddit.hot(limit=post_limit):
            blob = TextBlob(post.title)
            sentiment = blob.sentiment.polarity
            
            if sentiment > 0.1:
                mood = "🐂"
                bullish_count += 1
            elif sentiment < -0.1:
                mood = "🐻"
                bearish_count += 1
            else:
                mood = "😐"
                neutral_count += 1
                
            print(f"  {mood} {sentiment:.2f} | {post.title[:50]}...")
        
        # Apply weights
        weighted_bullish = bullish_count * weight
        weighted_bearish = bearish_count * weight
        weighted_neutral = neutral_count * weight
        
        total_bullish_score += weighted_bullish
        total_bearish_score += weighted_bearish
        total_neutral_score += weighted_neutral
        total_posts_analyzed += (bullish_count + bearish_count + neutral_count)
        
        source_breakdown[f"r/{sub_name}"] = {
            'bullish': bullish_count,
            'bearish': bearish_count,
            'neutral': neutral_count,
            'total_posts': bullish_count + bearish_count + neutral_count,
            'weight': weight,
            'type': 'reddit'
        }
        
        print(f"  r/{sub_name}: {bullish_count} bullish, {bearish_count} bearish, {neutral_count} neutral")
        
    except Exception as e:
        print(f"❌ Error analyzing r/{sub_name}: {e}")

# NEW: Analyze RSS news sources
print("\n📰 Analyzing financial news headlines...")

for news_config in news_sources:
    news_name = news_config['name']
    news_url = news_config['url']
    weight = news_config['weight']
    
    print(f"\n📰 Analyzing {news_name} (weight: {weight})...")
    
    bullish_count = 0
    bearish_count = 0
    neutral_count = 0
    
    try:
        # Parse RSS feed
        feed = feedparser.parse(news_url)
        
        # Analyze up to 10 recent headlines
        for entry in feed.entries[:10]:
            headline = entry.title
            blob = TextBlob(headline)
            sentiment = blob.sentiment.polarity
            
            if sentiment > 0.1:
                mood = "🐂"
                bullish_count += 1
            elif sentiment < -0.1:
                mood = "🐻"
                bearish_count += 1
            else:
                mood = "😐"
                neutral_count += 1
                
            print(f"  {mood} {sentiment:.2f} | {headline[:50]}...")
        
        # Apply weights
        weighted_bullish = bullish_count * weight
        weighted_bearish = bearish_count * weight
        weighted_neutral = neutral_count * weight
        
        total_bullish_score += weighted_bullish
        total_bearish_score += weighted_bearish
        total_neutral_score += weighted_neutral
        total_posts_analyzed += (bullish_count + bearish_count + neutral_count)
        
        source_breakdown[news_name] = {
            'bullish': bullish_count,
            'bearish': bearish_count,
            'neutral': neutral_count,
            'total_posts': bullish_count + bearish_count + neutral_count,
            'weight': weight,
            'type': 'news'
        }
        
        print(f"  {news_name}: {bullish_count} bullish, {bearish_count} bearish, {neutral_count} neutral")
        
    except Exception as e:
        print(f"❌ Error analyzing {news_name}: {e}")

# Calculate final weighted sentiment
total_weighted_score = total_bullish_score + total_bearish_score + total_neutral_score

if total_weighted_score > 0:
    bullish_pct = round((total_bullish_score / total_weighted_score) * 100, 1)
    bearish_pct = round((total_bearish_score / total_weighted_score) * 100, 1)
    neutral_pct = round((total_neutral_score / total_weighted_score) * 100, 1)
else:
    bullish_pct = bearish_pct = neutral_pct = 0

print(f"\n🎯 COMBINED SENTIMENT ANALYSIS:")
print(f"📊 Total headlines/posts analyzed: {total_posts_analyzed}")
print(f"🐂 Bullish: {bullish_pct}%")
print(f"🐻 Bearish: {bearish_pct}%")
print(f"😐 Neutral: {neutral_pct}%")

# Determine overall sentiment
if total_bullish_score > total_bearish_score:
    overall_sentiment = "bullish"
    print("📈 Overall Market Mood: BULLISH")
elif total_bearish_score > total_bullish_score:
    overall_sentiment = "bearish"
    print("📉 Overall Market Mood: BEARISH")
else:
    overall_sentiment = "neutral"
    print("📊 Overall Market Mood: MIXED")

# Save enhanced data with news sources
sentiment_data = {
    "sentiment": overall_sentiment,
    "bullish_percent": bullish_pct,
    "bearish_percent": bearish_pct,
    "neutral_percent": neutral_pct,
    "last_updated": datetime.datetime.now().isoformat(),
    "total_posts": total_posts_analyzed,
    "source_breakdown": source_breakdown,
    "data_sources": {
        "reddit": [sub['name'] for sub in subreddits_to_analyze],
        "news": [news['name'] for news in news_sources]
    }
}

with open('sentiment_data.json', 'w') as f:
    json.dump(sentiment_data, f, indent=2)

print(f"💾 Enhanced sentiment data with news sources saved to sentiment_data.json")