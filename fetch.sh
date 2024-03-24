# DH
wget "https://overpass-api.de/api/interpreter?data=[out:json][timeout:325]; area(id:3600192736)->.searchArea; nwr["network"="rcn"](area.searchArea); out geom;" -O dh.turbojson
wget "https://overpass-api.de/api/interpreter?data=[out:json][timeout:325]; area(id:3600192736)->.searchArea; nwr["rcn_ref"](area.searchArea); out geom;" -O dh.nodes.turbojson
# NL
wget "https://overpass-api.de/api/interpreter?data=[out:json][timeout:325]; area(id:3602323309)->.searchArea; nwr["network"="rcn"](area.searchArea); out geom;" -O holland.turbojson
rm -f holland.turbojson.gz
gzip holland.turbojson
wget "https://overpass-api.de/api/interpreter?data=[out:json][timeout:325]; area(id:3602323309)->.searchArea; nwr["rcn_ref"](area.searchArea); out geom;" -O holland.nodes.turbojson
