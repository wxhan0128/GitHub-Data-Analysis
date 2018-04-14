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
                test: /\.jsx?$/,
                exclude: /node_modules/,
                use: {
                    loader: "babel-loader"
                }
            }
        ]
    }
};

module.exports = config;