"""
purpose: talk and mimic people speaking.
currently the implementation is limited to sex bot because it's easier to find horny dumb dudes to gain experience..
the way I want to implement it is that the program will hold some kind of physics abstraction for the chat

TODO list:
-finish litorica HTML mangement

-Wikipeia ? not sure we need it, leave it for now.

-urban dictionary
-- from name to description + example? see later the format

-python automation
"""
# dummy change to check git
import requests
import re
import six
import pickle
from urllib.request import Request, urlopen
from urllib.error import URLError

try:
    from BeautifulSoup import BeautifulSoup
except ImportError:
    from bs4 import BeautifulSoup


def main():
    # testing cases:
    categories = get_all_litorica_category_to_list()
    chosen_category = categories[2]
    print("chosen category is: ", chosen_category)
    all_stories = get_all_litorica_category_stories(chosen_category)
    print(all_stories)
    chosen_story = all_stories[1]
    print(chosen_story)
    some_story = get_story_from_litorica(chosen_story[0])
    print('\n ******* another part **********\n'.join(some_story))


def get_all_litorica_category_stories(category, use_cashe=True):
    """
    get all name of all the stories, the URL of these and thier ranks
    :param: categry for all the stories
    :return: A list of a list of all the story per specific topic
    the inner list are in the format of:
    [url, score, title, description, date, author]
    """

    # try open a file if succeed great - parse everything from there.
    # if not get it from the web.0.21
    try:
        with open(category + ".pickle", "rb") as fp:
            list_of_lists = pickle.load(fp)
            print("succeed to load from cache file")
            return list_of_lists
    except EnvironmentError as e:
        print(e)
        print("file wasn't found for that category")
        print("collecting the data online...")

    # the form is a list of lists while list0 contain the format of the lists.
    list_of_list_of_stories = [[]]
    list_of_list_of_stories[0] = ["url", "score", "title", "description", "date", "author"]
    i = 1
    while True:
        url = build_category_litorica_url(category) + "/" + str(i) + "-page"
        r = requests.get(url)
        # this means we had wrapped around and we got redirected
        # (there is no error for non-exist numbers just redirection to the division)
        if (r.url != url):
            break
        html = get_html_from_url(url)
        parsed_html = BeautifulSoup(html, features="html.parser")
        print(url)
        print(i)
        i = i + 1
        story_list = parsed_html.body.find('div', attrs={'class': 'b-story-list'})
        stories_sections = story_list.findAll('div', attrs={'class': 'b-sl-item-r w-34t'})
        for story_section in stories_sections:
            # generate for each section:
            # url, score, title, description, date and author and put it in a list

            # url - must:
            story_url = story_section.find('a', {'class': 'r-34i'})['href']
            if story_url is None:
                continue

            # score - must:
            story_score_obj = story_section.find('span', attrs={'class': 'b-sli-rating'})
            if story_score_obj is None:
                continue
            story_score = story_score_obj.text

            # title:
            # if there was link there is a text so no need for checking:
            story_title = story_section.find('a', {'class': 'r-34i'}).text

            # description:
            story_description_obj = story_section.find('span', attrs={'class': 'b-sli-description p-57u'})
            sotry_description = None
            if story_description_obj is not None:
                story_description = story_description_obj.text

            # date:
            story_date_obj = story_section.find('span', attrs={'class': 'b-sli-date'})
            story_date = None
            if story_date_obj is not None:
                story_date = story_date_obj.text

            # author:
            story_author_obj = story_section.find('span', attrs={'class': 'b-sli-author'})
            story_author = None
            if story_author_obj is not None:
                story_author = story_author_obj.text
                story_author = story_author.replace("\n", "")
                story_author = re.sub(r"\s+\S+\s+", "", story_author)

            # append everything as a list into the list of lists:
            list_of_list_of_stories.append(
                [story_url, story_score, story_title, story_description, story_date, story_author])

    # save the data into a file with the same name:

    try:
        with open(category + ".pickle", "wb") as fp:
            pickle.dump(list_of_list_of_stories, fp)
        print("cache file was dumped with the name: " + category + ".pickle")
    except EnvironmentError:
        print("couldn't dump a cache file")
    return list_of_list_of_stories


