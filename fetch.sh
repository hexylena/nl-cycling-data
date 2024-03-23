wget "https://overpass-api.de/api/interpreter?data=[out:json][timeout:325]; area(id:3600192736)->.searchArea; nwr["network"="rcn"](area.searchArea); out geom;" -O holland.geojson
