# DH
wget "https://overpass-api.de/api/interpreter?data=[out:json][timeout:325]; area(id:3600192736)->.searchArea; nwr["network"="rcn"](area.searchArea); out geom;" -O dh.geojson
wget "https://overpass-api.de/api/interpreter?data=[out:json][timeout:325]; area(id:3600192736)->.searchArea; nwr["rcn_ref"](area.searchArea); out geom;" -O dh.nodes.geojson
# NL
wget "https://overpass-api.de/api/interpreter?data=[out:json][timeout:325]; area(id:3602323309)->.searchArea; nwr["network"="rcn"](area.searchArea); out geom;" -O holland.geojson
rm -f holland.geojson.gz
gzip holland.geojson
wget "https://overpass-api.de/api/interpreter?data=[out:json][timeout:325]; area(id:3602323309)->.searchArea; nwr["rcn_ref"](area.searchArea); out geom;" -O holland.nodes.geojson
