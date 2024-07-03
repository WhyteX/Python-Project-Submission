import requests
import warnings
import pandas as pd
import pycountry
import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.toast import ToastNotification

warnings.filterwarnings('ignore')

genres_dict = {'Genre':['Science-Fiction','Romance','Comedy','Crime','History','Kids & Family','Music & Musical','Animation','Documentary','Western','Made in Europe','Sport','War & Military','Reality TV','Action & Adventure','Drama','Fantasy','Horror','Mistery & Thriller'],
               'Abreviation':['scf','rma','cmy','crm','hst','fml','msc','ani','doc','wsn','eur','spt','war','rly','act','drm','fnt','hrr','trl']}

headers = {'content-type':'application/json',
            'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0',
            'Accept':'*/*'}


def get_country_name(abbreviation):
    try:
        country = pycountry.countries.get(alpha_2=abbreviation)
        return country.name if country else None
    except Exception as e:
        print(f"Error: {e}")
        return None

def userInputList(list_name,genre_country):
        
    start_index = 1
    for item in list_name:
        print(f'{start_index}. {item}')
        start_index +=1
    
    while True:
        try:
            if genre_country == 'country':
                user_input = input('Welcome! To enhance your experience, please choose a popular movie from a specific country. Select a country from the options above: ')
            elif genre_country == 'genre':
                user_input = input('Choose the number corresponding to the categories above: ') 
            
            if int(user_input) != 0 and int(user_input) in list(range(len(list_name)+1)):
                movie_picked = int(user_input)-1
                break
            
            else:
                if genre_country == 'country':
                    print('The number is either incorrect or you have inputed the name of the country, please try again')
                elif genre_country == 'genre':
                    print("The number is either incorrect or you have inputed the name of the genre, please try again")
                
   
        except:
            if genre_country == 'country':
                print('The number is either incorrect or you have inputed the name of the country, please try again')
            elif genre_country == 'genre':
                print("The number is either incorrect or you have inputed the name of the genre, please try again")
            

    return movie_picked
            
def getCountriesList():
    countries = {'Country':[],'Abreviation':[],'Language':[]}

    url = 'https://apis.justwatch.com/content/urls?path=/us'

    res = requests.get(url,headers=headers)

    for item in res.json()['href_lang_tags']:
        country_name = get_country_name((str(item['locale']).split("_"))[1])
        if country_name != None:
            countries['Country'].append(country_name)
            countries['Abreviation'].append((str(item['locale']).split("_"))[1])
            countries['Language'].append((str(item['locale']).split("_"))[0])

    return countries

