

template = f"""
<?xml version="1.0" encoding="UTF-8"?>
<urlset
      xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"
      xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
      xsi:schemaLocation="http://www.sitemaps.org/schemas/sitemap/0.9
            http://www.sitemaps.org/schemas/sitemap/0.9/sitemap.xsd">
<!-- created with Free Online Sitemap Generator www.xml-sitemaps.com -->


<url>
  <loc>https://minegishirei.github.io/github-pages.beaver/index.html</loc>
  <lastmod>2023-08-28T00:17:58+00:00</lastmod>
</url>

__replace__

</urlset>
"""


def create_sitemap(all_events):
    print(all_events)
    urlset = ""
    for id, event in all_events.items():
        url = f"""
<url>
  <loc>https://minegishirei.github.io/github-pages.beaver/product_detail.html?id={id}</loc>
</url>
        """
        urlset += url
    return template.replace("__replace__", urlset)
    






