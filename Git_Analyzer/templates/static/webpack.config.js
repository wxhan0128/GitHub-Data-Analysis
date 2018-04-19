require('babel-polyfill');

const webpack = require('webpack');
const path = require('path');

const config = {
    entry: ['babel-polyfill', './js/App.js'],
    output: {
        path: __dirname + '/dist',
        filename: 'bundle.js',
    },
    resolve: {
        extensions: ['.js', '.jsx', '.css']
    },
    module: {
        rules: [
            {
                test: /\.(js|jsx)$/,
                exclude: /node_modules/,
                loader: "babel-loader",
                query: {
                    presets: ['es2015', 'react', 'stage-0']
                }
            }
        ]
    }
};

module.exports = config;