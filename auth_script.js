async function login() {
    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;

    const response = await fetch("http://localhost:8002/auth/login?username=" + username + "&password=" + password, {
        method: "POST",
        credentials: "include" // Включаем отправку cookie
    });

    if (response.ok) {
        setTimeout(() => {  
            window.location.href = "crud.html"; // Переход на страницу админки
        }, 500);
    } else {
        const data = await response.json();
        showNotification(data.detail, "error");
    }
}

function showNotification(message, type) {
    const notificationContainer = document.getElementById("notification-container");

    const notification = document.createElement("div");
    notification.classList.add("notification", type);
    notification.innerText = message;

    notificationContainer.appendChild(notification);

    setTimeout(() => {
        notification.classList.add("fade-out");
        setTimeout(() => {
            notification.remove();
        }, 500);
    }, 3000);
}
