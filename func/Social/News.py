import requests
import html

KEY=open("keys//news").read()

def remove_special_characters(text):
    cleaned_text = text.encode('ascii', 'ignore').decode('ascii')
    return cleaned_text

def clean_news_headlines(headlines):
    cleaned_headlines = []
    for headline in headlines:
        # Decode HTML entities
        decoded_headline = html.unescape(headline)
        # Remove unwanted phrases or words
        cleaned_headline = decoded_headline.replace('Deal Dive:', '').replace('TC+ Roundup:', '')
        # Append the cleaned headline to the list
        cleaned_headlines.append(cleaned_headline)
    return cleaned_headlines

def News()->str:
    global KEY
    main_url = f'https://newsapi.org/v2/top-headlines?sources=techcrunch&apiKey={KEY}'
    main_page = requests.get(main_url).json()
    articles = main_page["articles"]
    head = []
    day=["First","Second","Third","Fourth","Fifth","Sixth","Seventh","Eighth","Ninth","Tenth"]
    for ar in articles:
        head.append(ar["title"])
    temp=[]
    for i in range (len(day)):
        temp.append(f"{day[i]} news is: {head[i]}\n")
    temp=clean_news_headlines(temp)
    r=""
    for i in temp:
        r+=i
    return r

if __name__=="__main__":
    print(News())