def justwatchGetMovies(country,index,language,genre):
    url = "https://apis.justwatch.com/graphql"

 

    json_data = {"operationName":"GetPopularTitles",
                "variables":{"first":100,
                            "offset": index,
                            "platform":"WEB",
                            "popularTitlesSortBy":"POPULAR",
                            "sortRandomSeed":0,
                            "creditsRole":"DIRECTOR",
                            "popularTitlesFilter":{"ageCertifications":[],
                                                    "excludeGenres":[],
                                                    "excludeProductionCountries":[],
                                                    "objectTypes":["MOVIE"],
                                                    "productionCountries":[],
                                                    "subgenres":[],
                                                    "genres":[f"{genre}"],
                                                    "packages":["nfx","prv"],
                                                    "excludeIrrelevantTitles":False,
                                                    "presentationTypes":[],
                                                    "monetizationTypes":[],
                                                    "searchQuery":""},
                            "watchNowFilter":{"packages":["nfx","prv"],
                                                "monetizationTypes":[]},
                            "language":f"{language}",
                            "country":f"{country}",
                            "allowSponsoredRecommendations":{"pageType":"VIEW_POPULAR",
                                                            "placement":"POPULAR_VIEW",
                                                            "language":f"{language}",
                                                            "country":f"{country}",
                                                            "appId":"3.8.2-webapp#8b4e6a0",
                                                            "platform":"WEB",
                                                            "supportedFormats":["IMAGE","VIDEO"],
                                                            "supportedObjectTypes":["MOVIE","SHOW","GENERIC_TITLE_LIST","SHOW_SEASON"],
                                                            "testingMode":False,}},
                "query":"query GetPopularTitles($allowSponsoredRecommendations: SponsoredRecommendationsInput, $backdropProfile: BackdropProfile, $country: Country!, $first: Int! = 70, $format: ImageFormat, $language: Language!, $platform: Platform! = WEB, $after: String, $popularTitlesFilter: TitleFilter, $popularTitlesSortBy: PopularTitlesSorting! = POPULAR, $profile: PosterProfile, $sortRandomSeed: Int! = 0, $watchNowFilter: WatchNowOfferFilter!, $offset: Int = 0, $creditsRole: CreditRole! = DIRECTOR) {\n  popularTitles(\n    allowSponsoredRecommendations: $allowSponsoredRecommendations\n    country: $country\n    filter: $popularTitlesFilter\n    first: $first\n    sortBy: $popularTitlesSortBy\n    sortRandomSeed: $sortRandomSeed\n    offset: $offset\n    after: $after\n  ) {\n    __typename\n    edges {\n      cursor\n      node {\n        ...PopularTitleGraphql\n        __typename\n      }\n      __typename\n    }\n    pageInfo {\n      startCursor\n      endCursor\n      hasPreviousPage\n      hasNextPage\n      __typename\n    }\n    sponsoredAd {\n      ...SponsoredAd\n      __typename\n    }\n    totalCount\n  }\n}\n\nfragment PopularTitleGraphql on MovieOrShow {\n  id\n  objectId\n  objectType\n  content(country: $country, language: $language) {\n    title\n    fullPath\n    scoring {\n      imdbVotes\n      imdbScore\n      tmdbPopularity\n      tmdbScore\n      __typename\n    }\n    dailymotionClips: clips(providers: [DAILYMOTION]) {\n      sourceUrl\n      externalId\n      provider\n      __typename\n    }\n    posterUrl(profile: $profile, format: $format)\n    ... on MovieOrShowOrSeasonContent {\n      backdrops(profile: $backdropProfile, format: $format) {\n        backdropUrl\n        __typename\n      }\n      __typename\n    }\n    isReleased\n    credits(role: $creditsRole) {\n      name\n      personId\n      __typename\n    }\n    scoring {\n      imdbVotes\n      __typename\n    }\n    runtime\n    genres {\n      translation(language: $language)\n      shortName\n      __typename\n    }\n    __typename\n  }\n  likelistEntry {\n    createdAt\n    __typename\n  }\n  dislikelistEntry {\n    createdAt\n    __typename\n  }\n  watchlistEntryV2 {\n    createdAt\n    __typename\n  }\n  customlistEntries {\n    createdAt\n    __typename\n  }\n  freeOffersCount: offerCount(\n    country: $country\n    platform: WEB\n    filter: {monetizationTypes: [FREE, ADS]}\n  )\n  watchNowOffer(country: $country, platform: WEB, filter: $watchNowFilter) {\n    id\n    standardWebURL\n    package {\n      id\n      packageId\n      clearName\n      __typename\n    }\n    retailPrice(language: $language)\n    retailPriceValue\n    lastChangeRetailPriceValue\n    currency\n    presentationType\n    monetizationType\n    availableTo\n    __typename\n  }\n  ... on Movie {\n    seenlistEntry {\n      createdAt\n      __typename\n    }\n    __typename\n  }\n  ... on Show {\n    tvShowTrackingEntry {\n      createdAt\n      __typename\n    }\n    seenState(country: $country) {\n      seenEpisodeCount\n      progress\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n\nfragment SponsoredAd on SponsoredRecommendationAd {\n  bidId\n  holdoutGroup\n  campaign {\n    name\n    externalTrackers {\n      type\n      data\n      __typename\n    }\n    hideRatings\n    hideDetailPageButton\n    promotionalImageUrl\n    promotionalVideo {\n      url\n      __typename\n    }\n    promotionalTitle\n    promotionalText\n    promotionalProviderLogo\n    watchNowLabel\n    watchNowOffer {\n      standardWebURL\n      presentationType\n      monetizationType\n      package {\n        id\n        packageId\n        shortName\n        clearName\n        icon\n        __typename\n      }\n      __typename\n    }\n    nodeOverrides {\n      nodeId\n      promotionalImageUrl\n      watchNowOffer {\n        standardWebURL\n        __typename\n      }\n      __typename\n    }\n    node {\n      nodeId: id\n      __typename\n      ... on MovieOrShowOrSeason {\n        content(country: $country, language: $language) {\n          fullPath\n          posterUrl\n          title\n          originalReleaseYear\n          scoring {\n            imdbScore\n            __typename\n          }\n          externalIds {\n            imdbId\n            __typename\n          }\n          backdrops(format: $format, profile: $backdropProfile) {\n            backdropUrl\n            __typename\n          }\n          isReleased\n          __typename\n        }\n        objectId\n        objectType\n        offers(country: $country, platform: $platform) {\n          monetizationType\n          presentationType\n          package {\n            id\n            packageId\n            __typename\n          }\n          id\n          __typename\n        }\n        __typename\n      }\n      ... on MovieOrShow {\n        watchlistEntryV2 {\n          createdAt\n          __typename\n        }\n        __typename\n      }\n      ... on Show {\n        seenState(country: $country) {\n          seenEpisodeCount\n          __typename\n        }\n        __typename\n      }\n      ... on Season {\n        content(country: $country, language: $language) {\n          seasonNumber\n          __typename\n        }\n        show {\n          __typename\n          id\n          content(country: $country, language: $language) {\n            originalTitle\n            __typename\n          }\n          watchlistEntryV2 {\n            createdAt\n            __typename\n          }\n        }\n        __typename\n      }\n      ... on GenericTitleList {\n        followedlistEntry {\n          createdAt\n          name\n          __typename\n        }\n        id\n        type\n        content(country: $country, language: $language) {\n          name\n          visibility\n          __typename\n        }\n        titles(country: $country, first: 40) {\n          totalCount\n          edges {\n            cursor\n            node: nodeV2 {\n              content(country: $country, language: $language) {\n                fullPath\n                posterUrl\n                title\n                originalReleaseYear\n                scoring {\n                  imdbScore\n                  __typename\n                }\n                isReleased\n                __typename\n              }\n              id\n              objectId\n              objectType\n              __typename\n            }\n            __typename\n          }\n          __typename\n        }\n        __typename\n      }\n    }\n    __typename\n  }\n  __typename\n}\n"}

    response = requests.post(url, headers=headers,json=json_data)
    return response.json()
    
