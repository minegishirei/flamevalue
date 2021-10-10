
#!/bin/bash
certbot-auto --nginx -d short-tips.info -d www.short-tips.info -m minegishirei@gmail.com --agree-tos -n
certbot-auto renew
/bin/bash