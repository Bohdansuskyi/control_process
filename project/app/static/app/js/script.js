// skrypt alarmu przekroczenia limitów temperatury
let temperatura = 85; 
        let limit = 80;

        function Temperature_check(temp) {
            const alertBox = document.getElementById('alertBox');
            if (temp > limit) {
                alertBox.classList.remove('d-none');
            } else {
                alertBox.classList.add('d-none');
            }
        }

Temperature_check(temperatura);

// skrypt odświeżania stron
let refreshTimer = null;
        const select = document.getElementById('refreshInterval');

        // Wczytanie zapisanego interwału z localStorage
        const savedInterval = localStorage.getItem('refreshInterval');
        if (savedInterval) {
            select.value = savedInterval;
            startTimer(parseInt(savedInterval));
        }

        select.addEventListener('change', function() {
            if (refreshTimer) {
                clearInterval(refreshTimer);
            }

            const interval = parseInt(this.value);

            // Zapisz wybraną wartość do localStorage
            localStorage.setItem('refreshInterval', interval);

            startTimer(interval);
        });

        function startTimer(interval) {
            if (interval > 0) {
                refreshTimer = setInterval(() => {
                    location.reload();
                }, interval);
            }
        }