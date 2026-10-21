const tg = window.Telegram.WebApp;
tg.ready();
tg.expand();

let currentLocation = 'ls_airport';
let currentTransport = 'walk';

const LOCATIONS = {
    "ls_airport": {name: "✈️ Аэропорт LS", x: 50, y: 30, type: "city"},
    "ls_train": {name: "🚂 Вокзал LS", x: 45, y: 35, type: "city"},
    "ls_city_hall": {name: "🏛 Мэрия LS", x: 47, y: 33, type: "gov"},
    "ls_police": {name: "👮 Полиция LS", x: 48, y: 34, type: "gov"},
    "ls_hospital": {name: "🏥 Больница LS", x: 46, y: 36, type: "gov"},
    "ls_santa_maria": {name: "🏖 Пляж Санта-Мария", x: 52, y: 38, type: "area"},
    "ls_grove_street": {name: "🌳 Гроув-стрит", x: 44, y: 37, type: "area"},
    "ls_autosalon": {name: "🚗 Автосалон LS", x: 49, y: 32, type: "shop"},
    "ls_shop_247": {name: "🛒 Магазин 24/7", x: 46, y: 32, type: "shop"},
    "ls_bank": {name: "🏦 Банк LS", x: 47, y: 34, type: "shop"},
    "sf_city_hall": {name: "🏛 Мэрия SF", x: 30, y: 55, type: "gov"},
    "sf_police": {name: "👮 Полиция SF", x: 31, y: 56, type: "gov"},
    "sf_hospital": {name: "🏥 Больница SF", x: 29, y: 54, type: "gov"},
    "sf_pier": {name: "🌊 Пирс SF", x: 32, y: 57, type: "area"},
    "sf_chinatown": {name: "🏮 Чайнатаун", x: 28, y: 55, type: "area"},
    "lv_airport": {name: "✈️ Аэропорт LV", x: 75, y: 65, type: "city"},
    "lv_strip": {name: "🎰 Стрип LV", x: 76, y: 67, type: "casino"},
    "lv_city_hall": {name: "🏛 Мэрия LV", x: 74, y: 64, type: "gov"},
    "lv_police": {name: "👮 Полиция LV", x: 75, y: 66, type: "gov"},
    "lv_hospital": {name: "🏥 Больница LV", x: 73, y: 65, type: "gov"},
    "desert_gas": {name: "⛽ Заправка в пустыне", x: 60, y: 75, type: "area"},
    "farm": {name: "🌾 Ферма", x: 35, y: 80, type: "area"}
};

function init() {
    const user = tg.initDataUnsafe.user;
    if (user) {
        document.getElementById('money').textContent = '$1 000';
        document.getElementById('location').textContent = 'ls_airport';
    }
    renderMap();
    renderLocations();
}

function renderMap() {
    const map = document.getElementById('map');
    map.innerHTML = '';
    for (const [id, loc] of Object.entries(LOCATIONS)) {
        const point = document.createElement('div');
        point.className = 'map-point' + (id === currentLocation ? ' current' : '');
        point.style.left = loc.x + '%';
        point.style.top = loc.y + '%';
        point.textContent = loc.name;
        point.onclick = () => selectLocation(id);
        map.appendChild(point);
    }
}

function renderLocations() {
    const list = document.getElementById('locations');
    list.innerHTML = '';
    for (const [id, loc] of Object.entries(LOCATIONS)) {
        const card = document.createElement('div');
        card.className = 'location-card' + (id === currentLocation ? ' current' : '');
        card.innerHTML = `
            <div class="location-info">
                <div class="location-name">${loc.name}</div>
                <div class="location-type">${loc.type}</div>
            </div>
            ${id !== currentLocation ? `<button class="travel-btn" onclick="selectLocation('${id}')">Ехать</button>` : '<span>📍 Вы здесь</span>'}
        `;
        list.appendChild(card);
    }
}

function selectLocation(locId) {
    if (locId === currentLocation) return;
    currentLocation = locId;
    document.getElementById('location').textContent = locId;
    renderMap();
    renderLocations();
    tg.sendData(JSON.stringify({action: 'travel', location: locId}));
}

document.getElementById('closeBtn').onclick = () => tg.close();

init();