def get_all_litorica_category_to_list():
    """
    all the topics are in the form of:
    https://www.literotica.com/c/anal-sex-stories/20-page
    :return: List of all the the categories as it will apear in the URL.
    """
    categories = [
        "anal-sex-stories",
        "bdsm-stories",
        "celebrity-stories",
        "chain-stories",
        "erotic-couplings",
        "erotic-horror",
        "exhibitionist-voyeur",
        "fetish-stories",
        "first-time-sex-stories",
        "gay-sex-stories",
        "group-sex-stories",
        "adult-how-to",
        "adult-humor",
        "illustrated-erotic-fiction",
        "taboo-sex-stories",
        "interracial-erotic-stories",
        "lesbian-sex-stories",
        "erotic-letters",
        "loving-wives",
        "mature-sex",
        "mind-control",
        "non-erotic-stories",
        "non-consent-stories",
        "non-human-stories",
        "erotic-novels",
        "adult-romance",
        "science-fiction-fantasy",
        "masturbation-stories",
        "transsexuals-crossdressers",
    ]
    return categories


def build_category_litorica_url(category):
    """
    build the category url
    :param category: category to be built from
    :return: full url from the category
    """
    return "https://www.literotica.com/c/" + category


def get_html_from_url(url):
    """
    reach the server and get the html respond.
    :param url: url that will try to get
    :return: html page respond from the server
    """

    headers = {
        'User-Agent': "Mozilla/5.0 (X11; Linux i686) "
                      "AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"}
    req = Request(url, headers=headers)
    try:
        response = urlopen(req)
    except URLError as e:
        if hasattr(e, 'reason'):
            print('We failed to reach a server.')
            print('Reason: ', e.reason)
        elif hasattr(e, 'code'):
            print("The server couldn't fulfill the request.")
            print('Error code: ', e.code)
        return "error"
    else:
        return response.read()


def get_story_from_litorica(url):
    """
    From web URL to string of the story.
    It assume that it is Litorica format story.
    :param url: the URL of the litorica site that need to be extracted
    :return: a list of strings of all the pages of the story
    """
    story_list = []
    html = get_html_from_url(url)
    parsed_html = BeautifulSoup(html, features="html.parser")
    # span class="b-pager-caption-t r-d45
    num_of_pages_obj = parsed_html.find('span', attrs={'class': 'b-pager-caption-t r-d45'})
    if num_of_pages_obj is None:
        print("couldn't obtain the number of pages")
        return story_list
    num_of_pages = num_of_pages_obj.text
    num_of_pages = re.sub("[^0-9]", "", num_of_pages)
    num_of_pages = int(num_of_pages)
    print(num_of_pages)
    current_page_story_obj = parsed_html.body.find('div', attrs={'class': 'b-story-body-x x-r15'})
    if current_page_story_obj is None:
        print("we failed to obtain the story of the first page.. returning empty list.")
        return story_list
    story_list.append(current_page_story_obj.text)

    # as we don't want to access URLs too often, we prefer using the already access previously for use of the 1st page
    # for later usages we will need to re-access anyway so start with the 2nd page to the end of pages..
    for i in range(2, num_of_pages + 1):
        html = get_html_from_url(url + "?page=" + str(i))
        parsed_html = BeautifulSoup(html, features="html.parser")
        current_page_story_obj = parsed_html.body.find('div', attrs={'class': 'b-story-body-x x-r15'})
        if current_page_story_obj is None:
            # only give up on this pages and the next ones.
            print("we failed to obtain the story of the", str(i), "page. returning the list we got.")
            return story_list
        story_list.append(current_page_story_obj.text)

    # we got all the pages. return the list.
    return story_list


if __name__ == "__main__":
    main()
