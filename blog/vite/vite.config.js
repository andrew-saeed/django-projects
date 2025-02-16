import path from 'path'
import { defineConfig } from 'vite'

const ROOT = path.resolve('')
const BASE = __dirname.replace(ROOT, '')

export default defineConfig({
    base: BASE,
    server: {
        port: 4200
    },
    build: {
        manifest: 'manifest.json',
        assetsDir: '.',
        outDir: `../static`,
        emptyOutDir: true,
        sourcemap: true,
        rollupOptions: {
            input: [
                'src/main.js',
                'src/style.css',
            ],
            output: {
                entryFileNames: '[hash].js',
                assetFileNames: '[hash].[ext]',
            }
        },
    },
    plugins: [
        {
            name: 'py',
            handleHotUpdate({ file, server }) {
                if (file.endsWith('.html')) {
                    server.ws.send({ type: 'full-reload' });
                }
            }
        },
    ],
})