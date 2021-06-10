document.addEventListener( 'DOMContentLoaded', function () {
	new Splide( '#image-slider', {
        'type' : 'loop',
		'fixedHeight': 450,
        'gap': '2em',
        'cover': true,
        'padding': {
            right: '10rem',
            left : '10rem',
        },
        'perPage': 1,
        'autoplay': true
	} ).mount();
} );

function onScanSuccess(qrCodeMessage) {
	// handle on success condition with the decoded message
}

var html5QrcodeScanner = new Html5QrcodeScanner(
	"reader", { fps: 10, qrbox: 250 });
html5QrcodeScanner.render(onScanSuccess);