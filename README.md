# namecheap
certbot manual auth hook for DNS-01 with namecheap

## requirements
- python
  - requests
  - beautifulsoup
  - lxml
  - requests-cache (optional, currently commented out)
- certbot
- namecheap api key https://www.namecheap.com/support/knowledgebase/article.aspx/9739/63/api--faq#c

## current limitations
- SLD/TLD extraction is extremely naive and does not support multipart tlds
- no cleanup hook, just an auth hook
  - update: a cleanup function has been added to remove old challenges before setting a new one
- none of the api calls are paginated yet but this probably doesn't matter bc the hook works based on an env var
- no error checking or handling of any sort
- was going to be a more robust wrapper of certbot that loops over all your domains, but heck it
- lol everything is hardcoded so make sure to put in your own username / api key

## example usage if you've got existing certs
edit existing renewal conf, e.g. `/etc/letsencrypt/renewal/tarawneh.org.conf` and make sure `authenticator = manual`, `pref_challs = dns-01,`, `manual_auth_hook = /path/to/auth`, `manual_public_ip_logging_ok = True`
```
[renewalparams]
account = 1234567890abcdef1234567890abcdef
authenticator = manual
server = https://acme-v02.api.letsencrypt.org/directory
pref_challs = dns-01,
manual_auth_hook = /home/trwnh/bin/namecheap/auth
manual_public_ip_logging_ok = True
```

## example usage if you're making a new cert

```
sudo certbot certonly \
     --preferred-challenges=dns \
     --manual \
     --manual-auth-hook=/path/to/auth \
     --agree-tos \
     -d domain.com,*.domain.com
```

## maintenance

you should be able to run `certbot renew` after that and the settings will be remembered? ~idk~ yes, this works without intervention

## etc

pay me for emotional damages caused by namecheap's api:
- recurring: https://liberapay.com/trwnh
- one-time: https://paypal.me/trwnh

interact with me elsewhere:
- fedi: https://mastodon.social/@trwnh
- smtp/xmpp: a@trwnh.com
