let extractFename = st => st.split(" ")[st.split(" ").length - 2];
let streetExtent = p => d3.extent([p.FRADDL, p.FRADDR, p.TOADDL, p.TOADDR])

function geocode(address, geoData) {    
    let isCorner = address.split("/").length > 1;
    
    let coords = [];
    if (isCorner) {
        let streetNames = address.split("/").map(d => d.trim());
        let streets = [];
        for (let st of streetNames) {
            streets.push(geoData.features
                            .filter(d => d.geometry !== null)
                            .filter(d => d.properties.FENAME !== null)
                            .filter(d => d.properties.FENAME == extractFename(st)))
        }
        console.log(streets[0])
        let street0Coords = streets[0].map(s => s.geometry.coordinates).flat();
        let street1Coords = streets[1].map(s => s.geometry.coordinates).flat();

        for (let coords0 of street0Coords) {
            for (let coords1 of street1Coords) {
                if (coords0[0] == coords1[0] & coords0[1] == coords1[1]) {
                    coords = coords0;
                }
            }
        }
    } else {
        let ad = address.split(" ").map(d => d.trim())
        console.log(ad)
        let number = +ad[0]
        let name = ad[ad.length - 2]
        let streets = geoData.features
                    .filter(d => d.geometry !== null)
                    .filter(d => d.properties.FENAME !== null)
                    .filter(d => d.properties.FENAME.includes(name))
        for (let st of streets) {
            let stExtent = streetExtent(st.properties)
            if (number >= stExtent[0] && number <= stExtent[1]) {
                let longExtent = st.geometry.coordinates.map(d => d[0]);
                let latExtent = st.geometry.coordinates.map(d => d[1]);

                let parser = d3.scaleLinear()
                    .range([[longExtent[0],latExtent[0]], [longExtent[1],latExtent[1]]])
                    .domain(stExtent)
                
                coords = parser(number)
            }
        }
    }
    return coords;
}


Promise.all([
    d3.json("Abila-geojson.json"),
    d3.csv("reports.csv")
]).then(function(data) {
    let abilaMap = data[0]
    let reports = data[1]
    let coords = []
    
    for(let { location } of reports)
        if (location != ""){
            if (!coords[location]) {
                coords[location] = { 
                location, 
                coords: geocode(location, abilaMap) 
                }  
            }
        }
    
    let result = Object.values(coords)
    
    console.log(JSON.stringify(result)) // This result was copied to a json file.
});
