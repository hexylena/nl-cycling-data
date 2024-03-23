
## Next Steps

- look at the nodes, and see if any of their lat/lon overlap exactly with any routes, collect all matching routes, guess the number from that.

## Log

we've got some nice queries for the overpass turbo API, which fetches roughly the data we need.

However it doesn't fetch the actual node data that we need, e.g.

```
Node 44751084 ✏
Relations 1

    1852352 network Fietsnetwerk Midden-Delfland

Coordinates

51.989431 / 4.2876399 (lat/lon)
```

and yeah, completely missing from the overpass results.
See e.g. [overpass](https://overpass-turbo.eu/) with a query like:

```
[out:json][timeout:325];
area(id:3600192736)->.searchArea;
nwr["network"="rcn"](area.searchArea);
out geom;
```

the RCN node data just isn't there, except for the ways.