def GetFullMoviesList(country,language,genre):  
    
    start_index = 0
    
    movies_list = {'Movie Name':[],'ID':[],'Full Path':[]}
    
    while True:

        data_content = justwatchGetMovies(country,start_index,language,genre)
        
        next_page_bool = data_content['data']['popularTitles']['pageInfo']['hasNextPage']
        
        movies_per_page = data_content['data']['popularTitles']['edges']
        
        for movie in movies_per_page:
            movie_title = movie['node']['content']['title']
            movie_fullpath = movie['node']['content']['fullPath']
            movie_id = movie['node']['id']
            if movie_fullpath == '':
                movies_list['Full Path'].append(movie_fullpath)
            else: 
                movies_list['Full Path'].append(f"{country}/movies")   
            movies_list['Movie Name'].append(movie_title)
            movies_list['ID'].append(movie_id)

            
        start_index += 100

        if next_page_bool == False:
            break
            
    return movies_list
 
def juswatchGetMovieItems(movie_name_full_path,country,language,movie_id):
    
    movie_recommendation_attributes = ['title','originalReleaseYear','shortDescription','runtime']
    movie_recommendation_items = []
    
    url = 'https://apis.justwatch.com/graphql'
    
    json_data = {
        "operationName": "GetNodeTitleDetails",
        "variables": {
            "platform": "WEB",
            "fullPath": f"{movie_name_full_path}",
            "entityId": f"{movie_id}",
            "language": f"{language}",
            "country": f"{country}",
            "episodeMaxLimit": 20,
            "allowSponsoredRecommendations": {
                "pageType": "VIEW_TITLE_DETAIL",
                "placement": "DETAIL_PAGE",
                "language": f"{language}",
                "country": f"{country}",
                "appId": "3.8.2-webapp#fef05e2",
                "platform": "WEB",
                "supportedFormats": [
                    "IMAGE",
                    "VIDEO"
                ],
                "supportedObjectTypes": [
                    "MOVIE",
                    "SHOW",
                    "GENERIC_TITLE_LIST",
                    "SHOW_SEASON"
                ],
                "testingMode": False}},
        "query": "query GetNodeTitleDetails($entityId: ID!, $country: Country!, $language: Language!, $episodeMaxLimit: Int, $platform: Platform! = WEB, $allowSponsoredRecommendations: SponsoredRecommendationsInput, $format: ImageFormat, $backdropProfile: BackdropProfile, $streamingChartsFilter: StreamingChartsFilter) {\n  node(id: $entityId) {\n    ... on Url {\n      metaDescription\n      metaKeywords\n      metaRobots\n      metaTitle\n      heading1\n      heading2\n      htmlContent\n      __typename\n    }\n    ...TitleDetails\n    __typename\n  }\n}\n\nfragment TitleDetails on Node {\n  id\n  __typename\n  ... on MovieOrShowOrSeason {\n    plexPlayerOffers: offers(\n      country: $country\n      platform: $platform\n      filter: {packages: [\"pxp\"]}\n    ) {\n      id\n      standardWebURL\n      package {\n        id\n        packageId\n        clearName\n        technicalName\n        shortName\n        __typename\n      }\n      __typename\n    }\n    maxOfferUpdatedAt(country: $country, platform: WEB)\n    appleOffers: offers(\n      country: $country\n      platform: $platform\n      filter: {packages: [\"atp\", \"itu\"]}\n    ) {\n      ...TitleOffer\n      __typename\n    }\n    disneyOffersCount: offerCount(\n      country: $country\n      platform: $platform\n      filter: {packages: [\"dnp\"]}\n    )\n    starOffersCount: offerCount(\n      country: $country\n      platform: $platform\n      filter: {packages: [\"srp\"]}\n    )\n    objectType\n    objectId\n    offerCount(country: $country, platform: $platform)\n    uniqueOfferCount: offerCount(\n      country: $country\n      platform: $platform\n      filter: {bestOnly: true}\n    )\n    offers(country: $country, platform: $platform) {\n      monetizationType\n      elementCount\n      package {\n        id\n        packageId\n        clearName\n        __typename\n      }\n      __typename\n    }\n    watchNowOffer(country: $country, platform: $platform) {\n      id\n      standardWebURL\n      __typename\n    }\n    promotedBundles(country: $country, platform: $platform) {\n      promotionUrl\n      __typename\n    }\n    availableTo(country: $country, platform: $platform) {\n      availableCountDown(country: $country)\n      availableToDate\n      package {\n        id\n        shortName\n        __typename\n      }\n      __typename\n    }\n    fallBackClips: content(country: \"US\", language: \"en\") {\n      videobusterClips: clips(providers: [VIDEOBUSTER]) {\n        ...TrailerClips\n        __typename\n      }\n      dailymotionClips: clips(providers: [DAILYMOTION]) {\n        ...TrailerClips\n        __typename\n      }\n      __typename\n    }\n    content(country: $country, language: $language) {\n      backdrops {\n        backdropUrl\n        __typename\n      }\n      fullBackdrops: backdrops(profile: S1920, format: JPG) {\n        backdropUrl\n        __typename\n      }\n      clips {\n        ...TrailerClips\n        __typename\n      }\n      videobusterClips: clips(providers: [VIDEOBUSTER]) {\n        ...TrailerClips\n        __typename\n      }\n      dailymotionClips: clips(providers: [DAILYMOTION]) {\n        ...TrailerClips\n        __typename\n      }\n      externalIds {\n        imdbId\n        __typename\n      }\n      fullPath\n      posterUrl\n      fullPosterUrl: posterUrl(profile: S718, format: JPG)\n      runtime\n      isReleased\n      scoring {\n        imdbScore\n        imdbVotes\n        tmdbPopularity\n        tmdbScore\n        jwRating\n        __typename\n      }\n      shortDescription\n      title\n      originalReleaseYear\n      originalReleaseDate\n      upcomingReleases(releaseTypes: DIGITAL) {\n        releaseCountDown(country: $country)\n        releaseDate\n        label\n        package {\n          id\n          packageId\n          shortName\n          clearName\n          __typename\n        }\n        __typename\n      }\n      genres {\n        shortName\n        translation(language: $language)\n        __typename\n      }\n      subgenres {\n        content(country: $country, language: $language) {\n          shortName\n          name\n          __typename\n        }\n        __typename\n      }\n      ... on MovieContent {\n        subgenres {\n          content(country: $country, language: $language) {\n            url: moviesUrl {\n              fullPath\n              __typename\n            }\n            __typename\n          }\n          __typename\n        }\n        __typename\n      }\n      ... on ShowContent {\n        subgenres {\n          content(country: $country, language: $language) {\n            url: showsUrl {\n              fullPath\n              __typename\n            }\n            __typename\n          }\n          __typename\n        }\n        __typename\n      }\n      ... on SeasonContent {\n        subgenres {\n          content(country: $country, language: $language) {\n            url: showsUrl {\n              fullPath\n              __typename\n            }\n            __typename\n          }\n          __typename\n        }\n        __typename\n      }\n      ... on MovieOrShowContent {\n        originalTitle\n        ageCertification\n        credits {\n          role\n          name\n          characterName\n          personId\n          __typename\n        }\n        interactions {\n          dislikelistAdditions\n          likelistAdditions\n          votesNumber\n          __typename\n        }\n        productionCountries\n        __typename\n      }\n      ... on SeasonContent {\n        seasonNumber\n        interactions {\n          dislikelistAdditions\n          likelistAdditions\n          votesNumber\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    popularityRank(country: $country) {\n      rank\n      trend\n      trendDifference\n      __typename\n    }\n    streamingCharts(country: $country, filter: $streamingChartsFilter) {\n      edges {\n        streamingChartInfo {\n          rank\n          trend\n          trendDifference\n          updatedAt\n          daysInTop10\n          daysInTop100\n          daysInTop1000\n          daysInTop3\n          topRank\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n  ... on MovieOrShow {\n    watchlistEntryV2 {\n      createdAt\n      __typename\n    }\n    likelistEntry {\n      createdAt\n      __typename\n    }\n    dislikelistEntry {\n      createdAt\n      __typename\n    }\n    customlistEntries {\n      createdAt\n      genericTitleList {\n        id\n        __typename\n      }\n      __typename\n    }\n    similarTitlesV2(\n      country: $country\n      allowSponsoredRecommendations: $allowSponsoredRecommendations\n    ) {\n      sponsoredAd {\n        ...SponsoredAd\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n  ... on Movie {\n    permanentAudiences\n    seenlistEntry {\n      createdAt\n      __typename\n    }\n    __typename\n  }\n  ... on Show {\n    permanentAudiences\n    totalSeasonCount\n    seenState(country: $country) {\n      progress\n      seenEpisodeCount\n      __typename\n    }\n    tvShowTrackingEntry {\n      createdAt\n      __typename\n    }\n    seasons(sortDirection: DESC) {\n      id\n      objectId\n      objectType\n      totalEpisodeCount\n      availableTo(country: $country, platform: $platform) {\n        availableToDate\n        availableCountDown(country: $country)\n        package {\n          id\n          shortName\n          __typename\n        }\n        __typename\n      }\n      content(country: $country, language: $language) {\n        posterUrl\n        seasonNumber\n        fullPath\n        title\n        upcomingReleases(releaseTypes: DIGITAL) {\n          releaseDate\n          releaseCountDown(country: $country)\n          package {\n            id\n            shortName\n            __typename\n          }\n          __typename\n        }\n        isReleased\n        originalReleaseYear\n        __typename\n      }\n      show {\n        id\n        objectId\n        objectType\n        watchlistEntryV2 {\n          createdAt\n          __typename\n        }\n        content(country: $country, language: $language) {\n          title\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    recentEpisodes: episodes(\n      sortDirection: DESC\n      limit: 3\n      releasedInCountry: $country\n    ) {\n      ...Episode\n      __typename\n    }\n    __typename\n  }\n  ... on Season {\n    totalEpisodeCount\n    episodes(limit: $episodeMaxLimit) {\n      ...Episode\n      __typename\n    }\n    show {\n      id\n      objectId\n      objectType\n      totalSeasonCount\n      customlistEntries {\n        createdAt\n        genericTitleList {\n          id\n          __typename\n        }\n        __typename\n      }\n      tvShowTrackingEntry {\n        createdAt\n        __typename\n      }\n      fallBackClips: content(country: \"US\", language: \"en\") {\n        videobusterClips: clips(providers: [VIDEOBUSTER]) {\n          ...TrailerClips\n          __typename\n        }\n        dailymotionClips: clips(providers: [DAILYMOTION]) {\n          ...TrailerClips\n          __typename\n        }\n        __typename\n      }\n      content(country: $country, language: $language) {\n        title\n        ageCertification\n        fullPath\n        genres {\n          shortName\n          __typename\n        }\n        credits {\n          role\n          name\n          characterName\n          personId\n          __typename\n        }\n        productionCountries\n        externalIds {\n          imdbId\n          __typename\n        }\n        upcomingReleases(releaseTypes: DIGITAL) {\n          releaseDate\n          __typename\n        }\n        backdrops {\n          backdropUrl\n          __typename\n        }\n        posterUrl\n        isReleased\n        videobusterClips: clips(providers: [VIDEOBUSTER]) {\n          ...TrailerClips\n          __typename\n        }\n        dailymotionClips: clips(providers: [DAILYMOTION]) {\n          ...TrailerClips\n          __typename\n        }\n        __typename\n      }\n      seenState(country: $country) {\n        progress\n        __typename\n      }\n      watchlistEntryV2 {\n        createdAt\n        __typename\n      }\n      dislikelistEntry {\n        createdAt\n        __typename\n      }\n      likelistEntry {\n        createdAt\n        __typename\n      }\n      similarTitlesV2(\n        country: $country\n        allowSponsoredRecommendations: $allowSponsoredRecommendations\n      ) {\n        sponsoredAd {\n          ...SponsoredAd\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    seenState(country: $country) {\n      progress\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment TitleOffer on Offer {\n  id\n  presentationType\n  monetizationType\n  retailPrice(language: $language)\n  retailPriceValue\n  currency\n  lastChangeRetailPriceValue\n  type\n  package {\n    id\n    packageId\n    clearName\n    technicalName\n    icon(profile: S100)\n    planOffers(country: $country, platform: WEB) {\n      title\n      retailPrice(language: $language)\n      isTrial\n      durationDays\n      __typename\n    }\n    __typename\n  }\n  standardWebURL\n  elementCount\n  availableTo\n  deeplinkRoku: deeplinkURL(platform: ROKU_OS)\n  subtitleLanguages\n  videoTechnology\n  audioTechnology\n  audioLanguages(language: $language)\n  __typename\n}\n\nfragment TrailerClips on Clip {\n  sourceUrl\n  externalId\n  provider\n  name\n  __typename\n}\n\nfragment SponsoredAd on SponsoredRecommendationAd {\n  bidId\n  holdoutGroup\n  campaign {\n    name\n    externalTrackers {\n      type\n      data\n      __typename\n    }\n    hideRatings\n    hideDetailPageButton\n    promotionalImageUrl\n    promotionalVideo {\n      url\n      __typename\n    }\n    promotionalTitle\n    promotionalText\n    promotionalProviderLogo\n    watchNowLabel\n    watchNowOffer {\n      standardWebURL\n      presentationType\n      monetizationType\n      package {\n        id\n        packageId\n        shortName\n        clearName\n        icon\n        __typename\n      }\n      __typename\n    }\n    nodeOverrides {\n      nodeId\n      promotionalImageUrl\n      watchNowOffer {\n        standardWebURL\n        __typename\n      }\n      __typename\n    }\n    node {\n      nodeId: id\n      __typename\n      ... on MovieOrShowOrSeason {\n        content(country: $country, language: $language) {\n          fullPath\n          posterUrl\n          title\n          originalReleaseYear\n          scoring {\n            imdbScore\n            __typename\n          }\n          externalIds {\n            imdbId\n            __typename\n          }\n          backdrops(format: $format, profile: $backdropProfile) {\n            backdropUrl\n            __typename\n          }\n          isReleased\n          __typename\n        }\n        objectId\n        objectType\n        offers(country: $country, platform: $platform) {\n          monetizationType\n          presentationType\n          package {\n            id\n            packageId\n            __typename\n          }\n          id\n          __typename\n        }\n        __typename\n      }\n      ... on MovieOrShow {\n        watchlistEntryV2 {\n          createdAt\n          __typename\n        }\n        __typename\n      }\n      ... on Show {\n        seenState(country: $country) {\n          seenEpisodeCount\n          __typename\n        }\n        __typename\n      }\n      ... on Season {\n        content(country: $country, language: $language) {\n          seasonNumber\n          __typename\n        }\n        show {\n          __typename\n          id\n          content(country: $country, language: $language) {\n            originalTitle\n            __typename\n          }\n          watchlistEntryV2 {\n            createdAt\n            __typename\n          }\n        }\n        __typename\n      }\n      ... on GenericTitleList {\n        followedlistEntry {\n          createdAt\n          name\n          __typename\n        }\n        id\n        type\n        content(country: $country, language: $language) {\n          name\n          visibility\n          __typename\n        }\n        titles(country: $country, first: 40) {\n          totalCount\n          edges {\n            cursor\n            node: nodeV2 {\n              content(country: $country, language: $language) {\n                fullPath\n                posterUrl\n                title\n                originalReleaseYear\n                scoring {\n                  imdbScore\n                  __typename\n                }\n                isReleased\n                __typename\n              }\n              id\n              objectId\n              objectType\n              __typename\n            }\n            __typename\n          }\n          __typename\n        }\n        __typename\n      }\n    }\n    __typename\n  }\n  __typename\n}\n\nfragment Episode on Episode {\n  id\n  objectId\n  seenlistEntry {\n    createdAt\n    __typename\n  }\n  content(country: $country, language: $language) {\n    title\n    shortDescription\n    episodeNumber\n    seasonNumber\n    isReleased\n    runtime\n    upcomingReleases {\n      releaseDate\n      label\n      package {\n        id\n        packageId\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n"
    }
    
    response = requests.post(url,headers=headers,json=json_data)
    
    for attribute in movie_recommendation_attributes:
        movie_recommendation_items.append(response.json()['data']['node']['content'][attribute])
        
    recommendation_name = f'The Movie picked for you is: {movie_recommendation_items[0]}\nReleased year: {movie_recommendation_items[1]}\nShort Description: {movie_recommendation_items[2]}\nRuntime: {int(movie_recommendation_items[3])//60}h{int(movie_recommendation_items[3]) % 60}min'
    
    return recommendation_name, movie_recommendation_items[0]

