function main(splash)
--    splash.args.url
  local url = "https://www.facebook.com/login.php"
  local wait = 4.0
  local email = splash.args.email or 'nikaskriabina@gmail.com'
  local password = splash.args.password or 'F,hfrflf,hf2016'
  assert(splash:go(url))
  assert(splash:wait(wait))
  splash:runjs("document.getElementById('email').value = '".. email .."'")
  splash:runjs("document.getElementById('pass').value = '".. password .."'")
  splash:runjs("document.getElementById('loginbutton').click()")
  assert(splash:wait(wait))
--  assert(splash:wait(wait))
  return {
    html = splash:html(),
    png = splash:png(),
    cookies = splash:get_cookies(),
    url = splash:evaljs("window.location.href")
  }
end