import requests
from operator import itemgetter
from pygal.style import LightColorizedStyle as LCS, LightenStyle as LC
import pygal
#Create request
url = 'https://hacker-news.firebaseio.com/v0/topstories.json'
r = requests.get(url)
print("Status code:", r.status_code)

#Process every article
submission_ids = r.json()
submission_dicts = []
titles = []
for submission_id in submission_ids[:30]:
    Url = ('https://hacker-news.firebaseio.com/v0/item/' + str(submission_id) + '.json')
    submission_r = requests.get(Url)
    print("Status code:", submission_r.status_code)
    response_dict = submission_r.json()
    submission_dict = {'title' : response_dict['title'],
                       'xlink': 'http://news.ycombinator.com/item?id=' + str(submission_id),
                       'value': response_dict.get('descendants', 0)}
    submission_dicts.append(submission_dict)

# Sort fo visualisation
submission_dicts = sorted(submission_dicts, key = itemgetter('value'), reverse = True)
for s_dict in submission_dicts:
    titles.append(s_dict['title'])
#Print output
#for submission_dict in submission_dicts:
 #   print("\nTitle:", submission_dict['title'])
 #   print("Link:", submission_dict['link'])
 #   print('Comments', submission_dict['comments'])
#Visualisation
my_style = LC('#08088A', base_style=LCS)
my_config = pygal.Config()
my_config.x_label_rotation = 45
my_config.show_legend = False
my_config.title_font_size = 24
my_config.label_font_size = 14
my_config.mayor_label_font_size = 18
my_config.truncate_label = 15
my_config.show_y_guides = False
my_config.width = 1000
chart = pygal.Bar(my_config, style=my_style)
chart.title = "Most commented articles"
chart.x_labels = titles
chart.add('', submission_dicts)
#Import to file
chart.render_to_file("most_commented_articles.svg")