def returnMovie():
    
    global watched_df_value
    global watched_movies

    try:
        watched_movies = pd.read_csv('Wacthed Movies.txt',delimiter='\t')  
    except:
        watched_movies = pd.DataFrame({'Country':[],'Movie Name':[],'ID':[]}) 
        
    country_data = [
        {
            'Country': countries_dict['Country'][i],
            'Abreviation': countries_dict['Abreviation'][i],
            'Language': countries_dict['Language'][i],
        }
        for i in range(len(countries_dict['Country']))
    ]

    def attributeByKey(country_name, attribute):
        for key_item in country_data:
            if key_item['Country'] == country_name:
                return key_item.get(attribute, None)
        return None

    country_selected = country_var.get()
    language_selected = attributeByKey(country_selected,'Language')
    abreviation_selected = attributeByKey(country_selected,'Abreviation')


    genre_by_name = dict(zip(genres_dict['Genre'], genres_dict['Abreviation']))
    genre_abr_selected = genre_by_name.get(genre_var.get(), None)


    dict_full_movies = GetFullMoviesList(abreviation_selected,language_selected,genre_abr_selected)

    df = pd.DataFrame(dict_full_movies)
    df = df[~df['ID'].isin(watched_movies['ID'].to_list())]

    df_random_row = df.sample(n=1)
    full_path_random = df_random_row['Full Path'].iloc[0]
    id_random = df_random_row['ID'].iloc[0]

    movie_recommendation, movie_name = juswatchGetMovieItems(full_path_random,abreviation_selected,language_selected,id_random)
    
    watched_dict_value = {'Country':[abreviation_selected],'Movie Name':[movie_name],'ID':[id_random]} 
    watched_df_value = pd.DataFrame(watched_dict_value)
    
    toast('success', 'Successfully Selected the movie')
    output_box.config(state='normal')
    output_box.delete(1.0,"end-1c")
    output_box.insert("end-1c",movie_recommendation)
    output_box.config(state='disabled')

