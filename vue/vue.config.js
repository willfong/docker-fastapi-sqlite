
// We want to add /static/ to the dirs when deploying to flask


module.exports = {
    publicPath: process.env.NODE_ENV === 'production'
      ? '/static/'
      : '/'
  
}

