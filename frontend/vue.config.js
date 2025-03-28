const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
  transpileDependencies: false
})

const path = require('path');
module.exports = defineConfig({
  transpileDependencies: false,
  configureWebpack: {
    resolve: {
      alias: {
        '@': path.resolve(__dirname, 'src')
      }
    }
  }
});