
// skrypt odświeżania tylko gdy są nowe dane
setInterval(function() {
    fetch("/api/check_update/")
        .then(response => response.json())
        .then(data => {
            if (data.new) {
                window.location.reload();
            }
        })
        .catch(err => console.error("Błąd podczas sprawdzania aktualizacji:", err));
}, 5000); // co 5 sekund

// Aktualna data i czas w navbarze
function updateClock() {
    const now = new Date();
    const dateString = now.toLocaleDateString('pl-PL');
    const timeString = now.toLocaleTimeString('pl-PL');

    const clockEl = document.getElementById('clock');
    if (clockEl) {
        clockEl.textContent = `${dateString} ${timeString}`;
    }
}
setInterval(updateClock, 1000);
updateClock();
