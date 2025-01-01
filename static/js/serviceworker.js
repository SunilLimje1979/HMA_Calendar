// ######################################## New ########################################

// var staticCacheName = 'HMA_Calender' ;

// self.addEventListener('install', function(event) {
//     event.waitUntil(
//         caches.open(staticCacheName).then(function(cache) {
//             console.log("caching sell")
//             return cache.addAll([
//                 '',
//             ]);
//         })
//     );
// });

// self.addEventListener('fetch', function(event) {
//     var requestUrl = new URL(event.request.url);
//     if (requestUrl.origin === location.origin) {
//         if ((requestUrl.pathname === '/')) {
//             // Bypass cache for HTML requests
//             event.respondWith(fetch(event.request));
//             return;
//         }
//     }
//     event.respondWith(
//         caches.match(event.request).then(function(response) {
//             return response || fetch(event.request);
//         })
//     );
// });

// ######################################## Updated Service Worker ########################################

var staticCacheName = 'hma-calendar-v1';

self.addEventListener('install', function(event) {
    console.log('Service Worker: Installing and caching static assets...');
    event.waitUntil(
        caches.open(staticCacheName).then(function(cache) {
            return cache.addAll([
                '/cal2025/calendar/',  // Cache the main HTML page
                '/cal2025/static/images/HMALogo.png',  // Cache your static image(s)
                '/cal2025/static/images/mobileappicon.png',
                '/cal2025/static/images/January.jpeg',
                '/cal2025/static/images/Feb.jpeg',
                '/cal2025/static/images/March.jpeg',
                '/cal2025/static/images/April.jpeg',
                '/cal2025/static/images/May.jpeg',
                '/cal2025/static/images/June.jpeg',
                '/cal2025/static/images/July.jpeg',
                '/cal2025/static/images/August.jpeg',
                '/cal2025/static/images/Sept.jpeg',
                '/cal2025/static/images/October.jpeg',
                '/cal2025/static/images/Nov.jpeg',
                '/cal2025/static/images/Dec.jpeg',
                '/cal2025/static/images/January(Back Side).jpeg',
                '/cal2025/static/images/Feb(Back Side).jpeg',
                '/cal2025/static/images/March(Back Side).jpeg',
                '/cal2025/static/images/April(Back Side).jpeg',
                '/cal2025/static/images/May(Back Side).jpeg',
                '/cal2025/static/images/June(Back Side).jpeg',
                '/cal2025/static/images/July(Back Side).jpeg',
                '/cal2025/static/images/August(Back Side).jpeg',
                '/cal2025/static/images/Sept(Back Side).jpeg',
                '/cal2025/static/images/Oct(Back Side).jpeg',
                '/cal2025/static/images/Nov(Back Side).jpeg',
                '/cal2025/static/images/Dec(Back Side).jpeg',
                'https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css',
                'https://cdn.jsdelivr.net/npm/@fortawesome/fontawesome-free@6.0.0/css/all.min.css',

            ]);
        })
    );
});

// Activate event - Clean up old caches
self.addEventListener('activate', function(event) {
    console.log('Service Worker: Activating and clearing old caches...');
    event.waitUntil(
        caches.keys().then(function(keys) {
            return Promise.all(
                keys.filter(key => key !== staticCacheName)
                    .map(key => caches.delete(key))
            );
        })
    );
});

// Fetch event - Serve from cache, fallback to network
self.addEventListener('fetch', function(event) {
    console.log('Service Worker: Fetching', event.request.url);
    event.respondWith(
        caches.match(event.request).then(function(response) {
            return response || fetch(event.request);
        }).catch(function() {
            // Fallback to main HTML page if offline and not in cache
            return caches.match('/cal2025/calendar/');
        })
    );
});


// ######################################## Old ########################################

// var staticCacheName = 'PWA-v1';

// self.addEventListener('install', function(event) {
// event.waitUntil(
// 	caches.open(staticCacheName).then(function(cache) {
// 	return cache.addAll([
// 		'',
// 	]);
// 	})
// );
// });

// self.addEventListener('fetch', function(event) {
// var requestUrl = new URL(event.request.url);
// 	if (requestUrl.origin === location.origin) {
// 	if ((requestUrl.pathname === '/')) {
// 		event.respondWith(caches.match(''));
// 		return;
// 	}
// 	}
// 	event.respondWith(
// 	caches.match(event.request).then(function(response) {
// 		return response || fetch(event.request);
// 	})
// 	);
// });



