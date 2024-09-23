import time

def rate_limit():
    print("Rate limit reached, pausing for a while...")
    time.sleep(60)
# Implements rate limiting to avoid hitting API limits.