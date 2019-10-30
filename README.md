# namecheap
certbot manual auth hook for DNS-01 with namecheap

## example usage if you've got existing certs
edit existing renewal conf, e.g. `/etc/letsencrypt/renewal/tarawneh.org.conf` and make sure `authenticator = manual`, `pref_challs = dns-01,`, `manual_auth_hook = /path/to/hook`, `manual_public_ip_logging_ok = True`
```
[renewalparams]
account = 1234567890abcdef1234567890abcdef
authenticator = manual
server = https://acme-v02.api.letsencrypt.org/directory
pref_challs = dns-01,
manual_auth_hook = /home/trwnh/bin/https
manual_public_ip_logging_ok = True
```

## example usage if you're making a new cert

```
sudo certbot certonly \
     --preferred-challenges=dns \
     --manual \
     --manual-auth-hook=/path/to/hook \
     --agree-tos \
     -d domain.com,*.domain.com
```

## maintenance

you should be able to run `certbot renew` after that and the settings will be remembered? idk

## etc

pay me for emotional damages caused by namecheap's api:
- recurring: https://liberapay.com/trwnh
- one-time: https://paypal.me/trwnh

interact with me elsewhere:
- fedi: https://mastodon.social/@trwnh
- smtp/xmpp: a@trwnh.com
