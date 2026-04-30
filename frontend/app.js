const API_URL = '/api';

// Tablarni almashtirish
function showTab(tabName) {
    document.querySelectorAll('.tab-content').forEach(tab => tab.classList.remove('active'));
    document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'));
    
    document.getElementById(tabName).classList.add('active');
    event.currentTarget.classList.add('active');

    if (tabName === 'cars') loadCars();
    if (tabName === 'rented') loadRentedCars();
    if (tabName === 'customers') loadCustomers();
    if (tabName === 'reports') loadReports();
    if (tabName === 'rent') loadRentData();
    if (tabName === 'return') loadActiveCustomersForReturn();
}

// Hisobotlarni yuklash
async function loadReports() {
    try {
        const resEarnings = await fetch(`${API_URL}/reports/earnings`);
        const earnings = await resEarnings.json();
        
        document.getElementById('month-earnings').innerText = earnings.month_total.toLocaleString() + " so'm";
        document.getElementById('year-earnings').innerText = earnings.year_total.toLocaleString() + " so'm";
        document.getElementById('total-rentals-count').innerText = earnings.total_rentals + " ta";

        // Tarixni yuklash
        const resHistory = await fetch(`${API_URL}/reports/history`);
        const history = await resHistory.json();
        const tbody = document.getElementById('history-body');
        
        tbody.innerHTML = history.map(h => `
            <tr style="border-bottom: 1px solid rgba(255,255,255,0.05);">
                <td style="padding: 10px;">${h.make} ${h.model}</td>
                <td style="padding: 10px;">${h.customer_name}</td>
                <td style="padding: 10px;">${h.rental_date}</td>
                <td style="padding: 10px;">${h.days} kun</td>
                <td style="padding: 10px;">${h.total_price.toLocaleString()} so'm</td>
            </tr>
        `).join('');

    } catch (e) {
        console.error("Hisobot yuklashda xatolik:", e);
    }
}

// Ijaradagi mashinalarni yuklash
async function loadRentedCars() {
    try {
        const res = await fetch(`${API_URL}/cars/rented`);
        const cars = await res.json();
        const list = document.getElementById('rented-cars-list');
        
        if (cars.length === 0) {
            list.innerHTML = '<p class="message">Hozirda ijarada mashinalar yo\'q.</p>';
            return;
        }

        list.innerHTML = cars.map(c => `
            <div class="card rented-card">
                <img src="${c.image_url}" alt="${c.make}" class="car-img" onerror="this.src='https://via.placeholder.com/300x150?text=Rasm+Mavjud+Emas'">
                <div class="card-info">
                    <h3>${c.make} ${c.model}</h3>
                    <p><strong>Raqam:</strong> ${c.car_id}</p>
                    <p><strong>Ijara sanasi:</strong> ${c.rental_date}</p>
                    <p><strong>Muddati:</strong> ${c.days} kun</p>
                    <p><strong>Umumiy:</strong> ${c.total_price.toLocaleString()} so'm</p>
                    <p class="status-badge">IJARA</p>
                </div>
            </div>
        `).join('');
    } catch (e) {
        document.getElementById('rented-cars-list').innerHTML = '<p class="error">Xatolik yuz berdi.</p>';
    }
}

// Qaytarish uchun faqat aktiv ijarachilarni yuklash
async function loadActiveCustomersForReturn() {
    try {
        const res = await fetch(`${API_URL}/customers`); // Faqat aktivlar
        const customers = await res.json();
        const select = document.getElementById('return-customer-id');
        
        select.innerHTML = '<option value="">-- Mijozni tanlang --</option>' + 
            customers.map(cust => `<option value="${cust.customer_id}" data-car="${cust.rented_car_id}">${cust.name} (Mashina: ${cust.rented_car_id})</option>`).join('');
        
        // Mijoz tanlanganda mashina ID sini avtomatik yozish
        select.onchange = (e) => {
            const selectedOption = e.target.options[e.target.selectedIndex];
            const carId = selectedOption.getAttribute('data-car');
            document.getElementById('return-car-id').value = carId || '';
        };
    } catch (e) {}
}

// Ijaraga olish uchun ma'lumotlarni (Mashina va Mijozlar) yuklash
async function loadRentData() {
    loadAvailableCarsForSelect();
    loadAllCustomersForSelect();
}

async function loadAllCustomersForSelect() {
    try {
        const res = await fetch(`${API_URL}/customers/all`);
        const customers = await res.json();
        const select = document.getElementById('rent-customer-id');
        
        select.innerHTML = '<option value="">-- Mijozni tanlang --</option>' + 
            customers.map(cust => `<option value="${cust.customer_id}">${cust.name} (ID: ${cust.customer_id})</option>`).join('');
    } catch (e) {}
}

