const API_URL = "http://localhost:8000/api";

// Tablarni almashtirish
function showTab(tabId) {
    document.querySelectorAll('.tab-content').forEach(el => el.classList.remove('active'));
    document.querySelectorAll('.tab-btn').forEach(el => el.classList.remove('active'));
    
    document.getElementById(tabId).classList.add('active');
    document.querySelector(`.tab-btn[onclick="showTab('${tabId}')"]`).classList.add('active');

    // Tab o'zgarganda ma'lumotlarni yangilash
    if (tabId === 'cars') loadCars();
    if (tabId === 'customers') loadCustomers();
}

// Mashinalarni API dan tortib olish
async function loadCars() {
    const list = document.getElementById('cars-list');
    list.innerHTML = '<p>Yuklanmoqda...</p>';
    try {
        const res = await fetch(`${API_URL}/cars/available`);
        const cars = await res.json();
        list.innerHTML = cars.map(c => `
            <div class="card">
                <img src="${c.image_url}" alt="${c.make}" class="car-img">
                <h3>${c.make} ${c.model} (${c.year})</h3>
                <p><strong>Raqam:</strong> ${c.car_id}</p>
                <p><strong>Narx:</strong> ${c.price_per_day.toLocaleString()} so'm / kun</p>
            </div>
        `).join('');
        if (cars.length === 0) list.innerHTML = '<p>Hozircha bo\'sh mashinalar yo\'q.</p>';
    } catch (e) {
        list.innerHTML = '<p class="message error">Serverga ulanib bo\'lmadi. Backend (API) ishlayotganiga ishonch hosil qiling.</p>';
    }
}

// Mijozlarni API dan tortib olish
async function loadCustomers() {
    const list = document.getElementById('customers-list');
    list.innerHTML = '<p>Yuklanmoqda...</p>';
    try {
        const res = await fetch(`${API_URL}/customers`);
        const customers = await res.json();
        list.innerHTML = customers.map(c => {
            const carsList = c.rented_cars.map(car => car.car_id).join(', ');
            return `
            <div class="card">
                <h3>👤 ${c.name}</h3>
                <p><strong>Mijoz ID:</strong> ${c.customer_id}</p>
                <p><strong>Ijaradagi mashinalar:</strong> <br> ${carsList ? `<span style="color:#00f2fe">${carsList}</span>` : "Yo'q"}</p>
            </div>
            `;
        }).join('');
        if (customers.length === 0) list.innerHTML = '<p>Hozircha mijozlar yo\'q.</p>';
    } catch (e) {
        list.innerHTML = '<p class="message error">Serverga ulanib bo\'lmadi.</p>';
    }
}

// Ijara formasi jo'natilganda
document.getElementById('rent-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const customer_id = parseInt(document.getElementById('rent-customer-id').value);
    const car_id = document.getElementById('rent-car-id').value;
    const days = parseInt(document.getElementById('rent-days').value);
    const msgEl = document.getElementById('rent-message');

    msgEl.className = 'message';
    msgEl.textContent = 'Kutilmoqda...';

    try {
        const res = await fetch(`${API_URL}/rent`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ customer_id, car_id, days })
        });
        const data = await res.json();
        msgEl.className = `message ${data.success ? 'success' : 'error'}`;
        msgEl.textContent = data.message;
        
        if(data.success) {
            document.getElementById('rent-form').reset();
        }
    } catch (e) {
        msgEl.className = 'message error';
        msgEl.textContent = "Server bilan aloqa yo'q! Backend ishga tushirilganini tekshiring.";
    }
});

// Qaytarish formasi jo'natilganda
document.getElementById('return-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const customer_id = parseInt(document.getElementById('return-customer-id').value);
    const car_id = document.getElementById('return-car-id').value;
    const msgEl = document.getElementById('return-message');

    msgEl.className = 'message';
    msgEl.textContent = 'Kutilmoqda...';

    try {
        const res = await fetch(`${API_URL}/return`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ customer_id, car_id })
        });
        const data = await res.json();
        msgEl.className = `message ${data.success ? 'success' : 'error'}`;
        msgEl.textContent = data.message;
        
        if(data.success) {
            document.getElementById('return-form').reset();
        }
    } catch (e) {
        msgEl.className = 'message error';
        msgEl.textContent = "Server bilan aloqa yo'q!";
    }
});

// Sahifa yuklanganda birinchi tabni ko'rsatish
loadCars();
