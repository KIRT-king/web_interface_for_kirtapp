let isButtonDisabled = false; // Флаг, чтобы отслеживать, заблокированы ли кнопки

// Функция для блокировки кнопок
function disableButtons() {
    if (isButtonDisabled) return; // Если кнопки уже заблокированы, ничего не делаем

    isButtonDisabled = true; // Устанавливаем флаг на заблокированные кнопки

    const searchButton = document.getElementById("searchButton");
    const latestButton = document.getElementById("latestButton");

    if (searchButton) {
        disableButton(searchButton);
    }

    if (latestButton) {
        disableButton(latestButton);
    }

    setTimeout(() => {
        if (searchButton) {
            enableButton(searchButton);
        }

        if (latestButton) {
            enableButton(latestButton);
        }

        isButtonDisabled = false; // Снимаем блокировку
    }, 3000); // 3 секунды
}

// Функция для блокировки конкретной кнопки
function disableButton(button) {
    if (!button.dataset.originalText) {
        button.dataset.originalText = button.innerHTML; // Сохраняем оригинальный текст кнопки
    }
    
    button.disabled = true;
    button.innerHTML = "🔒"; // Заменяем текст на замок

    // Фиксируем текущую ширину кнопки, чтобы она не менялась
    button.style.width = `${button.offsetWidth}px`;
}

// Функция для включения кнопки обратно
function enableButton(button) {
    button.disabled = false;
    const originalText = button.getAttribute("data-original-text");
    button.innerHTML = originalText; // Восстанавливаем оригинальный текст
}

// Поиск пользователей
async function searchUsers() {
    const name = document.getElementById("nameInput").value.trim();
    const email = document.getElementById("emailInput").value.trim();
    const phone = document.getElementById("phoneInput").value.trim();
    const errorMessage = document.getElementById("errorMessage");
    const tableBody = document.getElementById("userTableBody");
    
    errorMessage.textContent = "";
    tableBody.innerHTML = ""; 
    
    if (!name && !email && !phone) {
        errorMessage.textContent = "Please enter at least one search criteria.";
        return;
    }
    
    let query = `?`;
    if (name) query += `name=${encodeURIComponent(name)}&`;
    if (email) query += `email=${encodeURIComponent(email)}&`;
    if (phone) query += `phone_number=${encodeURIComponent(phone)}`;

    disableButtons(); // Блокируем обе кнопки

    try {
        const response = await fetch(`http://localhost:8002/crud/search${query}`);
        if (!response.ok) {
            throw new Error("Users not found.");
        }
        
        const users = await response.json();
        users.forEach(user => {
            const row = document.createElement("tr");
            row.innerHTML = `
                <td>${user.id}</td>
                <td>${user.username}</td>
                <td>${user.name}</td>
                <td>${user.lastname}</td>
                <td>${user.post}</td>
                <td>${user.email}</td>
                <td>${user.phone_number}</td>
                <td>${user.status}</td>
                <td>${user.last_check}</td>
            `;
            tableBody.appendChild(row);
        });
    } catch (error) {
        errorMessage.textContent = error.message;
    }
}

async function getLatestUsers() {
    const limit = document.getElementById("latestInput").value.trim() || 10;
    const tableBody = document.getElementById("userTableBody");
    
    tableBody.innerHTML = "";

    disableButtons(); // Блокируем обе кнопки

    try {
        const response = await fetch(`http://localhost:8002/crud/latest?limit=${limit}`);
        if (!response.ok) throw new Error("Failed to load users");

        const users = await response.json();
        users.forEach(user => {
            const row = document.createElement("tr");
            row.innerHTML = `
                <td>${user.id}</td>
                <td>${user.username}</td>
                <td>${user.name}</td>
                <td>${user.lastname}</td>
                <td>${user.post}</td>
                <td>${user.email}</td>
                <td>${user.phone_number}</td>
                <td>${user.status}</td>
                <td>${user.last_check}</td>
            `;
            tableBody.appendChild(row);
        });
    } catch (error) {
        console.error(error);
    }
}

// Функция для проверки админа
async function checkAdmin() {
    try {
        const response = await fetch("http://localhost:8002/auth/admin", {
            method: "GET",
            credentials: "include"
        });

        if (response.ok) {
            document.getElementById("content").style.display = "block"; 
        } else {
            throw new Error("Not an admin");
        }
    } catch (error) {
        window.location.href = "auth.html"; // Перенаправление, если не админ
    }
}

// Функция выхода
async function logout() {
    await fetch("http://localhost:8002/auth/logout", {
        method: "POST",
        credentials: "include"
    });
    window.location.href = "auth.html";
}

// Инициализация на DOMContentLoaded
document.addEventListener("DOMContentLoaded", () => {
    checkAdmin(); 

    const themeToggle = document.createElement("button");
    themeToggle.classList.add("theme-toggle");
    themeToggle.innerHTML = "🌙"; // Иконка луны
    document.body.appendChild(themeToggle);

    themeToggle.addEventListener("click", () => {
        document.body.classList.toggle("light-theme");
        themeToggle.innerHTML = document.body.classList.contains("light-theme") ? "☀️" : "🌙"; 
    });

    const notification = document.createElement("div");
    notification.classList.add("notification");
    notification.innerText = "Successfully logged in!";
    document.body.appendChild(notification);

    setTimeout(() => {
        notification.classList.add("show");
        setTimeout(() => notification.classList.remove("show"), 3000);
    }, 500);
});
