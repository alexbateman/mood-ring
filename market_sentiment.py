# My Financial Market Mood Ring - Data Fetcher
import praw
import datetime
from textblob import TextBlob

print("🔮 Financial Market Mood Ring Starting...")
print(f"Analysis started at: {datetime.datetime.now()}")

# Reddit API connection
reddit = praw.Reddit(
    client_id="wqtWJt88WTOZzVHesMGuCQ",
    client_secret="NfIXpUfZHmJ4UIyak0dzVspEVTfPTg",
    user_agent="FinancialMoodRing/1.0 by /u/YourUsername"
)

print("🔗 Connected to Reddit API")

# Sentiment tracking
bullish_count = 0
bearish_count = 0
neutral_count = 0

print("📊 Analyzing market sentiment from r/stocks...")

try:
    subreddit = reddit.subreddit("stocks")
    
    for post in subreddit.hot(limit=10):
        # Analyze sentiment of the title
        blob = TextBlob(post.title)
        sentiment = blob.sentiment.polarity  # -1 (negative) to 1 (positive)
        
        if sentiment > 0.1:
            mood = "🐂 BULLISH"
            bullish_count += 1
        elif sentiment < -0.1:
            mood = "🐻 BEARISH" 
            bearish_count += 1
        else:
            mood = "😐 NEUTRAL"
            neutral_count += 1
            
        print(f"{mood} | {sentiment:.2f} | {post.title[:60]}...")
        
except Exception as e:
    print(f"❌ Error: {e}")

# Calculate overall market mood
total_posts = bullish_count + bearish_count + neutral_count
print("\n🎯 MARKET MOOD SUMMARY:")
print(f"🐂 Bullish: {bullish_count}/{total_posts} ({bullish_count/total_posts*100:.1f}%)")
print(f"🐻 Bearish: {bearish_count}/{total_posts} ({bearish_count/total_posts*100:.1f}%)")
print(f"😐 Neutral: {neutral_count}/{total_posts} ({neutral_count/total_posts*100:.1f}%)")

if bullish_count > bearish_count:
    print("📈 Overall Market Mood: BULLISH")
elif bearish_count > bullish_count:
    print("📉 Overall Market Mood: BEARISH")
else:
    print("📊 Overall Market Mood: MIXED")