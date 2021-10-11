#!/bin/bash
certbot-auto --nginx -d example.com -d www.example.com -m your-account@gmail.com --agree-tos -n
certbot-auto renew
/bin/bash