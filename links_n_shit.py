#-*- coding: utf-8 -*-
import requests
import random

base = r'https://www.reddit.com/'
title_list = ['I don\'t know how I feel about carjackers.',
              'I can\'t believe how tall giraffes really are!',
              'Do you have Die Hard™ on Blu-Ray?',
              'Just give me two big ones, please.']

def login():
    username = 'arcbot'
    password = open('arc_pass.txt', 'r').read().strip()

    payload = {'api_type' : 'json', 'passwd' : password, 'user' : username}
    headers = {'user-agent': 'posting script for /u/arctem\'s /u/arcbot'}

    client = requests.session()
    client.headers = headers
    r = client.post(base + r'api/login', data=payload)
    j = r.json()
    client.modhash = j['json']['data']['modhash']
    print('Logged in as {}.'.format(username))

    return client

def choose_link():
    links = open('links.botdat', 'r').read().split('\n')
    already_used = open('used_links.botdat', 'r').read().split('\n')
    while True:
        chosen = random.choice(links)
        if chosen not in already_used:
            break
    already_used.append(chosen)
    open('used_links.botdat', 'w').write('\n'.join(already_used).strip())
    return chosen

def submit(link, client, subreddit='WordsNShit'):
    captcha = validate_captcha(client)
    if captcha:
        captcha, iden = captcha
    
    title = random.choice(title_list)
    
    payload = {'api_type' : 'json', 'kind' : 'link', 'sendreplies' : True,
               'sr' : subreddit, 'title' : title, 'uh' : client.modhash,
               'url' : link}

    if captcha:
        payload['captcha'], payload['iden'] = captcha, iden
    
    r = client.post(base + r'api/submit', data=payload)
    j = r.json()
    print(j)
    for error in j['json']['errors']:
        if error[0] == 'ALREADY_SUB':
            return False
    return True

def validate_captcha(client):
    r = client.get(base + r'api/needs_captcha.json')
    if r.text == 'true':
        r = client.post(base + r'api/new_captcha', data={'api_type' : 'json'})
        iden = r.json()['json']['data']['iden']
        r = client.get(base + r'captcha/{}'.format(iden))
        with open('captcha.png', 'wb') as f:
            for chunk in r.iter_content():
                f.write(chunk)
        return input('answer for captcha in captcha.png? '), iden
    else:
        return False
    
def main():
    client = login()

    while True:
        link = choose_link()
        print(link)
        if submit(link, client):
            #quit if successfully submitted
            break

if __name__ == '__main__':
    main()
