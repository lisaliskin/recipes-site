import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { VitePWA } from 'vite-plugin-pwa'

export default defineConfig({
  plugins: [
    vue(),
    VitePWA({
      registerType: 'autoUpdate',
      includeAssets: ['photos/*.jpg', 'apple-touch-icon.png'],
      manifest: {
        name: 'рецепты',
        short_name: 'рецепты',
        description: 'домашние рецепты с перерасчётом ингредиентов и списком покупок',
        theme_color: '#f5ecd7',
        background_color: '#f5ecd7',
        display: 'standalone',
        orientation: 'portrait',
        lang: 'ru',
        start_url: '/',
        icons: [
          {
            src: 'pwa-192.png',
            sizes: '192x192',
            type: 'image/png',
          },
          {
            src: 'pwa-512.png',
            sizes: '512x512',
            type: 'image/png',
            purpose: 'any maskable',
          },
        ],
      },
      workbox: {
        // Кешируем всё при установке (app shell + все фото)
        globPatterns: ['**/*.{js,css,html,svg,png,jpg,woff2}'],
        // Стратегия для HTML: сначала сеть, при офлайне — кеш
        navigateFallback: 'index.html',
        runtimeCaching: [
          {
            // Фото рецептов — сначала кеш, потом сеть
            urlPattern: /\/photos\/.+\.jpg$/,
            handler: 'CacheFirst',
            options: {
              cacheName: 'recipe-photos',
              expiration: {
                maxEntries: 60,
                maxAgeSeconds: 60 * 60 * 24 * 90, // 90 дней
              },
            },
          },
          {
            // Google Fonts
            urlPattern: /^https:\/\/fonts\.(googleapis|gstatic)\.com/,
            handler: 'CacheFirst',
            options: {
              cacheName: 'google-fonts',
              expiration: {
                maxEntries: 10,
                maxAgeSeconds: 60 * 60 * 24 * 365, // 1 год
              },
            },
          },
        ],
      },
    }),
  ],
})
