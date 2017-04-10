import json
import requests
from pygal.style import LightColorizedStyle as LCS, LightenStyle as LC
import pygal

#List of languages
languages = ['c', 'cpp', 'java', 'go', 'javascript', 'scala', 'perl', 'haskell']
for language in languages:
    #Choose repos by stars
    url = "https://api.github.com/search/repositories?q=language:" +str(language) + "&sort=star"
    r = requests.get(url)
    print("Status code:", r.status_code)
    #Save results as JSON
    respond_dicts = r.json()
    print("Total repositories:", respond_dicts['total_count'])
    # Analyse information
    repo_dicts = respond_dicts['items']
    # Arrays for names and stars
    names = []
    plot_dicts = []
    for repo_dict in repo_dicts:
        names.append(repo_dict['name'])
        label = repo_dict['description']
        if label == None:
            label = ''
        plot_dict = {'value': repo_dict['stargazers_count'],
                     'label': label,
                     'xlink': repo_dict['html_url']}
        plot_dicts.append(plot_dict)
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
    chart.title = "Most starred " + str(language) + " repositories"
    chart.x_labels = names
    chart.add('', plot_dicts)
    #Import to file
    chart.render_to_file(str(language) + "_stars_with_description.svg")