// Bo'sh mashinalarni yuklash
async function loadCars() {
    try {
        const res = await fetch(`${API_URL}/cars/available`);
        const cars = await res.json();
        const list = document.getElementById('cars-list');
        
        if (cars.length === 0) {
            list.innerHTML = '<p class="message">Hozirda bo\'sh mashinalar yo\'q.</p>';
            return;
        }

        list.innerHTML = cars.map(c => `
            <div class="card">
                <img src="${c.image_url}" alt="${c.make}" class="car-img" onerror="this.src='https://via.placeholder.com/300x150?text=Rasm+Mavjud+Emas'">
                <div class="card-info">
                    <h3>${c.make} ${c.model}</h3>
                    <p><strong>Yil:</strong> ${c.year}</p>
                    <p><strong>Raqam:</strong> ${c.car_id}</p>
                    <p class="price">${c.price_per_day.toLocaleString()} so'm / kun</p>
                    <button class="delete-btn" onclick="deleteCar('${c.car_id}')">O'chirish</button>
                </div>
            </div>
        `).join('');
    } catch (e) {
        document.getElementById('cars-list').innerHTML = '<p class="error">Serverga ulanib bo\'lmadi.</p>';
    }
}

// Mashinani o'chirish
async function deleteCar(carId) {
    if (!confirm("Rostdan ham bu mashinani o'chirib yubormoqchimisiz?")) return;
    
    try {
        const res = await fetch(`${API_URL}/cars/${carId}`, { method: 'DELETE' });
        const result = await res.json();
        alert(result.message || result.error);
        loadCars();
        loadAvailableCarsForSelect();
    } catch (e) {
        alert("Xatolik yuz berdi");
    }
}

// Aktiv ijarachilarni yuklash
async function loadCustomers() {
    try {
        const res = await fetch(`${API_URL}/customers`);
        const customers = await res.json();
        const list = document.getElementById('customers-list');

        if (customers.length === 0) {
            list.innerHTML = '<p class="message">Hozircha aktiv ijarachilar yo\'q.</p>';
            return;
        }

        list.innerHTML = customers.map(cust => `
            <div class="card customer-card">
                <div class="card-info">
                    <h3>👤 ${cust.name}</h3>
                    <p><strong>ID:</strong> ${cust.customer_id}</p>
                    <p><strong>Tel:</strong> ${cust.phone}</p>
                    <p class="rent-info">🚗 Mashina ID: <span>${cust.rented_car_id}</span></p>
                </div>
            </div>
        `).join('');
    } catch (e) {
        list.innerHTML = '<p class="error">Xatolik yuz berdi.</p>';
    }
}

// Dropdown ni to'ldirish
async function loadAvailableCarsForSelect() {
    try {
        const res = await fetch(`${API_URL}/cars/available`);
        const cars = await res.json();
        const select = document.getElementById('rent-car-id');
        
        select.innerHTML = '<option value="">-- Mashinani tanlang --</option>' + 
            cars.map(c => `<option value="${c.car_id}">${c.make} ${c.model} (${c.car_id})</option>`).join('');
    } catch (e) {}
}

// Yangi Mashina qo'shish
document.getElementById('car-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    // Avval rasmni yuklaymiz
    const imageInput = document.getElementById('new-car-image');
    let imageUrl = "images/default.png";

    if (imageInput.files.length > 0) {
        const formData = new FormData();
        formData.append("file", imageInput.files[0]);
        
        try {
            const uploadRes = await fetch(`${API_URL}/upload`, {
                method: 'POST',
                body: formData
            });
            const uploadResult = await uploadRes.json();
            if (uploadResult.filename) {
                imageUrl = uploadResult.filename;
            }
        } catch (err) {
            console.error("Rasm yuklashda xatolik:", err);
        }
    }

    const carData = {
        car_id: document.getElementById('new-car-id').value,
        make: document.getElementById('new-car-make').value,
        model: document.getElementById('new-car-model').value,
        year: parseInt(document.getElementById('new-car-year').value),
        price_per_day: parseFloat(document.getElementById('new-car-price').value),
        image_url: imageUrl
    };

    const res = await fetch(`${API_URL}/cars`, {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(carData)
    });
    const result = await res.json();
    alert(result.message || result.error);
    if (!result.error) {
        e.target.reset();
        loadCars();
    }
});

// Yangi Mijoz qo'shish
document.getElementById('customer-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const custData = {
        name: document.getElementById('new-cust-name').value,
        phone: document.getElementById('new-cust-phone').value
    };

    const res = await fetch(`${API_URL}/customers`, {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(custData)
    });
    const result = await res.json();
    alert(`${result.message}. Mijoz ID: ${result.customer_id}`);
    e.target.reset();
});

// Ijaraga olish
document.getElementById('rent-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const data = {
        customer_id: parseInt(document.getElementById('rent-customer-id').value),
        car_id: document.getElementById('rent-car-id').value,
        days: parseInt(document.getElementById('rent-days').value)
    };

    const res = await fetch(`${API_URL}/rent`, {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(data)
    });
    const result = await res.json();
    if (result.error) {
        alert(result.error);
    } else {
        alert(`${result.message}\nJami narx: ${result.total_price} so'm`);
        e.target.reset();
        loadAvailableCarsForSelect();
    }
});

// Qaytarish
document.getElementById('return-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const data = {
        customer_id: parseInt(document.getElementById('return-customer-id').value),
        car_id: document.getElementById('return-car-id').value
    };

    const res = await fetch(`${API_URL}/return`, {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(data)
    });
    const result = await res.json();
    alert(result.message || result.error);
    if (!result.error) e.target.reset();
});

// Dastlabki yuklash
loadCars();
