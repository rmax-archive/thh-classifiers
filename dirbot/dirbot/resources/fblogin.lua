function main(splash)
--    splash.args.url
  local url = "https://www.facebook.com/login.php"
  local wait = 2.0
  assert(splash:go(url))
  assert(splash:wait(wait))
  splash:runjs("document.getElementById('email').value = 'nikaskriabina@gmail.com'")
  splash:runjs("document.getElementById('pass').value = 'F,hfrflf,hf2016'")
  splash:runjs("document.getElementById('loginbutton').click()")
  assert(splash:wait(wait))
  assert(splash:wait(wait))
--  assert(splash:wait(wait))
--  assert(splash:go("https://www.facebook.com/100000118429707/info"))
--  assert(splash:wait(wait))
--  assert(splash:wait(wait))
  return {
    html = splash:html(),
    png = splash:png(),
    cookies = splash:get_cookies(),
    url = splash:evaljs("window.location.href")
  }
end