const { resolve } = require("path");
const MiniCssExtractPlugin = require("mini-css-extract-plugin");
const CssMinimizerPlugin = require("css-minimizer-webpack-plugin");
const UglifyJsPlugin = require("uglifyjs-webpack-plugin");
const HtmlWebpackPlugin = require("html-webpack-plugin");
const CopyWebpackPlugin = require("copy-webpack-plugin");

const pageDefaults = {
    DEFAULT_HOST: process.env.DEFAULT_HOST,
    DEFAULT_PORT: process.env.DEFAULT_PORT,
};

module.exports = {
    entry: {
        index: ["./src/js/index.js", "./src/css/index.css"],
    },
    module: {
        rules: [
            {
                test: /\.css$/,
                use: [
                    MiniCssExtractPlugin.loader,
                    {
                        loader: "css-loader",
                        options: {
                            url: false,
                        },
                    },
                ],
            },
        ],
    },
    plugins: [
        new HtmlWebpackPlugin({
            filename: "index.html",
            template: "src/index.html",
            minify: {
                collapseWhitespace: true,
            },
            ...pageDefaults,
            PAGE_MODE: "ports",
            PAGE_TITLE: "Controllo Porte Aperte Online | Test TCP Gratuito",
            PAGE_DESCRIPTION:
                "Controlla se una porta TCP è aperta o chiusa su IP o dominio. Test gratuito per port forwarding, modem/router, firewall, server, VPS e DNS dinamico.",
            PAGE_CANONICAL: "https://controlloporte.it/",
            OG_TITLE: "Controllo Porte Aperte Online",
            HERO_TITLE: "Controllo Porte Aperte Online",
            HERO_SUBTITLE:
                "Verifica se una porta TCP è aperta o chiusa su un indirizzo IP o dominio.",
            HOST_LABEL: "Host o indirizzo IP",
            HOST_PLACEHOLDER: "Inserisci un dominio o indirizzo IPv4",
            HOST_HINT: "Inserisci un dominio o indirizzo IPv4",
            HOST_ERROR: "Inserisci un dominio o indirizzo valido",
        }),

        new HtmlWebpackPlugin({
            filename: "controlloDDNS/index.html",
            template: "src/index.html",
            minify: {
                collapseWhitespace: true,
            },
            ...pageDefaults,
            PAGE_MODE: "ddns",
            PAGE_TITLE: "Controllo DDNS Online | Verifica DNS Dinamico",
            PAGE_DESCRIPTION:
                "Controlla se un nome host DDNS risolve allo stesso IP pubblico del visitatore. Verifica rapida per DNS dinamico, modem/router e accesso remoto.",
            PAGE_CANONICAL: "https://controlloporte.it/controlloDDNS/",
            OG_TITLE: "Controllo DDNS Online",
            HERO_TITLE: "Controllo DDNS Online",
            HERO_SUBTITLE:
                "Verifica se il nome host DNS dinamico punta al tuo IP pubblico attuale.",
            HOST_LABEL: "Nome host DDNS",
            HOST_PLACEHOLDER: "Inserisci un nome host DDNS",
            HOST_HINT: "Inserisci un nome host DNS dinamico, ad esempio casa.example.com",
            HOST_ERROR: "Inserisci un nome host DDNS valido",
        }),

        new MiniCssExtractPlugin({
            filename: "css/[name].min.css",
        }),

        new CopyWebpackPlugin({
            patterns: [{ from: "src/assets" }],
        }),
    ],
    devServer: {
        port: 8080,
        historyApiFallback: {
            disableDotRule: true,
            rewrites: [
                {
                    from: /^\/controlloDDNS\/.*$/,
                    to: "/controlloDDNS/index.html",
                },
            ],
        },
        proxy: [
            {
                context: ["/api", "/docs", "/metrics"],
                target: process.env.API_URL,
            },
        ],
    },
    optimization: {
        minimize: true,
        minimizer: [
            new UglifyJsPlugin({
                include: /\.js$/,
            }),
            new CssMinimizerPlugin(),
        ],
    },
    output: {
        path: resolve(__dirname, "dist"),
        filename: "js/[name].min.js",
        publicPath: "/",
    },
};
