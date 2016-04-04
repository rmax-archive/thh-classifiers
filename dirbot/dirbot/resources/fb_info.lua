function main(splash)
  local url = splash.args.url
  local cookies = splash.args.cookies
  local wait = 3.0
  local points = {"education", "living", "bio"}
--  points = {"bio"}
  splash:init_cookies(cookies)
  assert(splash:go(url))
  assert(splash:wait(wait))
  local overview_html = splash:html()
  local pages = {}
  pages["overview"] = overview_html
  local new_url = url
  for i, point in ipairs(points) do
      new_url = url .. "?section=" .. point
      assert(splash:go(new_url))
      assert(splash:wait(wait))
      pages[point] = splash:html()
  end
  return {
    html = info_html,
    png = splash:png(),
    cookies = splash:get_cookies(),
    pages = pages,
    url = splash.args.url,
  }
end