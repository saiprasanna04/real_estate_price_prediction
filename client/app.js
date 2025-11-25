function getBathValue() {
  var uiBathrooms = document.getElementsByName("uiBathrooms");
  for (var i = 0; i < uiBathrooms.length; i++) {
    if (uiBathrooms[i].checked) {
      return parseInt(uiBathrooms[i].value);
    }
  }
  return -1; // Invalid value
}

function getBHKValue() {
  var uiBHK = document.getElementsByName("uiBHK");
  for (var i = 0; i < uiBHK.length; i++) {
    if (uiBHK[i].checked) {
      return parseInt(uiBHK[i].value);
    }
  }
  return -1; // Invalid value
}

function onClickedEstimatePrice() {
  console.log("Estimate price button clicked");

  var sqftElem = document.getElementById("uiSqft");
  var bhk = getBHKValue();
  var bathrooms = getBathValue();
  var locationElem = document.getElementById("uiLocations");
  var estPriceElem = document.getElementById("uiEstimatedPrice");

  estPriceElem.innerHTML = "";

  if (!sqftElem.value || isNaN(sqftElem.value)) {
    alert("Please enter a valid square feet value");
    return;
  }
  if (bhk === -1) {
    alert("Please select a BHK option");
    return;
  }
  if (bathrooms === -1) {
    alert("Please select number of bathrooms");
    return;
  }
  if (!locationElem.value) {
    alert("Please select a location");
    return;
  }

  var url = "http://127.0.0.1:5000/predict_home_price";

  $.post(url, {
    total_sqft: parseFloat(sqftElem.value),
    bhk: bhk,
    bath: bathrooms,
    location: locationElem.value
  })
  .done(function(data) {
    console.log(data);
    if (data.estimated_price !== undefined) {
      estPriceElem.innerHTML = "<h2>" + data.estimated_price.toString() + " Lakh</h2>";
    } else if (data.error) {
      estPriceElem.innerHTML = "<p style='color:red'>" + data.error + "</p>";
    } else {
      estPriceElem.innerHTML = "<p style='color:red'>Unexpected response from server</p>";
    }
  })
  .fail(function(jqXHR, textStatus, errorThrown) {
    console.error("Request failed: " + textStatus, errorThrown);
    let errMsg = "Server error. Please try again later.";
    if (jqXHR.responseJSON && jqXHR.responseJSON.error) {
      errMsg = jqXHR.responseJSON.error;
    }
    estPriceElem.innerHTML = "<p style='color:red'>" + errMsg + "</p>";
  });
}

function onPageLoad() {
  console.log("document loaded");
  var url = "http://127.0.0.1:5000/get_location_names";
  $.get(url)
    .done(function(data) {
      console.log("got response for get_location_names request");
      if (data) {
        var locations = data.locations;
        var uiLocations = document.getElementById("uiLocations");
        $('#uiLocations').empty();
        for (var i in locations) {
          var opt = new Option(locations[i]);
          $('#uiLocations').append(opt);
        }
      }
    })
    .fail(function() {
      console.error("Failed to load location names from server");
    });
}

window.onload = onPageLoad;
