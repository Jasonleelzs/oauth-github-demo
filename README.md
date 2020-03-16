# oauth-github-demo
A authorization with github oauth2.0 verification

### code todos
1. 我们要让 Github OAuth 授权，就得到先到 Github 登记，https://github.com/settings/applications/new，设置应用的主页为 http://localhost:8099，跳转网站为 http://localhost:8099/oauth/redirect
2. 建一个 客户端的首页 / ，有跳转 github_authorize_uri 链接，带上一些参数，不完全举例：redirect_uri 验证完自动跳转到客户端某页面，client_id 表示 github 给客户端的授权码
3. 点击链接，登录访问 github 一个授权页面，点击授权，github 返回一个跳转链接，跳回 redirect_uri: http://localhost:8099/oauth/redirect?code=xxxxxxxx，
    因为是自己浏览器跳转，这个 code授权码 前端后端都能拿到
4. 用这个 code + client_id + cliend_secret 去申请 token，我们这里是在 response 里拿，也可以让 github call redirect_url
5. 用 token 放到 headers 里去请求就可以拿自己 github 账号信息了