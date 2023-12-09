$.getJSON("https://api.ipify.org?format=json", function (data) {
                    $("#IPClient").html("Your IP: " + data.ip + "");
                })