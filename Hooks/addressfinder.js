(function () {          
    var widget,
    initAF = function () {             
        widget =
        new AddressFinder.Widget(
            // Replace with the id of your search field
            document.getElementsByName[0]('address_search'),
            // Replace with your license key
            'G96CBFJ4HY37RQWNX8AK',
            'AU',
            {"address_params": {
                "gnaf": "1"
            }
        }
        );             
        widget.on('result:select', function (fullAddress, metaData) {              
            // Replace each of these fields with your address field ids
            switch(metaData.address_line_2){
                case null:
                    document.getElementsByName('address')[0].value = metaData.address_line_1;
                    break;
                default:
                    document.getElementsByName('address')[0].value = metaData.address_line_1 + ', ' + metaData.address_line_2;
                break;
            }; 
            document.getElementsByName('suburb')[0].value = metaData.locality_name;               
            document.getElementsByName('state')[0].value = metaData.state_territory;               
            document.getElementsByName('postcode')[0].value = metaData.postcode;               
            document.getElementsByName('gps_metadata')[0].value = metaData.longitude + ', ' + metaData.latitude;               
            document.getElementsByName('meshblock_metadata')[0].value = metaData.meshblock;               
            document.getElementsByName('sa1')[0].value = metaData.sa1_id;            
        });           
    };  

    function downloadAF() {            
        var script = document.createElement('script');
        script.src = 'https://api.addressfinder.io/assets/v3/widget.js';
        script.async = true;
        script.onload = initAF;             
        document.body.appendChild(script);
    };           
    document.addEventListener('DOMContentLoaded', downloadAF);         
})();
