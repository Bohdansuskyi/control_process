
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

// Aktualna data i czas w navbarze
function updateClock() {
    const now = new Date();
    const dateString = now.toLocaleDateString('pl-PL');
    const timeString = now.toLocaleTimeString('pl-PL');
    document.getElementById('clock').textContent = `${dateString} ${timeString}`;
}
setInterval(updateClock, 1000);
updateClock();