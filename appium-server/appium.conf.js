// Виправлена конфігурація для Appium 2.x
// Видалено секцію "appium" яка не підтримується в новій версії
module.exports = {
  server: {
    // Default Appium HTTP port. ADB connections use a different port (5555).
    port: 4723,
    // Listen on all network interfaces so containers or remote clients can
    // reach the server regardless of their IP.
    address: '0.0.0.0',
    // Логування тепер налаштовується через CLI аргументи
    'log-level': 'info',
    // Дозволити небезпечні функції для автоматизації
    'allow-insecure': ['adb_shell'],
    // Релакс безпеки для контейнерного середовища
    'relaxed-security': true
  }
};