def updateWatchedMovies():
    
    try:
   
        row_exists = watched_movies.isin(watched_df_value.to_dict(orient='list')).all(axis=1).any()

        if row_exists:
            toast('danger','Movie already present in the Watched List')
        
        else:    
            watched_movie_merged = pd.concat([watched_movies,watched_df_value],ignore_index=True)
            watched_movie_merged.to_csv('Wacthed Movies.txt',index=False,sep="\t")
            
            toast('success','Movie added in the Watched List')
            
    except NameError:
        toast('warning','No movie has been picked yet')
        pass

def setCountry(*args):
  def Filter(string, substr):
    return [str for str in string if
             any(sub in str.lower() for sub in substr)]
    
  current_filter = Filter(countries_dict['Country'], [country_filter_var.get().lower()])
  country['menu'].delete(0, 'end')
  for choice in current_filter:
        country['menu'].add_command(label=choice, command=tk._setit(country_var, choice))
  country_var.set(current_filter[0])

def setGenre(*args):
  def Filter(string, substr):
    return [str for str in string if
             any(sub in str.lower() for sub in substr)]
    
  current_filter = Filter(genres_dict['Genre'], [genre_filter_var.get().lower()])
  genre['menu'].delete(0, 'end')
  for choice in current_filter:
        genre['menu'].add_command(label=choice, command=tk._setit(genre_var, choice))
  genre_var.set(current_filter[0])

