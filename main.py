import json
import time
import requests
from flask import Flask, request, Request, render_template, \
                 jsonify, redirect
from configs import oauth_config


app = Flask(__name__)


def log(*args, **kwargs):
    time_format = '%Y-%m-%d %H:%M:%S'
    value = time.localtime(int(time.time()))
    dt = time.strftime(time_format, value)

    with open('app.log', 'a', encoding='utf-8') as f:
        print(dt, *args, file=f, **kwargs)


@app.route('/')
def index():
    return render_template('index.html', config=oauth_config)


@app.route('/oauth/redirect')
def oauth_redirect():
    # 获取到id
    authorization_code = request.args.get('code', '')

    log('authorization code', authorization_code)

    # 这个 url 包括 github_token_url, client_id, client_secret, authorization_code, redirect_uri
    apply_token_url = 'https://github.com/login/oauth/access_token?client_id={}&client_secret={}&code={}'.format(oauth_config['client_id'],
                                                                                                                 oauth_config['client_secret'],
                                                                                                                 authorization_code,
                                                                                                                 )
    r = requests.post(
        url=apply_token_url,
        headers={"accept": 'application/json'}
    )
    log("token response: ", r)
    access_token = r.json().get('access_token')
    log("access token: ", access_token)

    # 接下来就是用 token 去请求 github 数据了
    authorization = 'token {}'.format(access_token)
    r = requests.get(
        url=oauth_config.get('api_uri'),
        headers={
            "accept": 'application/json',
            "Authorization": authorization,
        }
    )
    github_messages = r.json()
    return render_template('redirect.html', github=github_messages)


if __name__ == '__main__':
    # 生成配置并且运行程序
    config = dict(
        debug=True,
        host='127.0.0.1',
        port=8099,
    )
    app.run(**config)
