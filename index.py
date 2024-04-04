import requests
import json
import time
from bs4 import BeautifulSoup

headers = {
    "Content-Type": "application/json",
    "X-Csrf-Token": "khdxFrMYQERKNwyeL1g5VXHMNZXV7aBZHM1y3xFN",
    "Cookie": "amp_af43d4=0fb8919b7a9646cca184dead6ff390e5...1hq5s3qgb.1hq5s3qgf.1.1.2; intercom-id-gpfdrxfd=7b7a34d9-34e5-46cd-9008-f0307f08e4d4; intercom-session-gpfdrxfd=; intercom-device-id-gpfdrxfd=e4e97269-6779-440a-b930-b4b16121a0bd; laravel_session=T8M9EDF58nRrsvQQqbtF0S2g7SdVXXPdfPbZ6h0w",
    "Origin": "https://anilist.co",
    "Referer": "https://anilist.co/search/anime?genres=Action",
    "Sec-Ch-Ua": '"Google Chrome";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
    "Sec-Ch-Ua-Mobile": "?0",
    "Sec-Ch-Ua-Platform": "Windows",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'
}

def getBody(page, genre): 
    return {
        "query": "query($page:Int = 1 $id:Int $type:MediaType $isAdult:Boolean = false $search:String $format:[MediaFormat]$status:MediaStatus $countryOfOrigin:CountryCode $source:MediaSource $season:MediaSeason $seasonYear:Int $year:String $onList:Boolean $yearLesser:FuzzyDateInt $yearGreater:FuzzyDateInt $episodeLesser:Int $episodeGreater:Int $durationLesser:Int $durationGreater:Int $chapterLesser:Int $chapterGreater:Int $volumeLesser:Int $volumeGreater:Int $licensedBy:[Int]$isLicensed:Boolean $genres:[String]$excludedGenres:[String]$tags:[String]$excludedTags:[String]$minimumTagRank:Int $sort:[MediaSort]=[POPULARITY_DESC,SCORE_DESC]){Page(page:$page,perPage:50){pageInfo{total perPage currentPage lastPage hasNextPage}media(id:$id type:$type season:$season format_in:$format status:$status countryOfOrigin:$countryOfOrigin source:$source search:$search onList:$onList seasonYear:$seasonYear startDate_like:$year startDate_lesser:$yearLesser startDate_greater:$yearGreater episodes_lesser:$episodeLesser episodes_greater:$episodeGreater duration_lesser:$durationLesser duration_greater:$durationGreater chapters_lesser:$chapterLesser chapters_greater:$chapterGreater volumes_lesser:$volumeLesser volumes_greater:$volumeGreater licensedById_in:$licensedBy isLicensed:$isLicensed genre_in:$genres genre_not_in:$excludedGenres tag_in:$tags tag_not_in:$excludedTags minimumTagRank:$minimumTagRank sort:$sort isAdult:$isAdult){id title{userPreferred}coverImage{extraLarge large color}startDate{year month day}endDate{year month day}bannerImage season seasonYear description type format status(version:2)episodes duration chapters volumes genres isAdult averageScore popularity nextAiringEpisode{airingAt timeUntilAiring episode}mediaListEntry{id status}studios(isMain:true){edges{isMain node{id name}}}}}}",
        "variables": {
            "page": page,
            "type": "ANIME",
            "genres": [genre]
        }
    }

finishedGenres = [
    { 'Action': 95 },
    { 'Adventure': 71 },
    { 'Comedy': 130 },
    { 'Drama': 61 },
    { 'Ecchi': 19 },
    { 'Fantasy': 84 },
    { 'Horror': 10 },
    { 'Mecha': 23 },
    { 'Music': 17 },
    { 'Mystery': 18 },
    { 'Psychological': 18 },
    { 'Romance': 47 },
    { 'Sports': 17 },
    { 'Mahou Shoujo': 9 },
    { 'Thriller': 5 },
    { 'Sci-Fi': 56 },
]

genres = [
    { 'Slice of Life': 52 },
    { 'Supernatural': 33 },
]
    
def getAniCoData(body):
    url = 'https://anilist.co/graphql'
    response = requests.post(url, json=body, headers=headers)
    parsed = response.json()

    try:
        data = parsed['data']['Page']['media']
    except Exception as ex:
        print(ex)
        print(parsed['data'])
        return False

    file_path = "data8.json"
    with open(file_path, 'a') as json_file:
        json.dump(data, json_file, indent=4)

    return True


for genre in genres:
    for genrePage in genre:
        for pageNum in range(1, genre[genrePage] + 1):
            body = getBody(pageNum, genrePage)
            response = getAniCoData(body)

            while response is False:
                print('Retrying...')
                response = getAniCoData(body)
                time.sleep(5.0)

            print(f'Finished: Genre: {genrePage} Page: {pageNum}')
            time.sleep(5.0)