def toast(style, message):
  toast = ToastNotification(
  title="Movie Picker App",
  message=message,
  bootstyle=style,
  duration=5000)
  toast.show_toast()


countries_dict = getCountriesList()

app = ttk.Window(themename='darkly')
app.resizable(False,False)
app.title('Movie Picker .1.0')

tabControl = ttk.Notebook(app, bootstyle='primary')

Tab_Control = ttk.Frame(app)
Tab_Control.pack(expand=1, fill=BOTH)
Tab_Control.grid_columnconfigure(0, weight=1, uniform="Tab_Control")
Tab_Control.grid_columnconfigure(1, weight=1, uniform="Tab_Control")


country_var = ttk.StringVar(app)
country_var.set(countries_dict['Country'])
country_label = ttk.Label(Tab_Control, text='Country Picker')
country_label.grid(column=0, row=0, sticky="w", padx=5)
country = ttk.OptionMenu(Tab_Control, country_var, countries_dict['Country'][0], *countries_dict['Country'])
country.config(width=30)
country.grid(column=0, row=1, sticky="ew", padx=5, pady=5)

keyword_filter_label = ttk.Label(Tab_Control, text='Country Filter')
keyword_filter_label.grid(column=1, row=0, sticky="w", padx=5)
country_filter_var = ttk.StringVar()
keyword_filter = ttk.Entry(Tab_Control, textvariable=country_filter_var)
keyword_filter.grid(column=1, row=1, sticky="ew", padx=5, pady=5)
country_filter_var.trace_add("write", setCountry)


