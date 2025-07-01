
// skrypt odświeżania stron

setInterval(function() {
        fetch("/api/check_update/")
            .then(response => response.json())
            .then(data => {
                if (data.new) {
                    window.location.reload(); // odśwież stronę
                }
            });
    }, 5000); // co 5 sekund