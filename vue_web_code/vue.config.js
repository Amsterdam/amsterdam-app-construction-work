module.exports = {
  configureWebpack: {
    devtool: 'source-map'
  },
  pluginOptions: {
    i18n: {
      locale: 'nl',
      fallbackLocale: 'en',
      localeDir: 'locales',
      enableInSFC: true
    }
  }
}