genre_var = ttk.StringVar(app)
genre_var.set(genres_dict['Genre'])
genre_label = ttk.Label(Tab_Control, text='Genre Picker')
genre_label.grid(column=0, row=2, sticky="w", padx=5)
genre = ttk.OptionMenu(Tab_Control, genre_var, genres_dict['Genre'][0], *genres_dict['Genre'])
genre.config(width=30)
genre.grid(column=0, row=3, sticky="ew", padx=5, pady=5)

genre_filter_label = ttk.Label(Tab_Control, text='Genre Filter')
genre_filter_label.grid(column=1, row=2, sticky="w", padx=5)
genre_filter_var = ttk.StringVar()
genre_filter = ttk.Entry(Tab_Control, textvariable=genre_filter_var)
genre_filter.grid(column=1, row=3, sticky="ew", padx=5, pady=5)
genre_filter_var.trace_add("write", setGenre)

output_label = ttk.Label(Tab_Control, text='Movie Details Output')
output_label.grid(column=0, row=4, sticky="ew", padx=5, pady=5, columnspan=2)

output_box = ttk.Text(Tab_Control,width = 50, height = 10, state='disabled')
output_box.grid(column=0, row=5, sticky='ew',padx=5, pady=5, columnspan=2)


submit = ttk.Button(Tab_Control, text='CHOOSE MOVIE', bootstyle='success', command=returnMovie)
submit.grid(column=0, row=6, sticky="ew", padx=5, pady=5, columnspan=2)

watched_movies_button = ttk.Button(Tab_Control, text='ADD TO WATCHED LIST', bootstyle='primary', command=updateWatchedMovies)
watched_movies_button.grid(column=0, row=7, sticky="ew", padx=5, pady=5, columnspan=2)


app.mainloop()
