
function parseData(events, keyword){
    const hashMap = {}
    for (const event of events) {
        const innerMap = {};
        innerMap['name'] = event['name'];
        innerMap['location'] = event['_embedded']['venues'][0]['city']['name']
        innerMap['venue'] = event['_embedded']['venues'][0]['name']
        innerMap['date'] = event['dates']['start']['localDate']
        innerMap['time'] = event['dates']['start']['localTime']
        innerMap['id'] = event['id']
        var prices = event.priceRanges
        if(prices){
            const priceMap = {}
            // possible that here is more than one option for prices
            priceMap['min'] = event['priceRanges'][0]['min']
            priceMap['max'] = event['priceRanges'][0]['max']

            innerMap['priceRanges'] = priceMap
        }
        hashMap[event['id']] = innerMap
    }
    return hashMap
}

function displayResults(data, keyword){
    const events = data['_embedded']['events'];
    const table = document.getElementById("results-tbody");
    var neededData = parseData(events, keyword);
    const headers = ['Name', 'Location', 'Venue', 'Date', 'Time', "Prices", "id"];
    console.log(neededData)
    for( var i in neededData){
        console.log(neededData[i])
    }
    Object.entries(neededData).forEach(([key, value]) => {
        const row = document.createElement('tr');

        for(const header of headers) {
            const td = document.createElement('td');
            if(header  == 'Prices') {
                var prices = -1
                if(value.priceRanges){
                    prices = '$'+value['priceRanges']['min'] + ' - '+ '$'+value['priceRanges']['max']
                }
                td.textContent = prices;
            } else if (header == "id") {
                td.textContent = value[header]
                td.style.display = "none"
            } else {
                td.textContent = value[header.toLowerCase()];
            }
            row.appendChild(td)
        }
        table.appendChild(row);
      });

}
// Used to find the artist ID. If the artist Id is not found in the first entry
// an error will be thrown
function findArtist(data, keyword){
    const artistName = data?._embedded?.attractions[0]?.name ?? '';
    if (!artistName || artistName.toLowerCase() !== keyword.toLowerCase()){
        throw new Error("No artist found.");
    } 
    return data?._embedded?.attractions[0]?.id
}

// Performs a search for the artist Id as well as the events they will be performing at
const APIKEY = '7kyWM9xf2TVWoiEpA7lEXDsAFLjvAGN1';
async function performSearch() {
    const keyword = document.getElementById("searchArtist").value;
    try {
        // get the artist Id
        const artistUrl = `https://app.ticketmaster.com/discovery/v2/attractions.json?apikey=${APIKEY}&keyword=${encodeURIComponent(keyword)}`;
        const artistResponse = await fetch(artistUrl);
        const artistData = await artistResponse.json()
        const artistId = findArtist(artistData, keyword)

        // get list of concerts
        const eventUrl = `https://app.ticketmaster.com/discovery/v2/events.json?apikey=${APIKEY}&attractionId=${encodeURIComponent(artistId)}`
        const eventResponse = await fetch(eventUrl);
        const eventData = await eventResponse.json()
        displayResults(eventData, keyword)
    } catch (error) {
             alert(error)
             console.log('Error occured', error);
    }
}

const form = document.getElementById('form');
form.addEventListener('submit', function(event) {
    console.log('SENDING')
    event.preventDefault();

    const xhr = new XMLHttpRequest();
    const url = 'https://hq3zqt2rb4.execute-api.us-east-1.amazonaws.com/Dev'; 

    xhr.open('POST', url);
    xhr.setRequestHeader('Content-Type', 'application/json'); // Set the request header if sending JSON data

    xhr.onreadystatechange = function() {
    if (xhr.readyState === XMLHttpRequest.DONE) {
        if (xhr.status === 200) {
        const response = JSON.parse(xhr.responseText);
        // Handle successful response
        console.log(response);
        } else {
        // Handle error response
        console.error('Request failed. Status:', xhr.status);
        }
    }
    };

    const row = document.querySelector('.selected');
    const showId = row.getElementsByTagName('td')[6].textContent
    const eventInfo = {
        'name' : row.getElementsByTagName('td')[0].textContent,
        'location' : row.getElementsByTagName('td')[1].textContent,
        'venue' : row.getElementsByTagName('td')[2].textContent,
        'date' : row.getElementsByTagName('td')[3].textContent,
        'time' : row.getElementsByTagName('td')[4].textContent,
        'price' : row.getElementsByTagName('td')[5].textContent
    }

    

    const data = {
        id : showId,
        payload : { 
            email: document.getElementById("email").value,
            eventData: eventInfo
        }
    };

    xhr.send(JSON.stringify(data)); // Convert data to JSON 
    
});

