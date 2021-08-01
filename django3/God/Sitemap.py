def sitemap(request):
    dt_now = datetime.datetime.now()
    now = dt_now.strftime('%Y%m%d%H')
    pop_page_list_copy = pop_page_list.copy()
    for page in pop_page_list_copy:
        page["lastmod"] = f"{dt_now.strftime('%Y')}-{dt_now.strftime('%m')}-{dt_now.strftime('%d')}T00:00:00+00:00" #"2021-07-30T13:25:37+00:00"
    params = {
        "pop_page_list" : pop_page_list_copy
    }
    return render(request,f"oversea_it/sitemap.xml", params)
