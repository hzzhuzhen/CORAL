const {defineConfig} = require('@vue/cli-service')
module.exports = defineConfig({
    transpileDependencies: true,
    devServer: {
        // port:7000,

        proxy: {
            '/users': {
                target: 'http://localhost:8082', // 对应 /users 的后端服务地址
                changeOrigin: true,
            },
            '/task': {
                target: 'http://localhost:8082', // 对应 /task 的后端服务地址
                changeOrigin: true,
            },
            '/inputFile': {
                target: 'http://localhost:8082', // 对应 /inputFile 的后端服务地址
                changeOrigin: true,
            },
            '/manual': {
                target: 'http://localhost:8082', // 对应 /manual 的后端服务地址
                changeOrigin: true,
            },
            '/prompt': {
                target: 'http://localhost:8082', // 对应 /prompt 的后端服务地址
                changeOrigin: true,
            },
            '/api': {
                target: 'http://localhost:8082', // 对应 /api 的后端服务地址
                changeOrigin: true,
            },
            // '/demo': {
            //     target: 'http://localhost:8082', // 对应 /demo 的后端服务地址
            //     changeOrigin: true,
            // },
            // '/demo': {
            //     target: 'http://26.112.253.186:8082', // 对应 /demo 的后端服务地址
            //     changeOrigin: true,
            // },
        }
    }
});
