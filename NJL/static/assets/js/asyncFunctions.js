function valueUpdate() {

    let data = JSON.parse("{{data|escapejs}}");

    let sensorValue

    document.getElementById('sensorValue').innerHTML =
        "0,25";
    let t = setInterval(valueUpdate, 2000);
}
