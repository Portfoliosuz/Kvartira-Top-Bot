import haversine
def taqqos(userlatitude, userlongitude, places):
    ret = []
    taqqoslist = {}
    for i in places:
        taqqoslist[float(haversine.haversine(
            (userlatitude, userlongitude), (i[0], i[1]), unit=haversine.Unit.KILOMETERS))]=[[userlatitude,userlongitude],[i[0],i[1]]]
    for i in sorted(taqqoslist.keys()):
        ret.append([i,taqqoslist[i]])
    return ret

