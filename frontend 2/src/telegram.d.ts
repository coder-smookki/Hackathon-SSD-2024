// telegram.d.ts
declare global {
    interface Window {
        Telegram: {
            WebApp: {
                initData: string;
                // Добавьте другие свойства, которые вам нужны
            };
        };
    }
}

// Убедитесь, что файл экспортируется как модуль
export {};
