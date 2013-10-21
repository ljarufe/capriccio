flippingBook.pages = [
	"/media/img/carta1.jpg",
	"/media/img/carta2.jpg",
	"/media/img/carta3.jpg",
	"/media/img/carta4.jpg",
	"/media/img/carta5.jpg",
	"pages/carta6.jpg",
	"pages/carta7.jpg",
	"pages/carta8.jpg",
	"pages/carta9.jpg",
	"pages/carta10.jpg"
];


flippingBook.contents = [
	[ "Portada", 1 ],
	[ "Final", 8 ]
];

// define custom book settings here
flippingBook.settings.bookWidth = 698;
flippingBook.settings.bookHeight = 560;
flippingBook.settings.pageBackgroundColor = 0x5b7414;
flippingBook.settings.backgroundColor = 0x83a51c;
flippingBook.settings.zoomUIColor = 0x919d6c;
flippingBook.settings.useCustomCursors = false;
flippingBook.settings.dropShadowEnabled = false;
flippingBook.settings.zoomImageWidth = 699;
flippingBook.settings.zoomImageHeight = 1120;
flippingBook.settings.downloadURL = "http://www.page-flip.com/new-demos/03-kitchen-gorenje-2008/kitchen_gorenje_2008.pdf";
flippingBook.settings.flipSound = "sounds/02.mp3";
flippingBook.settings.flipCornerStyle = "first page only";
flippingBook.settings.zoomHintEnabled = false;

flippingBook.settings.hardcover = false;
flippingBook.settings.hardcoverThickness = 2;
flippingBook.settings.highlightHardcover = true;
flippingBook.settings.frameAlpha = 10;
flippingBook.settings.smoothPages = true;

// default settings can be found in the flippingbook.js file
flippingBook.create();
